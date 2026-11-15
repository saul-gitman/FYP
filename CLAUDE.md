# CLAUDE.md: rules for agents working in this repo

**Project:** Aerogel k Simulator, the FYP simulation tool (PolyU AAE capstone 2026/27, supervisor Dr CHAN Kit-Ying). It predicts the thermal conductivity of a dry freeze-cast honeycomb aerogel skeleton, along (k∥) and across (k⊥) the channels, as separate heat paths: k_total = k_solid + k_gas + k_rad + k_conv.

## Read first
1. `idea.json`: the full design-session record (why everything is the way it is)
2. `docs/DESIGN.md`: UI, backend method table, folder structure, method-file contract
3. `docs/PLAN.md`: physics, sources, meeting constraints (§0a), timeline
4. `.agent/SUBAGENT_GUIDE.md`: the complete context pack handed to build agents

## Rules
- **Branch:** work on `main` (the user's instruction, 2026-11-15).
- **Skill:** follow the Ponytail skill (`.agent/skills/ponytail/SKILL.md`, level *full*): smallest complete change, reuse before writing, no unasked features.
- **README backend table must stay in sync:** whenever a method file under `aerosim/<row>/` is added, changed (name, level, equation, inputs, source) or removed, update the **Backend methods** table in `README.md` in the same commit. Also update `docs/DESIGN.md` §2 if the change affects the design.
- **Tests and checks live in `.agent/`:** pytest suite in `.agent/tests/`, checker scripts and screenshots in `.agent/checks/`. Run `python -m pytest` before every commit.
- **Method-file contract:** every file in `aerosim/<row>/` (not starting with `_`) follows `_template.py`: `NAME, LEVEL, ORDER, HELP, EQUATION, SOURCE, COST, INPUTS, run()`. Every input has `value, unit, status, source, help`. `.agent/tests/test_contract.py` enforces this. All UI words come from these variables or `aerosim/core/ui_text.py`. The front end has no hard-coded physics or labels.
- **Scope (v0.1):** structure = Honeycomb and Honeycomb + defects only. The Material row is a placeholder until the user decides.
- **Honesty:** never invent material constants. Every number has a source or a `hypothetical` status. Do not tune inputs to match literature values; report gaps. Count each heat path once (no double counting when a method resolves several paths).
- **Do not touch** `guide/` (handover pack, read-only) or `AAE4203_GNSS_Lab1/` (separate coursework).
- Commit messages and code must not contain model identifiers.
