# MH-Oval-01 — concept design memo

**Concept ID:** `MH-Oval-01`
**Cargo class:** H (water, propellant, food bricks, sintered metal stock; 100 G internal)
**Geometry:** Prolate spheroid (oval / egg shape), no fins, smooth body of revolution
**Status:** Pre-Phase A concept; first trip through `simulation/src/concept_eval.py`.
**Date:** 2026-04-27
**Operating under:** [CLAUDE.md](../../CLAUDE.md) §5 conventions, §7 forensic gates

---

## 1. The question

> *"Would it help if it came out the tube in a complete oval shape?"*

Tested directly. Same launch mass (1,200 kg) and same rail v_exit (6,500 m/s)
as `MH-Dart-01` so the only thing changing is shape. Asks: does a low-fineness
sealed oval recover anything over the slender dart?

**Short answer: no, not on trajectory alone.** It loses badly on apogee and
orbital fraction. **It does win on cargo bay shape, structure, and stability** —
which is why it stays in the concept registry rather than getting deleted.

---

## 2. Parameters  [ESTIMATE unless tagged]

| Parameter            | MH-Oval-01     | MH-Dart-01 (compare) |
| -------------------- | -------------- | -------------------- |
| Total mass           | 1,200 kg       | 1,200 kg             |
| Body diameter (max)  |  1.00 m        |  0.50 m              |
| Body length          |  3.00 m        |  6.00 m              |
| Fineness L/D         |   3.0          | 12.0                 |
| Frontal area         |  0.785 m²      |  0.196 m²            |
| Drag coefficient Cd₀ |  0.25          |  0.15                |
| **Ballistic coeff.** | **6,112 kg/m²**| **40,744 kg/m²**     |
| Rail v_exit          | 6,500 m/s      | 6,500 m/s            |

The oval has 4× the frontal area and 1.67× the Cd₀, so its BC drops by ~6.7×.
That single fact drives every trajectory result below.

**Cd₀ rationale:** Prolate spheroid at fineness 3, hypersonic regime — between
a sphere (Cd ~1.0) and a slender body (Cd ~0.10–0.15). 0.25 is a midpoint
[ESTIMATE]; CFD required to firm up.

---

## 3. Trajectory test results [DERIVED]

Run via `python simulation/src/concept_eval.py` on 2026-04-27.

```
====================================================================================================
  MH-Oval-01  —  cargo class H  —  prolate spheroid, no fins, smooth body of revolution
====================================================================================================

  Trajectory results [DERIVED — US Std Atm 1976 + RK4 0.1 s]:
     elev   apogee km   maxQ kPa   maxMach    vx@apo    v_circ    vx/vc   PkHF GW/m²   orb@apo
    ------------------------------------------------------------------------------------------
      15°         7.2    25877.7      19.1       580      7900    0.073         0.25        no
      30°        29.1    25877.7      19.1       946      7886    0.120         0.25        no
      45°       109.4    25877.7      19.1      1379      7837    0.176         0.25        no
```

**Plot:** `simulation/data/trajectory_runs/concept_MH-Oval-01.png`

### 3.1 Side-by-side with the dart

| Elevation | MH-Oval-01 apogee | MH-Dart-01 apogee | Ratio (Oval / Dart) |
| --------- | ----------------- | ----------------- | ------------------- |
| 15°       |   7.2 km          |  58.4 km          | 0.12×               |
| 30°       |  29.1 km          | 344.1 km          | 0.08×               |
| 45°       | 109.4 km          | 855.6 km          | 0.13×               |

| Elevation | MH-Oval-01 vx/vc | MH-Dart-01 vx/vc |
| --------- | ---------------- | ---------------- |
| 15°       | 0.073            | 0.477            |
| 30°       | 0.120            | 0.566            |
| 45°       | 0.176            | 0.517            |

The oval clears Kármán *only* at 45°, and only barely (109 km).  Its horizontal
velocity at apogee is 18% of orbital — the Tug rendezvous burn would be ~6 km/s,
which exceeds any reasonable Tug ΔV budget.

### 3.2 Verdict

`PARTIAL — altitude clears [at 45° only], but rendezvous burn is huge.`
**Not competitive with the dart on trajectory. Keep for non-trajectory wins.**

---

## 4. Where the oval still wins

Things the dart loses that the oval keeps:

