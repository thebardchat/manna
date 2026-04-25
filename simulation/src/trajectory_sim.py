"""
Manna Pod Trajectory Simulator

3-DOF point-mass ballistic integrator for Manna-H / Manna-I / Manna-B cargo pod variants.
US Standard Atmosphere 1976 (inline, no external deps beyond numpy/matplotlib).
RK4, 0.1 s time step.  Flat-Earth model with altitude-varying gravity.

Inputs:  variant name, rail elevation angle (15–45°), launch azimuth, ballistic coefficient
Outputs: altitude vs time, ground range vs time, dynamic pressure vs time, Mach vs altitude,
         apogee altitude, apogee range, max-Q, comparison table (v0.1 claims vs sim results)

Run directly:  python simulation/src/trajectory_sim.py
Plots saved:   simulation/data/trajectory_runs/trajectory_30deg_sanity_check.png

Author: Shane Brazelton + Claude (Anthropic)
Date:   2026-04-25
"""

from __future__ import annotations

import math
import os
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional, Tuple

import numpy as np
import matplotlib
matplotlib.use("Agg")   # headless — no display needed on Pi
import matplotlib.pyplot as plt


# ---------------------------------------------------------------------------
# Physical constants  [VERIFIED: NIST / IAU / COESA 1976]
# ---------------------------------------------------------------------------

R_EARTH: float = 6_371_000.0   # m   — WGS-84 mean radius
G0:      float = 9.80665        # m/s²— standard gravity (sea level)
GAMMA:   float = 1.4            # specific heat ratio, dry air
R_AIR:   float = 287.058        # J/(kg·K) — gas constant, dry air


# ---------------------------------------------------------------------------
# US Standard Atmosphere 1976 — inline implementation
# Ref: NOAA / NASA / USAF, "U.S. Standard Atmosphere, 1976"  [VERIFIED]
#
# Each layer entry: (base_alt_m, base_temp_K, lapse_rate_K/m, base_pressure_Pa)
# ---------------------------------------------------------------------------

_LAYERS: Tuple[Tuple[float, float, float, float], ...] = (
    (      0.0,  288.15, -0.0065,  101_325.00),   # troposphere
    ( 11_000.0,  216.65,  0.0000,   22_632.10),   # tropopause      (isothermal)
    ( 20_000.0,  216.65,  0.0010,    5_474.89),   # lower stratosphere
    ( 32_000.0,  228.65,  0.0028,      868.019),  # upper stratosphere
    ( 47_000.0,  270.65,  0.0000,      110.906),  # stratopause     (isothermal)
    ( 51_000.0,  270.65, -0.0028,       66.9389), # lower mesosphere
    ( 71_000.0,  214.65, -0.0020,        3.95642),# upper mesosphere
    ( 86_000.0,  186.87,  0.0000,        0.37338),# mesopause       (isothermal approx)
)


def atmo_temperature(alt_m: float) -> float:
    """Air temperature [K] at geometric altitude [m].  [VERIFIED: USSA 1976 Table 1]"""
    alt_m = max(alt_m, 0.0)
    if alt_m >= 86_000.0:
        return _LAYERS[-1][1]
    for i in range(len(_LAYERS) - 1, -1, -1):
        h_b, T_b, L_b, _ = _LAYERS[i]
        if alt_m >= h_b:
            return T_b + L_b * (alt_m - h_b)
    return _LAYERS[0][1]


def atmo_pressure(alt_m: float) -> float:
    """Air pressure [Pa] at geometric altitude [m].  [VERIFIED: USSA 1976 Table 1]"""
    alt_m = max(alt_m, 0.0)
    if alt_m >= 86_000.0:
        # Exponential decay above mesopause — density negligible above ~300 km
        _, T_b, _, P_b = _LAYERS[-1]
        H_scale = R_AIR * T_b / G0              # scale height ≈ 5460 m
        return P_b * math.exp(-(alt_m - 86_000.0) / H_scale)
    for i in range(len(_LAYERS) - 1, -1, -1):
        h_b, T_b, L_b, P_b = _LAYERS[i]
        if alt_m >= h_b:
            if abs(L_b) < 1e-12:                # isothermal layer
                return P_b * math.exp(-G0 * (alt_m - h_b) / (R_AIR * T_b))
            else:
                T = T_b + L_b * (alt_m - h_b)
                return P_b * (T / T_b) ** (-G0 / (L_b * R_AIR))
    return _LAYERS[0][3]


