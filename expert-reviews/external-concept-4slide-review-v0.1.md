# External Concept Review — 4-slide vehicle deck

**Reviewer:** Claude (Anthropic), engineering voice. **Not** a persona review under PERSONA_REVIEW_PROTOCOL.md.
**Subject:** External 4-slide vehicle concept presented to Shane, depicting:
  1. Vacuum-sealed launch tube (10⁻⁶ torr) · Mach 20–25 · 50–200 G on launch · SiH₄ chamber · SiO₂ glass heat shield · micro-encapsulated atmospheric exit
  2. Biconic waverider · UHTC + C/C · morphing aft surfaces (retracted in tube) · plasma + heat-pipe network
  3. Blunted Von Kármán ogive · 4-layer TPS · 2200 °C outer / ~300 °C inner
  4. TPS stack: SiO₂ ablative (1800–2200 °C) / UHTC ceramic (1200–1800 °C) / C/C composite (600–1200 °C) / aerogel (50–300 °C)

**Date:** 2026-05-14
**Disposition:** Forensic evaluation, not endorsement.
**Simulator runs:** `simulation/src/external_concept_animation.py` · 30° elevation · biconic Cd=0.12 · 1.0 m × 800 kg · R_nose=0.02 m  [ESTIMATE]
**Animation artifacts:** `simulation/data/external_concept/`

---

## Executive summary

The concept inherits the same fundamental ascent-physics problems Manna already has, with two added — and worse — failure modes:

1. **The "50–200 G on launch" envelope is contradicted by the atmospheric phase of the slide's own trajectory.** Simulating the slide's stated Mach 20–25 / biconic Cd / R_nose=2 cm vehicle through US Std Atm 1976 produces **341–533 G of axial deceleration in atmosphere** during the first 20–30 seconds of flight (see PkG column below). The slide's G envelope is for the rail; the airframe will see ~3–5× that pulling air out of the way.
2. **The "SiO₂ coat ignites → glass heat shield" framing is wrong physics**, but the underlying CVD glass-deposition mechanism it implies is *plausible* — it just requires being called by its right name and bounded with a number for deposit thickness, deposit dwell time, and silane consumption per launch.
3. **Apogee is sub-orbital and the architecture has no plan for the gap.** Mach 25 reaches 90.5 km — below the Kármán line. The deck does not show how the vehicle attains orbital velocity or transfers to the Tug (which is missing from the deck entirely).

Sim numbers below are reproducible by `python simulation/src/external_concept_animation.py`.

---

## Simulation results  [DERIVED]

| Case        | BC (kg/m²) | Apogee (km) | Range (km) | Max-Q (kPa) | Peak Mach | Peak HF (GW/m²) | Peak axial G | Orbital? |
|-------------|-----------:|------------:|-----------:|------------:|----------:|----------------:|-------------:|---------:|
| Concept-M20 |      8 488 |        60.7 |      192.3 |    28 370.5 |      20.0 |           0.286 |        340.8 |       no |
| Concept-M22 |      8 488 |        71.8 |      230.8 |    34 328.3 |      22.0 |           0.380 |        412.4 |       no |
| Concept-M25 |      8 488 |        90.5 |      295.9 |    44 328.9 |      25.0 |           0.558 |        532.5 |       no |

US Std Atm 1976 · RK4 0.1 s · flat-Earth + altitude-varying g · Cd=0.12 hypersonic · R_nose=0.02 m

**Calibration:** Manna-H sim (CLAUDE.md §10) at 10 822 m/s produced apogee 9.1 km and peak HF 1.15 GW/m² with BC≈2 500 kg/m². This concept's higher BC (×3.4) and slightly sharper nose offset its lower velocity to land in the same heat-flux ballpark while extending apogee.

---

## Findings

### Finding 1 — Atmospheric G-load exceeds the slide's structural envelope by ~3–5× [DERIVED]

