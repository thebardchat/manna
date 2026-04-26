"""
Manna BC × Elevation Parametric Sweep

Sweeps ballistic coefficient (1 k – 50 k kg/m²) and launch elevation angle
(15° – 85°) for each of the three Manna variant launch velocities.

Produces:
  • Console table — apogee, vx/v_circ ratio, orbital flag per cell
  • 3-panel contour plot (one per variant) — apogee altitude vs BC × elevation
  • Kármán-line (100 km) and orbital-capable contours overlaid

Run:  python simulation/src/sweep.py
Plots saved: simulation/data/trajectory_runs/sweep_bc_elevation.png

Author: Shane Brazelton + Claude (Anthropic)
Date:   2026-04-25
"""

from __future__ import annotations

import math
import sys
from pathlib import Path
from typing import Dict, List

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, str(Path(__file__).resolve().parent))
from trajectory_sim import MannaPod, SimResult, simulate, VARIANTS


# ---------------------------------------------------------------------------
# Sweep parameters
# ---------------------------------------------------------------------------

BC_VALUES: List[float] = [1_000, 2_000, 5_000, 10_000, 20_000, 50_000]   # kg/m²
ELEV_VALUES: List[float] = [15, 30, 45, 60, 75, 85]                       # degrees
_SWEEP_DT: float = 0.5   # coarser step for sweep speed; main sim uses 0.1 s


# ---------------------------------------------------------------------------
# Synthetic pod factory
# ---------------------------------------------------------------------------

def _make_sweep_pod(variant_name: str, bc_kg_m2: float) -> MannaPod:
    """
    Synthetic pod: exact launch velocity of the named variant, specified BC.
    Sets cd0=1.0 and derives diameter so that BC = mass/(cd0×A) = bc_kg_m2.  [DERIVED]
    """
    base = VARIANTS[variant_name]
    cd0  = 1.0
    mass = 1.0                                  # kg — arbitrary unit mass
    area = mass / (cd0 * bc_kg_m2)             # m²
    diam = math.sqrt(4.0 * area / math.pi)     # m
    return MannaPod(
        name=f"{variant_name}-BC{bc_kg_m2:.0f}",
        mass_kg=mass,
        diameter_m=diam,
        cd0=cd0,
        launch_v_ms=base.launch_v_ms,
        v01_apogee_km=base.v01_apogee_km,
    )


# ---------------------------------------------------------------------------
# Run sweep
# ---------------------------------------------------------------------------

def run_sweep() -> Dict[str, List[List[SimResult]]]:
    """
    Full BC × elevation grid for all three variants.
    Returns {variant_name: grid[bc_index][elev_index]}.  [DERIVED]
    """
    n_total = len(VARIANTS) * len(BC_VALUES) * len(ELEV_VALUES)
    done    = 0
    results: Dict[str, List[List[SimResult]]] = {}

    for vname in VARIANTS:
        rows: List[List[SimResult]] = []
        for bc in BC_VALUES:
            row: List[SimResult] = []
            for elev in ELEV_VALUES:
                pod = _make_sweep_pod(vname, bc)
                res = simulate(pod, elevation_deg=float(elev), dt=_SWEEP_DT)
                row.append(res)
                done += 1
                print(f"  {done:3d}/{n_total}  {vname}  BC={bc:>6,.0f}  elev={elev:>2}°  "
                      f"apogee={res.apogee_km:6.1f} km  vx/vc={res.vx_at_apogee/res.v_circ_at_apogee:.3f}",
                      flush=True)
            rows.append(row)
        results[vname] = rows

    return results


# ---------------------------------------------------------------------------
# Console table
# ---------------------------------------------------------------------------

def print_sweep_table(results: Dict[str, List[List[SimResult]]]) -> None:
    """Apogee and vx/v_circ tables for each variant."""
    elev_hdr = "  ".join(f"  {int(e):>2}°   " for e in ELEV_VALUES)

    for vname in VARIANTS:
        base  = VARIANTS[vname]
        vrows = results[vname]
        width = 100

        print()
        print("=" * width)
        print(f"  {vname}   v_launch = {base.launch_v_ms:,.1f} m/s"
              f"   BC parametric sweep   [DERIVED]")
        print("=" * width)

        # ── Apogee table ───────────────────────────────────────────────────
        print()
        print(f"  Apogee (km)  [O] = orbital_at_apogee flag set")
        print(f"  {'BC (kg/m²)':<13}  " + elev_hdr)
        print("  " + "-" * (width - 2))
        for i, bc in enumerate(BC_VALUES):
            cells = []
            for j in range(len(ELEV_VALUES)):
                res = vrows[i][j]
                tag = "[O]" if res.orbital_at_apogee else "   "
                cells.append(f"{res.apogee_km:6.1f}{tag}")
            print(f"  {int(bc):>13,}  " + "  ".join(cells))

        # ── vx/v_circ table ────────────────────────────────────────────────
        print()
        print(f"  vx_at_apogee / v_circ_at_apogee  (1.000 = circular orbit)")
        print(f"  {'BC (kg/m²)':<13}  " + elev_hdr)
        print("  " + "-" * (width - 2))
        for i, bc in enumerate(BC_VALUES):
            cells = []
            for j in range(len(ELEV_VALUES)):
                res = vrows[i][j]
                ratio = (res.vx_at_apogee / res.v_circ_at_apogee
                         if res.v_circ_at_apogee > 0 else 0.0)
                cells.append(f"{ratio:6.3f}   ")
            print(f"  {int(bc):>13,}  " + "  ".join(cells))

        print()

    print("  [DERIVED]  All values from US Std Atm 1976 + RK4 simulation")
    print(f"  [ESTIMATE] cd0 forced to 1.0 for sweep; real pods have cd0 ~ 0.4–0.45")
    print(f"  dt = {_SWEEP_DT} s (coarser than production 0.1 s for speed)")
    print()


