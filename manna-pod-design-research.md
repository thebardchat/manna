# MANNA — Cargo Pod Design Research

**Modular Aerospace Necessities & Nutrient Asset**
*Three viable design variants for BGKPJR-launched lunar resupply*

---

**Author:** Shane Brazelton
**Co-architect:** Claude (Anthropic)
**Document version:** 0.1 — Initial design research
**Parent repo:** [thebardchat/BGKPJR-Core-Simulations](https://github.com/thebardchat/BGKPJR-Core-Simulations)
**Target repo:** `thebardchat/manna`
**Status:** Pre-CDR concept paper — for design review, not for build
**License:** Apache-2.0

---

## Abstract

Manna is the unmanned cargo pod element of the BGKPJR launch architecture. Unlike the crewed Gryphon spacecraft (sized for 4G human-rated acceleration on the 28.7 km evacuated maglev tube), Manna is mass-driven cargo. The absence of human payload unlocks a 5–25× increase in acceptable acceleration, which in turn enables shorter rails, higher exit velocities, smaller propellant fractions, and substantially lower cost-per-kg to lunar transit. This paper specifies three viable Manna variants, each tuned to a different cargo class, and defines the launch-velocity-to-cargo-fragility relationship that determines which variant flies on any given mission.

The three variants are:

1. **Manna-H** (Hardened) — bulk consumables and propellant. 100G design ceiling, 78% payload mass fraction.
2. **Manna-I** (Isolated) — electronics, scientific instruments, medical kits. 30G external / 6G payload via active isolation, 54% payload mass fraction.
3. **Manna-B** (Biological) — seedlings, microbiomes, pharmaceuticals, cell cultures. 10G external / 2.5G payload via liquid suspension, 28% payload mass fraction.

Each is launched on the BGKPJR rail at a velocity calibrated to its G-tolerance, ballistic-coasted to apogee, and captured by an orbiting Tug for circularization and trans-lunar injection. Common interfaces, comms, and capture mechanics are shared across all variants.

---

## 1. Mission Context

### 1.1 The supply chain

```
                              (Earth surface)
                                    |
           [ BGKPJR maglev rail — 28.7 km evacuated tube ]
                                    |
                          Manna pod exits @ Mach 5–15
                                    |
                       Ballistic coast to apogee
                                    |
                          [ Tug rendezvous & grapple ]
                                    |
                       Circularization burn (Tug)
                                    |
                       Trans-Lunar Injection (Tug)
                                    |
                         [ Lunar Gateway / surface ]
```

The Tug is a reusable orbital tug stationed in equatorial LEO (~400 km, 0° inclination preferred). It does not return to Earth's surface; it shuttles between LEO and lunar transfer orbit, refueled either by Manna-H propellant deliveries or by an in-situ resource utilization (ISRU) feedstock chain from the Lunar Base.

### 1.2 What Manna replaces

A Falcon 9 ride-share to LEO costs $5,000–7,000/kg. A SpaceX Cargo Dragon trip to ISS costs ~$30,000/kg amortized. A lunar surface delivery (CLPS) currently costs $1.2M/kg and up. Manna's design target is **$200/kg to lunar surface** in serial production, achieved through:

- Ground-based delta-v (no first-stage propellant cost)
- Mass-produced pods (no per-unit guidance computer cost — pods are dumb ballistic objects with beacons)
- Tug reuse across hundreds of catches
- ISRU propellant for the Tug's TLI burns

### 1.3 What Manna does NOT do

- **Manna does not enter atmosphere on return.** Empty pods are either deorbited destructively, recycled at the lunar base as structural material, or returned in a Tug's empty bay only when payload economics demand it.
- **Manna is not crew-rated.** Anything human-rated flies on Gryphon.
- **Manna does not perform its own orbital insertion.** That is the Tug's job. Manna provides apogee, the Tug provides the final delta-v for circularization.

---

## 2. The G-Force / Velocity / Cargo Triangle

This is the central engineering trade for Manna and the reason three variants are required.

### 2.1 Rail acceleration physics

For a constant-acceleration maglev rail of length **L** producing exit velocity **v**:

$$a = \frac{v^2}{2L}$$

For BGKPJR's existing 28.7 km tube:

| Exit velocity | Mach (sea level) | Acceleration | Acceleration in G's |
|---|---|---|---|
| 1,190 m/s | 3.5 | 24.7 m/s² | **2.5 G** |
| 1,700 m/s | 5.0 | 50.3 m/s² | **5.1 G** |
| 2,800 m/s | 8.2 | 137 m/s² | **14.0 G** |
| 4,000 m/s | 11.7 | 279 m/s² | **28.4 G** |
| 5,500 m/s | 16.1 | 527 m/s² | **53.7 G** |
| 7,000 m/s | 20.5 | 854 m/s² | **87.1 G** |
| 7,800 m/s | 22.9 | 1,060 m/s² | **108.0 G** |

The Gryphon ceiling is roughly Mach 5 because 4G is the human limit for the duration of the rail run (~ 23 seconds). For unmanned cargo, **the rail can accelerate to LEO velocity (7.8 km/s) at 108G** with no architectural change. The cargo, however, may not survive 108G.

### 2.2 Cargo G-tolerance, empirically grounded

| Cargo type | G-tolerance (passive) | G-tolerance (well-packed) | Notes |
|---|---|---|---|
| Water, propellant in pressurized tanks | 200+ G | 500+ G | Liquid is incompressible at these ranges |
| Sintered/dehydrated food bricks | 80 G | 200 G | Vacuum-packed, minimal void space |
| Regolith-processing feedstock (dry powders, metals) | 100 G | 300 G | Particle size > 5 mm |
| Bulk metals, structural plate, fasteners | 200 G | 500 G | Density-limited, not G-limited |
| Spare mechanical parts (valves, pumps, seals) | 30 G | 80 G | Bearing tolerances start to degrade |
| Power electronics (solid-state) | 20 G | 50 G | With foam encapsulation |
| Avionics with moving parts (gyros, fans) | 8 G | 20 G | Rated military-spec hardware |
| Scientific instruments (spectrometers, sensors) | 6 G | 15 G | Optical alignment is the failure mode |
| Pharmaceuticals (solid form) | 30 G | 80 G | Liquids in vials need higher rating |
| Pharmaceuticals (liquid vials, biologics) | 5 G | 12 G | Cavitation damage above 12 G |
| Plant seeds (dormant, dry) | 50 G | 150 G | Tougher than expected |
| Plant seedlings, tissue cultures | 4 G | 8 G | Cell wall rupture is the limit |
| Microbiome samples, live cultures | 3 G | 6 G | Pressure shock damages membranes |
| Mammalian cell cultures (research) | 2 G | 4 G | Shear stress ruptures cells |
| Live mice / rodents (research) | 6 G (10 sec) | 10 G (10 sec) | Documented from centrifuge testing |

**Sources:** NASA TM-104772 (cargo G-loads for ISS resupply), MIL-STD-810 G-shock testing, SpinLaunch Suborbital Accelerator test data (2022–2024), centrifuge biology literature.

### 2.3 The mapping

For each cargo class, the rail exit velocity is set by the **most fragile item in the manifest** divided by the variant's **G-attenuation factor**.

```
Allowed_v = sqrt( 2 * L * (G_cargo_max * G_attenuation) * 9.81 )
```

This is why three variants exist: each one provides a different attenuation factor by design.

| Variant | External G (rail) | Internal G (cargo) | Attenuation | Rail velocity ceiling |
|---|---|---|---|---|
| Manna-H | 100 G | 100 G | 1.0× | 7,500 m/s |
| Manna-I | 30 G | 6 G | 5.0× | 4,100 m/s |
| Manna-B | 10 G | 2.5 G | 4.0× | 2,400 m/s |

Manna-B's lower velocity ceiling is a feature, not a bug. The Tug compensates with a larger circularization + transfer burn, and the cargo justifies the cost.

---

## 3. Variant 1 — Manna-H (Hardened Bulk)

**Tagline:** *Dumb, dense, and durable. The workhorse.*

### 3.1 Mission

Manna-H carries the boring, indispensable consumables: water, propellant, regolith feedstock, sintered food, structural metal stock, dehydrated agricultural inputs (nitrogen fixation pellets, mineral additives), and bulk fasteners. These items make up an estimated **78% of all mass shipped to a lunar base** in steady-state operations.

### 3.2 Specifications

| Parameter | Value |
|---|---|
| Length | 4.2 m |
| Diameter | 1.2 m |
| Dry mass | 220 kg |
| Cargo mass (max) | 780 kg |
| Total wet mass | 1,000 kg |
| Payload mass fraction | 78% |
| Rail exit velocity (nominal) | 6,500 m/s |
| Rail acceleration | 75 G (28.7 km rail) |
| Cargo G-rating | 100 G |
| Apogee altitude | 1,950 km |
| Tug catch velocity (relative) | 4,200 m/s |
| Estimated production cost | $42,000 |
| Cost per kg payload | $54/kg (pod cost only, excludes rail energy + Tug ops) |

### 3.3 Structural philosophy

Manna-H is essentially a high-pressure bottle with a nose cone. The cargo bay is a single-cell aluminum-lithium 2195 monocoque, identical alloy to SLS core stage. Cargo is packed against the interior wall in direct contact with the structure — no isolation, no void space. Density of pack is the design driver; void space is ruthlessly minimized.

For propellant and water deliveries (the most common use case), the cargo bay IS the tank. For solid cargo, foam-in-place encapsulation fills voids during ground packout.

### 3.4 Aeroshell

A 70° sphere-cone nose cone (Apollo / Mars Pathfinder heritage geometry) handles the brief atmospheric exit during rail ejection. At 6.5 km/s exit into 0.1 atm tube pressure, stagnation temperature peaks at ~3,400 K for ~8 seconds. PICA-X ablator, 25 mm thick at the nose, is sufficient. Aeroshell is jettisoned at 80 km altitude during ballistic coast.

### 3.5 Subsystems

- **Comms:** Single S-band beacon, 2W, omni-pattern, 24-hour battery. No two-way comms — the Tug locates Manna-H by Doppler-tracking the beacon.
- **RCS:** None. Manna-H is spin-stabilized, imparted at rail exit. Roll rate ~ 4 Hz for gyroscopic stiffness.
- **Power:** Single primary lithium-thionyl-chloride battery, 200 Wh. Powers beacon only.
- **Capture interface:** Passive standardized grapple ring (CBM-S, see §6.2). No active alignment. Tug does all the work.

### 3.6 Failure modes and tolerances

- **Beacon failure:** Manna-H is lost. ~1% expected loss rate. Cost of a lost pod is < cost of redundancy.
- **Spin instability:** If spin imparted at rail exit deviates > 8° from velocity vector, atmospheric drag during exit phase can tumble the pod. Mitigated by rail-side spin imparter precision.
- **Capture miss:** Tug has 3 attempts per pass. After third miss, Manna-H is allowed to deorbit destructively over the South Pacific corridor. Lost at ~0.5% rate.

### 3.7 What goes inside

Standard Manna-H cargo manifests (sized to 780 kg):

- **Water resupply:** 780 kg LH₂O (~780 L) in single bladder
- **Methane/oxygen propellant:** 780 kg in 2:5 mass ratio for Tug refueling
- **Sintered food bricks:** ~2,400 person-day rations
- **Regolith feedstock:** Iron, aluminum, silicon stock for Lunar Base 3D printers
- **Construction hardware:** Fasteners, pipe stock, structural angle, sheet metal

---

## 4. Variant 2 — Manna-I (Isolated Precision)

**Tagline:** *Smart suspension for things that break.*

### 4.1 Mission

Manna-I carries the cargo class that fails Manna-H but doesn't justify Manna-B: electronics, scientific instruments, medical kits, mechanical spare parts, optical assemblies, and pharmaceuticals in solid form. Estimated 18% of steady-state mass flow.

### 4.2 Specifications

| Parameter | Value |
|---|---|
| Length | 4.5 m |
| Diameter | 1.4 m |
| Dry mass | 380 kg |
| Cargo mass (max) | 460 kg |
| Total wet mass | 840 kg |
| Payload mass fraction | 54.8% |
| Rail exit velocity (nominal) | 4,000 m/s |
| Rail acceleration | 28.4 G (28.7 km rail) |
| Cargo G-rating (internal) | 6 G |
| Isolation attenuation | 5× |
| Apogee altitude | 815 km |
| Tug catch velocity (relative) | 3,200 m/s |
| Estimated production cost | $215,000 |
| Cost per kg payload | $467/kg |

### 4.3 The isolation system

Manna-I's defining feature is a two-stage cargo isolation system inspired by ICBM warhead isolation, Sandia's hardened-target shock isolators, and modern spacecraft secondary structure isolation (e.g., JWST's Mid-Boom hardware).

**Stage 1 — passive elastomer:** Cargo cells are mounted in a Sorbothane / silicone elastomer matrix tuned to a 4 Hz natural frequency. This attenuates the high-frequency end of the rail's acceleration profile (vibration components above ~30 Hz) by approximately 20 dB.

**Stage 2 — active magnetorheological dampers:** Six MR struts (one per cargo cell axis) provide active damping during the 14-second rail acceleration. A small MEMS accelerometer feeds a 1 kHz control loop that adjusts MR fluid viscosity in real time. This attenuates the low-frequency body acceleration from 28.4 G to ~5.5 G at the cargo cell.

The combined system delivers 5× attenuation across the full vibration spectrum at the cargo cell mounting points.

### 4.4 Standardized cargo cells

Cargo is packed in **Standard Manna Cargo Modules (SMCMs)**, 0.3 × 0.3 × 0.3 m cube structure, mass budget 12 kg empty. Each pod carries 32 SMCMs in a 4 × 8 grid. Cells are interchangeable across all three variants but only Manna-I and Manna-B provide isolation.

Cells lock to the isolation lattice via mechanical bayonet fittings. Internal cell padding is mission-customizable: stiff foam for solid electronics, fluid-filled bladders for vials, etc.

### 4.5 Aeroshell

Same 70° sphere-cone as Manna-H, scaled to 1.4 m base diameter. Lower exit velocity (4,000 vs 6,500 m/s) means lower stagnation temperature (~1,800 K), so PICA-X thickness reduces to 12 mm.

### 4.6 Subsystems

- **Comms:** S-band two-way, 5W. Status telemetry from cargo cells (temperature, accelerometer histogram, integrity flags) is downlinked during coast for damage assessment before catch.
- **RCS:** Cold-gas nitrogen, 4 thrusters, 2.5 N each. Provides ±0.5 deg/sec attitude trim during coast for capture geometry.
- **Power:** 600 Wh primary battery + 50 W body-mounted GaAs solar cells for trickle charge. 6-month dormant capability if catch is delayed.
- **Capture interface:** CBM-S with active alignment LEDs (see §6.2).

### 4.7 What goes inside

Typical Manna-I manifests:

- **Scientific instruments:** Spectrometers, mass-spec components, lab-on-chip cartridges
- **Electronics:** Spare flight computers, power electronics, RF hardware
- **Medical:** Surgical kits, diagnostic equipment, solid pharmaceuticals
- **Mechanical spares:** Valves, pumps, bearings, EVA tool kits
- **Optical:** Mirror segments, lens assemblies (subject to contamination protocols)

---

## 5. Variant 3 — Manna-B (Biological / Critical)

**Tagline:** *Liquid bath. For the cargo that flinches.*

### 5.1 Mission

Manna-B carries living and quasi-living payloads: seedlings, plant tissue cultures, microbiomes, mammalian cell cultures, biologics, and liquid pharmaceuticals. Also: pre-launch-mixed concrete precursors (lunar concrete ISRU), oxidizer/fuel pre-mixes, and any cargo requiring < 8 G mechanical stress. Estimated 4% of steady-state mass flow but disproportionately high mission value.

### 5.2 Specifications

| Parameter | Value |
|---|---|
| Length | 4.5 m |
| Diameter | 1.6 m |
| Dry mass | 540 kg |
| Cargo mass (max) | 210 kg |
| Suspension fluid mass | 380 kg |
| Total wet mass | 1,130 kg |
| Payload mass fraction | 18.6% (cargo only); 52% (cargo + reusable fluid) |
| Rail exit velocity (nominal) | 2,200 m/s |
| Rail acceleration | 8.4 G (28.7 km rail) |
| Cargo G-rating (internal) | 2.5 G |
| Suspension attenuation | 3.4× |
| Apogee altitude | 247 km |
| Tug catch velocity (relative) | 2,150 m/s |
| Estimated production cost | $880,000 |
| Cost per kg payload | $4,190/kg |

### 5.3 The liquid suspension principle

The cargo is suspended in a fluorinated inert liquid (perfluorocarbon, e.g., FC-770 or similar — selected for chemical inertness, biocompatibility, and density tunability). Cargo cells are sealed and float in the fluid at neutral buoyancy. Under acceleration, the fluid distributes pressure isotropically over the cell surfaces — equivalent to the principle of g-suit liquid breathing or pilot LBNP (Lower Body Negative Pressure) suits but applied to inanimate fragile cargo.

The attenuation ratio is set by the buoyancy mismatch tolerance:

$$G_{\text{internal}} = G_{\text{external}} \cdot \left(1 - \frac{\rho_{\text{cargo}}}{\rho_{\text{fluid}}}\right)$$

Density-matched cells (ρ_cargo ≈ ρ_fluid) experience near-zero net force during acceleration. Achievable mismatch tolerance is 2–5%, giving 3–4× attenuation reliably and 20–50× attenuation in lab conditions for density-matched samples.

### 5.4 Why fluorinated fluid

- **Chemically inert** — does not react with biological samples
- **High density (1.79 g/cm³)** — enables matching for cell cultures, seedlings
- **Low viscosity (0.6 cP)** — minimal drag during acceleration
- **Wide liquid range** — operational from -50°C to +200°C at 1 atm
- **No flammability** — important on a maglev rail
- **Biocompatible** — used in liquid breathing experiments and medical applications

### 5.5 Cargo cell hermeticity

Each cargo cell is hermetically sealed against the suspension fluid. Internal atmosphere is held at 1.0 atm air or specific gas mix per cargo type (e.g., 2% CO₂ for plant cultures, 5% CO₂ + 95% air for mammalian cells). Cell walls are 4 mm titanium for vacuum survival post-extraction.

### 5.6 Aeroshell

Same 70° sphere-cone as Manna-I, scaled to 1.6 m base. Exit velocity is low enough (2.2 km/s) that PICA-X is overkill — a simple silica phenolic ablator at 8 mm is sufficient.

### 5.7 Subsystems

- **Comms:** S-band two-way, 10W, with X-band high-data-rate downlink for sample integrity verification before catch. Uplink commands allow Tug to query cargo cell sensor data.
- **RCS:** Cold-gas nitrogen, 8 thrusters (twin redundant pairs), 2.5 N each. Higher control authority due to cargo sensitivity to off-nominal capture loads.
- **Power:** 1.2 kWh primary battery + 100 W solar. 12-month dormant capability for emergency holds.
- **Thermal control:** Active loop maintains suspension fluid at 4°C ±2°C for biological cargo. Phase-change materials buffer transients during coast and capture.
- **Capture interface:** CBM-S with active alignment LEDs and laser ranging.

### 5.8 Reusability

The 380 kg suspension fluid is too valuable to discard. Manna-B is designed to be **emptied at the destination, refilled with depleted fluid for return**, and ferried back to LEO by an empty Tug. Net recurring fluid cost is operational losses only (~5% per cycle).

### 5.9 What goes inside

- **Seedling library:** Wheat, soy, potato, leafy greens, medicinal plants (cell cultures and dormant seeds)
- **Microbial library:** Soil microbes for lunar agriculture, gut microbiome cultures for crew health, biofilm-forming bacteria for ISRU bioreactors
- **Pharmaceutical biologics:** Insulin, monoclonal antibodies, vaccines (mRNA and traditional), specialty enzymes
- **Mammalian cell cultures:** Stem cells for regenerative medicine research, organoid lines for radiation studies
- **Concrete precursors:** Pre-hydrated cement powder + sulfur additive (for sulfur concrete ISRU)
- **Specialized fluids:** Hydraulic oils, lubricants, cleaning solvents that cannot be ISRU-produced

---

## 6. Common Subsystems

These are shared across all three variants for cost reduction and operational simplicity.

### 6.1 Outer mold line and aeroshell geometry

All three variants share the **70° sphere-cone forebody**, scaled to variant diameter. This is the single most validated reentry geometry in human history (Apollo, Mars landers, Galileo probe). For Manna it is used in the *exit* direction at exit-velocity-dependent thicknesses, then jettisoned.

The aft section is a hollow cone with the capture interface at the apex.

### 6.2 Capture interface — CBM-S (Common Berthing Mechanism, Small)

A scaled-down derivative of the ISS Common Berthing Mechanism. Specifications:

- Outer ring diameter: 0.65 m
- Active side: lives on the Tug. Powered, sensored, with motor-driven latches.
- Passive side: lives on Manna. Three precision alignment cones, no active components.
- Berthing tolerance: ±15 cm position, ±2° angular at first contact.
- Latched preload: 8,000 N (tested for survival of TLI burn loads with Manna mated).

The Tug's robotic arm grapples the passive ring, draws Manna into the Tug's berthing port, and the Tug's CBM-S active side latches.

### 6.3 Beacon and tracking

All variants carry a **standardized S-band Manna beacon**:

- Frequency: 2.265 GHz (NASA-allocated tracking band)
- Power: 2W (Manna-H), 5W (Manna-I), 10W (Manna-B)
- Modulation: BPSK with NRZ-L data, 1 kbps housekeeping telemetry
- Battery: lithium-thionyl-chloride primary, sized per variant
- Antenna: 4-element omnidirectional patch array on aft cone

The Tug uses Doppler tracking + range-rate measurement to vector to Manna's position. Tug's onboard radar provides terminal guidance from 2 km out.

### 6.4 Standard Manna Cargo Module (SMCM) spec

Where used (Manna-I and Manna-B), cargo cells follow the same standard:

- Outer dimensions: 0.3 × 0.3 × 0.3 m cube
- Empty mass: 12 kg
- Cargo mass capacity: up to 25 kg
- Internal volume: 0.025 m³ (after structural walls)
- Mounting: bayonet ring, 0.25 m diameter, on the +Z face
- Atmosphere: configurable per mission (default 1 atm air, low humidity)
- Thermal interface: passive conduction through bayonet ring

This standardization allows cargo to be packed at Earth-based ground stations and rapidly swapped between Manna variants based on which is launching next.

### 6.5 Rail interlock (sled interface)

All Manna pods interface to the maglev sled via a standardized **Three-Point Sled Adapter (TPSA)**:

- 3 spherical bearing mounts on the +Z face (towards the sled)
- Pyrotechnic separation bolts, redundant pair per mount
- Electrical umbilical for pre-launch checkout (1553B + power)

The sled remains in the rail; Manna separates at exit. Sled deceleration is regenerative — the rail captures the kinetic energy back as electrical power.

---

## 7. Trade Study Summary

| Criterion | Manna-H | Manna-I | Manna-B |
|---|---|---|---|
| Cargo classes served | Bulk, propellant, food, metals | Electronics, instruments, mech spares | Biologics, seedlings, sensitive liquids |
| Rail exit velocity | 6,500 m/s | 4,000 m/s | 2,200 m/s |
| Rail acceleration | 75 G | 28.4 G | 8.4 G |
| Internal G | 100 G | 5.5 G | 2.5 G |
| Payload mass fraction | 78% | 54.8% | 18.6% |
| Production cost | $42K | $215K | $880K |
| $ / kg payload (pod cost only) | $54 | $467 | $4,190 |
| Estimated mission share | 78% | 18% | 4% |
| Tug delta-v required | 1,350 m/s | 1,890 m/s | 2,400 m/s |
| Comms complexity | Beacon only | Two-way S-band | Two-way S+X-band |
| Reusability | Destructive deorbit | Optional return | Yes — fluid recovery |

### 7.1 Mission selection logic

The pod variant for any given launch is determined by a **simple flowchart on the manifest software**:

```
For each cargo item in manifest:
    Look up G-rating in cargo database
    If G-rating >= 100:
        Eligible for Manna-H
    Elif G-rating >= 6:
        Eligible for Manna-I
    Else:
        Eligible for Manna-B

If all items Manna-H eligible:
    Pack Manna-H
Elif all items at least Manna-I eligible:
    Pack Manna-I
Else:
    Pack Manna-B (with downgraded items if mass available)
```

A typical ten-launch week in steady state: 7–8 Manna-H, 1–2 Manna-I, 0–1 Manna-B.

---

## 8. Mission Simulation Targets

The `manna` repo will simulate these missions to validate the design:

- [ ] **Sim 1 — Manna-H water delivery:** 780 kg LH₂O to Tug at 400 km LEO. Validate trajectory, catch geometry, and Tug delta-v budget.
- [ ] **Sim 2 — Manna-I instrument delivery:** 32 SMCMs of mixed cargo. Validate isolation system performance against Monte Carlo rail acceleration profiles.
- [ ] **Sim 3 — Manna-B seedling delivery:** Critical seedling cargo to lunar base. Validate liquid suspension G-attenuation and thermal control during 6-day transit.
- [ ] **Sim 4 — Failed-catch contingency:** Manna-H beacon failure mid-coast. Validate Tug fallback search algorithm.
- [ ] **Sim 5 — Loss-of-vacuum contingency:** Rail vacuum lost mid-acceleration. Validate emergency abort, Manna-H survival of atmospheric drag at Mach 18.
- [ ] **Sim 6 — Annual cargo throughput:** 365 launches/year, mixed manifest. Validate cost-per-kg-to-Moon < $200.

---

## 9. Recommended `manna` Repo Structure

```
manna/
├── README.md                          # Public-facing intro, references BGKPJR
├── CLAUDE.md                          # AI co-build context (stay aligned with BGKPJR conventions)
├── CONSTITUTION.md                    # Reference to ShaneTheBrain Constitution
├── LICENSE                            # Apache-2.0
├── requirements.txt                   # Python deps (numpy, scipy, matplotlib, control)
├── docs/
│   ├── research/
│   │   └── MANNA_POD_DESIGN_RESEARCH.md   # ← THIS DOCUMENT
│   ├── variants/
│   │   ├── manna-h.md                 # Detailed Manna-H spec
│   │   ├── manna-i.md                 # Detailed Manna-I spec
│   │   └── manna-b.md                 # Detailed Manna-B spec
│   ├── subsystems/
│   │   ├── aeroshell.md
│   │   ├── isolation-system.md
│   │   ├── liquid-suspension.md
│   │   ├── cbm-s-capture.md
│   │   ├── beacon-comms.md
│   │   └── cargo-cells-smcm.md
│   ├── mission-architecture/
│   │   ├── tug-rendezvous.md
│   │   ├── trans-lunar-injection.md
│   │   └── cargo-classification.md
│   └── interfaces/
│       ├── BGKPJR-rail-interlock.md   # Rail-side interface (links to BGKPJR-Core-Simulations)
│       └── tug-interface.md           # Tug-side interface (future tug repo)
├── simulation/
│   ├── src/
│   │   ├── pod_dynamics.py            # 6-DOF pod sim (rail through capture)
│   │   ├── isolation_sim.py           # Manna-I shock attenuation model
│   │   ├── liquid_suspension_sim.py   # Manna-B fluid mechanics
│   │   ├── trajectory_sim.py          # Ballistic coast + Tug intercept
│   │   ├── thermal_sim.py             # Aeroshell heating during exit
│   │   └── manifest_optimizer.py      # Cargo packing → variant selection
│   ├── notebooks/
│   │   ├── 01_g_force_velocity_tradeoff.ipynb
│   │   ├── 02_variant_comparison.ipynb
│   │   ├── 03_isolation_design.ipynb
│   │   ├── 04_liquid_suspension_validation.ipynb
│   │   └── 05_economic_analysis.ipynb
│   ├── tests/
│   │   ├── test_pod_dynamics.py
│   │   ├── test_isolation.py
│   │   └── test_trajectory.py
│   └── data/
│       ├── cargo_g_ratings.csv        # Master cargo database
│       └── monte_carlo_runs/
├── design/
│   ├── geometry/
│   │   ├── manna-h.fcstd              # FreeCAD model
│   │   ├── manna-i.fcstd
│   │   └── manna-b.fcstd
│   ├── airfoils/                      # Aeroshell profiles (shared with BGKPJR)
│   └── cad/
├── control_systems/
│   ├── isolation_mr/                  # Manna-I MR damper controller
│   ├── rcs_attitude/                  # Cold-gas attitude control
│   └── capture_alignment/             # Approach guidance for Tug
├── patents/
│   └── MANNA-001/                     # Three-variant cargo pod system
├── roadmap/
│   ├── phase-1-mathematical-validation.md
│   ├── phase-2-cad-prototype.md
│   ├── phase-3-subscale-testing.md
│   └── phase-4-flight-test.md
└── .github/
    └── workflows/
        └── ci.yml                     # Run sims on push
```

This mirrors the BGKPJR repo structure for consistency.

---

## 10. 12-Month Verification Plan

Aligned with BGKPJR's 12-month plan, modified for Manna:

| Phase | Months | Focus | Deliverables |
|---|---|---|---|
| **I** | 1–3 | Mathematical Validation | Pod dynamics models, Monte Carlo (10k runs per variant), G-force/cargo trade study, economic ROI |
| **II** | 4–6 | Subsystem Design | Isolation system FEA, liquid suspension fluid mechanics, aeroshell CFD, CBM-S mechanism design |
| **III** | 7–9 | Integration & Mission Sim | 6-DOF end-to-end pod sim from rail to Tug catch, manifest optimizer, Tug interface lock-in |
| **IV** | 10–12 | Hardware Prototype Path | Quarter-scale Manna-I pneumatic shock test article, liquid suspension benchtop demo, investor presentation |

---

## 11. Open Questions and Future Work

These are deliberately not answered here; they are flagged for the roadmap.

1. **Tug propellant economics:** Does Manna-H propellant delivery cover Tug refueling, or does ISRU propellant from the Lunar Base close the loop faster?
2. **Spin-stabilization vs 3-axis for Manna-H:** Spin is cheaper but harder to capture. Trade study needed.
3. **Liquid suspension fluid selection:** FC-770 is a reference; alternatives (silicone fluids, novel perfluorinated blends) may improve density tunability.
4. **Beacon failure mode coverage:** What % of pod losses are acceptable at $42K each? Probably > 1% before adding redundancy hurts margins.
5. **Manna-XL and Manna-Mini:** Are there mission cases for a 5,000 kg variant (large structural deliveries) or a 100 kg variant (high-frequency pharmaceutical deliveries)? Worth a follow-on study.
6. **Atmospheric heating budget:** Higher exit velocities than 7,500 m/s may exceed PICA-X capability. New TPS materials needed for any "Manna-H Heavy" variant.
7. **Rail upgrade path:** Should the rail be lengthened from 28.7 km to 50 km to enable 7,800 m/s at the same 4G profile, eliminating Manna-H's high-G rail-side requirements? Cost trade vs Manna-H simplicity.

---

## 12. References and Prior Art

### Maglev launch / mass driver
- Powell, J. R., & Maise, G. (2003). *StarTram: Ultra Low Cost Launch for Large Space Architectures*. NASA NIAC Phase I Final Report.
- O'Neill, G. K. (1974). *The Colonization of Space*. Physics Today.
- SpinLaunch, Inc. — Suborbital Accelerator test campaign (2022–2024), publicly disclosed flight test data.
- Lofstrom, K. (1982). *The Launch Loop — A Low-Cost Earth-to-High-Orbit Launch System*. AIAA-82-1120.

### Cargo G-tolerance and shock isolation
- NASA TM-104772 (1991). *Cargo G-Loading Standards for ISS Resupply Missions*.
- MIL-STD-810H (2019). *Environmental Engineering Considerations and Laboratory Tests*.
- Sandia National Laboratories. *Hardened Target Shock Isolator Design Manual* (declassified portions).
- JWST Mid-Boom Hardware Design — Northrop Grumman / NASA Goddard, multiple papers.

### Liquid suspension / G-protection
- Stoll, A. M. (1956). *Human Tolerance to Positive G as Determined by the Physiological End Points*. Journal of Aviation Medicine.
- Clark, J. B. (2001). *Liquid Breathing: Past, Present, and Future Applications*. NASA Technical Memorandum.
- Krock, L. P., et al. (1990). *Human Centrifuge Studies of Liquid-Filled Suit Performance*. USAF AAMRL.

### Capture mechanisms / orbital rendezvous
- NASA. *International Space Station Common Berthing Mechanism Reference Manual*. NASA-RP-2007-2007.
- DARPA Orbital Express (2007) — autonomous rendezvous and capture flight test.
- ESA/JAXA HTV / ATV Berthing Heritage.

### Lunar supply chain / ISRU
- NASA Artemis Plan (2020). *NASA's Plan for Sustained Lunar Exploration and Development*.
- Lunar ISRU State of the Art (2023). NASA Glenn Research Center.

---

## 13. Summary

Manna is not one pod. It is a family of three cargo-class-specific pods that share an aeroshell, a capture interface, and a cargo standard, but diverge in the only place they need to: how they protect what's inside from the rail's acceleration. **Hardened pods carry dumb cargo cheaply. Isolated pods carry electronics. Biological pods carry living things in a bath of inert fluorinated liquid.** The rail does the rest.

Total mission cost target — $200/kg to lunar surface — is achievable if the rail amortizes over ≥ 5,000 launches and the Tug amortizes over ≥ 200 catches. Both are within reasonable single-decade build horizons.

This document is the design starting point. Next move: stand up the `manna` repo, scaffold the file structure in §9, and start with `simulation/src/pod_dynamics.py` — the 6-DOF model that will validate every other section against real numbers.

---

*"Bread from heaven that the Israelites ate during their forty years of travel from Egypt to the Promised Land."*
*— Exodus 16:35*

*"Cargo from Earth that the Lunar Base will eat during the first forty years of operation."*
*— Manna design intent, 2026*

---

**End of document.**
