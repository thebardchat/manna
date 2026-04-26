# Expert Persona Review — Manna Pod Design v0.1

**Persona:** Lukens (systems engineering / requirements management / aerospace mechanisms)
**Background modeled:** 28+ years mechanical and systems engineering; NASA MSFC SE procedures
developer; Army UAS requirements management; SLS core stage program integration; X-33 /
X-37 / ISS flight mechanisms review; MBSE methodology; Cradle / IBM Rational DOORS; FCA/PCA
project engineering.  Active Secret Clearance.
**Document reviewed:** `docs/research/MANNA_POD_DESIGN_RESEARCH.md` v0.1 + `simulation/`
outputs (trajectory_sim.py, sweep.py) as of 2026-04-25.
**Review date:** 2026-04-25
**Protocol:** Persona Review Protocol v1.0

---

## Preamble

I am reading this as a systems engineer, not a physicist.  The Munk review already
covered the trajectory math errors adequately.  I won't repeat them, except where they
have direct SE process implications.  My job here is different: to determine whether
this concept is structured as an engineering program — or as a physics sketch that
happens to mention hardware.

My verdict after reading: the concept has genuine novelty and the author understands
the physics problem well enough to identify the right questions.  But the document is
missing every artifact a Pre-Phase A review board would require before approving work
to continue.  Eight issues are documented below.  Each is individually actionable.

---

## Issue 1 — No Concept of Operations (ConOps)

**Finding:**
The document describes a system but not a *mission*.  There is no Concept of Operations
document defining:

- Pre-launch state (who primes the rail? what is the loading sequence? weather constraints?)
- Launch event (trigger, commit criteria, abort authority)
- Ascent phase (autonomous pod or ground control? telemetry? command uplink?)
- Apogee event (what triggers tug capture attempt? go/no-go criteria?)
- Tug rendezvous (phasing orbit geometry, approach corridor, docking port definition)
- Contingency: pod misses tug (what happens to a 500 kg object at 4 km/s in LEO?)
- Disposal / deorbit concept for expended pods

**Why it matters:**
You cannot derive requirements without a ConOps.  The G-limits (100G, 5.5G, 2.5G),
mass fractions, structural requirements, interface loads — every one of these flows
down from the mission timeline.  Without a ConOps, the design has no authoritative
parent that the requirements trace to.  I've seen this exact gap kill Pre-Phase A
proposals at MSFC: reviewers ask "what is the mission?" and the team answers with
hardware specs.  Those are two different questions.

The question "what happens when a pod misses the tug?" is not a corner case — it is
a top-level safety requirement.  An uncontrolled 500 kg object in LEO is a space debris
event.  The Liability Convention (1972) makes the United States internationally
responsible for damage caused by space objects it launches.  This program cannot reach
Phase A without a debris mitigation plan, and a debris mitigation plan requires a ConOps.

**What is needed:**
Write a 3–5 page ConOps.  Include an event timeline with each phase named, stakeholders
identified, and go/no-go criteria for each phase transition.  The contingency branches
(missed tug, launch abort, pod structural failure) must appear in the first draft even
if the resolution is "TBD."  Tag every TBD explicitly.

---

## Issue 2 — Requirements Architecture Is Absent

**Finding:**
The document lists design parameters (mass, diameter, G-limit, launch velocity) but
does not define which of these are **requirements** (shall statements with verification
methods) versus **design decisions** (engineering choices that could have been made
differently).

Specifically:
- The 100G internal limit for Manna-H is stated as a design property, not a verified requirement.
  What standard does it trace to?  (MIL-STD-1540?  AIAA S-114?  ECSS-E-10-03?)
- The 78% payload mass fraction for Manna-H has no derivation.  Is this a requirement
  or a result?  If it is a requirement, what customer levied it?  If it is a result,
  what does the structural mass budget look like that produces 78%?
- The $200/kg mission target appears in the CLAUDE.md but not as a formal cost requirement
  with a production rate assumption and a development cost allocation.

**Why it matters:**
I wrote requirements management procedures for 17 NASA SE Engine sub-processes at MSFC.
The single most common failure mode in early concept development is confusing design
parameters with requirements.  When the design changes (and it will), untracked
requirements silently disappear.  The G-limits, mass fractions, and cost targets are
the most important numbers in this document — they need to be managed as requirements,
not as table entries.

