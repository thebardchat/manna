"""
Manna Pod Concept Evaluator

Drives every entry in `pod_concepts.CONCEPT_PODS` through:

  1. The 3-DOF trajectory simulator at three rail elevation angles
     (15°, 30°, 45° — the BGKPJR rail's stated incline range).
  2. A trajectory plot per concept (4 panels: altitude, range, dynamic
     pressure, Mach vs altitude).
  3. A console report with apogee, max-Q, peak Mach, peak heat flux,
     orbital-at-apogee flag, and a per-concept verdict.

Run:    python simulation/src/concept_eval.py
Plots:  simulation/data/trajectory_runs/concept_<id>.png
Report: stdout

Author: Shane Brazelton + Claude (Anthropic)
Date:   2026-04-27
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, str(Path(__file__).resolve().parent))
from trajectory_sim import simulate, SimResult, circular_orbital_velocity
from pod_concepts import CONCEPT_PODS, PodConcept, print_registry


ELEVATIONS_DEG: Tuple[float, ...] = (15.0, 30.0, 45.0)
KARMAN_KM: float = 100.0


# ---------------------------------------------------------------------------
# Run one concept across all elevations
# ---------------------------------------------------------------------------

def evaluate_concept(concept: PodConcept) -> Dict[float, SimResult]:
    """Simulate `concept` at each rail elevation; return {elev: SimResult}."""
    out: Dict[float, SimResult] = {}
    for elev in ELEVATIONS_DEG:
        out[elev] = simulate(concept.pod, elevation_deg=elev, dt=0.1)
    return out


# ---------------------------------------------------------------------------
# Pass / fail criteria
# ---------------------------------------------------------------------------
#
# These are coarse gates — a concept clearing them is "worth more design work,"
# not "ready to fly."

def verdict(results: Dict[float, SimResult]) -> Tuple[str, List[str]]:
    """
    Coarse pass/fail at 30° elevation, with notes pulled from the full sweep.
    Returns (label, bullet_points).
    """
    res30 = results[30.0]
    notes: List[str] = []

    karman_clearing_elevs = [e for e, r in results.items() if r.apogee_km >= KARMAN_KM]
    orbital_apogee_elevs  = [e for e, r in results.items() if r.orbital_at_apogee]
    best_vx_ratio = max(
        r.vx_at_apogee / r.v_circ_at_apogee
        for r in results.values() if r.v_circ_at_apogee > 0
    )

    if karman_clearing_elevs:
        notes.append(
            f"Clears Kármán line (≥{KARMAN_KM:.0f} km) at "
            f"{', '.join(f'{e:.0f}°' for e in karman_clearing_elevs)}."
        )
    else:
        notes.append(
            f"Does not clear Kármán line at any tested elevation "
            f"(best apogee {max(r.apogee_km for r in results.values()):.1f} km)."
        )

    if orbital_apogee_elevs:
        notes.append(
            "Reaches `orbital_at_apogee` (vx ≥ v_circ) at "
            f"{', '.join(f'{e:.0f}°' for e in orbital_apogee_elevs)} — Tug rendezvous viable."
        )
    else:
        notes.append(
            f"Best vx/v_circ at apogee = {best_vx_ratio:.3f}; below circular orbit speed "
            "— Tug must close significant ΔV."
        )

    peak_hf_gw = max(r.peak_heat_flux_W_m2 for r in results.values()) / 1e9
    notes.append(
        f"Peak Sutton-Graves stagnation heat flux across sweep = {peak_hf_gw:.2f} GW/m² "
        "[CONSTRAINT-NOT-MODELED — TPS unsized]."
    )

    if karman_clearing_elevs and orbital_apogee_elevs:
        label = "PROMISING — proceed to next-fidelity design pass"
    elif karman_clearing_elevs:
        label = "PARTIAL — altitude clears, but rendezvous burn is large"
    else:
        label = "FAILS — concept does not close trajectory; redesign"

    return label, notes


# ---------------------------------------------------------------------------
# Plot helpers
# ---------------------------------------------------------------------------

_PALETTE = {15.0: "#2196F3", 30.0: "#FF9800", 45.0: "#E53935"}


def plot_concept(
    concept:  PodConcept,
    results:  Dict[float, SimResult],
    out_dir:  Path,
) -> Path:
    """4-panel concept trajectory plot.  One PNG per concept."""
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle(
        f"{concept.concept_id} — {concept.geometry}\n"
        f"mass={concept.pod.mass_kg:,.0f} kg  D={concept.pod.diameter_m:.2f} m  "
        f"L={concept.length_m:.2f} m  L/D={concept.fineness_ratio:.1f}  "
        f"Cd₀={concept.pod.cd0:.2f}  BC={concept.pod.ballistic_coefficient:,.0f} kg/m²  "
        f"v_rail={concept.rail_v_exit:,.0f} m/s",
        fontsize=11,
    )
    ax_alt, ax_rng, ax_q, ax_mach = axes.flat

    for elev, res in sorted(results.items()):
        a = res.arrays
        c = _PALETTE.get(elev, "gray")
        lbl = f"{elev:.0f}°  apogee={res.apogee_km:.1f} km"

        ax_alt.plot(a["t"], a["z_km"],  color=c, label=lbl, linewidth=1.8)
        ax_rng.plot(a["t"], a["x_km"],  color=c, label=lbl, linewidth=1.8)
        ax_q.plot(a["t"],   a["q_kpa"], color=c, label=lbl, linewidth=1.8)
        asc = a["vz"] > 0
        ax_mach.plot(a["mach"][asc], a["z_km"][asc], color=c, label=lbl, linewidth=1.8)

    for ax in (ax_alt, ax_mach):
        ax.axhline(KARMAN_KM, color="gray", linestyle="--", linewidth=0.8,
                   label=f"Kármán ({KARMAN_KM:.0f} km)")

    _style(ax_alt,  "Time (s)",     "Altitude (km)")
    _style(ax_rng,  "Time (s)",     "Ground range (km)")
    _style(ax_q,    "Time (s)",     "Dynamic pressure (kPa)", log_y=True)
    _style(ax_mach, "Mach number",  "Altitude (km)")

    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"concept_{concept.concept_id}.png"
    fig.tight_layout()
    fig.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return out_path


def _style(ax, xlabel: str, ylabel: str, log_y: bool = False) -> None:
    ax.set_xlabel(xlabel, fontsize=10)
    ax.set_ylabel(ylabel, fontsize=10)
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.25)
    if log_y:
        ax.set_yscale("log")


# ---------------------------------------------------------------------------
# Console report
# ---------------------------------------------------------------------------

def print_concept_report(concept: PodConcept, results: Dict[float, SimResult]) -> None:
    width = 100
    print()
    print("=" * width)
    print(f"  {concept.concept_id}  —  cargo class {concept.cargo_class}  —  {concept.geometry}")
    print("=" * width)
    print(f"  Intent: {concept.intent}")
    print()
    print(f"  Geometry [ESTIMATE]:")
    print(f"    diameter        {concept.pod.diameter_m:.2f} m")
    print(f"    length          {concept.length_m:.2f} m")
    print(f"    fineness L/D    {concept.fineness_ratio:.1f}")
    print(f"    mass            {concept.pod.mass_kg:,.0f} kg total  "
          f"(~{concept.cargo_mass_kg:,.0f} kg cargo at 65% fraction)")
    print(f"    Cd₀             {concept.pod.cd0:.2f}     [ESTIMATE]")
    print(f"    BC              {concept.pod.ballistic_coefficient:,.0f} kg/m²  [DERIVED]")
    print(f"    rail v_exit     {concept.rail_v_exit:,.0f} m/s   [PLACEHOLDER]")

    print()
    print(f"  Trajectory results [DERIVED — US Std Atm 1976 + RK4 0.1 s]:")
    hdr = (f"    {'elev':>5}  {'apogee km':>10}  {'maxQ kPa':>9}  {'maxMach':>8}  "
           f"{'vx@apo':>8}  {'v_circ':>8}  {'vx/vc':>7}  {'PkHF GW/m²':>11}  {'orb@apo':>8}")
    print(hdr)
    print("    " + "-" * (len(hdr) - 4))
    for elev in sorted(results):
        r = results[elev]
        ratio = r.vx_at_apogee / r.v_circ_at_apogee if r.v_circ_at_apogee > 0 else 0.0
        print(f"    {elev:>4.0f}°  "
              f"{r.apogee_km:>10.1f}  "
              f"{r.max_q_pa/1000.0:>9.1f}  "
              f"{r.max_mach:>8.1f}  "
              f"{r.vx_at_apogee:>8.0f}  "
              f"{r.v_circ_at_apogee:>8.0f}  "
              f"{ratio:>7.3f}  "
              f"{r.peak_heat_flux_W_m2/1e9:>11.2f}  "
              f"{'YES' if r.orbital_at_apogee else 'no':>8}")

    label, notes = verdict(results)
    print()
    print(f"  Verdict:  {label}")
    for n in notes:
        print(f"    • {n}")

    if concept.open_issues:
        print()
        print(f"  Open issues:")
        for issue in concept.open_issues:
            print(f"    • {issue}")

    print()


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> int:
    out_dir = Path(__file__).resolve().parent.parent / "data" / "trajectory_runs"

    print_registry()

    for concept in CONCEPT_PODS.values():
        results = evaluate_concept(concept)
        print_concept_report(concept, results)
        plot_path = plot_concept(concept, results, out_dir)
        print(f"  Plot → {plot_path}")
        print()

    print("Concept evaluation complete.  [DERIVED — all numbers from sim]")
    return 0


if __name__ == "__main__":
    sys.exit(main())
