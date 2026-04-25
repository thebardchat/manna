# Expert Persona Review — Manna Pod Design v0.1

**Persona:** Munk (astrodynamics / applied physics reviewer)
**Document reviewed:** `docs/research/MANNA_POD_DESIGN_RESEARCH.md` v0.1
**Review date:** 2026-04-24
**Protocol:** Persona Review Protocol v1.0

---

## Preamble

I am reviewing this document as an adversarial technical peer — my job is to find
errors, not to celebrate the concept.  Seven issues are documented below.  Each is
individually actionable.

---

## Issue 1 — Trajectory Math Broken

**Finding:**
The v0.1 apogee claims (247 km, 850 km, 1950 km) were derived using:

```
h = (v_launch × sin θ)² / (2 × g₀)
```

with g₀ = 9.80665 m/s² (constant, sea-level value) and no atmospheric drag.

**Why it matters:**
1. Gravity decreases with altitude; constant-g overestimates drag-free apogees by
   up to 10–20% at 200+ km.
2. No drag model.  These pods will fly through the full atmosphere at hypersonic
   speeds (M 12–32).  Dynamic pressure at sea level for Manna-B at 4,318 m/s
   exceeds 11 MPa — enormous drag.  Real apogees are significantly lower.

**Resolution needed:**
Run a validated 3-DOF ballistic integrator with US Standard Atmosphere 1976 drag
and altitude-varying gravity.  Publish results.  Discard all v0.1 apogee numbers.

---

## Issue 2 — 35°N to Equatorial LEO Inconsistency

**Finding:**
v0.1 states the launch site is at 35°N latitude and the delivery target is equatorial
(0° inclination) LEO.

**Why it matters:**
Launching from 35°N produces a trajectory with a minimum orbital inclination of 35°.
Changing from a 35° inclined orbit to equatorial requires a Hohmann plane change with
ΔV ≈ 2 × v_orbit × sin(Δi/2) ≈ 2 × 7.8 × sin(17.5°) ≈ 4.7 km/s.  This is larger
than most LEO insertion burns.  This maneuver is not described, not budgeted, and
apparently not known to the v0.1 authors.

**Resolution needed:**
Either accept an inclined orbit matching launch latitude, relocate the launch site to
near-equatorial, or fully budget the plane-change ΔV and its propellant mass.

---

## Issue 3 — Capture vs. Impact Velocity Confusion

**Finding:**
v0.1 uses launch velocity figures to derive both "suborbital delivery" trajectories
and "LEO capture" scenarios without distinguishing the two.  Manna-H at 10,814 m/s
(total) has horizontal component 9,363 m/s, which exceeds circular orbital velocity
(~7,905 m/s at sea level).  v0.1 treats this as a suborbital ballistic hop.

**Why it matters:**
A vehicle with horizontal velocity > circular orbital velocity does not follow a
ballistic hop.  It enters an orbit (or escapes, depending on total energy).  The
delivery scenario (landing at a target after a ballistic arc) is physically impossible
at those velocities without a deceleration burn.  The paper conflates:
- Ballistic delivery (no propulsion after launch, must be subsonic enough at terminal
  to land or be decelerated)
- Orbital delivery (requires circularisation burn + deorbit + re-entry)

**Resolution needed:**
Bifurcate the design into two regimes and treat each separately.  The trajectory
simulator will flag when horizontal velocity exceeds orbital velocity.

---

## Issue 4 — PICA-X Exit Application Error

**Finding:**
v0.1 proposes PICA-X ablative heat shielding for the launch (exit) trajectory,
citing SpaceX Dragon heritage.

**Why it matters:**
PICA-X is optimised for **entry** (inbound): high velocity, long duration, large
heat-flux integration.  On launch exit, the vehicle accelerates through the
atmosphere (residence time ~1–5 seconds at hypersonic speeds).  The dominant concern
is stagnation-point heating over a short duration, not ablative mass loss.  PICA-X is
heavy, expensive, and almost certainly over-engineered for exit.  A metallic nose cap
or lightweight ceramic may suffice — but no analysis has been done.

**Resolution needed:**
Compute stagnation-point heat flux Q_s = k × ρ^0.5 × v³ for the exit trajectory.
Integrate over time to get total heat load per unit area.  Compare to candidate
materials.  Then select a thermal protection system.

---

## Issue 5 — Liquid Suspension Density Math Error

**Finding:**
v0.1 proposes an internal liquid suspension medium at "15 g/cc" (15,000 kg/m³) for
cargo shock isolation during EM launch acceleration.

**Why it matters:**
No practical liquid has a density of 15 g/cc.  For reference:
- Water: 1.0 g/cc
- Mercury: 13.6 g/cc (toxic, impractical)
- Gallium: ~6.1 g/cc
- Osmium (heaviest metal, solid): 22.6 g/cc

A 15 g/cc suspension fluid would dominate the pod's mass fraction.  The figure is
almost certainly wrong — likely a decimal error or unit confusion (perhaps 1.5 g/cc
was intended, which is achievable with dense polymer suspensions).

**Resolution needed:**
Re-derive the required density from the G-load and desired damping ratio.  Select a
real fluid.  Re-run the mass budget.

---

## Issue 6 — Fabricated Citations

**Finding:**
Three of the seven references in v0.1 were checked against peer-reviewed databases
(NASA ADS, Google Scholar, Semantic Scholar) and could not be verified.  Two appear
to be plausible-sounding fabrications (correct author name format, plausible journal
names, but no matching records found).

**Why it matters:**
Fabricated citations undermine all quantitative claims that relied on them.  Any
numerical value sourced from a non-existent paper must be treated as [PLACEHOLDER].

**Resolution needed:**
Remove all unverified citations immediately.  Do not replace with similar-sounding
alternatives.  Use real sources or explicitly label claims [ESTIMATE] / [PLACEHOLDER].

---

## Issue 7 — Undefined Cost Models

**Finding:**
v0.1 claims a delivery cost of $80–$240/kg for suborbital apogee.  No derivation,
power budget, amortisation schedule, or mass fraction analysis supports this figure.

**Why it matters:**
Cost credibility is the project's primary value proposition.  Without a cost model,
the figures are meaningless.  The range "$80–$240/kg" spans a 3× factor, which
indicates the authors have no confidence bound either.

**Resolution needed:**
Build a cost model that includes at minimum: EM rail capital cost amortised over N
launches, energy cost per launch (kWh × utility rate), pod fabrication cost,
operations cost.  Divide by payload kg.  Only then can a $/kg figure be published.

---

## Summary

| # | Issue                         | Severity | Status   |
|---|-------------------------------|----------|----------|
| 1 | Trajectory math broken        | Critical | Open     |
| 2 | 35°N → equatorial inconsistency | High   | Open     |
| 3 | Capture vs. impact confusion  | High     | Open     |
| 4 | PICA-X exit application error | Medium   | Open     |
| 5 | Liquid suspension density     | Medium   | Open     |
| 6 | Fabricated citations          | High     | Partial  |
| 7 | Undefined cost models         | Medium   | Open     |

*Issue #6 is marked Partial because citations have been removed from the document;
real replacements are not yet provided.*

---

*Review conducted under Persona Review Protocol v1.0.  Signed: Munk persona,
2026-04-24.*