def atmo_density(alt_m: float) -> float:
    """Air density [kg/m³] at geometric altitude [m].  [DERIVED: ideal gas law]"""
    T = atmo_temperature(alt_m)
    P = atmo_pressure(alt_m)
    return P / (R_AIR * T)


def atmo_speed_of_sound(alt_m: float) -> float:
    """Speed of sound [m/s] at geometric altitude [m].  [DERIVED: ideal gas]"""
    T = atmo_temperature(alt_m)
    return math.sqrt(GAMMA * R_AIR * T)


# ---------------------------------------------------------------------------
# Variant definitions
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class MannaPod:
    """Physical parameters for one Manna cargo pod variant.  [ESTIMATE unless tagged]"""
    name:              str
    mass_kg:           float   # total launch mass (pod + payload)     [ESTIMATE]
    diameter_m:        float   # maximum body diameter                  [ESTIMATE]
    cd0:               float   # reference drag coefficient, high-Mach  [ESTIMATE]
    launch_v_ms:       float   # rail exit velocity                     [DERIVED — matches v0.1 vacuum apogee]
    v01_apogee_km:     float   # v0.1 paper claimed apogee (vacuum, no drag)  [PLACEHOLDER]

    @property
    def frontal_area(self) -> float:
        """Cross-sectional (frontal) area [m²].  [DERIVED]"""
        return math.pi * (self.diameter_m / 2.0) ** 2

    @property
    def ballistic_coefficient(self) -> float:
        """BC = m / (Cd × A)  [kg/m²].  [DERIVED]"""
        return self.mass_kg / (self.cd0 * self.frontal_area)


# Launch velocities back-calculated from v0.1 vacuum apogee claims using:
#   v_z² = 2 × g₀ × R_E × h / (R_E + h)   (vis-viva, radial component)
#   v_launch = v_z / sin(30°)
# [DERIVED — these reproduce v0.1 claimed apogees exactly in a vacuum simulation]
VARIANTS: dict[str, MannaPod] = {
    "Manna-B": MannaPod(
        name="Manna-B",
        mass_kg=80.0,
        diameter_m=0.40,
        cd0=0.40,
        launch_v_ms=4_318.0,    # → v_z = 2159 m/s → 247 km vacuum apogee  [DERIVED]
        v01_apogee_km=247.0,
    ),
    "Manna-I": MannaPod(
        name="Manna-I",
        mass_kg=250.0,
        diameter_m=0.65,
        cd0=0.42,
        launch_v_ms=7_670.0,    # → v_z = 3835 m/s → 850 km vacuum apogee  [DERIVED]
        v01_apogee_km=850.0,
    ),
    "Manna-H": MannaPod(
        name="Manna-H",
        mass_kg=800.0,
        diameter_m=1.00,
        cd0=0.45,
        launch_v_ms=10_814.0,   # → v_z = 5407 m/s → 1950 km vacuum apogee [DERIVED]
        v01_apogee_km=1_950.0,
    ),
}


# ---------------------------------------------------------------------------
# Data containers
# ---------------------------------------------------------------------------

@dataclass
class TrajPoint:
    """State at one integration time step."""
    t:        float   # s
    x:        float   # m  downrange
    z:        float   # m  altitude
    vx:       float   # m/s
    vz:       float   # m/s
    rho:      float   # kg/m³
    q:        float   # Pa  dynamic pressure
    mach:     float
    g_accel:  float   # m/s²  local gravity

    @property
    def speed(self) -> float:
        return math.hypot(self.vx, self.vz)


@dataclass
class SimResult:
    """Full trajectory and summary statistics for one variant run."""
    variant:          MannaPod
    elevation_deg:    float
    azimuth_deg:      float
    points:           List[TrajPoint] = field(default_factory=list)
    apogee_km:        float = 0.0
    apogee_range_km:  float = 0.0
    max_q_pa:         float = 0.0
    max_q_alt_km:     float = 0.0
    max_mach:         float = 0.0
    impact_range_km:  float = 0.0
    impact_time_s:    float = 0.0
    orbital_flag:     bool  = False  # True if vx > circular orbital v at any point above 100 km

    @property
    def arrays(self) -> dict:
        """Convert trajectory list to numpy arrays (in convenient units)."""
        pts = self.points
        return {
            "t":     np.array([p.t    for p in pts]),
            "x_km":  np.array([p.x    for p in pts]) / 1000.0,
            "z_km":  np.array([p.z    for p in pts]) / 1000.0,
            "vx":    np.array([p.vx   for p in pts]),
            "vz":    np.array([p.vz   for p in pts]),
            "speed": np.array([p.speed for p in pts]),
            "q_kpa": np.array([p.q    for p in pts]) / 1000.0,
            "mach":  np.array([p.mach for p in pts]),
        }


