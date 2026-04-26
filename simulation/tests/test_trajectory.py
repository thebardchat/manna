"""
Unit tests for Manna trajectory simulator.

Validates atmosphere model against USSA 1976 tabulated values,
verifies RK4 physics, and checks all three variant outputs for
physical sanity.  Run with:  pytest simulation/tests/

Author: Shane Brazelton + Claude (Anthropic)
Date:   2026-04-25
"""

import math
import sys
from pathlib import Path

import pytest

# Allow import from simulation/src without installing the package
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from trajectory_sim import (
    atmo_temperature,
    atmo_pressure,
    atmo_density,
    atmo_speed_of_sound,
    gravity,
    circular_orbital_velocity,
    simulate,
    run_sanity_check,
    VARIANTS,
    MannaPod,
    SimResult,
    SUTTON_GRAVES_K,
    NOSE_RADIUS_M,
    _rk4_step,
    _derivatives,
)

import numpy as np


# ---------------------------------------------------------------------------
# Atmosphere model — spot-check against USSA 1976 Table 1  [VERIFIED values]
# ---------------------------------------------------------------------------

class TestAtmosphere:

    def test_sea_level_temperature(self):
        assert abs(atmo_temperature(0) - 288.15) < 0.01

    def test_sea_level_pressure(self):
        assert abs(atmo_pressure(0) - 101_325.0) < 1.0

    def test_sea_level_density(self):
        # USSA 1976: 1.2250 kg/m³  [VERIFIED]
        assert abs(atmo_density(0) - 1.2250) < 0.001

    def test_sea_level_speed_of_sound(self):
        # USSA 1976: 340.294 m/s  [VERIFIED]
        assert abs(atmo_speed_of_sound(0) - 340.294) < 0.5

    def test_tropopause_temperature(self):
        # Temperature at 11 km should be 216.65 K  [VERIFIED]
        assert abs(atmo_temperature(11_000) - 216.65) < 0.5

    def test_stratosphere_temperature_20km(self):
        # Isothermal tropopause layer: T(20 km) = 216.65 K  [VERIFIED]
        assert abs(atmo_temperature(20_000) - 216.65) < 0.5

    def test_pressure_decreases_monotonically(self):
        altitudes = range(0, 100_000, 5_000)
        pressures = [atmo_pressure(h) for h in altitudes]
        for i in range(len(pressures) - 1):
            assert pressures[i] > pressures[i + 1], (
                f"Pressure not monotonically decreasing at {i * 5000} m"
            )

    def test_density_positive_everywhere(self):
        for h in range(0, 300_000, 10_000):
            assert atmo_density(h) >= 0.0

    def test_density_at_100km_very_low(self):
        # Above Kármán line, density should be < 10⁻⁵ kg/m³  [VERIFIED: ~5.6e-7]
        assert atmo_density(100_000) < 1e-4

    def test_temperature_below_ground_clamped(self):
        # Negative altitudes should return sea-level temperature
        assert atmo_temperature(-1_000) == atmo_temperature(0)


# ---------------------------------------------------------------------------
# Gravity and orbital velocity
# ---------------------------------------------------------------------------

class TestGravity:

    def test_sea_level_gravity(self):
        assert abs(gravity(0) - 9.80665) < 0.001

    def test_gravity_decreases_with_altitude(self):
        assert gravity(100_000) < gravity(0)
        assert gravity(400_000) < gravity(100_000)

    def test_circular_orbital_velocity_leo(self):
        # At 400 km LEO: v_circ ≈ 7.67 km/s  [VERIFIED: ISS orbit]
        v = circular_orbital_velocity(400_000)
        assert 7_500 < v < 7_800

    def test_circular_orbital_velocity_sea_level(self):
        # Theoretical: sqrt(G₀ × R_E) ≈ 7905 m/s  [VERIFIED]
        v = circular_orbital_velocity(0)
        assert abs(v - 7_905) < 10


# ---------------------------------------------------------------------------
# RK4 step — verify against analytic free-fall  [VERIFIED: Newtonian mechanics]
# ---------------------------------------------------------------------------

