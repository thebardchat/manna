"""
External 4-slide vehicle concept — animated evaluation.

Plugs the 4-slide external concept (vacuum-tube launch, Mach 20–25, biconic
waverider, blunted Von Kármán ogive, 4-layer SiO₂/UHTC/C/C/aerogel TPS) into
the existing trajectory_sim and renders all simulation results as a single
synchronized 6-panel animation across three Mach cases.

Concept parameters (all [ESTIMATE] unless tagged):
  • Diameter           : 1.0 m   (matches assumed tube bore)
  • Mass               : 800 kg
  • Cd (hypersonic)    : 0.12    (biconic waverider, vs ~0.45 blunt sphere-cone)
  • Nose radius        : 0.02 m  (blunted Von Kármán ogive)
  • Elevation          : 30°
  • Mach cases         : 20 / 22 / 25 referenced to sea-level c (340.3 m/s)
                         → 6 806 / 7 487 / 8 508 m/s rail-exit velocity

Outputs (in simulation/data/external_concept/):
  • external_concept_animation.gif     — primary deliverable (Pillow)
  • external_concept_animation.mp4     — if ffmpeg is available
  • external_concept_storyboard.png    — 4-keyframe static fallback

Run:  python simulation/src/external_concept_animation.py

Author: Shane Brazelton + Claude (Anthropic)
Date:   2026-05-14
"""

from __future__ import annotations

import math
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter, FFMpegWriter

sys.path.insert(0, str(Path(__file__).resolve().parent))
from trajectory_sim import (  # noqa: E402
    MannaPod, SimResult, simulate, atmo_density,
    SUTTON_GRAVES_K, gravity,
)


# ---------------------------------------------------------------------------
# Concept parameters  [ESTIMATE — derived from slide content; no design memo]
# ---------------------------------------------------------------------------

CONCEPT_DIAMETER_M:   float = 1.00
CONCEPT_MASS_KG:      float = 800.0
CONCEPT_CD_HYPER:     float = 0.12
CONCEPT_NOSE_R_M:     float = 0.02
ELEVATION_DEG:        float = 30.0

# Mach cases reference sea-level speed of sound (USSA 1976 → 340.294 m/s @ 15°C)
SEA_LEVEL_C: float = 340.294
MACH_CASES: Dict[int, str] = {20: "#42A5F5", 22: "#FFB300", 25: "#E53935"}

# TPS sustainability bands  [ESTIMATE — order-of-magnitude from open literature]
HF_ABLATIVE_SUSTAINED_W_M2: float = 5.0e7   # ~50 MW/m² steady-state SiO₂/PICA ablation
HF_ABLATIVE_PEAK_W_M2:      float = 5.0e8   # ~500 MW/m² survivable for ~seconds

# Output paths
THIS_DIR    = Path(__file__).resolve().parent
DATA_DIR    = THIS_DIR.parent / "data" / "external_concept"
GIF_PATH    = DATA_DIR / "external_concept_animation.gif"
MP4_PATH    = DATA_DIR / "external_concept_animation.mp4"
STORY_PATH  = DATA_DIR / "external_concept_storyboard.png"


# ---------------------------------------------------------------------------
# Case container
# ---------------------------------------------------------------------------

@dataclass
class ConceptCase:
    mach:    int
    color:   str
    pod:     MannaPod
    result:  SimResult
    t:       np.ndarray   # s
    z_km:    np.ndarray   # km
    x_km:    np.ndarray   # km
    speed:   np.ndarray   # m/s
    mach_arr: np.ndarray
    q_kpa:   np.ndarray
    hf_w:    np.ndarray   # W/m² Sutton-Graves stagnation heat flux
    g_decel: np.ndarray   # |drag decel| in G (axial deceleration in atmosphere)


