"""
Manna BC Feasibility Study

Answers the existential question from the Lukens persona review (Issue #6):
"Can a cargo pod structure simultaneously achieve (a) the BC required to escape
the atmosphere, and (b) the cargo protection required by the G-limits?"

Method:
  1. For each variant, query the sweep results to find minimum BC required to:
     - Reach Kármán line (100 km apogee)
     - Achieve half-orbital velocity at apogee (50% v_circ)
     - Achieve orbital velocity at apogee (vx >= v_circ)
  2. For each target BC, compute the required pod mass given the variant's diameter
     and a realistic drag coefficient.
  3. Compute resulting payload mass fraction.
  4. Check whether any known structural material can produce the required BC
     within the given geometry.
  5. Flag infeasible cases and propose geometry changes.

Run:  python simulation/src/bc_feasibility.py
Output: console table + simulation/data/trajectory_runs/bc_feasibility.png

Author: Shane Brazelton + Claude (Anthropic)
Date:   2026-04-28
"""

from __future__ import annotations

import math
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Tuple

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, str(Path(__file__).resolve().parent))
from trajectory_sim import (
    MannaPod, SimResult, simulate, VARIANTS,
    circular_orbital_velocity, R_EARTH,
)


# ---------------------------------------------------------------------------
# Material density reference table  [VERIFIED: engineering handbooks]
# ---------------------------------------------------------------------------

MATERIALS: List[Tuple[str, float]] = [
    ("Aluminum 7075-T6",     2_810.0),   # kg/m³  [VERIFIED]
    ("Titanium Ti-6Al-4V",   4_430.0),   # kg/m³  [VERIFIED]
    ("Steel 4340",           7_850.0),   # kg/m³  [VERIFIED]
    ("Tungsten alloy",      17_000.0),   # kg/m³  [VERIFIED]
    ("Osmium (densest)",    22_590.0),   # kg/m³  [VERIFIED]
    ("Depleted uranium",    19_050.0),   # kg/m³  [VERIFIED]
    ("PICA-X (ablative)",    0_260.0),   # kg/m³  [ESTIMATE — range 200-400]
    ("Carbon-fiber/epoxy",   1_600.0),   # kg/m³  [VERIFIED]
]


# ---------------------------------------------------------------------------
# Target milestones
# ---------------------------------------------------------------------------

@dataclass
class Milestone:
    label: str
    min_apogee_km: float    # required apogee
    min_vx_frac: float      # required vx/v_circ at apogee (0 = don't care)


MILESTONES: List[Milestone] = [
    Milestone("Kármán line (100 km)",          100.0, 0.0),
    Milestone("Half orbital v at apogee",      100.0, 0.5),
    Milestone("Orbital v at apogee",           100.0, 1.0),
]


# ---------------------------------------------------------------------------
# BC sweep — finer grid than sweep.py, single variant, one elevation
# ---------------------------------------------------------------------------

_BC_FINE: List[float] = [
    1_000, 2_000, 3_000, 5_000, 7_500, 10_000,
    15_000, 20_000, 30_000, 50_000, 75_000, 100_000,
]
_ELEV_STUDY: float = 30.0   # degrees — nominal design point
_DT_STUDY:   float = 0.5    # s — coarser step for speed


def _make_pod(variant_name: str, bc: float) -> MannaPod:
    """Synthetic pod: variant launch velocity + target BC, cd0=0.4."""
    base = VARIANTS[variant_name]
    cd0  = 0.40
    mass = 1.0
    area = mass / (cd0 * bc)
    diam = math.sqrt(4.0 * area / math.pi)
    return MannaPod(
        name=f"{variant_name}-BC{bc:.0f}",
        mass_kg=mass,
        diameter_m=diam,
        cd0=cd0,
        launch_v_ms=base.launch_v_ms,
        v01_apogee_km=base.v01_apogee_km,
    )


