# MANNA

> **Modular Aerospace Necessities & Nutrient Asset**
> Cargo pods for the BGKPJR launch architecture — three viable variants for unmanned lunar resupply.

[![Constitution](https://img.shields.io/badge/Constitution-ShaneTheBrain-blue)](https://github.com/thebardchat/constitution)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Phase](https://img.shields.io/badge/Phase-Design%20Research-orange.svg)](docs/research/MANNA_POD_DESIGN_RESEARCH.md)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org)

---

## What is Manna?

Manna is the **unmanned cargo pod** that rides the [BGKPJR](https://github.com/thebardchat/BGKPJR-Core-Simulations) maglev rail to sub-orbital trajectory, where an in-orbit Tug catches it and ferries it to the Lunar Base.

Where Gryphon (BGKPJR's crewed spacecraft) is limited to 4G acceleration on the rail because of the human payload, Manna can take 8–100G depending on cargo class. That unlocks much higher exit velocity, smaller propellant fraction, and dramatically lower cost per kg.

This repo contains the design research, simulations, and CAD for three Manna pod variants.

---

## The three variants

| Variant | Cargo Class | Payload Mass Fraction | Internal G | Cost/kg |
|---|---|---|---|---|
| **Manna-H** (Hardened) | Bulk consumables, propellant, food, metals | 78% | 100 G | $54/kg |
| **Manna-I** (Isolated) | Electronics, instruments, mech spares | 54.8% | 5.5 G | $467/kg |
| **Manna-B** (Biological) | Seedlings, microbiomes, biologics | 18.6% | 2.5 G | $4,190/kg |

Mission target — **$200/kg to lunar surface in steady-state operations**.

For full design rationale, physics, and trade studies, see:
**[docs/research/MANNA_POD_DESIGN_RESEARCH.md](docs/research/MANNA_POD_DESIGN_RESEARCH.md)**

---

## Quick start

```bash
# Clone
git clone https://github.com/thebardchat/manna.git
cd manna

# Setup
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run pod dynamics simulation
python simulation/src/pod_dynamics.py --variant H

# Run cargo manifest optimizer
python simulation/src/manifest_optimizer.py --cargo-list manifests/example.csv
```

---

## Repository layout

See [docs/research/MANNA_POD_DESIGN_RESEARCH.md §9](docs/research/MANNA_POD_DESIGN_RESEARCH.md#9-recommended-manna-repo-structure) for the full structure.

---

## Status

- [x] Design research paper — three viable variants specified
- [ ] Pod dynamics simulator — 6-DOF rail-to-catch model
- [ ] Manna-I shock isolation FEA
- [ ] Manna-B liquid suspension benchtop validation
- [ ] CAD models (FreeCAD) for all three variants
- [ ] Manifest optimizer with cargo G-rating database
- [ ] Tug interface specification (coordinate with future tug repo)

---

## Ecosystem

| Repo | Connection |
|---|---|
| [BGKPJR-Core-Simulations](https://github.com/thebardchat/BGKPJR-Core-Simulations) | The maglev rail Manna launches from |
| [shanebrain-core](https://github.com/thebardchat/shanebrain-core) | Compute backbone for simulation runs |
| [constitution](https://github.com/thebardchat/constitution) | Engineering and ethics framework |

---

## License

Apache-2.0. See [LICENSE](LICENSE).

---

*Built by **Shane Brazelton** · Co-built with **Claude** (Anthropic) · Hazel Green, Alabama*

*Part of the [ShaneBrain Ecosystem](https://github.com/thebardchat) · Operating under the [Constitution](https://github.com/thebardchat/constitution)*