**Observation.** The slide annotates "50–200 G on launch." Sim shows peak *axial deceleration* during atmospheric exit reaches **341 G (M20) / 412 G (M22) / 533 G (M25)** — purely from aerodynamic drag, not the rail.

**Mechanism.** Drag decel = q / BC. With Mach 25 dynamic pressure peaking at ~44 MPa (1000× Saturn V max-Q, which was 33 kPa), and BC ≈ 8 500 kg/m², decel = 44e6 / 8 500 ≈ 5 200 m/s² ≈ 530 G. The math is unambiguous.

**Why it matters.** If the airframe is sized for 50–200 G, atmospheric drag breaks the vehicle in seconds. The 100 G upper bound of the slide envelope corresponds to where the sim sits *only after the trajectory has thinned the air enough* — around t ≈ 18 s for the M20 case. Before that, structural margin is negative.

**What to ask the concept author.**
- Is "50–200 G on launch" the rail envelope, the atmospheric-phase envelope, or both?
- If atmospheric only: what is the rail envelope?
- If rail only: what is the airframe sized for, and where is that number?

### Finding 2 — "SiO₂ ignites" is wrong, but the implied mechanism is real [DERIVED + ESTIMATE]

**Observation.** SiO₂ does not combust. Silicon dioxide is the *product* of silane oxidation: SiH₄ + 2 O₂ → SiO₂ + 2 H₂O. The slide's caption ("SiO₂ coat ignites → glass heat shield") describes the wrong reactant.

**What is actually happening (best reading).** As the vehicle pierces a sacrificial diaphragm separating the vacuum tube from atmospheric air containing silane, the SiH₄ pyrolyses on the hot vehicle surface and deposits a thin SiO₂ layer — a brief, transient CVD coating event. This is a known, if specialised, process (semiconductor industry uses it for SiO₂ thin films at < 800 °C).

**What is missing to evaluate this.**
- Silane chamber pressure and dwell time.
- Deposit thickness target (micrometers? millimeters?).
- Stoichiometric silane consumption per launch (kg of SiH₄ per pod) and how it is replenished.
- Containment plan for pyrophoric silane: TLV-Ceiling 1 ppm, autoignites in air, detonates with chlorine. Storage adjacent to a rail-exit tube is a fire-code issue.
- Whether the deposit survives Mach-25 stagnation shear, or is removed by the same flow that deposited it 50 ms later.

**Verdict.** Don't dismiss the idea; do dismiss the caption. Rewrite as *"micro-encapsulated CVD deposition of SiO₂ on rail exit; deposit acts as sacrificial outermost TPS layer."*

### Finding 3 — Sub-orbital apogee with no transfer architecture shown [DERIVED]

**Observation.** Mach 25 case reaches 90.5 km — below the Kármán line. None of the three cases shows horizontal velocity at apogee greater than 1/8 of circular orbital velocity at that altitude. None are orbital.

**Why it matters.** The deck depicts a vehicle, not a mission. Manna closes its architecture (or *attempts* to) by handing off to a Tug at apogee. This concept shows no Tug, no rendezvous geometry, no second stage, no propulsive insertion. So one of three things is true:

- (a) This vehicle is a ground-to-ground hypersonic platform, not a space launch system, and the slides are mis-framed as such.
- (b) The architecture has a Tug equivalent that simply isn't on these slides.
- (c) The author hasn't closed the velocity gap and may not realise it.

Distinguishing (a)/(b)/(c) is the most important question to ask before any further evaluation.

### Finding 4 — Peak heat flux is 6–11× the steady-state ablation limit, but pulse duration is short [DERIVED + ESTIMATE]

**Observation.** Peak Sutton-Graves stagnation heat flux: 0.29 / 0.38 / 0.56 GW/m² across the three Mach cases. Steady-state SiO₂ / PICA-X ablation handles ~50 MW/m² (5e7 W/m²); the slide concept exceeds this by **5.7× / 7.6× / 11.2×** at peak.

