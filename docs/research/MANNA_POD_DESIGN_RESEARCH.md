# Manna Pod Design Research — v0.1

> **STATUS: UNDER FORENSIC REVIEW — DO NOT TREAT AS VERIFIED**
> Seven issues flagged by Munk persona review.  See `CLAUDE.md §7` and
> `expert-reviews/manna-pod-design-persona-munk-v0.1.md`.

*Author: Shane Brazelton + Claude (Anthropic)  |  Date: 2026-04-24  |  Version: 0.1*

---

## 1  Concept Summary

The Manna system is an electromagnetic mass-driver (coilgun or railgun architecture)
that accelerates unpiloted cargo pods along a fixed ground-based rail, injecting them
into suborbital or LEO trajectories.  Target use cases:

- Humanitarian resupply to disaster zones (high-altitude airdrop)
- Pre-positioned orbital logistics (fuel, consumables)
- Rapid cargo delivery to remote stations

Three variants cover the mission envelope:

| Variant  | Payload mass | Max body diam | Intended apogee (v0.1 claim) |
|----------|-------------|--------------|-------------------------------|
| Manna-H  | ~500 kg     | 1.0 m        | **1,950 km** ⚠ [PLACEHOLDER]  |
| Manna-I  | ~150 kg     | 0.65 m       | **850 km**  ⚠ [PLACEHOLDER]   |
| Manna-B  | ~50 kg      | 0.40 m       | **247 km**  ⚠ [PLACEHOLDER]   |

> ⚠ All apogee figures are **vacuum estimates** computed with constant-g parabolic
> formula.  No drag model was applied.  See issue #1 in the Munk review.

---

## 2  Launch Architecture

The rail is mounted at a fixed elevation angle (15–45°, TBD by site constraints) and
launches pods via electromagnetic acceleration.  Key design parameters:

- **Rail elevation (nominal):** 30° above horizontal  [ESTIMATE]
- **Launch latitude:** 35°N  [PLACEHOLDER — site not selected]
- **Target delivery latitude:** Equatorial (0°)  [PLACEHOLDER]
- **Trajectory type:** Suborbital ballistic (intended); orbital capture (unconfirmed)

> ⚠ Issue #2 (Munk): A 35°N launch cannot reach an equatorial orbit without a
> plane-change ΔV of approximately 2–3 km/s.  This is not budgeted.

---

## 3  Trajectory Assumptions (v0.1 — BROKEN)

v0.1 used the closed-form constant-gravity parabolic equation:

```
h_apogee = (v_launch × sin θ)² / (2 × g₀)
```

with g₀ = 9.80665 m/s² constant, no atmosphere.

Launch velocities back-calculated to reproduce the claimed apogees:

| Variant  | v_launch (m/s) | θ (°) | v0.1 h_apogee (km) |
|----------|---------------|-------|---------------------|
| Manna-B  | 4,318         | 30    | 247                 |
| Manna-I  | 7,670         | 30    | 850                 |
| Manna-H  | 10,814        | 30    | 1,950               |

> ⚠ Issues:
> - No atmosphere → drag penalty not modeled → real apogees are lower.
> - Manna-H at 10,814 m/s has horizontal component 9,363 m/s > circular orbital
>   velocity (~7,905 m/s at sea level).  This is an orbital/escape trajectory,
>   not a suborbital ballistic hop.  See Munk issues #1 and #3.

---

## 4  Thermal Protection (v0.1 — DISPUTED)

v0.1 proposed PICA-X ablative heat shield for all variants based on SpaceX Dragon
heritage.  This was applied to protect the pod during **launch** (exit) through the
atmosphere.

> ⚠ Issue #4 (Munk): PICA-X is designed for **entry** (inbound, high-velocity
> deceleration).  The aerothermal environment on launch exit (outbound) is
> qualitatively different — shorter duration, lower peak heat flux per unit velocity
> because the vehicle is accelerating through the atmosphere rather than decelerating.
> The correct analysis is a stagnation-point heating budget for the exit trajectory;
> this has not been done.

---

## 5  Shock Isolation (v0.1 — DISPUTED)

v0.1 proposed an internal liquid suspension medium with density 15 g/cc to protect
cargo from launch G-forces.

> ⚠ Issue #5 (Munk): No commercially available suspension fluid exceeds ~4 g/cc
> (mercury is 13.6 g/cc but is toxic and impractical for cargo use).  The 15 g/cc
> figure appears to be a transcription or calculation error.  Even if achievable,
> a 15 g/cc filler would dominate mass budget.  This requires redesign.

---

## 6  Cost Model (v0.1 — UNDEFINED)

v0.1 cited a per-kg delivery cost of $80–$240/kg to suborbital apogee.

> ⚠ Issue #7 (Munk): No derivation, mass fraction, power budget, or amortization
> model supports this figure.  All cost claims are [PLACEHOLDER] until costed.

---

## 7  References

> ⚠ Issue #6 (Munk): The following citations were flagged as unverifiable in
> peer-reviewed literature.  They have been REMOVED from this document pending
> replacement with real sources.

*[Citations removed pending verification — see CLAUDE.md §7 issue #6]*

Confirmed real references:

- U.S. Standard Atmosphere, 1976. NOAA, NASA, USAF. Washington D.C.  [VERIFIED]
- Humble, R.W., Henry, G.N., Larson, W.J. (1995). *Space Propulsion Analysis and
  Design*. McGraw-Hill.  [VERIFIED]
- Wertz, J.R., Everett, D.F., Puschell, J.J. (2011). *Space Mission Engineering: The
  New SMAD*. Microcosm Press.  [VERIFIED]

---

*v0.1 produced: 2026-04-24.  Forensic review completed same session.*
*v0.2 (corrected) will incorporate trajectory simulator output and Munk issue resolutions.*
