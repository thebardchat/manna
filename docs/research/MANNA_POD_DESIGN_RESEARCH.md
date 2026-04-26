# Manna pod design — concept memorandum v0.2

> **MATURITY STATEMENT — READ BEFORE CITING**
> This document is a **Pre-Phase A concept memorandum**.  Numbers are
> estimates, derivations, and placeholders unless tagged `[VERIFIED]`.
> v0.2 integrates two forensic reviews (Munk persona and Lukens persona)
> and the first atmospheric trajectory simulation.  It is **not** ready
> for external distribution or patent filing.  See `expert-reviews/` for
> full review transcripts.

*Author: Shane Brazelton + Claude (Anthropic) | v0.2 | 2026-04-25*
*Supersedes: v0.1 (2026-04-24) — forensic issues incorporated below*

---

## 1  Concept summary

The Manna system is an electromagnetic mass-driver cargo pod family,
designed to be launched from the BGKPJR ground-based maglev rail
(Hazel Green, AL) to a suborbital trajectory, caught by a reusable
orbital Tug at apogee, and ferried to a Lunar Base.

**Three variants. Always.**

| Variant  | Cargo class                         | G limit | Mass   | Body diam | Target per-kg cost |
|----------|-------------------------------------|---------|--------|-----------|--------------------|
| Manna-H  | Bulk: water, propellant, food, metals | 100 G | 800 kg | 1.00 m    | $54/kg [PLACEHOLDER] |
| Manna-I  | Electronics, instruments, mech spares | 5.5 G | 250 kg | 0.65 m    | $467/kg [PLACEHOLDER] |
| Manna-B  | Biologics, seedlings, sensitive liquids | 2.5 G | 80 kg | 0.40 m   | $4,190/kg [PLACEHOLDER] |

> All mass, diameter, G-limit, and cost figures are `[ESTIMATE]` or
> `[PLACEHOLDER]` unless otherwise tagged.  Do not use in a patent
> application or external proposal without running each number through
> a formal verification pass.

---

## 2  Launch architecture

```
BGKPJR rail (28.7 km, 15–45° incline, Hazel Green AL, 34.93°N)
  │
  │  electromagnetic acceleration
  ▼
Manna pod exits rail at hypersonic velocity
  │
  │  ballistic suborbital arc — drag and gravity
  ▼
Tug (in matched ~35° inclination orbit) ← REFERENCE CONCEPT NOT YET BUILT
  │
  │  phasing rendezvous at apogee (<1 m/s closing rate)
  ▼
Lunar transfer insertion
  │
  ▼
Lunar Base (out of scope for this repo)
```

Key parameters (30° elevation nominal case):

| Parameter | Manna-B | Manna-I | Manna-H | Tag |
|-----------|---------|---------|---------|-----|
| Launch velocity | 4,319 m/s | 7,670 m/s | 10,823 m/s | [DERIVED] |
| Rail elevation (nominal) | 30° | 30° | 30° | [ESTIMATE] |
| Launch latitude | 34.93°N | 34.93°N | 34.93°N | [VERIFIED] |
| v0.1 claimed apogee (vacuum) | 247 km | 850 km | 1,950 km | ⚠ [SUPERSEDED] |
| **Simulated apogee (30°, atm)** | **4.2 km** | **6.0 km** | **9.1 km** | **[DERIVED — sim]** |
| Apogee overestimate (v0.1 / sim) | ~59× | ~142× | ~214× | [DERIVED] |
| Sea-level dynamic pressure | 11.4 MPa | 36.0 MPa | 71.7 MPa | [DERIVED] |
| Sea-level drag deceleration | 732 g | 2,047 g | 3,231 g | [DERIVED] |