* **Cargo bay shape.** 1.0 m × ~2.5 m usable interior; volumetrically efficient
  for compact cargo, dense items, and shapes that don't fit in a 0.50 m tube.
* **Structural simplicity.** Closed shell, no fins to attach, no L/D = 12
  beam-bending or Euler buckling concerns at 100 G acceleration or 25.9 MPa
  max-Q.
* **No fin/sabot interface with the rail.** One smooth body, simpler launch
  carriage.
* **Passive aerodynamic stability** (Apollo-CM-style — CP behind CG via shape
  alone), as long as we can place mass to keep CG forward.

These benefits are real, but they don't fix the trajectory.

---

## 5. The lift caveat — what the sim cannot see

The 3-DOF point-mass simulator models drag only. **It does not model lift.**

An oval flown at angle of attack is, by definition, a lifting body. X-37B-class
shapes get L/D ≈ 1 in hypersonic and ≈ 2 in subsonic. A pod that pulls a few
degrees of α during the ascent could trade horizontal velocity for altitude in
a way the dart cannot.

The numbers above are therefore the **no-lift floor**.  True performance is
somewhere between this floor and a fully-modelled lifting trajectory.  To
quantify the gap we'd need either:

* A 3-DOF sim extension that adds Cl(α) and a guidance law, or
* A 6-DOF sim that models the full angle of attack history.

Neither exists in this codebase yet. CLAUDE.md §10 lists "Pod dynamics 6-DOF"
as priority #7. **If the oval looks attractive for non-trajectory reasons, the
right next move is to build the lift extension and re-run, not to keep
parametrising shapes against drag-only physics.**

---

## 6. Open issues (carried forward)

These are tracked in `pod_concepts.MH_OVAL_01.open_issues`:

1. **Cd₀ = 0.25 is a hypersonic prolate-spheroid estimate.** CFD or wind-tunnel
   data needed before any apogee number is defensible at Mach 19.
2. **No lift modelled.** Sim is point-mass, drag-only. Real L/D from an oval
   at α could extend apogee meaningfully — needs 6-DOF or 3-DOF + lift.
3. **Total heat load.** Sutton-Graves *flux* (W/m²) goes as 1/√R_nose; a
   larger oval has larger R_nose, so flux per unit area drops slightly. But
   total heat *load* (flux × area × time) scales with frontal area, which is
   4× the dart. TPS sizing TBD.
4. **Stability without fins.** Apollo-CM trick — CP behind CG via shape alone.
   Works only if we can place mass to keep CG forward, which constrains cargo
   loading.
5. **Rail v_exit = 6.5 km/s is `[PLACEHOLDER]`.** Same caveat as MH-Dart-01.

---

## 7. What this experiment told us

- **BC dominates apogee in the drag-only regime.** Trading 4× frontal area for
  any reasonable Cd₀ reduction is a losing exchange.
- **Shape choice is not just "dart vs oval"** — it's "drag-dominated vs
  lift-capable trajectory." Once you bring lift into the architecture, the
  comparison is no longer about BC alone.
- **The oval is not dead** — it's a serious cargo-bay and structural concept.
  But it cannot be evaluated honestly until the simulator can model the lift
  it's clearly designed to use.

### Suggested next moves

1. **Build lift into the simulator.** Add `cl0`, an α schedule, and a lift
   force term to `_derivatives` in `trajectory_sim.py`. Re-run MH-Oval-01.
2. **MH-Oval-02 (lifting-body variant):** add a flat ventral surface to bias
   lift in one direction (X-37B/HL-20 lineage), assume α schedule peaks at
   ~10° during ascent.
3. **MH-Sabot-01:** combine — fly an oval up to max-Q under a discardable
   shroud, drop shroud, expose a lifting surface for the upper trajectory.

---

## 8. References (verified before citing — CLAUDE.md §11)

* US Standard Atmosphere 1976 — NASA-TM-X-74335. [VERIFIED]
* Sutton & Graves (1959). [VERIFIED]
* Hoerner, "Fluid-Dynamic Drag" (1965) — prolate spheroid Cd estimates.
  [CITATION NEEDED — chapter/page; verify before publishing.]
* X-37B / HL-20 lifting-body L/D figures: NASA TM/CR series. [CITATION NEEDED]

---

*Maintained by Shane Brazelton · Co-architected with Claude (Anthropic).
Concept memo. All numerical claims tagged per CLAUDE.md §5.2.*
