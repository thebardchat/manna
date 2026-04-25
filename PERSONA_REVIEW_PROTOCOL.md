# Persona Review Protocol v1.0

> Governance document for expert-persona forensic reviews in the manna project.
> Ratified: 2026-04-24.  Version: 1.0.

---

## Purpose

When a design document is produced quickly (as in a single-session design memo), it is
likely to contain errors that only surface under domain-specific scrutiny.  The Persona
Review Protocol creates structured adversarial review by having Claude embody a named
expert persona and produce a forensic critique — not a promotional summary.

---

## Process

1. **Select a Persona** — Choose a recognized expert type appropriate to the material
   (e.g., astrodynamicist, materials engineer, systems integrator).  Name the persona
   (e.g., "Munk" for a trajectory/aerodynamics expert).

2. **Assign the Task** — The persona is asked to:
   - Read the target document in full
   - Identify every numerical claim that appears unverified
   - Identify every physics assumption that could be wrong
   - Call out missing models, undefined variables, fabricated citations
   - Produce a numbered list of issues, each with: *finding*, *why it matters*,
     *what is needed to resolve it*

3. **Review is Forensic, Not Promotional** — The persona's job is to find real
   problems.  A review that finds no issues is automatically suspect.

4. **Versioned Output** — Review files are named:
   `expert-reviews/<document-slug>-persona-<name>-<doc-version>.md`

5. **Issues Logged** — All issues found MUST be logged in `CLAUDE.md §7` so they
   persist across sessions.

6. **Resolution Tracking** — Each issue gets a checkbox in `CLAUDE.md §10` roadmap.

---

## Validity

A review is authoritative only if:
- It names the Persona Review Protocol version it follows (this document, v1.0)
- It was produced in the same session as or immediately after the document it reviews
- Issues are numbered and individually actionable

---

## Example Persona: "Munk"

Named for Walter Munk (1917–2019), physical oceanographer and geophysicist — a figure
known for relentlessly questioning assumptions in numerical models.

In the manna project, the Munk persona represents a rigorous astrodynamics / applied
physics reviewer who will not accept:
- Vacuum trajectory claims presented as operational estimates
- Missing atmosphere models
- Fabricated or unverifiable citations
- Undefined cost or mass assumptions

---

*Protocol ratified by Shane Brazelton + Claude (Anthropic), 2026-04-24.*
