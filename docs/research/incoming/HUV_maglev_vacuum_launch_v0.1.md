# Hypersonic Unmanned Vehicle — Maglev Vacuum Launch System

**Source:** Conversation with Claude (claude.ai), captured by Shane 2026-04-27
**Status:** v0.1 incoming concept — not yet evaluated against Manna architecture
**Routed to:** `expert-reviews/HUV_maglev_vacuum_eval_v0.1.md` for forensic review

---

## Concept overview

A maglev-accelerated unmanned hypersonic vehicle launched from a vacuum-sealed
tube, with a patterned silicon-hydrogen (silane / SiH₄) exit coating that
self-applies a sacrificial heat shield on atmospheric contact.

Novel-IP claims, three junctions:

1. **Vacuum launch + reactive coating** — atmospheric contact triggers
   self-applied heat shield. Zero added weight from pre-installed thermal
   protection. The atmosphere does the work.
2. **Blunt nose at hypersonic speed** — counterintuitive but proven. Detached
   bow shock pushes thermal boundary layer off the surface. Sharp noses
   concentrate heat at the tip; blunt tips distribute it.
3. **Plasma actuators replacing all control surfaces** — no moving mechanical
   parts, nothing to jam under G-load or thermal expansion. Steering with
   ionised airflow.

---

## Launch system

Maglev vacuum tube:

- Mach 20–25 at exit  [ESTIMATE]
- Launch G-load: 50–200 G depending on tube length  [ESTIMATE]
- No pilot → no biological limit
- Vehicle rides magnetic field in near-vacuum — zero drag until exit
- Zero physical contact with tube walls during acceleration

Silicon-hydrogen (silane SiH₄) exit coating:

- Silane is pyrophoric — ignites instantly on air contact
- Burns and forms SiO₂ (silica glass) layer on vehicle skin
- Auto-generates heat shield on exit
- Micro-encapsulated in aerogel matrix; capsules crushed at exit pressure delta
- Applied via electrostatic application in sealed chamber just before exit

Closest real analog: DARPA HTV-2 + StarTram launch concept. No prior art combines
maglev vacuum launch with reactive ablative coating.  [CITATION NEEDED — verify
StarTram and HTV-2 references against NTRS]

---

## Vehicle design

**Shape: biconic waverider**

- Cylindrical rear to match tube bore
- Transitions to waverider geometry after exit
- Rides its own shockwave for lift at hypersonic speed
- Top-down profile: nose cap → forebody → payload/comms → aftbody

**Control: plasma actuators (replace all mechanical surfaces)**

- No hinges, no mechanical failure points
- Morphing control surfaces retracted during tube transit, deploy after exit
- Steering via ionised airflow

**Thermal management:**

- Silane coat handles the exit spike
- Internal heat pipe network redistributes thermal load
- Transpiration cooling on leading edges (bleed inert gas through porous skin)
- Aerogel insulation layer beneath skin

**Body materials:**

- Carbon-carbon composite skeleton
- Aerogel insulation layer
- Smooth cylindrical profile for tube fit

---

## Nose design — blunted Von Kármán ogive

- Blunt tip creates a strong detached shock — pushes heat away from the surface
- Counterintuitive but consistent with hypersonic blunt-body heating theory

Nose cap construction (outer → inner):

1. SiO₂ ablative coat (auto-applied by silane burn) — 1800–2200 °C  [ESTIMATE]
2. UHTC ceramic — 1200–1800 °C  [ESTIMATE]
3. Carbon-carbon (C/C) composite structural layer — 600–1200 °C  [ESTIMATE]
4. Aerogel insulation — 50–300 °C (payload-safe)  [ESTIMATE]

Transpiration cooling on nose / leading edges: porous skin, inert gas bleed.

---

## Thermal protection system — layer breakdown

| Layer | Material | Temp range | Mechanism |
|---|---|---|---|
| 1 (outer) | SiO₂ ablative coat | 1800–2200 °C | Slow ablation, carries heat off |
| 2 | UHTC ceramic | 1200–1800 °C | Radiates heat back outward |
| 3 | C/C composite | 600–1200 °C | Structural at high temperature |
| 4 (inner) | Aerogel insulation | 50–300 °C | Final thermal barrier |

Claimed result: 2200 °C at nose tip → < 300 °C at payload frame.  [ESTIMATE]

---

## G-force context

| Reference | Limit |
|---|---|
| F-22 / F-35 / Eurofighter / Su-57 | +9 G |
| F-16 (airframe test limit) | +12 G |
| Human (G-suit) | ~9–10 G sustained |
| X-47B class UAV | +15 G |
| Hypersonic drones | +20 G |
| Missiles | 30–50 G |
| **HUV maglev launch** | **50–200 G**  [ESTIMATE] |

---

## Weak points called out

| Problem | Proposed solution |
|---|---|
| Tube exit shock transition | Gradual pressure staging at tube end |
| Coating uniformity | Electrostatic application in sealed chamber just before exit |
| Vehicle tumble at exit | Spin-stabilisation during maglev run |
| Silane storage (volatile) | Micro-encapsulated in aerogel matrix; crushed at exit pressure delta |

---

## Next engineering layers (per source doc)

1. Tube length vs G-load tradeoff
2. Silane microencapsulation material (capsule rupture trigger)
3. Spin-stabilisation frequency
4. Payload shielding under G-spike

---

## Terminology reference

- **Radome** — nose cone housing on conventional aircraft (radar dome)
- **Von Kármán ogive** — aerodynamically optimised curved nose profile
- **UHTC** — Ultra-High Temperature Ceramics (survive 2000 °C+)
- **C/C composite** — carbon-carbon composite (structural, high-temp)
- **Aerogel** — ultra-low density insulation
- **SiH₄** — silane (silicon-hydrogen); pyrophoric
- **SiO₂** — silica glass; product of silane combustion
- **Transpiration cooling** — coolant gas bled through porous skin
- **Waverider** — vehicle that rides its own shockwave for lift
- **Biconic** — two-cone nose / body geometry
- **Plasma actuator** — flow control device using ionised air, no moving parts
