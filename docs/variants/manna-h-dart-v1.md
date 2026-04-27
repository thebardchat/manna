# MH-Dart-01 — concept design memo

**Concept ID:** `MH-Dart-01`
**Cargo class:** H (water, propellant, food bricks, sintered metal stock; 100 G internal)
**Geometry:** Slender dart — ogive nose, smooth cylindrical body, fixed cruciform fins
**Status:** Pre-Phase A concept; first trip through `simulation/src/concept_eval.py`.
**Date:** 2026-04-27
**Operating under:** [CLAUDE.md](../../CLAUDE.md) §5 conventions, §7 forensic gates

---

## 1. Why a new pod

Per CLAUDE.md §10, the canonical Manna-H strawman (m=800 kg, D=1.0 m, Cd₀=0.45 →
BC ≈ 2,265 kg/m²) reaches **9.1 km apogee at 30°** in the trajectory simulator —
97% below the v0.1 paper's vacuum claim of 1,950 km. The architecture as written
does not close.

Sweep (`simulation/src/sweep.py`) shows the trajectory gap closes if BC moves into
the **5,000 → 50,000 kg/m²** band:

| BC target          | Outcome at 30–45° elevation                |
| ------------------ | ------------------------------------------ |
|  ~2,000 kg/m²      | Sub-orbital, sub-Kármán (canonical H)      |
|  ~5,000 kg/m²      | Clears Kármán at steep elevation           |
|  ~50,000 kg/m²     | Approaches orbital velocity at apogee      |

`MH-Dart-01` is the first concrete attempt to land in that band without breaking
the rail energy budget or the H-class cargo profile.

---

## 2. Design strategy

Two paths to higher BC:

1. **Add mass.** More propellant in same envelope = heavier pod. Fights the rail.
2. **Shrink frontal area.** Same cargo, longer thinner tube. Helps the rail.

**MH-Dart-01 takes path 2.** Trade frontal area for length:

```
                   ── 6.00 m ──
                  ┌────────────┐
   ────────► nose │            │ fins
                  └────────────┘
                       0.50 m diameter
```

Fineness ratio L/D = 12.0 (ogive-cylinder dart territory; cf. APFSDS rounds at
20–30). H-class cargo is overwhelmingly liquids and granulars — they pack in a
tube fine. This shape is *wrong* for spares and biologics, which is why this
concept is H-only.

---

## 3. Parameters  [ESTIMATE unless tagged]

| Parameter            | Value                  | Tag                |
| -------------------- | ---------------------- | ------------------ |
| Total mass           | 1,200 kg               | [ESTIMATE]         |
| Cargo mass (65%)     |   780 kg               | [ESTIMATE]         |
| Body diameter        |  0.50 m                | [ESTIMATE]         |
| Body length          |  6.00 m                | [ESTIMATE]         |
| Fineness L/D         | 12.0                   | [DERIVED]          |
| Frontal area         |  0.196 m²              | [DERIVED]          |
| Drag coefficient Cd₀ |  0.15                  | [ESTIMATE — slender hypersonic body, Hoerner heritage] |
| Ballistic coeff.     | 40,744 kg/m²           | [DERIVED]          |
| Rail v_exit          | 6,500 m/s              | [PLACEHOLDER — pulled from CLAUDE.md §1; awaiting BGKPJR rail energy budget] |

**Cd₀ rationale:** Hoerner ("Fluid-Dynamic Drag", 1965) gives Cd ≈ 0.10 – 0.18
for fineness-12 ogive-cylinders at supersonic/hypersonic speeds with skin
friction dominant. Use 0.15 central. [CITATION NEEDED] — verify Hoerner
chapter/page; CFD required to firm up.

---

## 4. Trajectory test results [DERIVED]

Run via `python simulation/src/concept_eval.py` on 2026-04-27.
Sim: 3-DOF, US Std Atm 1976, RK4 dt=0.1 s, flat-Earth + altitude-varying gravity.

```
====================================================================================================
  MH-Dart-01  —  cargo class H  —  slender dart, ogive nose, fixed cruciform fins
====================================================================================================

  Trajectory results [DERIVED — US Std Atm 1976 + RK4 0.1 s]:
     elev   apogee km   maxQ kPa   maxMach    vx@apo    v_circ    vx/vc   PkHF GW/m²   orb@apo
    ------------------------------------------------------------------------------------------
      15°        58.4    25877.7      19.1      3755      7868    0.477         0.25        no
      30°       344.1    25877.7      19.1      4361      7699    0.566         0.25        no
      45°       855.6    25877.7      19.4      3840      7422    0.517         0.25        no
```

**Plot:** `simulation/data/trajectory_runs/concept_MH-Dart-01.png`

### 4.1 What worked