def run_bc_sweep(variant_name: str) -> List[SimResult]:
    """Run all BC values for one variant at the study elevation."""
    results = []
    for bc in _BC_FINE:
        pod = _make_pod(variant_name, bc)
        res = simulate(pod, elevation_deg=_ELEV_STUDY, dt=_DT_STUDY)
        results.append(res)
    return results


# ---------------------------------------------------------------------------
# Find minimum BC for each milestone
# ---------------------------------------------------------------------------

def find_min_bc(results: List[SimResult], milestone: Milestone) -> Optional[float]:
    """
    Return the minimum BC (from _BC_FINE) at which the milestone is met.
    Returns None if not met at any swept BC.  [DERIVED]
    """
    for res in results:
        bc   = res.variant.mass_kg / (res.variant.cd0 * res.variant.frontal_area)
        apo  = res.apogee_km
        vfrac = (res.vx_at_apogee / res.v_circ_at_apogee
                 if res.v_circ_at_apogee > 0 else 0.0)
        if apo >= milestone.min_apogee_km and vfrac >= milestone.min_vx_frac:
            return bc
    return None


# ---------------------------------------------------------------------------
# Physical mass required to achieve a target BC with given geometry
# ---------------------------------------------------------------------------

def required_mass(bc: float, diameter_m: float, cd0: float = 0.40) -> float:
    """
    m = BC × Cd × A   where A = π(d/2)²   [DERIVED]
    Returns total pod mass in kg required to achieve the target BC.
    """
    area = math.pi * (diameter_m / 2.0) ** 2
    return bc * cd0 * area


def required_shell_density(
    mass_kg: float,
    diameter_m: float,
    length_m: float,
    wall_fraction: float = 0.15,
) -> float:
    """
    Minimum material density [kg/m³] for a thin cylindrical shell to achieve
    the required structural mass.

    Structural mass = total mass × (1 - payload_fraction).
    Assumed payload fraction: 78% (Manna-H design target).

    Shell volume = π × d × t × L   where t = wall_fraction × d/2

    This is a conservative estimate — real structure has end caps, ribs, etc.
    [ESTIMATE — no structural design exists yet]
    """
    structural_mass = mass_kg * 0.22   # 22% structure at 78% payload fraction
    r = diameter_m / 2.0
    t = wall_fraction * r             # wall thickness = 15% of radius
    shell_volume = math.pi * diameter_m * t * length_m   # m³
    if shell_volume <= 0:
        return float("inf")
    return structural_mass / shell_volume


def find_achievable_material(density_req: float) -> Optional[str]:
    """Return the first material in MATERIALS that meets or exceeds the density."""
    for name, density in MATERIALS:
        if density >= density_req:
            return name
    return None


# ---------------------------------------------------------------------------
# Per-variant feasibility record
# ---------------------------------------------------------------------------

@dataclass
class FeasibilityResult:
    variant_name:    str
    launch_v_ms:     float
    current_bc:      float
    current_mass_kg: float
    diameter_m:      float

    # Per milestone:
    milestone_bc:          List[Optional[float]]  # kg/m² required
    milestone_mass:        List[Optional[float]]  # kg total pod mass
    milestone_pf:          List[Optional[float]]  # payload mass fraction
    milestone_shell_rho:   List[Optional[float]]  # required shell density kg/m³
    milestone_material:    List[Optional[str]]     # achievable material
    milestone_feasible:    List[bool]


