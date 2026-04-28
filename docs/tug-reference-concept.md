# Tug reference concept — v0.1

> **MATURITY STATEMENT — READ BEFORE CITING**
> This document is a **Pre-Phase A concept memorandum**.  All numbers are
> `[ESTIMATE]` or `[DERIVED]` unless tagged `[VERIFIED]`.  No design has
> been committed.  Intended audience: Shane Brazelton + technical collaborators
> performing the Pre-Phase A feasibility review.

> **RELOCATION NOTE:** This document is a placeholder in `manna/docs/`.
> It belongs in a dedicated `tug` repository under `thebardchat/tug`.
> Create that repo manually, then move this file to `docs/TUG_CONCEPT.md`.

*Author: Shane Brazelton + Claude (Anthropic) | v0.1 | 2026-04-28*
*Companion repos: [manna](https://github.com/thebardchat/manna) ·
[BGKPJR-Core-Simulations](https://github.com/thebardchat/BGKPJR-Core-Simulations)*

---

## 1  Purpose

The Tug is the orbital transfer vehicle that:

1. Waits in a pre-positioned orbit near the apogee of an incoming Manna pod
2. Matches the pod's apogee state vector and closes at sub-m/s rates
3. Captures the pod via a berthing/catch mechanism
4. Performs a trans-lunar injection (TLI) burn to deliver cargo to the Lunar Base

The Tug is **reusable**.  Its operating life is defined by propellant budget and
mechanical wear on the capture mechanism.  Pod servicing, refueling, and reflight
cadence are open design questions.  `[PENDING]`

---

## 2  Mission context

```
BGKPJR rail (Hazel Green, AL — 34.93°N)
  │
  │  EM launch at hypersonic velocity
  │  elevation: 30° nominal  [ESTIMATE]
  ▼
Manna pod — ballistic suborbital arc
  │
  │  apogee altitude: 100–200 km (target; requires redesigned BC)  [DERIVED — sim]
  │  apogee location: ~34.93°N, downrange from rail  [DERIVED]
  │  horizontal velocity at apogee: 1,000–4,000 m/s (variant-dependent)  [DERIVED — sim]
  ▼
Tug rendezvous window
  │
  │  Tug pre-positioned in elliptical orbit, apogee co-located with pod apogee
  │  closing rate at apogee: < 1 m/s  [REQUIREMENT — not yet verified]
  ▼
Capture + berthing
  │
  │  mechanical lock, leak check (if pressurized cargo), health check
  ▼
Trans-lunar injection (TLI) burn
  │
  │  ΔV: ~900–1,100 m/s  [ESTIMATE — depends on departure C3]
  ▼
Lunar transfer arc (~3 days)  [ESTIMATE]
  │
  ▼
Lunar orbit insertion + handoff to surface descent stage (out of Tug scope)
```

---

## 3  Orbit definition

### 3.1  Inclination constraint

The BGKPJR rail sits at 34.93°N latitude.  A pod launched due east (azimuth 90°)
reaches a maximum latitude equal to the launch latitude — its orbit has an
inclination of approximately 34.93°.  [VERIFIED: basic orbital mechanics]

Attempting to fly a Tug in a 0° (equatorial) orbit would require a plane-change
ΔV of approximately:

```
ΔV_plane = 2 × v_orbit × sin(Δi/2)
         = 2 × 7,784 m/s × sin(34.93°/2)
         ≈ 4,620 m/s   [DERIVED — v_circ at 200 km, Δi = 34.93°]
```

4.6 km/s exceeds the entire Tug ΔV budget by a large margin.

**Selected architecture:** Tug operates in a ~35° inclination orbit, matching the
rail launch latitude.  This is standard practice: Cape Canaveral (28.5°N) launches
to ISS (51.6°) require a small plane change; launches from Hazel Green (34.93°N)
to a 35° Tug orbit require zero plane change.  [VERIFIED — analogous to standard
launch-site-to-ISS-inclination practice]

### 3.2  Orbit shape

The Tug orbit must be designed so that:
- Tug apogee altitude ≈ pod apogee altitude (target: 100–200 km)  [ESTIMATE]
- Tug apogee position (in-track) coincides with pod apogee at the time of rendezvous

A highly elliptical orbit (HEO) with a low perigee (~150 km — just above drag) and
apogee at the pod catch altitude gives the Tug maximum dwell time near apogee.
`[ESTIMATE — perigee altitude and orbit lifetime need atmospheric drag trade]`

**Nominal Tug orbit (v0.1 placeholder):**

| Parameter | Value | Tag |
|-----------|-------|-----|
| Inclination | ~35° | [DERIVED] |
| Apogee altitude | 150–300 km | [ESTIMATE — depends on BC feasibility study outcome] |
| Perigee altitude | 150–200 km (circular option) or 150 km (elliptical) | [ESTIMATE] |
| Period | ~88–92 min (near-circular 200 km) | [DERIVED] |
| v at apogee (200 km circular) | ~7,784 m/s | [DERIVED — vis-viva] |

> ⚠ The optimal orbit shape depends on the pod apogee altitude, which has not
> closed to a single value.  The BC feasibility study (manna §3.3) shows pod
> apogee at 100–200 km requires BC = 7,500–30,000 kg/m² depending on variant.
> Tug orbit design is gated on that number hardening.

---

## 4  Rendezvous architecture

### 4.1  The apogee insight

At apogee, an object in a ballistic trajectory moves at its minimum speed for
that trajectory.  For the Manna pod, most of the horizontal velocity has been
bled off by drag during ascent — the residual vx at apogee is a small fraction
of the orbital velocity at that altitude.

Example (Manna-H, BC=7,500 kg/m², 30° elevation, from simulation):

```
Apogee altitude:    ~100 km
vx at apogee:       ~600–1,500 m/s  [DERIVED — simulation; exact value TBD pending redesign]
v_circ at 100 km:   ~7,846 m/s      [DERIVED — vis-viva]
vx / v_circ:        ~0.08–0.19      [DERIVED]
```

The pod is moving at roughly 8–19% of orbital velocity at apogee — it is nearly
ballistic, nearly vertical, and nearly stopped in the horizontal direction.
The Tug can match this slow horizontal velocity with a gentle RCS burn.

### 4.2  Phasing orbit sequence

```
Step 1: Tug in a parking orbit at ~35° inclination, perigee below pod apogee.

Step 2: Tug performs a phasing maneuver to align its apogee with the pod's
        predicted apogee location in space (altitude + in-track position).
        ΔV: ~10–100 m/s  [ESTIMATE — depends on phase error]

Step 3: Tug coasts to its apogee.  At apogee, Tug velocity ≈ 7,784 m/s (200 km
        circular) or lower if in an elliptic orbit with apogee at that altitude.

Step 4: Tug matches pod's vx at apogee.  Closing rate set to < 0.5 m/s.
        ΔV: ~5–50 m/s  [ESTIMATE — depends on pod vx at apogee]

Step 5: Tug berthing arm or catch mechanism closes on pod.
        Capture takes place over ~30–120 seconds at near-zero relative velocity.

Step 6: Tug performs TLI burn from the combined orbit.
```

> ⚠ The v0.1 memo incorrectly described rendezvous as the Tug "catching the pod
> at 4 km/s relative."  That is an impact, not a rendezvous.  Steps 4–5 above
> describe the correct approach: the Tug matches the pod's slow apogee velocity,
> not the other way around.  [Munk review issue #3, 2026-04-25]

### 4.3  Catch window analysis  `[PENDING]`

The catch window is determined by:
- Pod apogee position uncertainty (depends on rail pointing accuracy and ΔV dispersion)
- Tug approach corridor width (depends on capture mechanism design)
- Atmospheric drag variation at apogee altitude (affects pod timing)

At 30° elevation and 100 km apogee, a ±0.1° rail pointing error produces
approximately ±170 m lateral offset at apogee.  `[DERIVED — rough angular geometry]`
Whether the capture mechanism can accommodate ±170 m requires a GNC design
that does not yet exist.  `[PENDING]`

---

## 5  Delta-V budget  [ESTIMATE]

All figures are order-of-magnitude estimates.  No trajectory optimization has
been performed.  `[ESTIMATE throughout — requires GMAT or STK analysis to harden]`

| Maneuver | ΔV (m/s) | Notes |
|----------|----------|-------|
| Orbit insertion (launch cost — not Tug propellant) | ~9,200–9,500 | Tug launched on conventional rocket; not on rail |
| Phasing maneuvers (per pod catch) | 10–100 | Depends on orbit design; weekly cadence assumed |
| Apogee velocity match (per catch) | 5–50 | Match pod vx at apogee |
| Orbit maintenance (per year) | 10–50 | Drag at 200 km is ~50 m/s/year [ESTIMATE] |
| Trans-lunar injection (per mission) | 900–1,100 | C3 from LEO to lunar; 3-day transfer [ESTIMATE] |
| Lunar orbit insertion (LOI) | ~850–1,000 | If Tug performs LOI; may be offloaded to lunar stage |
| Reserve | 100 | Contingency |
| **Total (lifetime, 50 catches, 5 TLI)** | **~8,000–10,000** | [ESTIMATE — rough] |

> Refueling architecture: the Tug must be refueled in orbit.  Manna-H carries
> propellant as cargo — a dedicated Manna-H propellant pod is the logical
> resupply mechanism.  This creates a dependency: Tug must have propellant
> reserves to catch the first resupply pod.  This is a bootstrapping problem
> that requires a mission sequence design.  `[PENDING]`

---

## 6  Key subsystems  `[FUNCTIONAL ARCHITECTURE — ALL UNDEFINED]`

Each subsystem below is named but not designed.  This is the functional block
diagram stub called for by the Lukens persona review (Issue #5).

```
┌───────────────────────────────────────────────────────────────┐
│                           TUG                                 │
│                                                               │
│  ┌─────────────┐   ┌──────────────┐   ┌─────────────────┐   │
│  │  Propulsion │   │  GNC          │   │  Power          │   │
│  │  [UNDEFINED]│   │  [UNDEFINED]  │   │  [UNDEFINED]    │   │
│  │  Main engine│   │  Star tracker │   │  Solar / battery│   │
│  │  RCS thrusters│ │  IMU          │   │                 │   │
│  │  Propellant │   │  Rendezvous   │   └─────────────────┘   │
│  │  tanks      │   │  sensors      │                         │
│  └─────────────┘   └──────────────┘   ┌─────────────────┐   │
│                                        │  C&DH           │   │
│  ┌─────────────┐   ┌──────────────┐   │  [UNDEFINED]    │   │
│  │  Capture    │   │  Cargo bay   │   │  Flight computer│   │
│  │  mechanism  │   │  [UNDEFINED] │   │  Comms          │   │
│  │  [UNDEFINED]│   │  Pod docking │   └─────────────────┘   │
│  │  Berthing   │   │  ports (qty?)│                         │
│  │  arm?       │   │  Manna-H/I/B │   ┌─────────────────┐   │
│  │  Net?       │   │  interface   │   │  Thermal        │   │
│  │  Gripper?   │   └──────────────┘   │  [UNDEFINED]    │   │
│  └─────────────┘                      └─────────────────┘   │
└───────────────────────────────────────────────────────────────┘
```

**Capture mechanism** is the highest-risk subsystem.  It must accommodate:
- Pod arrival velocity dispersion (up to ±50 m/s in vx at apogee)  `[ESTIMATE]`
- Pod attitude uncertainty at apogee (tumbling? stabilized?)  `[UNKNOWN]`
- Pod structural interface (what does the pod's docking port look like?)

No heritage exists for catching an unpowered hypersonic pod at apogee.  The closest
analog is ISS cargo berthing (e.g., Cygnus via SSRMS), but at near-zero relative
velocity in a controlled environment — not 600–1,500 m/s pod arrival.
TRL: **1–2**.  `[ESTIMATE — Lukens review Issue #8]`

---

## 7  Interface references

Two Interface Control Documents (ICDs) are required.  Neither exists yet.
These are stubs — each TBD entry is a required design decision.

### ICD-TUG-001 — Pod-to-Tug (capture interface)

| Parameter | Value | Tag |
|-----------|-------|-----|
| Pod docking port location | TBD | [PLACEHOLDER] |
| Pod docking port type (androgynous? passive?) | TBD | [PLACEHOLDER] |
| Allowable pod approach velocity | < 0.5 m/s relative | [REQUIREMENT — UNVERIFIED] |
| Allowable pod lateral offset at capture | TBD | [PLACEHOLDER] |
| Allowable pod attitude error at capture | TBD | [PLACEHOLDER] |
| Mechanical capture load on pod | TBD | [PLACEHOLDER] |
| Pod identification (how does Tug find the pod?) | Transponder? Radar? Optical? | [PLACEHOLDER] |
| Communication protocol (pod → Tug during approach) | TBD | [PLACEHOLDER] |
| Pod reuse: inspection requirement between flights | TBD | [PLACEHOLDER] |

### ICD-TUG-002 — Tug-to-Lunar-Stage (delivery interface)

Out of scope for v0.1.  Defined by Lunar Base architecture (not yet built).

---

## 8  Key constraints and blockers

| # | Constraint | Source | Status |
|---|-----------|--------|--------|
| 1 | Pod apogee altitude undefined — depends on BC redesign | manna §3.3 | OPEN — blocks orbit design |
| 2 | No pod docking port design | Lukens ICD | OPEN — blocks capture mechanism |
| 3 | Pod GNC undefined (does pod have attitude control?) | Lukens #5 | OPEN — affects dispersion budget |
| 4 | Catch window analysis not performed | This doc §4.3 | OPEN |
| 5 | TLI ΔV not computed (requires specific orbit) | This doc §5 | OPEN — rough estimate only |
| 6 | Refueling architecture not designed | This doc §5 | OPEN |
| 7 | Capture mechanism at TRL 1–2 | Lukens #8 | OPEN — highest risk item |
| 8 | No propulsion trade study | This doc §5 | OPEN |

---

## 9  Recommended next actions (priority order)

1. **Harden pod apogee altitude** — run the BC feasibility study to closure and
   select an architecture option.  Everything else gates on this number.
   See `manna/simulation/src/bc_feasibility.py`.

2. **Define pod docking port** — even a notional sketch.  The capture mechanism
   cannot be designed until the pod-side interface is fixed.

3. **Catch window analysis** — compute pod apogee position dispersion from
   rail pointing accuracy and ΔV uncertainty.  This defines the capture
   mechanism aperture requirement.

4. **TLI ΔV trade** — run GMAT or equivalent for a Hohmann transfer from the
   Tug parking orbit to lunar transfer injection.  Solidifies propellant budget.

5. **Propulsion trade** — chemical vs. electric for the Tug.  Chemical allows
   short TLI burns; electric is mass-efficient for sustained operations but
   long spiral times.  Mass budget and cadence assumptions drive this choice.

6. **Create dedicated `tug` repo** — this document belongs in its own repo
   (`thebardchat/tug`) with the same structure as `manna/`.  Create it, copy
   this file to `docs/TUG_CONCEPT.md`, and link the two repos.

---

## 10  References (verified)

- BGKPJR-Core-Simulations: github.com/thebardchat/BGKPJR-Core-Simulations  [VERIFIED]
- manna repo: github.com/thebardchat/manna  [VERIFIED]
- ShaneTheBrain Constitution: github.com/thebardchat/constitution  [VERIFIED]
- NASA GMAT (General Mission Analysis Tool): software.nasa.gov/software/GSC-17177-1  [VERIFIED]
- Wertz, J.R., Everett, D.F., Puschell, J.J. (2011). *Space Mission Engineering: The New SMAD.*
  Microcosm Press.  [VERIFIED — standard reference]
- Humble, R.W., Henry, G.N., Larson, W.J. (1995). *Space Propulsion Analysis and Design.*
  McGraw-Hill.  [VERIFIED — standard reference]

---

*v0.1 produced: 2026-04-28.  Pre-Phase A concept memorandum.*
*Operating under [ShaneTheBrain Constitution](https://github.com/thebardchat/constitution)*
*Pi before cloud · Faith first*