This is also a Cradle/DOORS moment: every number in this document should be a tracked
object with a unique ID, a source, a rationale, and a verification method.  You don't
need the tool on day one, but you need the discipline.

**What is needed:**
Write a Requirements Traceability Matrix (RTM) stub — even a 20-row spreadsheet.
Each row: Requirement ID, Shall statement, Source (ConOps reference or customer),
Rationale, Verification Method (analysis / test / inspection / demonstration), and
Status.  The G-limits and mass fractions must appear as tracked requirements before
any simulation output is used to verify them.

---

## Issue 3 — Interface Control Documents (ICDs) Do Not Exist

**Finding:**
The Manna pod has at least two critical interface boundaries that are completely
undefined:

**Interface 1 — Rail to Pod (Launch End)**
- What force profile does the EM rail exert on the pod during acceleration?
- What is the launch vector uncertainty (angular error at rail exit)?
- What structural attach points exist between pod and rail?
- What is the mechanical and electrical disconnect sequence at launch?
- What connectors mate during loading?  (Power, telemetry, safing plugs)
- What is the maximum muzzle velocity uncertainty (ΔV at rail exit)?

**Interface 2 — Pod to Tug (Capture End)**
- What is the allowable misalignment tolerance for tug catch mechanism?
- What is the approach velocity corridor at apogee?
- What signals does the pod transmit for tug rendezvous?
- What structural loads does the capture mechanism impart on the pod?
- Is the pod reusable?  (ICD must define inspection requirements between uses)

**Why it matters:**
I reviewed flight mechanism interfaces on X-33, X-37, and ISS payloads at Jacobs /
NASA MSFC.  The rail-to-pod interface is the single highest-loaded mechanical event
in the mission (peak decel at launch: H-variant = 71 MPa dynamic pressure, equivalent
to 3,000+ g's on the structure in the first 0.1 seconds — per simulation output
2026-04-25).  Without a formal ICD, there is no structural specification for the pod
skin, no defined load path, and no basis for structural analysis.

The pod-to-tug interface defines the entire rendezvous architecture.  The v0.1 memo
says the pod "reaches the tug" — this is not an interface definition.  It is a
collision description.  Real rendezvous requires: matching state vectors at apogee,
defined approach corridor, communication protocol, and a catch mechanism that can
accommodate the dispersions in pod arrival state.

**What is needed:**
Produce ICD stubs for both interfaces.  A stub ICD is 1–2 pages per interface:
name the interface, list the mechanical, electrical, and RF parameters that must be
controlled, and tag each with [PLACEHOLDER] or [TBD].  An ICD stub with 20 TBDs
is infinitely more useful than no ICD.  It forces the right questions.

---

## Issue 4 — G-Loading Claims Have No Verification Path

**Finding:**
The three variants are differentiated primarily by internal G-tolerance:
- Manna-H: 100 G (bulk cargo)
- Manna-I: 5.5 G (electronics, instruments)
- Manna-B: 2.5 G (biologics, seedlings)

No verification method is defined for any of these limits.

**Why it matters:**
At NASA MSFC, G-tolerance requirements for payloads are verified by one of four methods:
analysis, test (centrifuge or drop tower), similarity (compare to verified heritage
design), or inspection.  For a novel cargo class like biologics in an EM-launched pod,
similarity may not exist.  Centrifuge testing of live plant seedlings at 2.5G for the
duration of rail acceleration (estimated < 1 second from simulation data) is technically
different from steady-state G tolerance — the shock response spectrum matters, not just
peak G.

For Manna-H at 100G: the rail acceleration pulse is not a constant 100G — it is a
time-varying load with a specific shock response spectrum.  Bulk liquids (water, fuel)
behave as hydrostatic loads under sustained acceleration but as sloshing dynamics under
a < 1 second impulse.  The 100G figure needs to be accompanied by a pulse duration and
a frequency spectrum before it means anything to a structural analyst.