def analyze_variant(variant_name: str, sweep: List[SimResult]) -> FeasibilityResult:
    base = VARIANTS[variant_name]
    current_bc = base.ballistic_coefficient

    ms_bc: List[Optional[float]] = []
    ms_mass: List[Optional[float]] = []
    ms_pf: List[Optional[float]] = []
    ms_rho: List[Optional[float]] = []
    ms_mat: List[Optional[str]] = []
    ms_feas: List[bool] = []

    for ms in MILESTONES:
        min_bc = find_min_bc(sweep, ms)
        if min_bc is None:
            ms_bc.append(None)
            ms_mass.append(None)
            ms_pf.append(None)
            ms_rho.append(None)
            ms_mat.append(None)
            ms_feas.append(False)
            continue

        mass = required_mass(min_bc, base.diameter_m)
        payload_fraction = base.mass_kg / mass   # payload = original launch mass
        pod_length_m = base.diameter_m * 3.0     # rough 3:1 L/D estimate [ESTIMATE]
        shell_rho = required_shell_density(mass, base.diameter_m, pod_length_m)
        mat = find_achievable_material(shell_rho)

        ms_bc.append(min_bc)
        ms_mass.append(mass)
        ms_pf.append(payload_fraction)
        ms_rho.append(shell_rho)
        ms_mat.append(mat)
        ms_feas.append(mat is not None and payload_fraction > 0.0)

    return FeasibilityResult(
        variant_name=variant_name,
        launch_v_ms=base.launch_v_ms,
        current_bc=current_bc,
        current_mass_kg=base.mass_kg,
        diameter_m=base.diameter_m,
        milestone_bc=ms_bc,
        milestone_mass=ms_mass,
        milestone_pf=ms_pf,
        milestone_shell_rho=ms_rho,
        milestone_material=ms_mat,
        milestone_feasible=ms_feas,
    )


# ---------------------------------------------------------------------------
# Console output
# ---------------------------------------------------------------------------

def print_feasibility(results: List[FeasibilityResult]) -> None:
    sep = "=" * 110

    print()
    print(sep)
    print("Manna BC Feasibility Study  [DERIVED]")
    print(f"  Elevation: {_ELEV_STUDY}°  |  cd0=0.40  |  US Std Atm 1976  |  RK4 dt={_DT_STUDY} s")
    print(f"  Milestones: {' | '.join(m.label for m in MILESTONES)}")
    print(sep)

    for fr in results:
        print()
        print(f"  {'─'*100}")
        print(f"  {fr.variant_name}   v_launch={fr.launch_v_ms:,.0f} m/s   "
              f"current BC={fr.current_bc:,.0f} kg/m²   d={fr.diameter_m:.2f} m   "
              f"mass={fr.current_mass_kg:.0f} kg")
        print(f"  {'─'*100}")

        for i, ms in enumerate(MILESTONES):
            bc   = fr.milestone_bc[i]
            mass = fr.milestone_mass[i]
            pf   = fr.milestone_pf[i]
            rho  = fr.milestone_shell_rho[i]
            mat  = fr.milestone_material[i]
            feas = fr.milestone_feasible[i]

            status = "✅ FEASIBLE" if feas else "❌ INFEASIBLE"
            if bc is None:
                print(f"  {ms.label:40s}  BC not achievable in sweep → {status}")
                continue

            gap = bc / fr.current_bc
            print(f"  {ms.label:40s}  "
                  f"BC={bc:>8,.0f} kg/m²  ({gap:4.1f}×current)  "
                  f"mass={mass:>7,.0f} kg  "
                  f"payload_frac={pf:.2%}  "
                  f"shell_ρ={rho:>7,.0f} kg/m³  "
                  f"material={mat or 'NONE — BEYOND OSMIUM'}  "
                  f"{status}")

    print()
    print(sep)
    print("Notes:")
    print("  [DERIVED]  BC values from simulation sweep at 30° elevation, cd0=0.40")
    print("  [ESTIMATE] Shell density assumes 3:1 L/D, 15% relative wall thickness, 78% payload fraction")
    print("  [ESTIMATE] 'Material' column is minimum-density material that could achieve required shell density")
    print("  payload_frac = original_variant_mass / required_total_mass — fraction usable as payload")
    print("  INFEASIBLE = required shell density exceeds all known structural materials (>22,590 kg/m³ osmium)")
    print(sep)
    print()


