# Handover: FYP (aerogel thermal simulator, PolyU AAE capstone 2026/27)

Updated 2026-11-13. Master handover for all projects and sessions: `saul-gitman/MyMCP`, `docs/HANDOVER.md`.

## What you wanted to build (verbatim, 29 Oct 2026, spelling tidied)
> here are some context for my final year project in exchange in polyu, i am build a simulation tool, build that for me, give a plan first. i will steer you when the council AI is available, you have to use the council to debate with gpt and qwen, give them some context a plan first. until the council is ready, u extract and gather information first, after council works, u throw the context, and debate with 6sol (high), and qwen next (max), and tell them to judge you.

So: a simulation tool for the FYP, plan first, then have the plan debated and judged by two other models through the council MCP (GPT "6sol" at high effort, then Qwen at max effort).

## The project
*Thermo-optically functional CFRP laminates for lightweight electrified systems* (supervisor Dr CHAN Kit-Ying; interim report 21 Dec 2026; final April 2027). Stack: BN/CNF/MTMS freeze-cast aerogel surface → CFRP → CNT/CNF/MTMS aerogel interlayer → CFRP, heater on the back. The tool covers structure → properties (steps 2→3 of processing → structure → properties). Supervisor guidance: aerogel alone first, simple idealised geometry, one fixed composition then vary pore size, along and across the alignment, compare trends and not absolute numbers.

Plan `docs/PLAN.md` (v0.2, plus `docs/COUNCIL_SETUP.md` for the council orchestration notes): Python 3, NumPy/SciPy finite-volume, YAML inputs labelled measured / literature / derived / hypothetical, pytest verification suite, auto report. v0.1 core (before 21 Dec): cell geometry, derived porosity and density, axial plus transverse conduction, Knudsen gas, wall-mixture bounds, pore-size sweep. v0.2 radiation and 3D; v0.3 composition; v1.0 laminate. Expected early flag: with porosity fixed, pure conduction barely changes with pore size, so pore-size effects come from radiation and gas rarefaction.

## State
- **v0.1 built on `main` (2026-11-15):** `aerosim/` backend (13 method files), web UI, tests in `.agent/tests/`, physics in `docs/PHYSICS.md`. See README.md.
- The council step stalled on 29 Oct: council returned metadata only (no answer text) and "GPT 6.1 sol" was not on the server. Open decision: use a stand-in model (sends the brief off-hardware) or wait. Later commits record the Legion MCP connection test results and corrected council model names.
- `guide/` holds the contents of the handover zip `FYP_Handover_2026-10-29.zip`.

## Change log
| Date | Commit | Change |
|---|---|---|
| 10-29 | `e552301` | Simulator build plan and council review brief |
| 10-29 | `84ef349` | Plan and brief revised against the meeting transcript; council setup notes |
| 10-29 | `e2a9de5`, `9f2105b` | Handover zip contents under `guide/`; Legion MCP test results; corrected council model names |
| 10-30 | `587239f`, `8c01bcb` | GNSS Lab 1 folder: data, processing, report, GIFs, figures, benchmark baseline (removed from this repo on 11-15 in `a72c77a`; it lives in `AAE-4004-lab`) |
| 11-13 | handover | `main` created by merging both branches above, plus this file |
| 11-15 | `da8de1a` … `8f10105` | Design session merged; v0.1 simulator built (`aerosim/`, `web/`, `.agent/`) |
| 11-15 | `a72c77a` | AAE4203 GNSS Lab 1 folder removed (unrelated coursework) |
| 11-19 | docs | `docs/FUTURE_WORK.md`: honeycomb slice model (corrected proof, bounds, not built) and a report checklist; check script `.agent/checks/slice_model_check.py` |

## Sessions
`session_0143oVsKsbxuFFSfjRSorAqD` PolyU exchange simulation tool (10-29, blocked on council) ·
`session_0143oVsH2r1sHdcV9Yt4RkuJ` PolyU exchange project setup and pore-size study plan (10-29, blocked on council) ·
`session_0143oVsJAkHdZm66bSpB3Fny` UBX data processing and 3D visualization (10-30, pushed here and to AAE-4004-lab) ·
`session_0143oVsGXh4V8fwmnWfhskgN` Repository memory search (11-12).

## Branches
Before this handover the repo had no `main`; GitHub's default branch is still `claude/compassionate-lamport-ff9nt6` (plan only). Set the default to `main` in Settings, Branches. The old `claude/*` branches (`admiring-pascal`, `quirky-thompson`, `compassionate-lamport`, `beautiful-tesla`, `gifted-volta`) are merged and can be deleted. `quirky-thompson` and `beautiful-tesla` still contain the removed GNSS lab folder.