Additionally, the simulation now shows peak stagnation heat flux of **1.15 GW/m²** for
Manna-H at launch (Sutton-Graves estimate, R_nose = 5 cm assumed [CONSTRAINT-NOT-MODELED]).
For comparison, Space Shuttle TPS was sized for ~500 kW/m² on the windward leading
edge at re-entry.  This is a load that would vaporize PICA-X in milliseconds.
The G-loading verification plan must also address the simultaneous thermal-mechanical
load environment, not G in isolation.

**What is needed:**
For each variant, define a verification matrix: G-limit → verification method →
responsible party → completion criteria.  Flag "test required" vs "analysis allowed"
for each.  The Manna-H thermal-mechanical combined load environment must be modeled
before any material selection is defensible.

---

## Issue 5 — Functional Architecture Is Undefined

**Finding:**
The document describes the pod as a physical object (mass, diameter, outer mold line)
but does not define its functional architecture.  Specifically, the following subsystems
are referenced but not decomposed:

- **Thermal Protection System (TPS)** — PICA-X cited for launch exit; now demonstrated
  to be inadequate at the required heat flux (§4 of this review).  What is the
  replacement candidate?  What are the TPS functional requirements?
- **Structural subsystem** — no structural concept (monocoque?  stringer-skin?
  truss-core?).  No reference to load paths.
- **Payload isolation subsystem** — the Manna-I and Manna-B liquid suspension concept
  is described (§5.3 of v0.1, disputed by Munk §7.5) but the isolation system is
  not part of a formal functional decomposition.
- **Navigation / Guidance** — none defined.  Does the pod have attitude control?
  Can it adjust trajectory after launch?  The simulation assumes a ballistic point
  mass — no GNC is modeled.
- **Communication** — does the pod transmit telemetry?  How does the tug locate it
  at apogee?  (Radar?  Optical?  Transponder?)
- **Power** — what powers the avionics (if any) during flight?

**Why it matters:**
Co-authoring an MBSE architecture methodology with SAIC taught me that functional
architecture decomposition is not optional even at Pre-Phase A — it is the tool that
reveals hidden requirements.  The GNC question above is a perfect example: if the pod
has no GNC, then the dispersion budget at apogee falls entirely on launch rail pointing
accuracy.  If rail pointing accuracy is ±0.01°, the apogee position uncertainty at
400 km altitude is on the order of ±70 km — far beyond any reasonable tug catch
window.  This is a critical requirement gap invisible without a functional decomposition.

**What is needed:**
Produce a one-page functional block diagram.  Boxes: TPS, Structure, Propulsion (none?),
GNC (none?), C&DH (if any), Comm (if any), Power (if any), Payload Isolation.  Draw
the interfaces between boxes.  Mark boxes with no design as "UNDEFINED."  The number
of "UNDEFINED" boxes is not a score — it is a scope list.

---

## Issue 6 — Architecture Does Not Close Against Requirements (Trajectory Gap)

**Finding:**
The trajectory simulation (now verified as of 2026-04-25) quantifies the architecture
closure gap:

| Variant  | v0.1 apogee claim | Sim apogee (30°, BC ~2k kg/m²) | Ratio |
|----------|-------------------|-------------------------------|-------|
| Manna-H  | 1,950 km         | 9.1 km                        | 0.005 |
| Manna-I  | 850 km           | 6.0 km                        | 0.007 |
| Manna-B  | 247 km           | 4.2 km                        | 0.017 |

The parametric sweep shows that to reach 100 km (Kármán line) with Manna-H's launch
velocity, the pod requires BC ≥ ~5,000 kg/m² at steep elevation angles (75–85°).
Current Manna-H BC is ~2,264 kg/m².  To approach orbital insertion velocity at apogee,
BC ≥ 50,000 kg/m² is required (sweep finding: vx/v_circ = 1.05 at BC=50,000, elev=30°).

This is not a simulation anomaly.  This is an architectural failure at the system level.

**Why it matters:**
In the NASA SE process I wrote at MSFC, a System Requirements Review (SRR) is the
gate that confirms the requirements baseline is achievable before committing design
resources.  The trajectory gap above is an SRR failure: the system's defined parameters
cannot produce the required performance.  The gap is not 10% or 20% — it is 200× in
apogee altitude for the H variant.