def _build_pod(mach: int) -> MannaPod:
    v_launch = mach * SEA_LEVEL_C
    return MannaPod(
        name=f"Concept-M{mach}",
        mass_kg=CONCEPT_MASS_KG,
        diameter_m=CONCEPT_DIAMETER_M,
        cd0=CONCEPT_CD_HYPER,
        launch_v_ms=v_launch,
        v01_apogee_km=v_launch ** 2 * math.sin(math.radians(ELEVATION_DEG)) ** 2
                       / (2.0 * 9.80665) / 1000.0,   # vacuum, constant-g reference
    )


def _build_case(mach: int, color: str) -> ConceptCase:
    pod = _build_pod(mach)
    res = simulate(pod, elevation_deg=ELEVATION_DEG, dt=0.1, t_max=1800.0)
    a   = res.arrays
    t      = a["t"]
    speed  = a["speed"]
    # Sutton-Graves heat flux at our (smaller) concept nose radius
    rho    = np.array([atmo_density(z * 1000.0) for z in a["z_km"]])
    hf     = SUTTON_GRAVES_K * np.sqrt(np.maximum(rho, 0.0) / CONCEPT_NOSE_R_M) * speed ** 3
    # Axial drag deceleration in G  ( |a_drag| = q / BC )
    bc     = pod.ballistic_coefficient
    a_drag = (a["q_kpa"] * 1000.0) / bc
    g_decel = a_drag / 9.80665
    return ConceptCase(
        mach=mach, color=color, pod=pod, result=res,
        t=t, z_km=a["z_km"], x_km=a["x_km"], speed=speed, mach_arr=a["mach"],
        q_kpa=a["q_kpa"], hf_w=hf, g_decel=g_decel,
    )


# ---------------------------------------------------------------------------
# Figure construction
# ---------------------------------------------------------------------------

def _setup_axes(fig) -> Dict[str, plt.Axes]:
    gs = fig.add_gridspec(2, 3, hspace=0.42, wspace=0.32)
    ax = {
        "traj": fig.add_subplot(gs[0, 0]),
        "alt":  fig.add_subplot(gs[0, 1]),
        "mach": fig.add_subplot(gs[0, 2]),
        "q":    fig.add_subplot(gs[1, 0]),
        "hf":   fig.add_subplot(gs[1, 1]),
        "g":    fig.add_subplot(gs[1, 2]),
    }
    return ax


def _style(ax: plt.Axes, xlabel: str, ylabel: str, title: str,
           log_y: bool = False) -> None:
    ax.set_xlabel(xlabel, fontsize=9)
    ax.set_ylabel(ylabel, fontsize=9)
    ax.set_title(title, fontsize=10, weight="bold")
    ax.grid(True, alpha=0.25)
    ax.tick_params(labelsize=8)
    if log_y:
        ax.set_yscale("log")


