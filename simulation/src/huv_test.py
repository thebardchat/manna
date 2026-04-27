"""
HUV (Hypersonic Unmanned Vehicle — Maglev Vacuum Launch) Trajectory Test

Tests the design proposed in `docs/research/incoming/HUV_maglev_vacuum_launch_v0.1.md`
as a candidate launch concept against the Manna H/I/B baselines.

Two HUV variants are defined:

    HUV-25  Mach 25 max-performance     (v_exit = 8500 m/s)   [ESTIMATE]
    HUV-20  Mach 20 conservative case   (v_exit = 6800 m/s)   [ESTIMATE]

Each is run at three elevations (15°, 30°, 45°) to bracket the BGKPJR rail
envelope. Peak launch G-load is computed analytically from tube length L:
    a = v_exit² / (2L);  G = a / g0
The 28.7 km BGKPJR baseline is used as the reference tube length.

Run:  PYTHONPATH=. python simulation/src/huv_test.py
Out:  simulation/data/huv_test/huv_trajectory_comparison.png
      simulation/data/huv_test/huv_test_results.md   (markdown summary)

Author: Shane Brazelton + Claude (Anthropic)
Date:   2026-04-27
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import List

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from simulation.src.trajectory_sim import (
    G0,
    MannaPod,
    R_EARTH,
    SimResult,
    VARIANTS,
    simulate,
)


# ---------------------------------------------------------------------------
# HUV variant definitions  [ESTIMATE — derived from concept doc, not measured]
# ---------------------------------------------------------------------------

# Speed-of-sound at sea level (USSA 1976): sqrt(1.4 × 287.058 × 288.15) ≈ 340.3 m/s
MACH_TO_MS = 340.3

# Slender hypersonic body, sized between DARPA HTV-2 (~900 kg, 0.91 m wide) and
# Manna-H (800 kg, 1.00 m).  Diameter chosen to slot inside a BGKPJR-class tube;
# Cd0 estimated for a blunt-ogive cylindrical-rear projectile at hypersonic Mach.
HUV_MASS_KG       = 1500.0   # [ESTIMATE]
HUV_DIAMETER_M    = 0.60      # [ESTIMATE]
HUV_CD0           = 0.30      # [ESTIMATE — slender biconic, post-cap]

HUV_VARIANTS: dict[str, MannaPod] = {
    "HUV-25": MannaPod(
        name="HUV-25",
        mass_kg=HUV_MASS_KG,
        diameter_m=HUV_DIAMETER_M,
        cd0=HUV_CD0,
        launch_v_ms=25.0 * MACH_TO_MS,    # 8507 m/s  [ESTIMATE]
        v01_apogee_km=0.0,                 # no paper claim — sim is the reference
    ),
    "HUV-20": MannaPod(
        name="HUV-20",
        mass_kg=HUV_MASS_KG,
        diameter_m=HUV_DIAMETER_M,
        cd0=HUV_CD0,
        launch_v_ms=20.0 * MACH_TO_MS,    # 6806 m/s  [ESTIMATE]
        v01_apogee_km=0.0,
    ),
}

ELEVATIONS_DEG = (15.0, 30.0, 45.0)
BGKPJR_TUBE_LENGTH_M = 28_700.0   # [VERIFIED — CLAUDE.md §1]


# ---------------------------------------------------------------------------
# Analytic helpers
# ---------------------------------------------------------------------------

def peak_g_for_tube(v_exit_ms: float, tube_length_m: float) -> float:
    """Constant-acceleration peak G-load required to reach v_exit in tube_length."""
    a = v_exit_ms ** 2 / (2.0 * tube_length_m)
    return a / G0


def vacuum_apogee_km(v_exit_ms: float, elevation_deg: float) -> float:
    """Vacuum apogee from radial vis-viva with constant g0 (paper-style claim)."""
    v_z = v_exit_ms * math.sin(math.radians(elevation_deg))
    denom = 2.0 * G0 * R_EARTH - v_z ** 2
    if denom <= 0:
        return float("inf")
    h_m = (v_z ** 2 * R_EARTH) / denom
    return h_m / 1000.0


# ---------------------------------------------------------------------------
# Run sweep
# ---------------------------------------------------------------------------

def run_sweep() -> List[SimResult]:
    """Run HUV variants × elevations.  Also re-run Manna-H for comparison."""
    results: List[SimResult] = []

    print(f"\n{'='*78}")
    print(f"HUV trajectory test — Mach 20/25, elevations {ELEVATIONS_DEG} deg")
    print(f"{'='*78}\n")

    pods = [*HUV_VARIANTS.values(), VARIANTS["Manna-H"]]
    for pod in pods:
        for el in ELEVATIONS_DEG:
            res = simulate(pod, elevation_deg=el)
            results.append(res)
            vac = vacuum_apogee_km(pod.launch_v_ms, el)
            ratio = res.apogee_km / vac if vac > 0 else 0.0
            print(
                f"  {pod.name:<8} el={el:>4.0f}°  "
                f"BC={pod.ballistic_coefficient:>6.0f} kg/m²  "
                f"sim_apogee={res.apogee_km:>6.1f} km   "
                f"vac_apogee={vac:>7.1f} km  "
                f"sim/vac={ratio:>5.3f}   "
                f"vx@apo={res.vx_at_apogee:>5.0f}   "
                f"PkHF={res.peak_heat_flux_W_m2/1e9:>5.2f} GW/m²"
            )
    print()
    return results


# ---------------------------------------------------------------------------
# Plot
# ---------------------------------------------------------------------------

_COLOR_BY_NAME = {"HUV-25": "#FF1744", "HUV-20": "#FFB300", "Manna-H": "#1976D2"}
_LINESTYLE_BY_EL = {15.0: ":", 30.0: "-", 45.0: "--"}


def plot_results(results: List[SimResult], out_dir: Path) -> Path:
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle(
        "HUV Trajectory Test — Mach 20/25 vs. Manna-H baseline | US Std Atm 1976 | RK4",
        fontsize=12,
    )
    ax_alt, ax_q, ax_v, ax_hf = axes.flat

    for res in results:
        a = res.arrays
        c = _COLOR_BY_NAME.get(res.variant.name, "gray")
        ls = _LINESTYLE_BY_EL.get(res.elevation_deg, "-")
        lbl = f"{res.variant.name} @ {res.elevation_deg:.0f}°"

        ax_alt.plot(a["t"], a["z_km"], color=c, linestyle=ls, linewidth=1.6, label=lbl)
        ax_q.plot(a["t"], a["q_kpa"], color=c, linestyle=ls, linewidth=1.6, label=lbl)
        asc = a["vz"] > 0
        ax_v.plot(a["mach"][asc], a["z_km"][asc], color=c, linestyle=ls, linewidth=1.6,
                  label=lbl)

        # Peak heat flux: bar plot grouped by variant + elevation
        ax_hf.bar(lbl, res.peak_heat_flux_W_m2 / 1e9, color=c,
                  alpha=0.6 + 0.15 * ELEVATIONS_DEG.index(res.elevation_deg))

    for ax in (ax_alt, ax_v):
        ax.axhline(100.0, color="gray", linestyle="--", linewidth=0.7,
                   label="Kármán line")

    ax_alt.set_xlabel("Time (s)")
    ax_alt.set_ylabel("Altitude (km)")
    ax_alt.set_title("Altitude vs time")
    ax_alt.legend(fontsize=7, ncol=2)
    ax_alt.grid(True, alpha=0.25)

    ax_q.set_xlabel("Time (s)")
    ax_q.set_ylabel("Dynamic pressure (kPa)")
    ax_q.set_title("Dynamic pressure vs time")
    ax_q.set_yscale("log")
    ax_q.legend(fontsize=7, ncol=2)
    ax_q.grid(True, alpha=0.25)

    ax_v.set_xlabel("Mach")
    ax_v.set_ylabel("Altitude (km)")
    ax_v.set_title("Mach vs altitude (ascent only)")
    ax_v.legend(fontsize=7, ncol=2)
    ax_v.grid(True, alpha=0.25)

    ax_hf.set_ylabel("Peak stagnation heat flux (GW/m²)")
    ax_hf.set_title("Sutton-Graves peak heat flux  [R_nose=5 cm]")
    ax_hf.tick_params(axis="x", rotation=45, labelsize=7)
    ax_hf.grid(True, axis="y", alpha=0.25)

    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "huv_trajectory_comparison.png"
    fig.tight_layout()
    fig.savefig(out_path, dpi=140, bbox_inches="tight")
    plt.close(fig)
    return out_path


# ---------------------------------------------------------------------------
# Markdown summary
# ---------------------------------------------------------------------------

def write_markdown_summary(results: List[SimResult], out_dir: Path) -> Path:
    md_path = out_dir / "huv_test_results.md"
    lines: List[str] = []
    lines.append("# HUV Trajectory Test — Results\n")
    lines.append(f"**Tube reference:** BGKPJR rail, L = {BGKPJR_TUBE_LENGTH_M/1000:.1f} km  "
                 "[VERIFIED — CLAUDE.md §1]\n")
    lines.append("**Simulator:** `simulation/src/trajectory_sim.py` "
                 "(RK4, US Std Atm 1976, flat-Earth, varying-g)\n")
    lines.append("**Heat flux model:** Sutton-Graves (1959) "
                 "[CONSTRAINT-NOT-MODELED — R_nose = 5 cm assumed]\n\n")

    lines.append("## Peak G-load required (constant-acceleration tube model)\n")
    lines.append("| Variant | v_exit | Tube L | Peak a | Peak G |\n")
    lines.append("|---|---|---|---|---|\n")
    for name, pod in HUV_VARIANTS.items():
        g_pk = peak_g_for_tube(pod.launch_v_ms, BGKPJR_TUBE_LENGTH_M)
        a = pod.launch_v_ms ** 2 / (2.0 * BGKPJR_TUBE_LENGTH_M)
        lines.append(f"| {name} | {pod.launch_v_ms:.0f} m/s | {BGKPJR_TUBE_LENGTH_M/1000:.1f} km "
                     f"| {a:.0f} m/s² | **{g_pk:.0f} G** |\n")
    lines.append("\n")

    lines.append("## Trajectory simulation results\n")
    lines.append("| Variant | El° | BC kg/m² | Sim apogee (km) | Vacuum apogee (km) "
                 "| sim/vac | vx@apo (m/s) | v_circ@apo | vx/vc | "
                 "Peak HF (GW/m²) | Orbital flag |\n")
    lines.append("|---|---|---|---|---|---|---|---|---|---|---|\n")
    for res in results:
        vac = vacuum_apogee_km(res.variant.launch_v_ms, res.elevation_deg)
        ratio = res.apogee_km / vac if vac > 0 else 0.0
        vxr = res.vx_at_apogee / res.v_circ_at_apogee if res.v_circ_at_apogee > 0 else 0.0
        flag = "YES ⚠" if res.orbital_flag else "no"
        lines.append(
            f"| {res.variant.name} | {res.elevation_deg:.0f} "
            f"| {res.variant.ballistic_coefficient:.0f} "
            f"| {res.apogee_km:.1f} | {vac:.1f} | {ratio:.3f} "
            f"| {res.vx_at_apogee:.0f} | {res.v_circ_at_apogee:.0f} | {vxr:.3f} "
            f"| {res.peak_heat_flux_W_m2/1e9:.2f} | {flag} |\n"
        )

    lines.append("\n")
    lines.append("## Tags\n")
    lines.append("- All sim outputs: [DERIVED]\n")
    lines.append("- HUV mass / diameter / Cd0 / v_exit: [ESTIMATE] from concept doc\n")
    lines.append("- Vacuum apogee column: [PLACEHOLDER] — paper-style claim, no atmosphere\n")
    lines.append("- Peak heat flux: [CONSTRAINT-NOT-MODELED] — Sutton-Graves only, "
                 "no real-gas chemistry, no shock-layer radiation\n")

    md_path.write_text("".join(lines))
    return md_path


# ---------------------------------------------------------------------------
# Entry
# ---------------------------------------------------------------------------

def write_trajectories_json(results: List[SimResult], out_dir: Path,
                             max_points: int = 600) -> Path:
    """Dump downsampled (t, x_km, z_km, v) per run for browser animation."""
    runs = []
    for res in results:
        a = res.arrays
        n = len(a["t"])
        # Stride to keep ≤ max_points per run; preserves temporal density well enough
        stride = max(1, n // max_points)
        runs.append({
            "name":             res.variant.name,
            "elevation_deg":    res.elevation_deg,
            "mass_kg":          res.variant.mass_kg,
            "diameter_m":       res.variant.diameter_m,
            "cd0":              res.variant.cd0,
            "bc_kg_m2":         res.variant.ballistic_coefficient,
            "v_exit_ms":        res.variant.launch_v_ms,
            "apogee_km":        res.apogee_km,
            "apogee_range_km":  res.apogee_range_km,
            "peak_hf_W_m2":     res.peak_heat_flux_W_m2,
            "vx_at_apogee_ms":  res.vx_at_apogee,
            "v_circ_at_apogee_ms": res.v_circ_at_apogee,
            "max_q_pa":         res.max_q_pa,
            "max_mach":         res.max_mach,
            "t_s":   [round(float(x), 2) for x in a["t"][::stride].tolist()],
            "x_km":  [round(float(x), 3) for x in a["x_km"][::stride].tolist()],
            "z_km":  [round(float(x), 3) for x in a["z_km"][::stride].tolist()],
            "v_ms":  [round(float(x), 1) for x in a["speed"][::stride].tolist()],
        })
    out_path = out_dir / "huv_trajectories.json"
    with out_path.open("w") as f:
        json.dump({
            "earth_radius_km":  6371.0,
            "karman_km":        100.0,
            "tube_length_km":   BGKPJR_TUBE_LENGTH_M / 1000.0,
            "runs":             runs,
        }, f, separators=(",", ":"))
    return out_path


def main() -> None:
    out_dir = Path(__file__).resolve().parent.parent / "data" / "huv_test"
    results = run_sweep()
    plot_path = plot_results(results, out_dir)
    md_path = write_markdown_summary(results, out_dir)
    json_path = write_trajectories_json(results, out_dir)

    print(f"  Plot       → {plot_path}")
    print(f"  Summary    → {md_path}")
    print(f"  JSON       → {json_path}")
    print()

    print("Tube G-load (analytic, constant accel, BGKPJR L=28.7 km):")
    for name, pod in HUV_VARIANTS.items():
        g_pk = peak_g_for_tube(pod.launch_v_ms, BGKPJR_TUBE_LENGTH_M)
        print(f"  {name}  v={pod.launch_v_ms:>5.0f} m/s  →  peak {g_pk:>5.0f} G")
    print()


if __name__ == "__main__":
    main()
