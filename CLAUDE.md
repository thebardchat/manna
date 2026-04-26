# CLAUDE.md
### Context file for Claude Code sessions in the `manna` repo
**Last updated:** 25 April 2026
**Maturity:** Pre-Phase A concept memorandum
**Operating under:** [ShaneTheBrain Constitution](https://github.com/thebardchat/constitution) · [Persona Review Protocol v1.0](./PERSONA_REVIEW_PROTOCOL.md)

---

## 1. What this repo is

`manna` defines and simulates the **Manna** *cargo pod family* — creating uncrewed cargo pod variants launched from the [BGKPJR](https://github.com/thebardchat/BGKPJR-Core-Simulations) maglev rail to sub-orbital trajectory, captured by an orbiting Tug, and ferried to the Lunar Base.

**Three variants. Always.**

| Variant | Cargo class | Internal G | Rail v_exit | Mass fraction |
|---|---|---|---|---|
| **Manna-H** | Bulk: water, propellant, food, metals | 100 G | 6,500 m/s | 78% |
| **Manna-I** | Electronics, instruments, mech spares | 5.5 G | 4,000 m/s | 54.8% |
| **Manna-B** | Biologics, seedlings, sensitive liquids | 2.5 G | 2,200 m/s | 18.6% |

**Mission target:** $200/kg to lunar surface in steady-state operations.
**Status:** Concept-level. None of the numbers above survive forensic review without revision (see §7).

> **Note (2026-04-25):** Simulation uses back-calculated velocities derived from v0.1 vacuum apogee claims
> (H: 10,822 m/s, I: 7,670 m/s, B: 4,319 m/s). Rail v_exit figures above are [PLACEHOLDER] awaiting
> rail energy budget from BGKPJR. See `simulation/src/trajectory_sim.py` for authoritative sim values.

---

## 2. Where this fits in the ecosystem

```
        ┌──────────────────────┐
        │  BGKPJR-Core-Sims    │  Maglev rail, 28.7 km, 15-45° incline
        │  (the rail)          │  Hazel Green, AL · 34.93° N
        └──────────┬───────────┘
                   │ launches
                   ▼
        ┌──────────────────────┐
        │      manna           │  ← THIS REPO
        │  (the cargo pod)     │
        └──────────┬───────────┘
                   │ caught by
                   ▼
        ┌──────────────────────┐
        │       tug            │  Reusable orbital tug · NOT YET BUILT
        │  (transfer vehicle)  │  Reference concept needed
        └──────────┬───────────┘
                   │ delivers to
                   ▼
        ┌──────────────────────┐
        │   Lunar Base         │  Out of scope for these repos
        └──────────────────────┘
```

The Cloudflare Worker named `manna` (separate, deployed under `brazeltonshane.workers.dev`) is the **public-facing API** that surfaces launch manifests, pod telemetry, and catch status. Different artifact, same naming for system coherence.

---

## 3. Hardware / infrastructure (Shane's, not the pod's)

These paths and IPs apply to every Claude Code session for this user, not just `manna`:

| Component | Detail |
|---|---|
| **Compute** | Raspberry Pi 5 (16 GB RAM) · Pironman 5-MAX chassis |
| **Storage** | 2× WD Blue SN5000 2 TB NVMe — RAID 1 via mdadm |
| **Core path** | `/mnt/shanebrain-raid/shanebrain-core/` |
| **Pi Tailscale IP** | `100.67.120.6` — use directly, never MagicDNS |
| **Pulsar0100 (Windows / N8N)** | `100.81.70.117` |
| **bullfrog-max-r2d2** | `100.87.222.17` |
| **laptop-ts6v7fna** | `100.94.122.125` |
| **FastMCP** | port 8008, 27 tools |
| **Weaviate** | port 8080 |
| **Ollama** | port 11434 |
| **N8N** | runs on Pulsar0100 |

**Networking rule:** Always use Tailscale IPs directly. MagicDNS is unreliable in this stack.

---

## 4. Repo layout

```
manna/
├── README.md                    # Public-facing intro
├── CLAUDE.md                    # ← YOU ARE HERE
├── CONSTITUTION.md              # Reference link to ShaneTheBrain Constitution
├── PERSONA_REVIEW_PROTOCOL.md   # Standing protocol for AI persona reviews
├── LICENSE                      # Apache-2.0
├── requirements.txt
├── docs/
│   ├── research/
│   │   └── MANNA_POD_DESIGN_RESEARCH.md   # The design memo (re-title to v0.2)
│   ├── variants/                # Per-variant specs (manna-h.md, etc.)
│   ├── subsystems/              # Aeroshell, isolation, capture, etc.
│   ├── mission-architecture/    # Trajectory, rendezvous, TLI
│   └── interfaces/              # Rail-side and Tug-side ICDs
├── simulation/
│   ├── src/
│   │   ├── trajectory_sim.py    # ✅ 3-DOF RK4 integrator, US Std Atm 1976
│   │   └── sweep.py             # ✅ BC × elevation parametric sweep (108 runs)
│   ├── tests/
│   │   ├── test_trajectory.py   # ✅ 42 tests
│   │   └── test_sweep.py        # ✅ 8 tests
│   └── data/
│       ├── cargo_g_ratings.csv  # ← SINGLE SOURCE OF TRUTH for cargo classification
│       └── trajectory_runs/     # Plot output (PNG)
├── design/                      # FreeCAD models (geometry, airfoils, cad)
├── control_systems/             # MR damper control, RCS, capture alignment
├── patents/MANNA-001/
├── roadmap/                     # Phase I-IV verification plan
└── expert-reviews/              # Persona-based forensic reviews
```

---

## 5. Conventions

### 5.1 Code style
- Python 3.10+
- PEP 8, type hints encouraged
- All physics math: show the equation, then the numerical result
- All simulation outputs: include input parameters in the output filename or header
- ALL simulation outputs: include actual visualizations to scale
- ALL diagrams of cargo bay must loop loading protocol in visualization

### 5.2 Documentation style
- Match BGKPJR's voice: technical, direct, with ASCII diagrams when they help
- Sentence case in headings (not Title Case)
- Tables for trade studies, not prose
- Every numerical claim gets a tag: `[VERIFIED]`, `[DERIVED]`, `[ESTIMATE]`, or `[PLACEHOLDER]`
- No fabricated citations. If a citation cannot be verified, mark it `[CITATION NEEDED]` instead

### 5.3 The three variants are first-class
- Every analysis must consider all three variants unless explicitly variant-specific
- Don't favor one variant over the others
- The cost/complexity ordering (H < I < B) is intentional and stable

### 5.4 Cargo G-rating CSV is canonical
File: `simulation/data/cargo_g_ratings.csv`
- Any new cargo type gets added here first
- Every variant-selection algorithm reads from this file
- Never hardcode G-ratings in simulation code

---

## 6. Author's preferences (apply to every session)

These are Shane's standing preferences from his user profile. They override default Claude behavior:

- **Zero preamble.** No "I'd be happy to" or "Certainly." Straight to the answer.
- **If something won't work or is the wrong move, say so immediately.** Then give the alternative.
- **ADHD-friendly format.** Short blocks. Checkboxes for multi-step tasks. File structure first.
- **Pragmatic and technical.** Solutions over explanations.
- **Be proactive.** Anticipate needs. Suggest unprompted. If there's a better way, say so.
- **Faith, family, sobriety are non-negotiable values.** Tone always respects these.
- **Local-first.** Pi before cloud. Ollama before OpenAI. Weaviate before Pinecone.
- **Decode garbled voice-to-text input** rather than asking for clarification.
- **PARTNER DIRECTIVE:** If asked "Is there a way?" and YES + best solution exists, say so immediately.

---

## 7. Known issues from forensic review

The v0.1 design memo (in `docs/research/MANNA_POD_DESIGN_RESEARCH.md`) was reviewed via persona-based forensic exercise (channeling NASA STMD aerospace credentials — see `expert-reviews/`). The review found:

### 7.1 Trajectory math is vacuum-vertical-launch approximation
The apogee numbers (1,950 km / 815 km / 247 km) assume vertical launch with no atmosphere. The actual rail is inclined 15–45°. **Real apogees are roughly 4× lower than v0.1 claims.** Must run a real ballistic simulator with NRLMSISE-00 or US Std Atm 1976 drag model before any apogee number is defensible.

**Status (2026-04-25): CONFIRMED via simulation.** Real apogees at 30° elevation: H=9.1 km, I=6.0 km, B=4.2 km. Sim matches vacuum claims exactly when drag disabled. [DERIVED]

### 7.2 35° N rail cannot reach equatorial LEO
Hazel Green is at latitude 34.93° N. Direct launches to 0° inclination cost 4.6 km/s in plane change — exceeds the entire Tug delta-v budget. **Architecture as written does not close.** The fix: put the Tug in a matched ~35° inclination orbit (this is what Cape Canaveral does at 28.5°). Re-derive Tug delta-v.

### 7.3 "Tug catches at 4 km/s relative" is impact, not capture
Berthing happens at sub-m/s closing rates. Real architecture: Tug pre-positions in a phasing orbit, matches pod's apogee state vector (which is *slow* at apogee — that's the insight), then closes at meter-per-second rates. The v0.1 paper conflates ballistic intercept with rendezvous.

### 7.4 PICA-X application is for entry, not exit
The 70° sphere-cone heritage is from Apollo / MSL *entry* designs. Atmospheric *exit* has reversed thermal profile (atmosphere thinning while velocity rises). Geometry probably still works, but TPS sizing must be redone with NASA DPLR/LAURA + FIAT for the exit case. The 25 mm PICA-X claim is unsupported until that runs.

**Status (2026-04-25): Peak stagnation heat flux quantified via Sutton-Graves.** At launch: H=1.15 GW/m², I=0.41 GW/m², B=0.07 GW/m². [CONSTRAINT-NOT-MODELED — R_nose=5 cm assumed]

### 7.5 Liquid suspension math is internally inconsistent
The equation in §5.3 of v0.1 gives 50× attenuation at 2% density mismatch. The paper claims 3–4×. The actual physics for non-density-matched cells (cells at 1.05 g/cm³ in FC-770 at 1.79 g/cm³) is closer to 2.4× attenuation. **The right answer was reached for the wrong reason.** Fix the derivation.

### 7.6 Citations were fabricated
Several entries in the v0.1 References section were AI-generated and do not correspond to verifiable documents. **Strip them all.** Replace only with citations that can be web-fetched and confirmed. Better to have an empty References section than a misleading one.

### 7.7 Cost figures are not derived
$54/kg, $467/kg, $4,190/kg are reasoned guesses. Real per-kg costs require: separated marginal / operational / allocated capital cost models, comparison to CLPS ($1M-$3M/kg current), and production-rate sensitivity analysis.

---

## 8. Things to NEVER do

- **Never use Manna's design profile for Gryphon (or vice versa).** They are different vehicles. Manna takes 8–100G; Gryphon takes 4G. Same rail, different missions.
- **Never collapse the three variants into "one Manna pod."** The whole architecture is built on cargo-class differentiation.
- **Never optimize Manna-B's cost down.** $4,190/kg is correct — biological cargo is expensive because the protection is expensive. Optimizing it down means re-introducing failures the variant exists to prevent.
- **Never over-engineer Manna-H.** It is deliberately the dumbest of the three. Adding features = adding cost = breaking the per-kg target.
- **Never use a named persona review without going through PERSONA_REVIEW_PROTOCOL.md.** Especially: never use Ms. Munk's name, NASA's name, or any institution's name in any external-facing context based on a persona review.
- **Never trust apogee/velocity numbers from v0.1.** They are vertical-launch approximations. Use the trajectory simulator for any real number.
- **Never publish a citation without verifying it.** Web-fetch, NASA Technical Reports Server, NTRS, or established peer-reviewed source. No exceptions.
- **Never push to a public branch without running tests.** `pytest simulation/tests/` must pass.
- **Never add cloud dependencies when local works.** Pi-first. Ollama-first. Weaviate-first.

---

## 9. Frequently used commands

```bash
# Activate environment
cd /mnt/shanebrain-raid/shanebrain-core/manna  # adjust to actual path
source venv/bin/activate

# Run trajectory simulation (all 3 variants, 30° elevation)
python simulation/src/trajectory_sim.py

# Run BC × elevation parametric sweep (108 simulations, ~30 s)
python simulation/src/sweep.py

# Run tests
pytest simulation/tests/ -v

# Run manifest optimizer (when built)
python simulation/src/manifest_optimizer.py --cargo-list manifests/example.csv

# Monte Carlo (when built — computationally heavy)
python simulation/src/monte_carlo.py --variant I --runs 10000
```

---

## 10. Current state and next moves

### What exists right now
- [x] Design Concept Memorandum (`docs/research/MANNA_POD_DESIGN_RESEARCH.md`)
- [x] Three-variant taxonomy
- [x] Repo scaffolding
- [x] Cargo G-rating CSV starter
- [x] Persona-based forensic review (Munk persona, see `expert-reviews/`)
- [x] PERSONA_REVIEW_PROTOCOL.md
- [x] **Trajectory simulator** — `simulation/src/trajectory_sim.py` (RK4, US Std Atm 1976, 50/50 tests)
- [x] **BC × elevation parametric sweep** — `simulation/src/sweep.py` (108 runs, contour plots)
- [x] **Sutton-Graves stagnation heat flux** — `SimResult.peak_heat_flux_W_m2` [CONSTRAINT-NOT-MODELED]
- [x] **Orbital analysis at apogee** — `vx_at_apogee`, `v_circ_at_apogee`, `orbital_at_apogee`
- [x] **Adaptive RK4 sub-stepping** — prevents numerical blow-up under extreme drag

### Key sweep findings (2026-04-25)  [DERIVED]
- Current variants (BC ≈ 1,600–2,300 kg/m²) achieve 4–9 km apogee at 30° — 97% below v0.1 claims
- To reach Kármán line (100 km), need BC ≥ ~5,000 kg/m² at steep elevation (75–85°)
- To approach orbital velocity at apogee, Manna-H needs BC ≥ 50,000 kg/m² (sweep found vx/v_circ = 1.05 at 30–45°)
- Peak heat flux at launch: H=1.15 GW/m², I=0.41 GW/m², B=0.07 GW/m² — critical constraint

### What's missing (priority order)
1. **Re-derive variant parameters** — sim shows BC must increase 20–30× to close the trajectory gap; requires pod redesign
2. **Re-title v0.1 to v0.2** with sim-corrected numbers and Maturity Statement
3. **Tug Reference Concept** — separate `tug` repo, 5–10 page concept doc
4. **Inclination-fix architecture** — Tug in ~35° matched orbit (option c)
5. **Real citations pass** — strip fabricated ones
6. **Liquid suspension math fix** — §7.5
7. **Pod dynamics 6-DOF** — `simulation/src/pod_dynamics.py`
8. **Thermal protection trade study** — Sutton-Graves says ~1 GW/m² at exit; TPS must close

---

## 11. References (verified)

These are checked. Use them confidently.

- [BGKPJR-Core-Simulations](https://github.com/thebardchat/BGKPJR-Core-Simulations) — parent rail repo
- [ShaneTheBrain Constitution](https://github.com/thebardchat/constitution) — governing ethics document
- [shanebrain-core](https://github.com/thebardchat/shanebrain-core) — compute backbone
- NASA NTRS (technical reports server): https://ntrs.nasa.gov
- NASA GMAT (General Mission Analysis Tool, free): https://software.nasa.gov/software/GSC-17177-1
- US Standard Atmosphere 1976: NASA-TM-X-74335
- NRLMSISE-00 atmosphere model: https://ccmc.gsfc.nasa.gov/modelweb/atmos/nrlmsise00.html
- 3M FC-770 data sheet: https://www.3m.com (verify document for liquid suspension specs)
- Sutton & Graves, "A General Stagnation-Point Convective Heating Equation" (1959) — used for heat flux estimates

### References to verify before citing
*Anything that looked like a citation in `MANNA_POD_DESIGN_RESEARCH.md` v0.1 must be re-checked. Do not trust until web-fetched.*

---

## 12. Working with this repo

### When starting a new Claude Code session
1. Read this file end-to-end
2. Check `roadmap/` for current phase
3. Check `expert-reviews/` for any new findings
4. Check git log for recent commits
5. Then start work

### When delivering an artifact
1. Match the conventions in §5
2. Tag every numerical claim per §5.2
3. Include the variant context (which of H/I/B does this apply to?)
4. If it's a research-style document, run it past the Forensic Quality Gate from §7 before declaring done
5. If it requires persona review, follow `PERSONA_REVIEW_PROTOCOL.md`

### When something breaks
1. Don't escalate severity in language. Bugs are bugs. Outages are outages. Be precise.
2. Show the error verbatim.
3. Identify the smallest change that would fix it.
4. Fix it, don't theorize about it.

---

## 13. Notes for future Claude

This repo is part of an aerospace project that is genuinely novel and genuinely hard. It is also being built by a one-person team (Shane) with help from collaborators (Claude, eventually Scott Lukens for review, eventually domain experts as the work matures).

The author is **not asking for cheerleading.** He's asking for engineering rigor and forensic honesty. When the numbers don't close, say so. When the citation isn't verifiable, flag it. When the architecture has a problem (35° N → equatorial LEO), name it.

The author is **also not asking for paralysis.** Pre-Phase A concept work is allowed to have open questions. Tag them clearly, keep moving forward.

The author is dyslexic-adjacent and works primarily through voice-to-text on a commute. Prefer short blocks, clear headers, action items. Ambiguity is the enemy. Concreteness wins.

When in doubt, this is the test: **Would this output help Shane explain this concept to Scott Lukens (NASA/aerospace systems engineer, stepfather) in a 10-minute conversation, without misleading anyone, with all the open questions clearly labeled?** If yes, ship it. If no, fix it first.

---

## 14. Session log

| Date | Session | Author |
|------|---------|--------|
| 2026-04-24 | Three-variant taxonomy, v0.1 memo, Munk review, Protocol v1.0 | Shane + Claude (claude.ai) |
| 2026-04-25 | Trajectory simulator — RK4, US Std Atm 1976, all 3 variants | Shane + Claude Code |
| 2026-04-25 | Math verification (vis-viva velocities), NASA/SpaceX HTML redesign, 50/50 tests | Shane + Claude Code |
| 2026-04-25 | BC×elevation sweep (108 sims), Sutton-Graves heat flux, orbital-at-apogee, adaptive RK4 | Shane + Claude Code |

---

*Maintained by Shane Brazelton · Co-architected with Claude (Anthropic) · Hazel Green, Alabama*
*Operating under the [Constitution](https://github.com/thebardchat/constitution) · Pi before cloud · Faith first*

> *"Bread from heaven that the Israelites ate during their forty years..."* — Exodus 16:35
