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

### 3.3  Ballistic coefficient (BC) feasibility study  [DERIVED — simulation]

Sources: `simulation/src/sweep.py` (108-run parametric sweep),
`simulation/src/bc_feasibility.py` (per-variant feasibility analysis,
30° elevation, cd0=0.40, dt=0.5 s).

**Minimum BC required per variant and milestone (30° elevation):**

| Variant | Kármán line (100 km) | Half orbital v | Full orbital v |
|---------|---------------------|----------------|----------------|
| Manna-B (d=0.40 m) | 30,000 kg/m² (18.8×) | Not achievable | Not achievable |
| Manna-I (d=0.65 m) | 10,000 kg/m² (5.6×) | 20,000 kg/m² (11.1×) | Not achievable |
| Manna-H (d=1.00 m) |  7,500 kg/m² (3.3×) | 15,000 kg/m² (6.6×)  | 50,000 kg/m² (22.1×) |

**Required pod mass and payload fraction at each milestone:**

| Variant | Milestone | Required BC | Total pod mass | Payload fraction | Min material |
|---------|-----------|-------------|----------------|------------------|--------------|
| Manna-B | Kármán | 30,000 | 1,508 kg | 5.3% | Steel 4340 |
| Manna-I | Kármán | 10,000 | 1,327 kg | 18.8% | Aluminum 7075 |
| Manna-I | Half orbital | 20,000 | 2,655 kg | 9.4% | Titanium Ti-6Al-4V |
| Manna-H | Kármán | 7,500 | 2,356 kg | 34.0% | Aluminum 7075 |
| Manna-H | Half orbital | 15,000 | 4,712 kg | 17.0% | Aluminum 7075 |
| Manna-H | Full orbital | 50,000 | 15,708 kg | 5.1% | Steel 4340 |

> ⚠ **Finding (2026-04-28):** Materials are not the blocking constraint — payload fraction is.
> - The current 78% mass fraction target is unreachable at any useful apogee.
> - Manna-H at full orbital insertion requires 15,708 kg total and delivers
>   only 5.1% payload — the economics completely break vs. the $54/kg target.
> - Manna-B cannot reach orbital velocity at any BC achievable with 30° launch —
>   the launch velocity (4,319 m/s) is insufficient.
> See `simulation/data/trajectory_runs/bc_feasibility.png` for visualizations.
> [DERIVED — simulation/src/bc_feasibility.py]

**Architecture conclusion:** Current pod geometry cannot reach operational
apogee at viable payload fractions.  Three paths forward (not mutually exclusive):

1. **Evacuated launch tube** — eliminate sea-level drag entirely; most
   leverage, requires tube infrastructure alongside rail
2. **High-altitude rail terminus** — reduce atmosphere traversed; depends
   on BGKPJR terrain options
3. **Lower apogee + elliptical Tug orbit** — accept 100–200 km apogee,
   park Tug in a highly elliptical orbit with apogee at that altitude;
   re-derive Tug ΔV budget accordingly; most architecturally conservative

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

### 5.2  Liquid suspension medium — corrected derivation  [DERIVED]

v0.1 proposed a density-matched liquid suspension medium.  Two errors
were identified by the Munk persona review:

1. **Density error:** v0.1 cited 15 g/cm³ for the suspension fluid.
   No commercially available fluid exceeds ~4 g/cm³.  Mercury (13.6 g/cm³)
   is toxic and excluded.  The 15 g/cm³ figure was a calculation error.

2. **Attenuation equation inconsistency:** v0.1's equation produced
   50× attenuation at 2% density mismatch but claimed 3–4× for the
   large-mismatch FC-770 case.  These are inconsistent with each other
   and neither was derived from first principles.

**Correct derivation:**

Consider a biological cell (density ρ_c) immersed in a suspension fluid
(density ρ_f) inside a closed container that accelerates at rate a.

In the accelerating pod frame, each fluid parcel of volume δV experiences
an inertial pseudo-force ρ_f·δV·a.  The resulting pressure field satisfies:

```
dP/dx = ρ_f × a       (pressure increases opposite to acceleration direction)
```

For a spherical cell of volume V = (4/3)πr³, the net pressure force
(buoyancy) acting on the cell is:

```
F_buoy = ρ_f × V × a   (in the acceleration direction)
```

The net mechanical load on the cell structure (the force the cell walls
must resist) equals the inertial load minus buoyancy:

```
F_net = ρ_c × V × a  −  ρ_f × V × a  =  (ρ_c − ρ_f) × V × a
```

The effective acceleration experienced by the cell (normalized to cell mass):

```
a_eff = F_net / (ρ_c × V)  =  (1 − ρ_f/ρ_c) × a
```

**Attenuation factor** = a_applied / |a_eff|:

```
Attenuation  =  ρ_c / |ρ_c − ρ_f|
```

For FC-770 (ρ_f = 1.79 g/cm³) and biological cells (ρ_c = 1.05 g/cm³):

```
Attenuation  =  1.05 / |1.05 − 1.79|  =  1.05 / 0.74  =  1.42×   [DERIVED]
```

Note: since ρ_f > ρ_c, the buoyancy force *exceeds* the cell's inertial
load — the cell floats *toward* the front wall rather than the back wall.
The net mechanical load is in the opposite direction to the pod acceleration,
at 1.42× reduced magnitude compared to unsupported flight.

**Comparison to v0.1 claims:**

| Source | Attenuation for FC-770/cell | Method |
|--------|----------------------------|--------|
| v0.1 equation (50× at 2% mismatch) | ~1.4× (using same formula) | ρ_c/|Δρ|, inconsistently applied |
| v0.1 text claim | 3–4× | No derivation |
| This derivation (v0.2) | **1.42×** | First-principles buoyancy [DERIVED] |

**Design implication:**  1.42× attenuation is grossly insufficient.
To protect cargo at 2.5G, a rail acceleration of ~100G (Manna-B launch)
would still impose ~70G on the cell structure after suspension.  A single
liquid suspension layer cannot close the gap.

**Required isolation:**  A multi-stage isolation system is needed.  Options
(not yet designed):
- Nested suspension + mechanical damper stages in series
- Active vibration cancellation (adds power, mass, complexity)
- Reduced launch acceleration for Manna-B (constrains rail energy budget)

This is an open architectural problem.  `[PENDING — isolation trade study required]`

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
| 2 | BC feasibility gap: need 20–30× increase for orbital | Sim sweep | CRITICAL | ✅ Feasibility study complete — payload fraction breaks before materials do (§3.3) |
| 3 | 35°N → equatorial plane change not budgeted | Munk #2 | HIGH | 🔵 Fix selected (§3.4) |
| 4 | Tug rendezvous architecture undefined | Munk #3 | HIGH | OPEN |
| 5 | TPS exit heating: PICA-X sizing unverified | Munk #4 | HIGH | 🔵 Heat flux quantified (§4) |
| 6 | Liquid suspension density error + attenuation derivation | Munk #5 | MEDIUM | ✅ Correct derivation: 1.42× attenuation (§5.2); isolation trade study needed |
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
*v0.2.1 updated: 2026-04-28.  BC feasibility study (§3.3), corrected liquid suspension derivation (§5.2).*
*v0.3 planned: ConOps draft, ICD stubs, isolation trade study.*
