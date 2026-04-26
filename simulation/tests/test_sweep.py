"""
Smoke tests for the BC × elevation parametric sweep module.

Uses a minimal 2-BC × 2-elevation grid with coarse dt to keep runtime under
a few seconds while still exercising the full code path.

Author: Shane Brazelton + Claude (Anthropic)
Date:   2026-04-25
"""

import math
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from sweep import _make_sweep_pod, run_sweep, BC_VALUES, ELEV_VALUES
from trajectory_sim import simulate, VARIANTS


# ---------------------------------------------------------------------------
# Synthetic pod factory
# ---------------------------------------------------------------------------

class TestMakeSweepPod:

    def test_bc_matches_target(self):
        """_make_sweep_pod must produce a pod whose BC equals the requested value."""
        for bc_target in [1_000.0, 10_000.0, 50_000.0]:
            pod = _make_sweep_pod("Manna-B", bc_target)
            bc_actual = pod.ballistic_coefficient
            assert abs(bc_actual - bc_target) / bc_target < 1e-9, (
                f"BC mismatch: target={bc_target}, actual={bc_actual:.4f}"
            )

    def test_launch_velocity_matches_variant(self):
        """Sweep pod inherits the launch velocity of the named variant."""
        for vname in VARIANTS:
            for bc in [1_000.0, 50_000.0]:
                pod = _make_sweep_pod(vname, bc)
                assert pod.launch_v_ms == VARIANTS[vname].launch_v_ms

    def test_diameter_positive(self):
        for bc in BC_VALUES:
            pod = _make_sweep_pod("Manna-H", bc)
            assert pod.diameter_m > 0.0

    def test_higher_bc_smaller_pod(self):
        """Higher BC → smaller frontal area → smaller diameter."""
        pod_lo = _make_sweep_pod("Manna-B", 1_000.0)
        pod_hi = _make_sweep_pod("Manna-B", 50_000.0)
        assert pod_hi.diameter_m < pod_lo.diameter_m


# ---------------------------------------------------------------------------
# Minimal grid sweep (fast)
# ---------------------------------------------------------------------------

@pytest.fixture(scope="module")
def mini_sweep():
    """Run a 2-BC × 2-elevation mini sweep for all variants.  Shared across tests."""
    results = {}
    for vname in VARIANTS:
        rows = []
        for bc in [1_000.0, 10_000.0]:
            row = []
            for elev in [30.0, 60.0]:
                pod = _make_sweep_pod(vname, bc)
                res = simulate(pod, elevation_deg=elev, dt=1.0)
                row.append(res)
            rows.append(row)
        results[vname] = rows
    return results


class TestMiniSweep:

    def test_all_variants_present(self, mini_sweep):
        for vname in VARIANTS:
            assert vname in mini_sweep

    def test_grid_shape(self, mini_sweep):
        for vname in VARIANTS:
            assert len(mini_sweep[vname]) == 2       # 2 BC values
            for row in mini_sweep[vname]:
                assert len(row) == 2                 # 2 elevation angles

    def test_apogees_positive(self, mini_sweep):
        for vname in VARIANTS:
            for row in mini_sweep[vname]:
                for res in row:
                    assert res.apogee_km > 0.0

    def test_higher_bc_higher_or_equal_apogee(self, mini_sweep):
        """
        For the same launch velocity and elevation, higher BC (less drag)
        should yield equal or greater apogee.
        """
        for vname in VARIANTS:
            for j in range(2):   # both elevations
                apo_lo_bc = mini_sweep[vname][0][j].apogee_km   # BC=1k
                apo_hi_bc = mini_sweep[vname][1][j].apogee_km   # BC=10k
                assert apo_hi_bc >= apo_lo_bc, (
                    f"{vname} elev_idx={j}: BC=10k apogee ({apo_hi_bc:.1f} km) "
                    f"should be ≥ BC=1k apogee ({apo_lo_bc:.1f} km)"
                )

    def test_vx_at_apogee_field_populated(self, mini_sweep):
        for vname in VARIANTS:
            for row in mini_sweep[vname]:
                for res in row:
                    assert res.vx_at_apogee >= 0.0

    def test_v_circ_at_apogee_field_populated(self, mini_sweep):
        for vname in VARIANTS:
            for row in mini_sweep[vname]:
                for res in row:
                    assert res.v_circ_at_apogee > 0.0

    def test_peak_heat_flux_populated(self, mini_sweep):
        for vname in VARIANTS:
            for row in mini_sweep[vname]:
                for res in row:
                    assert res.peak_heat_flux_W_m2 > 0.0