* **Clears Kármán line at 30° and 45°.** 344 km and 856 km apogee respectively
  — comfortable margin for an orbiting Tug pre-positioned in a phasing orbit
  to match the apogee state vector (CLAUDE.md §7.3).
* **vx/v_circ at apogee = 0.566 (peak, at 30°).** Up from ≈0.30 for the
  canonical Manna-H. The Tug now needs to close ~3.4 km/s of ΔV instead of
  ~5.4 km/s — a 37% reduction in rendezvous burn.
* **Peak heat flux 0.25 GW/m²** — 4.6× lower than canonical Manna-H (1.15
  GW/m²), because launch velocity is 6.5 km/s vs. 10.8 km/s. PICA-X-class TPS
  is plausible at this heat flux. [CONSTRAINT-NOT-MODELED — Sutton-Graves with
  R_nose=5 cm assumed; geometry not yet defined.]

### 4.2 What didn't

* **Does not reach `orbital_at_apogee` at any elevation.** Best vx/v_circ =
  0.566, short of the ≥1.000 needed for a true rendezvous-with-no-Tug-burn
  insertion. Concept is **PARTIAL** by the verdict gate in `concept_eval.py`.
* **Max-Q = 25.9 MPa.** That's the bare q = ½ρ₀v² at the rail muzzle
  (1.225 kg/m³ × 6,500² / 2). Identical at all elevations because peak-Q
  happens at launch, not later. **This is an order of magnitude above any
  flying reusable launch vehicle** — Falcon 9 max-Q is ~30–35 kPa, Shuttle
  was ~33 kPa. The launch tube must be evacuated or the muzzle altitude must
  be much higher, or the pod must accept loads that today are only seen by
  artillery shells.
* **Peak Mach 19.1** — squarely in the hypersonic regime. The Cd₀ = 0.15
  estimate is most exposed here; needs CFD or wind-tunnel data to firm up.

### 4.3 Verdict

`PARTIAL — altitude clears, but rendezvous burn is large.`
**Worth more design work; not ready to fly.**

---

## 5. Open issues (carried forward)

These are tracked in `pod_concepts.MH_DART_01.open_issues`:

1. **Cd₀ = 0.15 is a slender-body estimate.** CFD or wind-tunnel data needed
   before any apogee number is defensible at Mach 19.
2. **Sutton-Graves with R_nose = 5 cm assumed.** Smaller nose ⇒ higher q̇
   per unit area; this pod has the same nose radius assumption as canonical
   variants but a different geometry. TPS sizing TBD.
3. **Slender body bending modes.** L/D = 12 at 100 G rail acceleration and
   through 25.9 MPa max-Q is a structural call — Euler buckling, first
   bending mode frequency, fin attachment loads all unsized.
4. **Cargo bay aspect ratio.** 0.50 m × ~4 m usable ⇒ liquids/granulars/stock
   only. Anything compact and dense is a different concept.
5. **Fins vs. spin-stabilization.** Fins add drag, complicate rail
   interface (must clear sabot or fold). Open trade.
6. **Rail v_exit = 6.5 km/s is `[PLACEHOLDER]`.** BGKPJR rail energy budget
   has not been published; this concept dies if real v_exit is < 5 km/s.
7. **Max-Q = 25.9 MPa at the muzzle.** Either evacuate the launch tube,
   raise the muzzle altitude, or harden the pod. Cargo at 100 G already
   handles the inertial load; the structural load is on the airframe and
   nose tip, not the cargo.

---

## 6. Next iteration candidates

If we keep iterating in this concept space, two clear next steps:

* **MH-Dart-02:** Same geometry, push mass to 1,800 kg (more cargo, same
  rail velocity if BGKPJR can deliver the energy). BC rises to ~61,000 kg/m².
  Should push vx/v_circ above 0.65.
* **MH-Sabot-01:** Discardable aerodynamic shroud during max-Q phase →
  expose smaller, lighter dart at altitude. Splits the geometry between
  rail-launch (low-drag profile to survive 25.9 MPa) and post-shroud
  (lower-mass dart for higher BC).

Different cargo class concepts (I-class instruments, B-class biologics)
need fundamentally different geometries — track those as separate concept
IDs (e.g. `MI-Module-01`, `MB-Cradle-01`).

---

## 7. References (verified before citing — CLAUDE.md §11)

* US Standard Atmosphere 1976 — NASA-TM-X-74335. [VERIFIED]
* Sutton & Graves (1959), "A General Stagnation-Point Convective Heating
  Equation." [VERIFIED — heritage source for the heat flux constant.]
* Hoerner, "Fluid-Dynamic Drag" (1965). [CITATION NEEDED — chapter/page
  for the fineness-12 ogive Cd estimate; verify before publishing.]

---

*Maintained by Shane Brazelton · Co-architected with Claude (Anthropic).
First-pass concept memo. All numerical claims tagged per CLAUDE.md §5.2.*