> ⚠ **Finding (2026-04-25):** The v0.1 apogee claims were computed with
> a vacuum constant-g parabolic formula.  Atmospheric simulation (RK4,
> US Std Atm 1976, dt=0.1 s) shows all three variants are stopped by
> drag in the lower troposphere (<11 km AGL).  The v0.1 numbers are
> physically unrealizable with the current pod geometry.
> See `simulation/src/trajectory_sim.py` for the authoritative model.

---

## 3  Trajectory analysis — v0.2 corrected

### 3.1  v0.1 formula (invalid — documented for traceability)

v0.1 used the closed-form constant-gravity vacuum parabolic equation:

```
h_apogee = (v_launch × sin θ)² / (2 × g₀)
```

with g₀ = 9.80665 m/s² constant, no atmosphere.  This is appropriate
only for low-velocity, low-altitude projectiles in vacuum.  It is not
valid for hypersonic velocities in the real atmosphere.

### 3.2  Atmospheric simulation results  [DERIVED — simulation]

Simulation: 3-DOF RK4 integrator, US Standard Atmosphere 1976, Mach-
dependent drag coefficient correction, dt=0.1 s adaptive sub-stepping.
Source: `simulation/src/trajectory_sim.py`.

All three variants at 30° elevation, full atmospheric drag:

```
Variant   v_launch   BC       Sim apogee   Max Mach   Max-Q alt   Status
Manna-B   4,319 m/s  1,592    4.2 km       12.7       ~1.2 km     Stopped in troposphere
Manna-I   7,670 m/s  1,794    6.0 km       22.5       ~1.4 km     Stopped in troposphere
Manna-H   10,823 m/s 2,264    9.1 km       31.8       ~1.6 km     Stopped in troposphere
```

No variant approaches the Kármán line (100 km).  None achieves orbital
velocity at apogee.

### 3.3  Ballistic coefficient (BC) feasibility gap  [DERIVED — sweep]

A parametric sweep of BC (1,000–50,000 kg/m²) × elevation (15°–85°)
was run for all three variants (108 simulations total).  Source:
`simulation/src/sweep.py`.

Key findings:

| Milestone | Required BC | Required elevation | Current BC | Gap factor |
|-----------|-------------|-------------------|------------|------------|
| Kármán line (100 km) | ≥5,000 kg/m² | 75–85° | 1,592–2,264 | 2–3× BC + steep angle |
| Orbital velocity at apogee | ≥50,000 kg/m² | 30–45° | 1,592–2,264 | 20–30× |

**Architecture conclusion:** Current pod geometry cannot reach the
operational apogee.  Three paths forward (not mutually exclusive):
1. **Evacuated launch tube** — eliminate sea-level drag, most leverage
2. **High-altitude rail site** — reduce atmospheric column traversed
3. **Radical BC increase** — BC=50,000 at d=0.40 m requires mass=1,005 kg for Manna-B (not feasible with current sizing); requires structural redesign

### 3.4  Inclination constraint  [ARCHITECTURE ISSUE]

Hazel Green rail (34.93°N) cannot reach equatorial LEO without a plane-
change ΔV of approximately 4.6 km/s.  This exceeds a reasonable Tug
delta-v budget.

**Fix (selected):** Tug operates in a matched ~35°-inclination orbit,
analogous to Cape Canaveral launches to 28.5° inclination ISS orbit.
Re-derivation of Tug ΔV budget is required.  `[PENDING]`

---

## 4  Thermal protection — stagnation heating  [CONSTRAINT-NOT-MODELED]

### 4.1  Sutton-Graves stagnation heat flux  [DERIVED — simulation]

```
q̇ = K × √(ρ / R_nose) × v³
K = 1.83×10⁻⁴ W·s³/(kg^0.5·m^0.5)   [Sutton & Graves 1959]
R_nose = 0.05 m (assumed)  [ESTIMATE]
```

Peak stagnation heat flux at launch (sea-level, hypersonic exit):

