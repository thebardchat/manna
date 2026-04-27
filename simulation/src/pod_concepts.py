"""
Manna Pod Concept Registry

Alternative pod geometries proposed to close the trajectory gap exposed by
the v0.1 → v0.2 simulation work (CLAUDE.md §10).  The canonical H/I/B
strawmen in `trajectory_sim.VARIANTS` are kept untouched as historical
reference; this module is where new concepts get parked, evaluated, and
either promoted, iterated, or discarded.

Each concept entry is a `PodConcept` carrying:
  • a `MannaPod` (the physics object the simulator already knows how to fly)
  • metadata: cargo class (H / I / B), geometry style, design intent,
    open issues, and the source rail v_exit assumption.

Adding a new concept = append one entry to `CONCEPT_PODS`.
Running it = `python simulation/src/concept_eval.py`.

Status tags follow CLAUDE.md §5.2:
  [VERIFIED] [DERIVED] [ESTIMATE] [PLACEHOLDER] [CONSTRAINT-NOT-MODELED]

Author: Shane Brazelton + Claude (Anthropic)
Date:   2026-04-27
"""

from __future__ import annotations

import math
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List

sys.path.insert(0, str(Path(__file__).resolve().parent))
from trajectory_sim import MannaPod


# ---------------------------------------------------------------------------
# Concept wrapper
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class PodConcept:
    """A candidate pod design and the engineering context around it."""

    concept_id:   str         # e.g. "MH-Dart-01"
    cargo_class:  str         # "H", "I", or "B"
    geometry:     str         # short geometry tag (e.g. "slender dart")
    pod:          MannaPod    # physics object simulate() consumes
    length_m:     float       # body length [ESTIMATE]
    rail_v_exit:  float       # rail exit velocity assumption [PLACEHOLDER]
    intent:       str         # one-line design intent
    notes:        str = ""    # multi-line free-form rationale + open issues
    open_issues:  List[str] = field(default_factory=list)

    @property
    def fineness_ratio(self) -> float:
        """L/D ratio.  [DERIVED]"""
        return self.length_m / self.pod.diameter_m

    @property
    def cargo_mass_kg(self) -> float:
        """Approximate cargo mass after a 35% structural fraction.  [ESTIMATE]"""
        return self.pod.mass_kg * 0.65


# ---------------------------------------------------------------------------
# Concept #1 — MH-Dart-01
# ---------------------------------------------------------------------------
#
# Cargo class:  H   (water, propellant, food bricks, sintered metal stock)
# Geometry:     Slender dart — ogive nose, smooth cylindrical body, fixed fins
# Goal:         Close the gap between v0.1 nominal Manna-H (BC ≈ 2,265 kg/m²,
#               sim apogee 9 km @ 30°) and the orbital-rendezvous regime
#               (BC ≥ ~50,000 needed per CLAUDE.md §10 sweep findings).
#
# Strategy:     Trade frontal area for length.  A 0.50 m × 6.0 m dart at
#               1,200 kg has the same payload class as Manna-H but ~18× the BC,
#               at the cost of a much smaller cargo bay diameter (no large
#               machinery — but bulk H-cargo is liquids/granulars/stock that
#               packs fine in a long thin tube).
#
# Cd₀ rationale:
#   - Slender body of revolution at hypersonic speeds: skin-friction-dominated.
#   - Reference: Hoerner, "Fluid-Dynamic Drag" — fineness ratio 12 ogive
#     gives Cd ≈ 0.10–0.18 in supersonic/hypersonic regimes.
#   - Use 0.15 as central [ESTIMATE]; CFD required to firm up.
#
# Open issues kept in `open_issues` list below.

_DART_DIAMETER_M     = 0.50
_DART_LENGTH_M       = 6.0
_DART_MASS_KG        = 1_200.0   # 780 kg cargo @ 65% structural mass fraction
_DART_CD0            = 0.15      # [ESTIMATE — slender hypersonic body]
_DART_RAIL_V         = 6_500.0   # m/s — matches CLAUDE.md §1 placeholder for H-class