def _draw_static_background(ax: Dict[str, plt.Axes],
                            cases: List[ConceptCase]) -> None:
    """Plot full trajectories faintly + axis limits + reference bands."""
    # ---- trajectory side view ----
    a_t = ax["traj"]
    max_x = max(c.x_km.max() for c in cases)
    max_z = max(c.z_km.max() for c in cases) * 1.10
    for c in cases:
        a_t.plot(c.x_km, c.z_km, color=c.color, alpha=0.20, linewidth=1.0)
    a_t.axhline(100.0, color="gray", linestyle="--", linewidth=0.7,
                label="Kármán (100 km)")
    a_t.set_xlim(0, max_x)
    a_t.set_ylim(0, max_z)
    _style(a_t, "Downrange (km)", "Altitude (km)",
           "Trajectory — 30° rail elevation")

    # ---- altitude vs time ----
    a_a = ax["alt"]
    t_end = min(900.0, max(c.t.max() for c in cases))
    a_a.axhline(100.0, color="gray", linestyle="--", linewidth=0.7)
    a_a.set_xlim(0, t_end)
    a_a.set_ylim(0, max_z)
    _style(a_a, "Time (s)", "Altitude (km)", "Altitude vs time")

    # ---- Mach vs time ----
    a_m = ax["mach"]
    a_m.set_xlim(0, t_end)
    a_m.set_ylim(0, max(28, max(c.mach_arr.max() for c in cases) * 1.08))
    _style(a_m, "Time (s)", "Mach number", "Mach vs time")

    # ---- dynamic pressure ----
    a_q = ax["q"]
    a_q.set_xlim(0, t_end)
    q_top = max(c.q_kpa.max() for c in cases) * 2.0
    a_q.set_ylim(1.0, max(q_top, 100.0))
    _style(a_q, "Time (s)", "Dynamic pressure (kPa)",
           "Dynamic pressure (max-Q)", log_y=True)

    # ---- heat flux ----
    a_h = ax["hf"]
    a_h.set_xlim(0, t_end)
    hf_top = max(c.hf_w.max() for c in cases) * 2.0
    a_h.set_ylim(1.0e4, max(hf_top, 1.0e9))
    a_h.axhline(HF_ABLATIVE_SUSTAINED_W_M2, color="#FF9800", linestyle=":",
                linewidth=0.9, label="~50 MW/m² (sustained)")
    a_h.axhline(HF_ABLATIVE_PEAK_W_M2, color="#E53935", linestyle=":",
                linewidth=0.9, label="~500 MW/m² (peak)")
    a_h.legend(fontsize=7, loc="lower right")
    _style(a_h, "Time (s)", "Stagnation heat flux (W/m²)",
           "Sutton-Graves heat flux [R_nose=2 cm]", log_y=True)

    # ---- G-load (axial drag decel) ----
    a_g = ax["g"]
    a_g.set_xlim(0, t_end)
    g_top = max(c.g_decel.max() for c in cases) * 1.15
    a_g.set_ylim(0, max(g_top, 220.0))
    a_g.axhspan(100, 200, color="#FFCDD2", alpha=0.35,
                label="100–200 G slide envelope")
    a_g.axhline(100.0, color="#E53935", linestyle="--", linewidth=0.7)
    a_g.legend(fontsize=7, loc="upper right")
    _style(a_g, "Time (s)", "Axial decel (G)",
           "Atmospheric deceleration (drag)")


# ---------------------------------------------------------------------------
# Frame schedule — log-spaced so early dynamics get more frames
# ---------------------------------------------------------------------------

def _frame_times(t_max: float, n_frames: int = 150) -> np.ndarray:
    """First 90 s gets 70% of frames, rest spreads to t_max."""
    n_early = int(round(n_frames * 0.70))
    n_late  = n_frames - n_early
    early   = np.linspace(0.0, 90.0, n_early, endpoint=False)
    late    = np.linspace(90.0, t_max, n_late)
    return np.concatenate([early, late])


# ---------------------------------------------------------------------------
# Animator
# ---------------------------------------------------------------------------