| Variant | Peak heat flux | Condition |
|---------|----------------|-----------|
| Manna-B | 0.07 GW/m² | v=4,319 m/s, ρ=1.225 kg/m³ |
| Manna-I | 0.41 GW/m² | v=7,670 m/s, ρ=1.225 kg/m³ |
| Manna-H | 1.15 GW/m² | v=10,823 m/s, ρ=1.225 kg/m³ |

> ⚠ 1.15 GW/m² for Manna-H is catastrophic.  For reference, Space
> Shuttle peak entry heating was ~0.06 GW/m².  Manna-H at sea-level
> launch exit is ~19× hotter.  PICA-X ablative limits are ~1 MW/m²
> sustained.  This constraint is not currently modeled in the trajectory
> simulator — pod would not survive the exit in current configuration.
> [CONSTRAINT-NOT-MODELED — requires NASA DPLR/LAURA + FIAT analysis]

### 4.2  PICA-X application error (Munk review issue #4)

v0.1 cited 70° sphere-cone with PICA-X from Apollo/MSL entry heritage.
Entry and exit are reversed thermal environments:
- **Entry:** high velocity → atmosphere compresses → peak heating early
- **Exit (launch):** low velocity at surface → peak velocity when dense air is passed

The exit heating profile must be computed separately.  PICA-X geometry
is probably still correct; TPS thickness calculation must be redone for
the exit trajectory.  `[PENDING: NASA DPLR + FIAT analysis]`

---

## 5  Shock isolation — Manna-B  [UNDER REVISION]

### 5.1  Requirement

Manna-B cargo (biologics, seedlings) must survive 2.5G maximum.
Rail launch imposes the full launch acceleration profile plus vibration.

### 5.2  Liquid suspension medium

v0.1 proposed a density-matched liquid suspension medium.  The v0.1
density claim (15 g/cm³) was flagged by the Munk review:

> No commercially available suspension fluid exceeds ~4 g/cm³.
> Mercury (13.6 g/cm³) is toxic and impractical.  The 15 g/cm³ figure
> appears to be a transcription or calculation error.

FC-770 (3M fluorinert, 1.79 g/cm³) is a practical candidate.  For
biological cells with density ~1.05 g/cm³ suspended in FC-770:

```
Density mismatch ratio:  1.79 / 1.05 = 1.70
Theoretical G attenuation ≈ 2.4× at this mismatch  [ESTIMATE — needs full derivation]
```

v0.1 claimed 3–4× attenuation via an internally inconsistent equation.
The correct derivation gives ~2.4× for the FC-770 / cell-mass combination.
Whether 2.4× is sufficient to protect 2.5G cargo from 100–800G rail
launch requires a complete isolation trade study.  `[PENDING]`

---

## 6  Systems engineering gaps  [FROM LUKENS PERSONA REVIEW]

The Lukens persona review (Scott Lukens, 28+ yr systems engineer, NASA
MSFC, Boeing SLS) identified the following gaps as Pre-Phase A blockers:

