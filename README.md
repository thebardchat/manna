# Manna

Electromagnetic mass-driver cargo delivery system — three-variant suborbital/LEO pod design.

> Built by Shane Brazelton + Claude (Anthropic) · Runs on Raspberry Pi 5

---

## Variants

| Variant  | Role              | Launch v (m/s) | BC (kg/m²) |
|----------|-------------------|----------------|------------|
| Manna-B  | Basic / budget    | 4,318          | ~1,591     |
| Manna-I  | Intermediate      | 7,670          | ~1,789     |
| Manna-H  | Heavy / bulk      | 10,814         | ~2,264     |

## Quick start

```bash
pip install -r requirements.txt
python simulation/src/trajectory_sim.py
pytest simulation/tests/
```

Plots saved to `simulation/data/trajectory_runs/`.

---

## Status

v0.1 design memo is **under forensic review** — 7 issues flagged.  See `CLAUDE.md §7`.
The trajectory simulator is the primary tool for resolving issue #1 (broken trajectory math).

---

*[@thebardchat](https://github.com/thebardchat) · Hazel Green, Alabama · 2026*

> Try Claude: https://claude.ai/referral/4fAMYN9Ing