From a program management perspective, this means the Pre-Phase A work has identified
a fundamental feasibility question that must be resolved before any Phase A funding is
justified.  The question is: can a cargo pod structure simultaneously achieve (a) the
BC required to escape the atmosphere, and (b) the cargo protection required by the G-
limits?

To achieve BC = 50,000 kg/m² with cd0 = 0.4:
  mass = BC × cd0 × area = 50,000 × 0.4 × 0.126 m² (for 0.4m dia) = 2,520 kg

A 2,520 kg pod with 0.4m diameter and mass fraction 78% carries only 1,965 kg of
payload — but the pod shell itself must be extremely dense (>19,000 kg/m³ for a
solid cylinder, approaching osmium density) to achieve the required BC with this
geometry.  This is not a conventional structure.

**What is needed:**
Before any further design work: run a BC feasibility study.  For each variant:
(1) define the required BC to meet the apogee requirement,
(2) derive the structural mass required to achieve that BC for a given geometry,
(3) compute the resulting payload mass fraction,
(4) determine whether any known material can produce the required BC while meeting
    the structural loads.
If this study cannot close, the mission concept requires a different approach — such
as a staged-burn upper stage on the pod, or a lower but achievable apogee with a
waiting tug in a highly elliptical orbit.

---

## Issue 7 — Safety Architecture Is Missing

**Finding:**
The document contains no safety analysis artifacts.  The following are absent:

- Failure Modes and Effects Analysis (FMEA) — what fails, what is the effect,
  what is the detection method, what is the criticality?
- Mission Hazard Analysis — the hazards to ground personnel, the launch corridor,
  and the air traffic in the trajectory footprint are not assessed
- Malfunction Turn Analysis — if the pod launches with an off-nominal velocity vector,
  what is the resulting impact footprint?  Does it intersect populated areas?
- Space Debris Compliance — what is the pod's orbit lifetime if it reaches orbital
  altitude but the tug misses?  Does it comply with the 25-year deorbit rule?
  (Orbital Debris Mitigation Standard Practices, NASA-STD-8719.14)

**Why it matters:**
I co-generated a Mission Hazard Report for the International Space Welding Experiment
at Jacobs/MSFC.  I can tell you from experience: the FAA and Range Safety will not
issue a launch license for any electromagnetic launch system without a complete Malfunction
Turn Analysis and a range safety compliance demonstration.  This is not a regulatory
hurdle to clear later — it is a feasibility gate.  A system that cannot demonstrate safe
failure modes in the launch corridor cannot operate from a ground site in the continental
United States.

The 100G Manna-H case is also a safety concern at the launch end.  If the pod
structurally fails during rail acceleration (brittle fracture of a dense structural
shell under impulse loading), the energy released is catastrophic at ground level.
This requires a Fracture Control Plan, which is a NASA requirement for all flight
hardware (NASA-STD-5019).

**What is needed:**
Three deliverables before Phase A:
1. Preliminary FMEA (top-level only — identify single-point failures with catastrophic
   or critical consequences)
2. Malfunction Turn Analysis (worst-case off-nominal launch angles and resulting
   ground impact footprint)
3. Space debris compliance assessment (orbit lifetime at max credible apogee for each
   variant)

---

## Issue 8 — Technology Readiness Levels Not Assessed

**Finding:**
No Technology Readiness Level (TRL) assessment is provided for any component of the
Manna system.  Based on available information:

| Subsystem | Estimated Current TRL | Assessment |
|-----------|----------------------|------------|
| EM rail (coilgun/railgun at required scale) | TRL 3–4 | Small-scale rail demonstrators exist; multi-km, km/s-class systems are not demonstrated |
| TPS for EM launch exit profile (1+ GW/m²) | TRL 1–2 | No known material tested at this heat flux for exit (entry TPS is better-understood) |
| Liquid suspension isolation (Manna-I/B) | TRL 2–3 | FC-770-based liquid isolation at 5–100G, < 1 s pulse duration: not demonstrated |
| Pod capture mechanism (tug end) | TRL 1–2 | No tug design exists; no capture mechanism defined |
| Integrated pod structure (for required BC) | TRL 1 | No structural concept proven capable of BC = 5,000–50,000 kg/m² |