class TestRK4:

    def test_vertical_free_fall(self):
        """No drag (infinite BC), vertical drop: z(t) = -½g₀t²."""
        # Create a pod with enormous BC (effectively no drag)
        pod = MannaPod(
            name="test",
            mass_kg=1e9,        # huge mass → huge BC → negligible drag
            diameter_m=0.001,
            cd0=0.1,
            launch_v_ms=0.0,
            v01_apogee_km=0.0,
        )
        state = np.array([0.0, 0.0, 0.0, 0.0])
        dt = 0.1
        # After 1 s free-fall from rest, z should be -½×9.8×1² = -4.9 m
        for _ in range(10):
            state = _rk4_step(state, dt, pod)
        expected_z = -0.5 * 9.80665 * 1.0**2
        assert abs(state[1] - expected_z) < 0.01, (
            f"Free-fall z after 1 s: got {state[1]:.4f}, expected {expected_z:.4f}"
        )

    def test_horizontal_no_gravity_no_drag(self):
        """Vertical launch with minimal gravity effect (short step) — vx constant."""
        pod = MannaPod(
            name="test",
            mass_kg=1e9,
            diameter_m=0.001,
            cd0=0.1,
            launch_v_ms=0.0,
            v01_apogee_km=0.0,
        )
        state = np.array([0.0, 1_000_000.0, 1_000.0, 0.0])  # very high alt, vx=1 km/s
        dt = 0.1
        new_state = _rk4_step(state, dt, pod)
        # vx should not change significantly in one step (no drag, minimal gravity effect)
        assert abs(new_state[2] - 1_000.0) < 1.0   # vx ≈ 1000 m/s


# ---------------------------------------------------------------------------
# Full variant simulations — sanity checks  [DERIVED outputs]
# ---------------------------------------------------------------------------

class TestVariantSimulations:

    @pytest.fixture(scope="class")
    def results(self):
        """Run all three variants once at 30° elevation for the whole test class."""
        return {name: simulate(pod, elevation_deg=30.0, dt=0.1)
                for name, pod in VARIANTS.items()}

    def test_all_variants_have_points(self, results):
        for name, res in results.items():
            assert len(res.points) > 10, f"{name}: trajectory has < 10 points"

    def test_apogee_ordering(self, results):
        """Heavier, faster pod should reach higher apogee (in absence of opposite BC effect)."""
        ap_b = results["Manna-B"].apogee_km
        ap_i = results["Manna-I"].apogee_km
        ap_h = results["Manna-H"].apogee_km
        assert ap_b < ap_i, f"Manna-B ({ap_b:.1f} km) should be below Manna-I ({ap_i:.1f} km)"
        assert ap_i < ap_h, f"Manna-I ({ap_i:.1f} km) should be below Manna-H ({ap_h:.1f} km)"

    def test_sim_apogees_below_v01_claims(self, results):
        """Atmospheric drag must reduce apogee below vacuum v0.1 claims for all variants."""
        for name in ("Manna-B", "Manna-I", "Manna-H"):
            res = results[name]
            sim = res.apogee_km
            v01 = res.variant.v01_apogee_km
            assert sim < v01, (
                f"{name}: sim apogee {sim:.1f} km should be less than "
                f"v0.1 vacuum claim {v01:.1f} km"
            )

    def test_apogees_above_zero(self, results):
        for name, res in results.items():
            assert res.apogee_km > 0.0, f"{name}: apogee should be positive"

    def test_max_q_positive(self, results):
        for name, res in results.items():
            assert res.max_q_pa > 0.0, f"{name}: max-Q should be positive"

    def test_max_q_at_low_altitude(self, results):
        """Max dynamic pressure occurs in the lower atmosphere (< 50 km)."""
        for name, res in results.items():
            assert res.max_q_alt_km < 50.0, (
                f"{name}: max-Q altitude {res.max_q_alt_km:.1f} km should be < 50 km"
            )

    def test_max_mach_supersonic(self, results):
        """All variants are launched at hypersonic velocities; max Mach >> 1."""
        for name, res in results.items():
            assert res.max_mach > 5.0, (
                f"{name}: max Mach {res.max_mach:.1f} should exceed 5 (hypersonic)"
            )

    def test_manna_h_catastrophic_drag(self, results):
        """
        Manna-H at 10,814 m/s hits ~71 MPa dynamic pressure at sea level (3000+ g drag).
        Atmosphere kills velocity before 100 km is reached — apogee should be << 100 km.
        This directly disproves the v0.1 claim of 1,950 km.  [DERIVED]
        """
        res = results["Manna-H"]
        assert res.apogee_km < 100.0, (
            f"Manna-H apogee {res.apogee_km:.1f} km: atmosphere should prevent reaching 100 km"
        )
        # The v0.1 paper was off by at least 20× for Manna-H
        v01 = res.variant.v01_apogee_km
        assert res.apogee_km < v01 / 20.0, (
            f"Manna-H drag error should be > 20×: sim={res.apogee_km:.1f} km, v0.1={v01:.1f} km"
        )

    def test_all_variants_suborbital_flag_false(self, results):
        """None of the variants reach 100 km with horizontal v > orbital v after atmospheric drag."""
        for name, res in results.items():
            assert not res.orbital_flag, (
                f"{name}: orbital_flag should be False — drag prevents all variants "
                f"from reaching the Kármán line with orbital-class horizontal velocity"
            )

    def test_ballistic_coefficient_manna_h_gt_manna_b(self, _results=None):
        """Manna-H has larger BC than Manna-B (higher mass, moderate area growth)."""
        bc_h = VARIANTS["Manna-H"].ballistic_coefficient
        bc_b = VARIANTS["Manna-B"].ballistic_coefficient
        assert bc_h > bc_b, (
            f"Manna-H BC ({bc_h:.0f}) should exceed Manna-B BC ({bc_b:.0f})"
        )