class ConceptAnimator:
    def __init__(self, cases: List[ConceptCase], n_frames: int = 150) -> None:
        self.cases = cases
        self.fig = plt.figure(figsize=(15, 9), dpi=110)
        self.fig.suptitle(
            "External 4-slide vehicle concept — simulated trajectory results\n"
            "30° elevation · biconic waverider Cd=0.12 · 1.0 m × 800 kg · R_nose=2 cm  "
            "[ESTIMATE]",
            fontsize=12, weight="bold",
        )
        self.ax = _setup_axes(self.fig)
        _draw_static_background(self.ax, cases)

        t_max = min(900.0, max(c.t.max() for c in cases))
        self.frame_t = _frame_times(t_max, n_frames=n_frames)

        # Active lines: full traces grown to current frame, plus a marker dot
        self.lines: Dict[str, Dict[int, plt.Line2D]] = {
            k: {} for k in ("traj", "alt", "mach", "q", "hf", "g")
        }
        self.markers: Dict[str, Dict[int, plt.Line2D]] = {
            k: {} for k in ("traj", "alt", "mach", "q", "hf", "g")
        }
        for c in self.cases:
            label = f"Mach {c.mach} @ rail exit  (BC={c.pod.ballistic_coefficient:,.0f} kg/m²)"
            for key in self.lines:
                ln, = self.ax[key].plot([], [], color=c.color, linewidth=1.9,
                                        label=label if key == "alt" else None)
                self.lines[key][c.mach] = ln
                mk, = self.ax[key].plot([], [], "o", color=c.color,
                                        markersize=6, markeredgecolor="black",
                                        markeredgewidth=0.6)
                self.markers[key][c.mach] = mk
        self.ax["alt"].legend(fontsize=8, loc="lower right")

        # Live readout text in lower-left of figure
        self.readout = self.fig.text(
            0.005, 0.005, "", fontsize=9, family="monospace",
            verticalalignment="bottom",
        )

    # -- per-frame update ----------------------------------------------------
    def _update(self, frame_idx: int) -> Tuple[plt.Artist, ...]:
        t_now = float(self.frame_t[frame_idx])
        readout_lines = [f"t = {t_now:7.1f} s"]
        artists: List[plt.Artist] = [self.readout]

        for c in self.cases:
            mask = c.t <= t_now
            if not mask.any():
                continue
            i_last = int(np.argmax(np.cumsum(mask))) - 0
            # numpy: last True index = mask.size - 1 - mask[::-1].argmax() (safer)
            i_last = int(mask.size - 1 - np.argmax(mask[::-1]))

            for key, (xs, ys) in {
                "traj": (c.x_km,      c.z_km),
                "alt":  (c.t,         c.z_km),
                "mach": (c.t,         c.mach_arr),
                "q":    (c.t,         c.q_kpa),
                "hf":   (c.t,         c.hf_w),
                "g":    (c.t,         c.g_decel),
            }.items():
                ln = self.lines[key][c.mach]
                mk = self.markers[key][c.mach]
                ln.set_data(xs[:i_last + 1], ys[:i_last + 1])
                mk.set_data([xs[i_last]], [ys[i_last]])
                artists.extend([ln, mk])

            readout_lines.append(
                f"  M{c.mach}:  alt={c.z_km[i_last]:6.1f} km   "
                f"v={c.speed[i_last]:6.0f} m/s   "
                f"M={c.mach_arr[i_last]:5.1f}   "
                f"q={c.q_kpa[i_last]:6.1f} kPa   "
                f"hf={c.hf_w[i_last]/1e6:6.1f} MW/m²   "
                f"G={c.g_decel[i_last]:5.1f}"
            )

        self.readout.set_text("\n".join(readout_lines))
        return tuple(artists)

    def render(self) -> FuncAnimation:
        return FuncAnimation(
            self.fig,
            self._update,
            frames=len(self.frame_t),
            interval=66,         # 15 fps in interactive playback
            blit=False,           # blit=False is fine for headless write
            repeat=False,
        )


# ---------------------------------------------------------------------------
# Storyboard (4 keyframes as a single PNG)
# ---------------------------------------------------------------------------

