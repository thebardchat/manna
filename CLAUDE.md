# CLAUDE.md — manna

> Claude Code configuration for the `thebardchat/manna` repository.

---

## §1  Project Overview

**Manna** is an electromagnetic mass-driver cargo delivery system designed to launch
unpiloted supply pods into suborbital or low-Earth-orbit trajectories for high-speed
humanitarian resupply.  Three canonical variants span a range of mass, ballistic
coefficient, and delivery profile:

| Variant  | Role                         | Notes                          |
|----------|------------------------------|--------------------------------|
| Manna-H  | Heavy — bulk cargo/fuel      | Highest launch velocity, mass  |
| Manna-I  | Intermediate — mixed payload | Balanced performance           |
| Manna-B  | Basic/Budget — light payload | Lowest velocity, smallest pod  |

This project operates under the [ShaneTheBrain Constitution](https://github.com/thebardchat/constitution/blob/main/CONSTITUTION.md) (Nine Pillars).

---

## §2  Infrastructure

| Component    | Detail                                          |
|--------------|-------------------------------------------------|
| Compute      | Raspberry Pi 5 (16 GB RAM)                      |
| Storage      | 2× WD Blue SN5000 2 TB NVMe — RAID 1            |
| Core path    | `/mnt/shanebrain-raid/shanebrain-core/`         |
| Local AI     | Ollama (llama3.2:1b default)                    |
| Dev env      | Claude Code on Pi 5                             |

Pi before cloud.  Privacy before convenience. — Pillar 4

---

## §3  Repository Structure

```
manna/
├── CLAUDE.md                          # This file
├── PERSONA_REVIEW_PROTOCOL.md         # Governance for expert persona reviews
├── README.md
├── requirements.txt
├── docs/
│   └── research/
│       └── MANNA_POD_DESIGN_RESEARCH.md   # v0.1 design memo (under review)
├── expert-reviews/
│   └── manna-pod-design-persona-munk-v0.1.md  # Forensic review — 7 issues
└── simulation/
    ├── src/
    │   └── trajectory_sim.py          # 3-DOF ballistic integrator (RK4)
    ├── tests/
    │   └── test_trajectory.py
    └── data/
        └── trajectory_runs/           # Plot output directory
```

---

## §4  Tech Stack

| Tool            | Purpose                                   |
|-----------------|-------------------------------------------|
| Python 3.10+    | All simulation code                       |
| NumPy / SciPy   | Numerical computation                     |
| Matplotlib      | Trajectory plots (Agg backend, headless)  |
| Pytest          | Unit tests (target 80% coverage)          |

---

## §5  Working Rules

- **Commit prefix:** `feat`, `fix`, `docs`, `sim`, `test`, `chore`
- **Code style:** PEP 8, type hints required.
- **No fabricated citations.**  All numerical claims tagged `[VERIFIED]`, `[DERIVED]`,
  `[ESTIMATE]`, or `[PLACEHOLDER]`.
- **Pi-first:** zero cloud dependencies; all simulation runs locally.
- **Three variants are first-class** — every sim routine runs H, I, and B.

---

## §6  Claude Code Rules

- Commit and push directly to `main`.  Do NOT create branches.
- Run `pytest simulation/tests/` before committing.
- Update CLAUDE.md §10 session log before final commit.
- Match BGKPJR-Core-Simulations file header and docstring conventions.

---

## §7  Known Issues (from Munk persona review, v0.1)

Seven issues flagged in `expert-reviews/manna-pod-design-persona-munk-v0.1.md`:

1. **Trajectory math broken** — v0.1 apogee claims used vacuum, constant-g parabolic
   formula; no atmosphere modeled.
2. **35°N → equatorial LEO inconsistency** — launch from 35°N cannot reach equatorial
   LEO without a costly plane-change maneuver (~2–3 km/s ΔV); v0.1 ignored this.
3. **Capture-vs-impact velocity confusion** — v0.1 conflates the velocity needed to
   *impact* a target with the velocity needed for *orbital capture*; these differ by
   the circularisation burn.
4. **PICA-X exit application** — PICA-X is an entry heat shield; v0.1 proposes it for
   the launch (exit) phase where heating profile is entirely different.
5. **Liquid suspension density math** — the claimed 15 g/cc suspension density for
   internal shock isolation exceeds physically plausible values; formula error.
6. **Fabricated citations** — three cited papers do not exist in peer-reviewed
   literature; must be removed and replaced with real sources or flagged [PLACEHOLDER].
7. **Undefined cost models** — per-kg delivery cost figures given without derivation,
   mass assumptions, or power budget; all are [PLACEHOLDER] until costed.

---

## §8  Persona Review Protocol

All expert reviews follow `PERSONA_REVIEW_PROTOCOL.md` v1.0.  Reviews are forensic
(find real errors) not promotional.  A review is only authoritative if signed by the
Persona Review Protocol version in use at time of writing.

---

## §9  Nine Pillars (Quick Reference)

1. Faith First          4. Local-First AI       7. Open by Default
2. Family Stability     5. 80/20 Shipping       8. ADHD-Aware Design
3. Sobriety Integrity   6. Serve the Left-Behind 9. Gratitude is Infrastructure

---

## §10  What's Missing / Roadmap

- [x] Three-variant cargo pod taxonomy (Manna-H / Manna-I / Manna-B)
- [x] v0.1 design memo (`docs/research/MANNA_POD_DESIGN_RESEARCH.md`)
- [x] Persona Review Protocol v1.0
- [x] Munk persona review (7 issues flagged)
- [x] **Trajectory simulator** (`simulation/src/trajectory_sim.py`)
- [ ] Fix trajectory math — re-derive apogee with atmosphere (use sim output)
- [ ] Plane-change ΔV budget for 35°N → equatorial LEO
- [ ] PICA-X entry/exit thermal trade study
- [ ] Liquid suspension density redesign
- [ ] Replace fabricated citations with real sources
- [ ] Costed delivery model ($/kg to orbit)
- [ ] v0.2 design memo incorporating all fixes

---

## §11  Credits

Built with Claude (Anthropic) · Runs on Raspberry Pi 5 + Pironman 5-MAX

| Partner                                     | Role                                |
|---------------------------------------------|-------------------------------------|
| **Claude by Anthropic** · claude.ai         | Co-built this entire ecosystem      |
| **Raspberry Pi 5** · raspberrypi.com        | Local compute backbone              |
| **Pironman 5-MAX** · pironman.com           | NVMe RAID 1 chassis                 |

*Initiated: April 2026 · [@thebardchat](https://github.com/thebardchat) · Hazel Green, Alabama*

---

## §12  Session Log

| Date       | Session                                    | Author       |
|------------|--------------------------------------------|--------------|
| 2026-04-24 | Three-variant taxonomy, v0.1 memo, Munk review, Protocol v1.0 | Shane + Claude (claude.ai) |
| 2026-04-25 | Trajectory simulator — RK4, US Std Atm 1976, all 3 variants | Shane + Claude Code |