# ---------------------------------------------------------------------------
# Ballistic coefficient calculation  [DERIVED]
# ---------------------------------------------------------------------------

class TestBallisticCoefficient:

    def test_manna_b_bc(self):
        pod = VARIANTS["Manna-B"]
        expected = pod.mass_kg / (pod.cd0 * math.pi * (pod.diameter_m / 2) ** 2)
        assert abs(pod.ballistic_coefficient - expected) < 0.1

    def test_bc_dimensions(self):
        for pod in VARIANTS.values():
            bc = pod.ballistic_coefficient
            assert bc > 0.0
            assert bc < 1e6   # sanity upper bound


# ---------------------------------------------------------------------------
# Elevation angle sweep — verify basic physics
# ---------------------------------------------------------------------------

class TestElevationAngle:

    @pytest.mark.parametrize("elev", [15, 30, 45])
    def test_valid_elevations(self, elev):
        pod = VARIANTS["Manna-B"]
        res = simulate(pod, elevation_deg=elev, dt=0.5)  # coarser dt for speed
        assert res.apogee_km > 0.0
        assert len(res.points) > 5

    def test_45deg_higher_apogee_than_15deg(self):
        pod = VARIANTS["Manna-B"]
        res_15 = simulate(pod, elevation_deg=15.0, dt=0.5)
        res_45 = simulate(pod, elevation_deg=45.0, dt=0.5)
        assert res_45.apogee_km > res_15.apogee_km


# ---------------------------------------------------------------------------
# New SimResult fields — vx_at_apogee, v_circ_at_apogee, peak heat flux
# ---------------------------------------------------------------------------

class TestNewSimResultFields:

    @pytest.fixture(scope="class")
    def result_b(self):
        return simulate(VARIANTS["Manna-B"], elevation_deg=30.0, dt=0.5)

    @pytest.fixture(scope="class")
    def result_h(self):
        return simulate(VARIANTS["Manna-H"], elevation_deg=30.0, dt=0.5)

    def test_vx_at_apogee_positive(self, result_b):
        """Horizontal velocity at apogee must be positive (pod still moving downrange)."""
        assert result_b.vx_at_apogee > 0.0

    def test_vx_at_apogee_less_than_launch_velocity(self, result_b):
        """Drag reduces vx; apogee horizontal speed < launch speed."""
        assert result_b.vx_at_apogee < VARIANTS["Manna-B"].launch_v_ms

    def test_v_circ_at_apogee_physical(self, result_b):
        """v_circ at apogee should be in the range 7–8 km/s (LEO-regime)."""
        vc = result_b.v_circ_at_apogee
        assert 6_000 < vc < 9_000, f"v_circ_at_apogee={vc:.0f} m/s outside [6k, 9k]"

    def test_orbital_at_apogee_false_for_all_variants(self):
        """None of the v0.1 variants achieve orbit at apogee — drag is fatal."""
        for name, pod in VARIANTS.items():
            res = simulate(pod, elevation_deg=30.0, dt=0.5)
            assert not res.orbital_at_apogee, (
                f"{name}: orbital_at_apogee should be False — "
                f"vx={res.vx_at_apogee:.0f} m/s vs v_circ={res.v_circ_at_apogee:.0f} m/s"
            )

    def test_peak_heat_flux_enormous(self, result_h):
        """
        Manna-H at Mach 32 at sea level: Sutton-Graves predicts ~1 GW/m².
        Confirms the thermal constraint is catastrophic.  [CONSTRAINT-NOT-MODELED]
        """
        hf_gw = result_h.peak_heat_flux_W_m2 / 1e9
        assert hf_gw > 0.1, (
            f"Peak heat flux {hf_gw:.2f} GW/m² unexpectedly low; check Sutton-Graves calc"
        )

    def test_peak_heat_flux_positive(self, result_b):
        assert result_b.peak_heat_flux_W_m2 > 0.0

    def test_sutton_graves_constants_physical(self):
        """Spot-check the Sutton-Graves constant and nose radius are reasonable."""
        assert 1e-5 < SUTTON_GRAVES_K < 1e-3
        assert 0.01 < NOSE_RADIUS_M < 1.0