# ---------------------------------------------------------------------------
# Physics helpers
# ---------------------------------------------------------------------------

def gravity(alt_m: float) -> float:
    """Altitude-dependent gravitational acceleration [m/s²].  [VERIFIED: inverse-square]"""
    r = R_EARTH + max(alt_m, 0.0)
    return G0 * (R_EARTH / r) ** 2


def circular_orbital_velocity(alt_m: float) -> float:
    """Circular orbital speed at altitude alt_m [m/s].  [VERIFIED: Keplerian]"""
    r = R_EARTH + max(alt_m, 0.0)
    return math.sqrt(G0 * R_EARTH ** 2 / r)


def cd_mach_correction(cd0: float, mach: float) -> float:
    """
    Simple Mach-number drag coefficient for a blunt body.
    Applies a modest transonic bump (+8% near M=1) decaying at supersonic speeds.
    Constant at subsonic and hypersonic extremes.  [ESTIMATE — no CFD yet]
    """
    if mach < 0.8:
        return cd0
    # Gaussian bump centred at M=1.0, width σ=0.4
    bump = 0.08 * math.exp(-0.5 * ((mach - 1.0) / 0.4) ** 2)
    return cd0 * (1.0 + bump)


# ---------------------------------------------------------------------------
# RK4 integrator
# ---------------------------------------------------------------------------

def _derivatives(state: np.ndarray, pod: MannaPod) -> np.ndarray:
    """
    Equations of motion for a point mass under gravity + aerodynamic drag.
    State = [x, z, vx, vz] (flat-Earth, 2-D).  [DERIVED]

    dx/dt  = vx
    dz/dt  = vz
    dvx/dt = -q_eff × (vx / v)   drag opposing velocity
    dvz/dt = -q_eff × (vz / v) - g(z)
    where q_eff = (0.5 ρ v² Cd A) / m = (dynamic pressure) / BC_eff
    """
    x, z, vx, vz = state
    alt = max(z, 0.0)

    v    = math.hypot(vx, vz)
    g    = gravity(alt)
    rho  = atmo_density(alt)
    a_snd = atmo_speed_of_sound(alt)
    mach = v / a_snd if a_snd > 0.0 else 0.0

    q        = 0.5 * rho * v * v                              # dynamic pressure [Pa]
    cd_eff   = cd_mach_correction(pod.cd0, mach)
    bc_eff   = pod.mass_kg / (cd_eff * pod.frontal_area)      # effective BC [kg/m²]
    a_drag   = q / bc_eff                                     # drag decel magnitude [m/s²]

    if v > 0.5:
        ax = -a_drag * (vx / v)
        az = -a_drag * (vz / v) - g
    else:
        ax = 0.0
        az = -g

    return np.array([vx, vz, ax, az])


def _rk4_step(state: np.ndarray, dt: float, pod: MannaPod) -> np.ndarray:
    """Single RK4 integration step.  [VERIFIED: classic 4th-order Runge-Kutta]"""
    k1 = _derivatives(state,                   pod)
    k2 = _derivatives(state + 0.5 * dt * k1,  pod)
    k3 = _derivatives(state + 0.5 * dt * k2,  pod)
    k4 = _derivatives(state + dt * k3,         pod)
    return state + (dt / 6.0) * (k1 + 2.0 * k2 + 2.0 * k3 + k4)


# ---------------------------------------------------------------------------
# Main simulation runner
# ---------------------------------------------------------------------------