| Issue | Severity | SE Phase gate | Status |
|-------|----------|---------------|--------|
| No ConOps document | HIGH | Pre-Phase A | OPEN |
| No requirements architecture / RTM | HIGH | Pre-Phase A | OPEN |
| No Interface Control Documents (rail-to-pod, pod-to-Tug) | HIGH | MDR | OPEN |
| G-loading claims unverified structurally | MEDIUM | Pre-Phase A | OPEN |
| No functional block diagram | HIGH | Pre-Phase A | OPEN |
| BC trajectory gap 200× (architecture doesn't close) | CRITICAL | Pre-Phase A | PARTIALLY ADDRESSED (§3.3) |
| No safety architecture (FMEA, malfunction-turn) | HIGH | Pre-Phase A | OPEN |
| TRL not assessed for any subsystem | MEDIUM | Pre-Phase A | OPEN |

See `expert-reviews/manna-pod-design-persona-lukens-v0.1.md` for the
full review transcript.

---

## 7  Cost model  [PLACEHOLDER]

v0.1 cited $54/kg, $467/kg, $4,190/kg for H/I/B respectively.

> ⚠ No derivation, mass fraction, power budget, or amortization model
> supports these figures.  They are order-of-magnitude guesses.
>
> Real per-kg cost requires:
> - Separated marginal / operational / allocated capital cost models
> - Production-rate sensitivity analysis
> - Comparison to CLPS benchmark ($1M–$3M/kg current lunar delivery)
>
> All cost figures remain `[PLACEHOLDER]` until costed.

---

## 8  Concept art

An AI-generated concept illustration of the three Manna variants is
available in `design/concept-art/manna-variants-concept-v1.webp`.

> ⚠ **Known text error in image:** The red (Manna-H) pod is labeled
> "DAINA-H" in the generated image — an AI text hallucination.  The
> correct designation is Manna-H.  Image is for visual concept reference
> only, not for external distribution.

---

## 9  Open issues tracker (v0.2)

| # | Issue | Source | Priority | Status |
|---|-------|---------|----------|--------|
| 1 | Trajectory: real apogees 59–214× below v0.1 claims | Munk / Sim | CRITICAL | ✅ Confirmed |
| 2 | BC feasibility gap: need 20–30× increase for orbital | Sim sweep | CRITICAL | ✅ Quantified |
| 3 | 35°N → equatorial plane change not budgeted | Munk #2 | HIGH | 🔵 Fix selected (§3.4) |
| 4 | Tug rendezvous architecture undefined | Munk #3 | HIGH | OPEN |
| 5 | TPS exit heating: PICA-X sizing unverified | Munk #4 | HIGH | 🔵 Heat flux quantified (§4) |
| 6 | Liquid suspension density error (15 g/cc) | Munk #5 | MEDIUM | 🔵 Redesign started (§5) |
| 7 | No ConOps | Lukens #1 | HIGH | OPEN |
| 8 | No requirements / RTM | Lukens #2 | HIGH | OPEN |
| 9 | No ICDs | Lukens #3 | HIGH | OPEN |
| 10 | No functional block diagram | Lukens #5 | HIGH | OPEN |
| 11 | Safety architecture missing | Lukens #7 | HIGH | OPEN |
| 12 | Fabricated citations in v0.1 | Munk #6 | HIGH | ✅ Stripped |
| 13 | Cost figures not derived | Munk #7 | MEDIUM | OPEN |
| 14 | TRL not assessed | Lukens #8 | MEDIUM | OPEN |

---

## 10  References

### Verified references

- U.S. Standard Atmosphere, 1976. NOAA/NASA/USAF. Washington D.C.  [VERIFIED]
- Sutton, K. and Graves, R.A. (1971). *A General Stagnation-Point
  Convective Heating Equation for Arbitrary Gas Mixtures.* NASA TR R-376.  [VERIFIED]
- Humble, R.W., Henry, G.N., Larson, W.J. (1995). *Space Propulsion
  Analysis and Design.* McGraw-Hill.  [VERIFIED]
- Wertz, J.R., Everett, D.F., Puschell, J.J. (2011). *Space Mission
  Engineering: The New SMAD.* Microcosm Press.  [VERIFIED]
- BGKPJR-Core-Simulations repo (rail specs): github.com/thebardchat/BGKPJR-Core-Simulations  [VERIFIED]

### Citations pending verification

*The following were cited in v0.1 and stripped pending verification.
Do not re-add until web-fetched from NASA NTRS, ADS, or established
peer-reviewed source.*

- Any entry from the v0.1 References section not listed above is removed.
- CLPS cost benchmark ($1M–$3M/kg): cited from NASA press releases —
  needs NTRS or GAO report citation before formal use.

---

*v0.2 produced: 2026-04-25.  Trajectory simulation complete.*
*v0.3 planned: add ConOps draft, ICD stubs, Tug reference concept.*