# ---------------------------------------------------------------------------
# Plot — apogee vs BC per variant with milestone lines
# ---------------------------------------------------------------------------

def plot_feasibility(
    sweeps: dict[str, List[SimResult]],
    out_dir: Path,
) -> Path:
    _COLORS = {"Manna-B": "#2196F3", "Manna-I": "#FF9800", "Manna-H": "#E53935"}
    fig, axes = plt.subplots(1, 3, figsize=(18, 6), sharey=False)
    fig.suptitle(
        f"BC Feasibility Study — Apogee vs Ballistic Coefficient\n"
        f"Elevation {_ELEV_STUDY}° | cd0=0.40 | US Std Atm 1976 | RK4",
        fontsize=12,
    )

    for ax, vname in zip(axes, VARIANTS):
        res_list = sweeps[vname]
        bc_vals   = [r.variant.mass_kg / (r.variant.cd0 * r.variant.frontal_area)
                     for r in res_list]
        apo_vals  = [r.apogee_km for r in res_list]
        vfrac_vals = [(r.vx_at_apogee / r.v_circ_at_apogee
                       if r.v_circ_at_apogee > 0 else 0.0) for r in res_list]

        color = _COLORS.get(vname, "gray")
        ax.semilogx(bc_vals, apo_vals, color=color, linewidth=2, marker="o",
                    markersize=5, label="Apogee (km)")

        # Kármán line
        ax.axhline(100.0, color="lime", linestyle="--", linewidth=1.5,
                   label="Kármán 100 km")

        # Current BC marker
        current_bc = VARIANTS[vname].ballistic_coefficient
        ax.axvline(current_bc, color="gray", linestyle=":", linewidth=1.2,
                   label=f"Current BC={current_bc:.0f}")

        ax.set_xlabel("Ballistic coefficient (kg/m²)", fontsize=10)
        ax.set_ylabel("Apogee altitude (km)", fontsize=10)
        ax.set_title(f"{vname}\nv_launch={VARIANTS[vname].launch_v_ms:,.0f} m/s", fontsize=10)
        ax.legend(fontsize=8)
        ax.grid(True, which="both", alpha=0.25)

        # vx/v_circ on twin axis
        ax2 = ax.twinx()
        ax2.semilogx(bc_vals, vfrac_vals, color="cyan", linewidth=1.5,
                     linestyle="--", marker="^", markersize=4, label="vx/v_circ")
        ax2.axhline(1.0, color="cyan", linestyle=":", linewidth=0.8)
        ax2.set_ylabel("vx / v_circ at apogee", fontsize=9, color="cyan")
        ax2.tick_params(axis="y", labelcolor="cyan")
        ax2.set_ylim(0, 1.2)
        ax2.legend(fontsize=8, loc="upper left")

    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "bc_feasibility.png"
    fig.tight_layout()
    fig.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return out_path


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def run_feasibility_study(
    out_dir: Optional[Path] = None,
) -> List[FeasibilityResult]:
    if out_dir is None:
        out_dir = Path(__file__).resolve().parent.parent / "data" / "trajectory_runs"

    print("\nManna BC Feasibility Study")
    print(f"  Running BC sweep for all 3 variants at {_ELEV_STUDY}° elevation ...")
    print(f"  BC range: {[int(b) for b in _BC_FINE]} kg/m²")
    print()

    sweeps: dict[str, List[SimResult]] = {}
    for vname in VARIANTS:
        print(f"  {vname} ...", end=" ", flush=True)
        s = run_bc_sweep(vname)
        sweeps[vname] = s
        print(f"done ({len(s)} runs)")

    print()
    feas_results = [analyze_variant(vn, sweeps[vn]) for vn in VARIANTS]
    print_feasibility(feas_results)

    out_path = plot_feasibility(sweeps, out_dir)
    print(f"  Plot → {out_path}")
    print()

    return feas_results


if __name__ == "__main__":
    run_feasibility_study()