def simulate(
    pod:           MannaPod,
    elevation_deg: float = 30.0,
    azimuth_deg:   float = 90.0,   # azimuth stored for future 3-D extension; not used in 2-D
    dt:            float = 0.1,    # s — RK4 time step
    t_max:         float = 3_600.0,# s — integration ceiling (1 hr >> any suborbital flight)
) -> SimResult:
    """
    Integrate 3-DOF flat-Earth ballistic trajectory for one Manna pod variant.

    Returns SimResult containing the full trajectory and derived statistics.
    Orbital flag is set when horizontal velocity exceeds circular orbital velocity
    above 100 km — a necessary (not sufficient) condition for orbital insertion.
    [DERIVED — all outputs are simulation results, not paper claims]
    """
    el_rad = math.radians(elevation_deg)
    vx0 = pod.launch_v_ms * math.cos(el_rad)
    vz0 = pod.launch_v_ms * math.sin(el_rad)

    state = np.array([0.0, 0.0, vx0, vz0])
    result = SimResult(variant=pod, elevation_deg=elevation_deg, azimuth_deg=azimuth_deg)

    t         = 0.0
    apogee_z  = 0.0
    apogee_x  = 0.0
    max_q     = 0.0
    max_q_alt = 0.0

    while t < t_max:
        x, z, vx, vz = state
        alt  = max(z, 0.0)
        v    = math.hypot(vx, vz)
        rho  = atmo_density(alt)
        a_snd = atmo_speed_of_sound(alt)
        mach = v / a_snd if a_snd > 0.0 else 0.0
        q    = 0.5 * rho * v * v
        g    = gravity(alt)

        # Orbital check: flag if horizontal speed exceeds circular orbital v above Karman line
        if alt > 100_000.0 and vx > circular_orbital_velocity(alt):
            result.orbital_flag = True

        # Store trajectory point
        pt = TrajPoint(t=t, x=x, z=z, vx=vx, vz=vz,
                       rho=rho, q=q, mach=mach, g_accel=g)
        result.points.append(pt)

        # Apogee tracking
        if z > apogee_z:
            apogee_z = z
            apogee_x = x

        # Max-Q tracking
        if q > max_q:
            max_q     = q
            max_q_alt = alt

        # Termination: ground impact (allow 2 s for initial rail climb out of z=0)
        if t > 2.0 and z <= 0.0:
            break

        state = _rk4_step(state, dt, pod)
        t += dt

    # Final derived statistics
    result.apogee_km       = apogee_z / 1000.0
    result.apogee_range_km = apogee_x / 1000.0
    result.max_q_pa        = max_q
    result.max_q_alt_km    = max_q_alt / 1000.0
    result.max_mach        = max((p.mach for p in result.points), default=0.0)

    if result.points:
        last = result.points[-1]
        result.impact_range_km = last.x / 1000.0
        result.impact_time_s   = last.t

    return result


# ---------------------------------------------------------------------------
# Plotting
# ---------------------------------------------------------------------------

_COLORS = {"Manna-B": "#2196F3", "Manna-I": "#FF9800", "Manna-H": "#E53935"}
_KARMAN_KM = 100.0   # Kármán line


def _make_label(res: SimResult) -> str:
    v = res.variant
    orb = " [ORBITAL⚠]" if res.orbital_flag else ""
    return f"{v.name} — BC={v.ballistic_coefficient:.0f} kg/m²{orb}"


def plot_all(results: List[SimResult], out_dir: Path) -> Path:
    """Generate 4-panel trajectory comparison plot and save as PNG."""
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle(
        f"Manna Pod Trajectory — {results[0].elevation_deg:.0f}° Elevation | "
        "US Std Atm 1976 | RK4 0.1 s",
        fontsize=13,
    )
    ax_alt, ax_rng, ax_dyn, ax_mach = axes.flat

    for res in results:
        a   = res.arrays
        c   = _COLORS.get(res.variant.name, "gray")
        lbl = _make_label(res)

        ax_alt.plot(a["t"],  a["z_km"],  color=c, label=lbl, linewidth=1.8)
        ax_rng.plot(a["t"],  a["x_km"],  color=c, label=lbl, linewidth=1.8)
        ax_dyn.plot(a["t"],  a["q_kpa"], color=c, label=lbl, linewidth=1.8)

        # Mach vs altitude — ascending leg only (vz > 0)
        asc = a["vz"] > 0
        ax_mach.plot(a["mach"][asc], a["z_km"][asc], color=c, label=lbl, linewidth=1.8)

    # Kármán line reference
    for ax in (ax_alt, ax_mach):
        ax.axhline(_KARMAN_KM, color="gray", linestyle="--", linewidth=0.8,
                   label="Kármán line (100 km)")

    _style_ax(ax_alt,  "Time (s)",       "Altitude (km)")
    _style_ax(ax_rng,  "Time (s)",       "Ground range (km)")
    _style_ax(ax_dyn,  "Time (s)",       "Dynamic pressure (kPa)", log_y=True)
    _style_ax(ax_mach, "Mach number",    "Altitude (km)")

    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "trajectory_30deg_sanity_check.png"
    fig.tight_layout()
    fig.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return out_path