**Why it matters:**
NASA's Technology Readiness Assessment (TRA) process (NPR 7120.8) is the standard tool
for identifying which subsystems require technology maturation funding before they can
support a Phase A design.  The TRL assessment above shows that **every major subsystem
is below TRL 4** — meaning none have been demonstrated in a relevant environment.  This
is normal for Pre-Phase A work, but it must be documented.

A common failure mode I have observed: programs proceed to Phase A with TRL 3 subsystems
and then discover — at Preliminary Design Review (PDR) — that the critical technology
does not mature on schedule.  The resulting schedule slip and cost growth are avoidable
if the technology maturation paths are identified and resourced at Pre-Phase A.

The EM rail is the highest-risk item.  The existing BGKPJR-Core-Simulations work
presumably addresses this, but the maturation path from that simulation work to a
28.7 km rail capable of 10,822 m/s exit velocity has not been described in terms of
technology demonstrations required, cost, and schedule.

**What is needed:**
Produce a TRL matrix for all major subsystems.  For each subsystem below TRL 6, define:
(1) the technology demonstration required to reach TRL 6,
(2) estimated duration and cost of that demonstration,
(3) which Phase dependency it gates.
This is the input to the Technology Development Plan — the document that convinces a
program sponsor that the risks are understood and funded.

---

## Summary Table

| # | Issue | Severity | SE Phase Gate | Blocking? |
|---|-------|----------|---------------|-----------|
| 1 | No ConOps | High | Pre-Phase A | Yes — requirements cannot be derived |
| 2 | No requirements architecture / RTM | High | Pre-Phase A | Yes — design has no traceability baseline |
| 3 | No ICDs (rail-to-pod, pod-to-tug) | High | Pre-Phase A / SRR | Yes — structural analysis impossible without load definition |
| 4 | G-loading claims have no verification path | Medium | SRR | Yes — requirement is untestable as stated |
| 5 | Functional architecture undefined | High | Pre-Phase A | Yes — subsystem requirements cannot be derived |
| 6 | Architecture doesn't close (200× trajectory gap) | Critical | Pre-Phase A feasibility | Yes — fundamental feasibility undemonstrated |
| 7 | Safety architecture missing | High | Pre-Phase A / launch license | Yes — range safety gate |
| 8 | TRL not assessed | Medium | Pre-Phase A | No — but increases Phase A cost and schedule risk |

**Eight issues.  Six are Pre-Phase A blockers.**

---

## Recommended Next Actions (Priority Order)

1. **ConOps draft** — 3–5 pages, mission timeline, stakeholders, go/no-go criteria.
   Drives everything else.  Write this first.

2. **BC feasibility study** — Can the architecture physically close?  If not, the
   concept needs a different mission profile.  This is the existential question.

3. **Functional block diagram** — One page.  Reveal the hidden requirements before
   spending design time on subsystems that may be redefined.

4. **Safety prelim** — Malfunction Turn Analysis for the launch corridor.  Without this,
   no site selection is possible.

5. **TRL matrix** — 1–2 pages.  Identifies where technology investment is needed.

6. **ICD stubs** — 2 × 1–2 pages.  Rail-to-pod and pod-to-tug.  Even 20 TBDs per
   interface is sufficient to drive the right conversations.

7. **RTM stub** — 20 rows minimum.  G-limits, mass fractions, apogee requirements,
   cost target.  Track them as requirements from this point forward.

---

## Closing Note

The underlying concept — EM-launched cargo pods caught by an orbital tug — is
architecturally sound as a long-term vision.  The trajectory simulator work is
legitimate first-principles physics, done correctly.  The forensic quality gate applied
by the Munk review is exactly the right process.

What the program needs now is systems engineering structure.  The physics questions
will not resolve cleanly until the requirements are defined, the interfaces are controlled,
and the feasibility gap is honestly characterized.  Pre-Phase A is the right time to
face all of this.

The simulation finding that BC must increase 20–30× to close the trajectory gap is not
a failure of the concept — it is the concept doing its job, which is to tell you the
truth about what the physics requires.  Every major launch system in history has gone
through a version of this moment.

---

*Review conducted per Persona Review Protocol v1.0.*
*Persona: Lukens (systems engineering / requirements management / aerospace mechanisms)*
*Session: 2026-04-25 | Shane Brazelton + Claude (Anthropic)*