**Mitigant.** The pulse is **short** — atmospheric heating drops by ~3 orders of magnitude as the vehicle climbs above 50 km (ρ falls by ~10⁵). Sim shows the heating window is ≈ 12 seconds wide above the 50 MW/m² threshold for the M25 case. Sized ablative may survive this.

**Risk.** Survival means *erosion*. At 0.56 GW/m² with SiO₂ molar enthalpy of vaporisation ~12 MJ/kg and density 2.2 g/cm³, the ablation recession rate is roughly q / (ρ × h_eff) ≈ 5.6e8 / (2 200 × 1.2e7) = ~0.021 m/s = **21 mm/s**. Over a 12-second pulse that's **252 mm of SiO₂ ablated** at the stagnation point. The slide's 4-layer stack does not show how thick layer 1 is, but 252 mm is large.

**What to ask.**
- Layer-1 SiO₂ thickness, by station along the vehicle.
- Does transpiration cooling through the UHTC pores (shown in slide 3) start before or after the SiO₂ layer is consumed? (If after, it's a transient cliff.)
- FIAT or equivalent ablation simulation for the worst stagnation point.

### Finding 5 — Biconic waverider geometry conflicts with the "uncrewed cargo" mission posture [JUDGMENT]

**Observation.** Waveriders need a controlled angle of attack to ride their own shock. The slide shows morphing aft surfaces, which can provide that authority — but morphing surfaces are mechanism-rich, fault-intolerant, and expensive.

**Why it matters in the Manna context.** Manna-H is specifically the *dumb* variant — no actuators, no morphing, mass fraction 78 %. Importing this concept's airframe to Manna-H breaks the doctrine: morphing surfaces eat mass fraction and add cost. Conversely, removing the morphing surfaces from this concept turns it into a non-waverider biconic, which is a perfectly fine body but loses its only justification for being a waverider in the first place.

**Verdict.** Either the morphing surfaces are doing real work (in which case quantify it: L/D, control authority budget, actuator mass) or they should be removed (in which case the shape choice needs to be re-justified vs a sphere-cone or simple biconic without lift). Don't keep them on the slide as decoration.

### Finding 6 — "Vacuum to 1 atm via diaphragm at Mach 25" is the hardest part and is hand-waved [JUDGMENT]

**Observation.** The slide shows the vehicle passing from 10⁻⁶ torr (essentially perfect vacuum) into the SiH₄ chamber and out into ambient atmosphere. The pressure rise across this transition is 1.3e-4 → 1.0e5 Pa — **9 orders of magnitude in milliseconds**.

**What that does to the vehicle.** The bow shock that forms in the SiH₄ chamber sees the vehicle going Mach 25 with no upstream flow until the instant it hits the diaphragm. Diaphragm rupture energy, fragment dispersal, and the resulting shock-on-vehicle pressure spike are the dominant load case for the *first* second of flight — likely worse than any subsequent max-Q event.

**What is missing.** Diaphragm material, thickness, rupture pressure, fragment containment plan, overpressure on the airframe at the moment of rupture, and whether the silane chamber acts as a shock tube or as an open-air transition.

**Why it matters.** This problem is solvable (light-gas guns and shock tubes have done variants of it for decades), but the solution is not shown and the number is not given. Without it, every downstream slide is being evaluated against a launch case that may or may not survive its own first millisecond.

### Finding 7 — TPS layer stack chart is qualitatively fine, quantitatively undefined [JUDGMENT]

**Observation.** Slide 4 shows temperature ranges per layer (SiO₂ 1800–2200 / UHTC 1200–1800 / C/C 600–1200 / aerogel 50–300). Slide 3 shows the layers and labels them with their materials and an outer/inner temperature spread of 2200 → ~300 °C.

**What is right.** The materials are credible. The ordering is correct (highest-temperature ablative outermost, aerogel against the payload bay). The 4-layer concept is the right *topology* for an ablative-then-insulator stack.

**What is missing.** Thicknesses. A 4-layer stack can resolve a 1900 K temperature drop only with adequate thickness — for silica aerogel (k ≈ 0.02 W/m·K), holding a 250 K drop across the last layer under a 0.56 GW/m² stagnation pulse for 12 seconds requires non-trivial thickness budget. Without numbers, the slide is a topology diagram, not a TPS design.

**What to ask.**
- Thickness per layer, by station (nose / forebody / aftbody).
- Transient FE (FIAT or similar) showing the back-face temperature profile.
- Soakback after the pulse — heat trapped in C/C will leak inward over minutes.
- Mass of the TPS as a fraction of the vehicle.

### Finding 8 — No citations, no equations, no margin column [JUDGMENT]

**Observation.** The slides are visualisations. There are no references, no equations on the figures (Mach numbers and temperatures only), and no margin column on any number. This is normal for a marketing deck. It is not sufficient for a forensic evaluation.

**What is needed before further review.** A backing document of 5–15 pages with:
- Source for the 50–200 G envelope (which load case, what method).
- Source for the 2200 °C outer temperature (uniform? stagnation only? aerothermal CFD or steady-state assumption?).
- Sutton-Graves or equivalent heat-flux estimate by the author, with the velocity and density values they used.
- Reference altitude / Mach envelope for the morphing surfaces' control authority.
- Diaphragm rupture analysis (overpressure, fragment energy).
- TPS thicknesses with ablation rate budget.

Without that document, the deck cannot be evaluated against this concept's own claims — only against simulator runs of approximated parameters.

---

## Recommended disposition

1. **Hold.** Do not adopt this concept into the Manna baseline.
2. **Request a backing document** (Finding 8) before the next pass.
3. **Run the animation** (`python simulation/src/external_concept_animation.py`) when discussing the deck with the originator. The G-load and dynamic-pressure panels are the fastest path to a productive conversation about where the airframe sizing has to live.
4. **Borrow the topology, not the deck.** The 4-layer ablative-to-aerogel TPS stack and the blunted Von Kármán nose are credible inputs to Manna's own TPS trade study (CLAUDE.md §10 line item 8). Cite them as *topology references*; don't import their numbers.
5. **Do not use this for Manna-B or Manna-I.** The 50–200 G envelope and the morphing surfaces both break those variants by construction.

---

## Open questions for the concept's author (in priority order)

1. Is the airframe sized for the **atmospheric** load case (≥ 500 G axial decel for the Mach 25 trajectory), or only for the rail load case (50–200 G)?
2. What is the diaphragm rupture analysis at the tube exit?
3. Where is the Tug / second stage / propulsive element that closes the velocity gap to orbit?
4. What is the per-layer TPS thickness? What ablation rate budget was used for SiO₂?
5. What is the silane consumption per launch and how is the chamber re-stocked?
6. What L/D does the morphing-surface waverider achieve at Mach 20+, and what control authority is required to hold the optimal AoA?
7. Are there *any* CFD or transient thermal results behind these slides?

---

## Limitations of this review

- **Parameters are estimated.** The slides do not state Cd, mass, diameter, or nose radius. Sim used 1.0 m × 800 kg / Cd=0.12 / R_nose=2 cm — all [ESTIMATE]. Changing any one of these by ±50% changes the sim numbers materially. Direction of the findings does not change.
- **Sutton-Graves is a constraint, not a design tool.** It gives stagnation heat flux only; it ignores radiation, real-gas chemistry, transpiration, and surface catalysis. Use it to *flag* TPS infeasibility (Finding 4), not to size hardware.
- **Flat-Earth approximation.** Apogees above ~100 km should be re-run in a spherical-Earth integrator. Sim numbers above 60 km altitude are accurate to ≲ 5%; above 150 km, error grows.
- **Animation does not depict failure modes.** It depicts simulation results assuming the airframe is structurally infinite. Finding 1 is *not* shown by the vehicle exploding; it is shown by the deceleration trace exceeding the 100–200 G band.

---

*Generated by Claude during session `claude/new-session-U5rRz`. All numerical claims are reproducible by `python simulation/src/external_concept_animation.py` from the repo root.*