_DART_FRONTAL_AREA   = math.pi * (_DART_DIAMETER_M / 2.0) ** 2
_DART_BC             = _DART_MASS_KG / (_DART_CD0 * _DART_FRONTAL_AREA)


MH_DART_01 = PodConcept(
    concept_id="MH-Dart-01",
    cargo_class="H",
    geometry="slender dart, ogive nose, fixed cruciform fins",
    pod=MannaPod(
        name="MH-Dart-01",
        mass_kg=_DART_MASS_KG,
        diameter_m=_DART_DIAMETER_M,
        cd0=_DART_CD0,
        launch_v_ms=_DART_RAIL_V,
        v01_apogee_km=0.0,        # no v0.1 claim — this is a new concept
    ),
    length_m=_DART_LENGTH_M,
    rail_v_exit=_DART_RAIL_V,
    intent=(
        "H-class bulk cargo dart — push BC into the 40 k+ range by trading "
        "frontal area for length; keep mass at ~1.2 t to match rail energy budget."
    ),
    notes=(
        "Replaces the v0.1 Manna-H blunt-body (1.0 m × ~1.5 m, BC ≈ 2,265) with "
        "a 0.50 m × 6.0 m dart (BC ≈ 40,000+).  Cargo bay is a long thin tube; "
        "good for liquids and granulars, bad for any single dense item > 0.4 m. "
        "Rail v_exit of 6.5 km/s pulled from CLAUDE.md §1 placeholder — must be "
        "validated against BGKPJR rail energy budget."
    ),
    open_issues=[
        "Cd0 = 0.15 is a slender-body estimate; CFD/wind-tunnel needed.",
        "Sutton-Graves heating with R_nose=5 cm assumed — small nose => "
        "higher heat flux per unit area; TPS sizing TBD.",
        "Long thin pod has higher slenderness => watch bending modes during "
        "rail acceleration and through max-Q.",
        "Cargo bay aspect ratio constrains payload — fine for water/propellant, "
        "wrong shape for spares, instruments, biologics.",
        "Fins add drag and complicate rail interface; passive aero-stable vs "
        "spin-stabilised is an open trade.",
        "Rail v_exit 6.5 km/s is [PLACEHOLDER] — BGKPJR may not deliver this.",
    ],
)


# ---------------------------------------------------------------------------
# Concept registry
# ---------------------------------------------------------------------------
#
# Append further concepts here as they're proposed.  Order is presentation order;
# `concept_eval.py` walks this dict.

CONCEPT_PODS: Dict[str, PodConcept] = {
    MH_DART_01.concept_id: MH_DART_01,
}


# ---------------------------------------------------------------------------
# Quick-look summary printer
# ---------------------------------------------------------------------------

def print_registry() -> None:
    """One-line-per-concept summary; useful for sanity checks."""
    print()
    print("Manna Pod Concept Registry  [DERIVED geometric values]")
    print("=" * 92)
    print(f"  {'concept':<14} {'class':<5} {'mass kg':>8} {'D m':>6} {'L m':>6} "
          f"{'L/D':>5} {'Cd0':>6} {'BC kg/m²':>10} {'v_rail m/s':>11}")
    print("  " + "-" * 90)
    for c in CONCEPT_PODS.values():
        print(f"  {c.concept_id:<14} {c.cargo_class:<5} "
              f"{c.pod.mass_kg:>8,.0f} "
              f"{c.pod.diameter_m:>6.2f} "
              f"{c.length_m:>6.2f} "
              f"{c.fineness_ratio:>5.1f} "
              f"{c.pod.cd0:>6.2f} "
              f"{c.pod.ballistic_coefficient:>10,.0f} "
              f"{c.rail_v_exit:>11,.0f}")
    print()


if __name__ == "__main__":
    print_registry()
