# CLAUDE.md — tug repo
### Context file for Claude Code sessions in the `tug` repo
**Last updated:** 29 April 2026
**Maturity:** Pre-Phase A concept memorandum
**Operating under:** [ShaneTheBrain Constitution](https://github.com/thebardchat/constitution) · [Persona Review Protocol v1.0](https://github.com/thebardchat/manna/blob/main/PERSONA_REVIEW_PROTOCOL.md)

---

## 1. What this repo is

`tug` defines the **reusable orbital Tug** — the transfer vehicle that catches
Manna cargo pods at apogee and ferries them to the Lunar Base.

The Tug is the middle link in the ShaneTheBrain lunar cargo chain:

```
BGKPJR rail → Manna pod → [TUG] → Lunar Base
```

**Status:** Pre-Phase A.  One concept document exists (`docs/TUG_CONCEPT.md`).
No design has been committed.  All numbers are `[ESTIMATE]` or `[DERIVED]`.

---

## 2. Where this fits in the ecosystem

```
        ┌──────────────────────┐
        │  BGKPJR-Core-Sims    │  Maglev rail, 28.7 km, Hazel Green AL
        └──────────┬───────────┘
                   │ launches
                   ▼
        ┌──────────────────────┐
        │      manna           │  Cargo pod family (H / I / B variants)
        └──────────┬───────────┘
                   │ caught by
                   ▼
        ┌──────────────────────┐
        │       tug            │  ← THIS REPO
        │  (transfer vehicle)  │
        └──────────┬───────────┘
                   │ delivers to
                   ▼
        ┌──────────────────────┐
        │   Lunar Base         │  Out of scope for these repos
        └──────────────────────┘
```

---

## 3. Hardware / infrastructure (Shane's, not the Tug's)

| Component | Detail |
|---|---|
| **Compute** | Raspberry Pi 5 (16 GB RAM) · Pironman 5-MAX chassis |
| **Storage** | 2× WD Blue SN5000 2 TB NVMe — RAID 1 via mdadm |
| **Core path** | `/mnt/shanebrain-raid/shanebrain-core/` |
| **Pi Tailscale IP** | `100.67.120.6` — use directly, never MagicDNS |
| **Pulsar0100 (Windows / N8N)** | `100.81.70.117` |
| **bullfrog-max-r2d2** | `100.87.222.17` |
| **laptop-ts6v7fna** | `100.94.122.125` |
| **FastMCP** | port 8008 |
| **Weaviate** | port 8080 |
| **Ollama** | port 11434 |

**Networking rule:** Always use Tailscale IPs directly. MagicDNS is unreliable.

---

## 4. Repo layout

```
tug/
├── README.md
├── CLAUDE.md                    # ← YOU ARE HERE
├── docs/
│   └── TUG_CONCEPT.md           # ✅ Reference concept v0.1 (10 sections)
├── simulation/                  # NOT YET CREATED — GMAT / Python trajectory work goes here
├── design/                      # NOT YET CREATED — CAD, block diagrams
├── interfaces/                  # NOT YET CREATED — ICD stubs
└── expert-reviews/              # NOT YET CREATED — persona reviews when ready
```

---

## 5. Conventions

### 5.1 Code style
- Python 3.10+, PEP 8, type hints encouraged
- All physics math: show the equation, then the numerical result
- All simulation outputs: include input parameters in output filename or header

### 5.2 Documentation style
- Match manna's voice: technical, direct, ASCII diagrams when they help
- Sentence case in headings
- Tables for trade studies, not prose
- Every numerical claim tagged: `[VERIFIED]`, `[DERIVED]`, `[ESTIMATE]`, or `[PLACEHOLDER]`
- No fabricated citations. Unverifiable → `[CITATION NEEDED]`

### 5.3 Tug is one vehicle (no variants yet)
- Do not split into sub-variants without explicit direction from Shane
- If a propulsion trade or size trade creates distinct configurations, name them explicitly

---

## 6. Author's preferences (apply to every session)

- **Zero preamble.** No "I'd be happy to." Straight to the answer.
- **If something won't work, say so immediately.** Then give the alternative.
- **ADHD-friendly format.** Short blocks. Checkboxes for multi-step tasks.
- **Pragmatic and technical.** Solutions over explanations.
- **Be proactive.** Anticipate needs. Suggest unprompted.
- **Faith, family, sobriety are non-negotiable values.**
- **Local-first.** Pi before cloud. Ollama before OpenAI. Weaviate before Pinecone.
- **Decode garbled voice-to-text input** rather than asking for clarification.
- **PARTNER DIRECTIVE:** If asked "Is there a way?" and YES + best solution exists, say so immediately.

---

## 7. Open blockers (from TUG_CONCEPT.md §8)

These are Pre-Phase A blockers.  Nothing else can proceed until these resolve.

| # | Blocker | Gates |
|---|---------|-------|
| 1 | Pod apogee altitude undefined — depends on manna BC redesign | Tug orbit shape, ΔV budget |
| 2 | No pod docking port design | Capture mechanism design |
| 3 | Pod GNC undefined (does pod have attitude control?) | Catch window analysis |
| 4 | Catch window analysis not performed | Capture mechanism aperture |
| 5 | TLI ΔV not computed (requires specific orbit hardened) | Propellant budget, vehicle mass |
| 6 | Refueling architecture not designed | Operational concept |
| 7 | Capture mechanism at TRL 1–2 | Highest risk item — technology maturation path needed |
| 8 | No propulsion trade study (chemical vs. electric) | Vehicle mass, cadence |

**Blocker 1 is gated on `manna`.**  Watch `thebardchat/manna` for BC feasibility
study closure before driving Tug orbit design.

---

## 8. Key known constraints

- **Tug orbit inclination must be ~35°** — matching BGKPJR rail latitude (34.93°N).
  Equatorial orbit costs 4,620 m/s plane change — not viable.  [DERIVED]

- **Rendezvous is at sub-m/s closing rate, not 4 km/s.**  At apogee, the pod's
  horizontal velocity is ~8–19% of circular orbital velocity.  The Tug matches
  this slow speed via phasing orbit + RCS.  The v0.1 manna memo described a
  4 km/s catch — that was an impact description, not rendezvous.  [CORRECTED]

- **Tug must be launched on a conventional rocket** (not the BGKPJR rail).
  The rail launches uncrewed cargo pods, not a complex crewed/reusable vehicle.

- **Refueling dependency:** Tug propellant is resupplied via Manna-H propellant
  pods.  Tug must have enough reserve to catch the first resupply pod —
  bootstrapping sequence not yet designed.

---

## 9. Things to NEVER do

- **Never confuse Tug with Manna.** Tug is the catcher and transfer stage.
  Manna is the pod. They are different vehicles with different design drivers.
- **Never design the Tug to catch pods at high relative velocity.**
  Berthing happens at sub-m/s.  Anything else is a collision.
- **Never assume equatorial orbit.** Tug lives at ~35° inclination.
- **Never publish a citation without verifying it.**  Web-fetch or NTRS.
- **Never push to main without running any available tests.**
- **Never add cloud dependencies when local works.**

---

## 10. Frequently used commands

```bash
# (When simulation exists)
python simulation/src/tug_trajectory.py     # Tug orbit + rendezvous analysis
python simulation/src/delta_v_budget.py     # ΔV trade
pytest simulation/tests/ -v                 # Run tests

# Reference: manna BC feasibility (run from manna repo)
python simulation/src/bc_feasibility.py    # Pod apogee closure study
```

---

## 11. Current state and next moves

### What exists right now
- [x] `docs/TUG_CONCEPT.md` — reference concept v0.1 (10 sections)
- [x] `README.md`

### Priority order
1. **Wait for manna BC feasibility closure** — pod apogee altitude must harden before Tug orbit can be designed (Blocker 1)
2. **TLI ΔV trade** — run GMAT or Python vis-viva for Hohmann from ~35°/200 km parking orbit to C3 ≥ 0 (lunar transfer)
3. **Propulsion trade** — chemical vs. electric; inputs are cadence assumption + mass budget
4. **Catch window analysis** — rail pointing accuracy → pod apogee position dispersion → capture mechanism aperture
5. **Functional block diagram** — one page, all subsystems named, interfaces drawn
6. **ICD stubs** — ICD-TUG-001 (pod-to-Tug capture interface), ICD-TUG-002 (Tug-to-lunar-stage)
7. **ConOps draft** — 3–5 pages, mission timeline, go/no-go criteria per phase transition

---

## 12. References (verified)

- [manna repo](https://github.com/thebardchat/manna) — cargo pod family  [VERIFIED]
- [BGKPJR-Core-Simulations](https://github.com/thebardchat/BGKPJR-Core-Simulations) — rail  [VERIFIED]
- [ShaneTheBrain Constitution](https://github.com/thebardchat/constitution)  [VERIFIED]
- NASA GMAT: https://software.nasa.gov/software/GSC-17177-1  [VERIFIED]
- US Standard Atmosphere 1976: NASA-TM-X-74335  [VERIFIED]
- Wertz, Everett, Puschell (2011). *Space Mission Engineering: The New SMAD.* Microcosm Press.  [VERIFIED]
- Humble, Henry, Larson (1995). *Space Propulsion Analysis and Design.* McGraw-Hill.  [VERIFIED]

---

## 13. Session log

| Date | Session | Author |
|------|---------|--------|
| 2026-04-28 | TUG_CONCEPT.md v0.1 — orbit definition, rendezvous architecture, ΔV budget, ICD stubs, 8 blockers | Shane + Claude (manna session) |
| 2026-04-29 | CLAUDE.md initialized | Shane + Claude |

---

*Maintained by Shane Brazelton · Co-architected with Claude (Anthropic) · Hazel Green, Alabama*
*Operating under the [Constitution](https://github.com/thebardchat/constitution) · Pi before cloud · Faith first*