def _style_ax(ax, xlabel: str, ylabel: str, log_y: bool = False) -> None:
    ax.set_xlabel(xlabel, fontsize=10)
    ax.set_ylabel(ylabel, fontsize=10)
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.25)
    if log_y:
        ax.set_yscale("log")


# ---------------------------------------------------------------------------
# Summary table
# ---------------------------------------------------------------------------

def print_summary(results: List[SimResult]) -> None:
    """Print comparison table: v0.1 paper claims vs. simulator results."""
    cols = (
        f"{'Variant':<12} "
        f"{'v0.1 claim (km)':>16} "
        f"{'Sim apogee (km)':>16} "
        f"{'Delta (km)':>11} "
        f"{'Sim/v0.1':>9} "
        f"{'Max-Q (kPa)':>12} "
        f"{'Max Mach':>9} "
        f"{'BC (kg/m²)':>11} "
        f"{'Orbital':>8}"
    )
    sep = "=" * len(cols)

    print()
    print(sep)
    print("Manna Trajectory Simulator — v0.1 Paper Claims vs. Simulation  [DERIVED]")
    print("Elevation: 30°  |  US Std Atm 1976  |  RK4 0.1 s  |  Flat-Earth + varying-g")
    print(sep)
    print(cols)
    print("-" * len(cols))

    for res in results:
        v01   = res.variant.v01_apogee_km
        sim   = res.apogee_km
        delta = sim - v01
        ratio = sim / v01 if v01 > 0 else float("nan")
        maxq  = res.max_q_pa / 1000.0
        orb   = "YES ⚠" if res.orbital_flag else "no"
        bc    = res.variant.ballistic_coefficient

        print(
            f"{res.variant.name:<12} "
            f"{v01:>16.1f} "
            f"{sim:>16.1f} "
            f"{delta:>+11.1f} "
            f"{ratio:>9.3f} "
            f"{maxq:>12.1f} "
            f"{res.max_mach:>9.1f} "
            f"{bc:>11.0f} "
            f"{orb:>8}"
        )

    print(sep)
    print()
    print("  [DERIVED]  Sim apogee — includes US Std Atm 1976 drag + altitude-varying gravity")
    print("  [PLACEHOLDER]  v0.1 claims — vacuum, constant g₀; reproduced from vis-viva formula")
    print("  [ESTIMATE] Cd₀, mass, diameter — awaiting structural design and CFD")
    print("  Orbital flag — horizontal v exceeded circular orbital v above Kármán line (100 km)")
    print()


# ---------------------------------------------------------------------------
# Run-all entry point
# ---------------------------------------------------------------------------

def run_sanity_check(
    elevation_deg: float = 30.0,
    dt:            float = 0.1,
    out_dir:       Optional[Path] = None,
) -> List[SimResult]:
    """
    Run all three Manna variants at the specified elevation angle.
    Saves plots and prints summary table.  Returns results list.
    """
    if out_dir is None:
        out_dir = Path(__file__).resolve().parent.parent / "data" / "trajectory_runs"

    print(f"\nManna trajectory simulation  |  elevation={elevation_deg}°  |  dt={dt} s")
    print("─" * 60)

    results: List[SimResult] = []
    for pod in VARIANTS.values():
        print(f"  {pod.name:<10}  BC={pod.ballistic_coefficient:,.0f} kg/m²  "
              f"v_launch={pod.launch_v_ms:,.0f} m/s  ... ", end="", flush=True)
        res = simulate(pod, elevation_deg=elevation_deg, dt=dt)
        results.append(res)
        orb = " [ORBITAL ⚠]" if res.orbital_flag else ""
        print(f"apogee={res.apogee_km:.1f} km  max-Q={res.max_q_pa/1000:.0f} kPa{orb}")

    out_path = plot_all(results, out_dir)
    print(f"\n  Plot → {out_path}")

    print_summary(results)
    return results


if __name__ == "__main__":
    run_sanity_check()