def _save_storyboard(animator: ConceptAnimator, out_path: Path) -> None:
    """Render four keyframes side-by-side as a static fallback."""
    keyframe_t = [5.0, 30.0, 90.0, animator.frame_t[-1]]
    fig, axes = plt.subplots(2, 2, figsize=(16, 11), dpi=110)
    fig.suptitle("External 4-slide concept — storyboard (4 keyframes)",
                 fontsize=13, weight="bold")
    for ax, t_now in zip(axes.flat, keyframe_t):
        for c in animator.cases:
            ax.plot(c.x_km, c.z_km, color=c.color, alpha=0.25, linewidth=1.0)
            mask = c.t <= t_now
            i_last = int(mask.size - 1 - np.argmax(mask[::-1]))
            ax.plot(c.x_km[:i_last + 1], c.z_km[:i_last + 1],
                    color=c.color, linewidth=2.0,
                    label=f"M{c.mach}")
            ax.plot([c.x_km[i_last]], [c.z_km[i_last]], "o",
                    color=c.color, markersize=8, markeredgecolor="black")
        ax.axhline(100.0, color="gray", linestyle="--", linewidth=0.7)
        ax.set_xlabel("Downrange (km)")
        ax.set_ylabel("Altitude (km)")
        ax.set_title(f"t = {t_now:.0f} s")
        ax.grid(True, alpha=0.25)
        ax.legend(fontsize=8, loc="lower right")
    fig.tight_layout()
    fig.savefig(out_path, dpi=140, bbox_inches="tight")
    plt.close(fig)


# ---------------------------------------------------------------------------
# Summary table — printed alongside artifact paths
# ---------------------------------------------------------------------------

def _print_summary(cases: List[ConceptCase]) -> None:
    hdr = (
        f"{'Case':<14} {'BC':>10} {'Apogee km':>11} {'Range km':>10} "
        f"{'MaxQ kPa':>10} {'MaxMach':>8} {'PkHF GW/m²':>12} "
        f"{'PkG':>7} {'Orb':>4}"
    )
    sep = "=" * len(hdr)
    print()
    print(sep)
    print("External 4-slide concept — simulation results  [DERIVED]")
    print("US Std Atm 1976 · RK4 0.1 s · flat-Earth + varying-g · "
          "Cd=0.12 · R_nose=2 cm")
    print(sep)
    print(hdr)
    print("-" * len(hdr))
    for c in cases:
        r = c.result
        print(
            f"{c.pod.name:<14} "
            f"{c.pod.ballistic_coefficient:>10,.0f} "
            f"{r.apogee_km:>11.1f} "
            f"{r.apogee_range_km:>10.1f} "
            f"{r.max_q_pa/1000.0:>10.1f} "
            f"{r.max_mach:>8.1f} "
            f"{r.peak_heat_flux_W_m2/1e9:>12.3f} "
            f"{c.g_decel.max():>7.1f} "
            f"{'YES' if r.orbital_flag else 'no':>4}"
        )
    print(sep)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    print("\nExternal 4-slide concept — animated evaluation")
    print("─" * 60)
    cases: List[ConceptCase] = []
    for mach, color in MACH_CASES.items():
        print(f"  simulating Mach {mach:<3}  v_launch={mach * SEA_LEVEL_C:,.0f} m/s ... ",
              end="", flush=True)
        c = _build_case(mach, color)
        print(f"apogee={c.result.apogee_km:.1f} km   "
              f"peak HF={c.result.peak_heat_flux_W_m2/1e9:.2f} GW/m²")
        cases.append(c)

    _print_summary(cases)

    animator = ConceptAnimator(cases, n_frames=150)
    anim = animator.render()

    # GIF (always — Pillow is in requirements via matplotlib)
    print(f"\n  writing GIF → {GIF_PATH}  (~10–30 s)...", flush=True)
    anim.save(GIF_PATH, writer=PillowWriter(fps=15))
    print("  GIF done.")

    # MP4 (only if ffmpeg is present)
    if FFMpegWriter.isAvailable():
        print(f"  writing MP4 → {MP4_PATH} ...", flush=True)
        anim.save(MP4_PATH, writer=FFMpegWriter(fps=24, bitrate=2400))
        print("  MP4 done.")
    else:
        print("  ffmpeg not available — skipping MP4 (GIF only).")

    plt.close(animator.fig)

    # Storyboard fallback — single PNG with 4 keyframes
    _save_storyboard(animator, STORY_PATH)
    print(f"  storyboard PNG → {STORY_PATH}")

    print("\n  All artifacts in:", DATA_DIR)


if __name__ == "__main__":
    main()