# ---------------------------------------------------------------------------
# Contour plots
# ---------------------------------------------------------------------------

def plot_sweep_contours(
    results: Dict[str, List[List[SimResult]]],
    out_dir: Path,
) -> Path:
    """
    3-panel contour plot — apogee (km) vs BC × elevation for each variant.
    Green contour = Kármán line (100 km).  Cyan star = orbital_at_apogee.
    """
    bc_arr   = np.array(BC_VALUES,   dtype=float)
    elev_arr = np.array(ELEV_VALUES, dtype=float)
    log_bc   = np.log10(bc_arr)

    fig, axes = plt.subplots(1, 3, figsize=(18, 7), sharey=True)
    fig.suptitle(
        "Manna Parametric Sweep — Apogee Altitude (km)\n"
        "BC × Launch Elevation  |  US Std Atm 1976  |  RK4  |  cd0 = 1.0 (sweep)",
        fontsize=12,
    )

    cmap   = plt.cm.plasma
    levels = np.linspace(0, 1, 21)   # normalised to data range per panel

    cf_last = None
    for ax, vname in zip(axes, VARIANTS):
        vrows = results[vname]
        base  = VARIANTS[vname]

        # 2-D apogee array: shape (n_bc, n_elev)
        Z = np.zeros((len(BC_VALUES), len(ELEV_VALUES)))
        orbital_pts: List[tuple] = []
        for i in range(len(BC_VALUES)):
            for j in range(len(ELEV_VALUES)):
                res = vrows[i][j]
                Z[i, j] = res.apogee_km
                if res.orbital_at_apogee:
                    orbital_pts.append((elev_arr[j], log_bc[i]))

        XX, YY = np.meshgrid(elev_arr, log_bc)

        vmin, vmax = Z.min(), max(Z.max(), 1.0)
        cf = ax.contourf(XX, YY, Z, levels=20, vmin=vmin, vmax=vmax, cmap=cmap)
        cf_last = cf

        # Labelled contour lines at fixed km values present in this panel
        km_contours = [v for v in [1, 5, 10, 50, 100, 200, 500] if vmin <= v <= vmax]
        if km_contours:
            cs = ax.contour(XX, YY, Z, levels=km_contours,
                            colors="white", linewidths=0.8, alpha=0.6)
            ax.clabel(cs, fmt="%g km", fontsize=7, colors="white")

        # Kármán line (100 km) — green
        if vmin < 100.0 <= vmax:
            ax.contour(XX, YY, Z, levels=[100.0],
                       colors="lime", linewidths=2.0)

        # Orbital-capable cells — cyan stars
        if orbital_pts:
            ox = [p[0] for p in orbital_pts]
            oy = [p[1] for p in orbital_pts]
            ax.scatter(ox, oy, color="cyan", marker="*", s=200, zorder=5,
                       label="orbital_at_apogee")
            ax.legend(fontsize=8, loc="upper left")

        ax.set_xlabel("Elevation angle (°)", fontsize=10)
        ax.set_title(f"{vname}\nv_launch = {base.launch_v_ms:,.0f} m/s", fontsize=10)

        # Y-axis: log BC ticks
        ax.set_yticks(log_bc)
        ax.set_yticklabels([f"{int(bc):,}" for bc in BC_VALUES])

    axes[0].set_ylabel("Ballistic coefficient (kg/m²)", fontsize=10)

    if cf_last is not None:
        fig.colorbar(cf_last, ax=axes.tolist(), label="Apogee altitude (km)",
                     shrink=0.8, pad=0.02)

    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "sweep_bc_elevation.png"
    fig.tight_layout()
    fig.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return out_path


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    out_dir = Path(__file__).resolve().parent.parent / "data" / "trajectory_runs"

    print("Manna BC × Elevation Parametric Sweep")
    print(f"  BC values (kg/m²): {[int(b) for b in BC_VALUES]}")
    print(f"  Elevation (°):     {[int(e) for e in ELEV_VALUES]}")
    print(f"  Variants:          {list(VARIANTS.keys())}")
    print(f"  dt = {_SWEEP_DT} s  |  {len(VARIANTS)*len(BC_VALUES)*len(ELEV_VALUES)} simulations")
    print()

    sweep_results = run_sweep()
    print()
    print_sweep_table(sweep_results)

    out_path = plot_sweep_contours(sweep_results, out_dir)
    print(f"  Plot → {out_path}")
    print()
    print("Sweep complete.  [DERIVED]  All outputs from US Std Atm 1976 + RK4 simulation.")
