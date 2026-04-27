# HUV Trajectory Test — Results
**Tube reference:** BGKPJR rail, L = 28.7 km  [VERIFIED — CLAUDE.md §1]
**Simulator:** `simulation/src/trajectory_sim.py` (RK4, US Std Atm 1976, flat-Earth, varying-g)
**Heat flux model:** Sutton-Graves (1959) [CONSTRAINT-NOT-MODELED — R_nose = 5 cm assumed]

## Peak G-load required (constant-acceleration tube model)
| Variant | v_exit | Tube L | Peak a | Peak G |
|---|---|---|---|---|
| HUV-25 | 8508 m/s | 28.7 km | 1261 m/s² | **129 G** |
| HUV-20 | 6806 m/s | 28.7 km | 807 m/s² | **82 G** |

## Trajectory simulation results
| Variant | El° | BC kg/m² | Sim apogee (km) | Vacuum apogee (km) | sim/vac | vx@apo (m/s) | v_circ@apo | vx/vc | Peak HF (GW/m²) | Orbital flag |
|---|---|---|---|---|---|---|---|---|---|---|
| HUV-25 | 15 | 17684 | 33.8 | 257.2 | 0.131 | 2447 | 7883 | 0.310 | 0.56 | no |
| HUV-25 | 30 | 17684 | 305.4 | 1078.8 | 0.283 | 4094 | 7721 | 0.530 | 0.56 | no |
| HUV-25 | 45 | 17684 | 929.9 | 2597.3 | 0.358 | 3977 | 7384 | 0.539 | 0.56 | no |
| HUV-20 | 15 | 17684 | 24.5 | 162.2 | 0.151 | 1894 | 7889 | 0.240 | 0.29 | no |
| HUV-20 | 30 | 17684 | 193.9 | 650.7 | 0.298 | 3269 | 7787 | 0.420 | 0.29 | no |
| HUV-20 | 45 | 17684 | 567.1 | 1449.5 | 0.391 | 3181 | 7574 | 0.420 | 0.29 | no |
| Manna-H | 15 | 2264 | 3.5 | 426.9 | 0.008 | 296 | 7902 | 0.037 | 1.15 | no |
| Manna-H | 30 | 2264 | 9.1 | 1950.0 | 0.005 | 258 | 7899 | 0.033 | 1.15 | no |
| Manna-H | 45 | 2264 | 18.6 | 5620.2 | 0.003 | 308 | 7893 | 0.039 | 1.15 | no |

## Tags
- All sim outputs: [DERIVED]
- HUV mass / diameter / Cd0 / v_exit: [ESTIMATE] from concept doc
- Vacuum apogee column: [PLACEHOLDER] — paper-style claim, no atmosphere
- Peak heat flux: [CONSTRAINT-NOT-MODELED] — Sutton-Graves only, no real-gas chemistry, no shock-layer radiation
