# Handover: FYP (aerogel thermal simulation, PolyU AAE capstone 2026/27)

Updated 2026-11-24. Master handover for all projects and sessions: `saul-gitman/MyMCP`, `docs/HANDOVER.md`.

## What you are building
- **Project:** *Thermo-optically functional CFRP laminates for lightweight electrified systems* (supervisor Dr CHAN Kit-Ying). Interim report 21 Dec 2026, final report 16 Apr 2027, oral 19–21 Apr 2027.
- **Experiment this semester:** six laminates, L1–L5 and a plain reference P, made with two fixed slurries: B10 (BN surface aerogel) and C2.5 (CNT interlayer), both with CNF and MTMS. Measured: through-thickness thermal resistance, heater temperature with a 2 W heater in the dark, under 1000 W/m² of sun, and both together; solar reflectance from 300 to 2500 nm.
- **Simulation:** how well the freeze-cast aerogel layer conducts heat, from its recipe and its structure; later, how the six specimens heat up. Two pieces of code, kept apart on purpose:

| Piece | What it is | Where | State |
|---|---|---|---|
| aerosim (HTML app) | v0.1 web tool. One row per heat path (solid, gas, radiation, convection), each with a fast formula and a detailed pixel method, for a dry honeycomb aerogel. The wall conductivity is one borrowed number, 4.0 W/m·K, back-calculated from Chan et al. 2022. | repo root today (`aerosim/`, `web/`, `docs/`, `.agent/`, `results/`); moving to `aerosim_html/` | built 2026-11-15; 53 tests pass |
| K_cond GPU solver | One Python file for Google Colab (GPU) or any computer. Step 1 builds a 3-D voxel model of one cell wall (BN sheets or CNT rods, CNF and PMSQ glue, pores, contact resistances) and computes the wall conductivity from the recipe. Step 2 puts that wall into the honeycomb at its true thickness (cells empty, air or epoxy) and gives the layer conductivity along the channels, across them and through the plate. | `K_cond_GPU_solver/colab_k_cond.py` | first version 2026-11-24 |

Why two pieces: the HTML app explains each heat path and stays light (NumPy + SciPy, runs anywhere). The GPU solver computes the one number the app was missing, the wall conductivity for the real recipe. It needs heavy compute, so it lives on its own, and its result goes back into the app later (the app's Material row).

## Repo layout
- **Decided 2026-11-24:** `aerosim_html/` (the app, code unchanged), `K_cond_GPU_solver/` (solver, plan, input/output list), `report/` (the FYP report folder from OneDrive), `guide/` (handover pack, read-only).
- **On GitHub now:** `K_cond_GPU_solver/` is pushed; the app is still at the root. The move into `aerosim_html/` (63 renames, 5 of them PNG screenshots) could not be pushed from the session: its git commits were refused by the session's permission check, and the hub's GitHub connection writes file contents only (no moves, no images). The move is ready as `fyp-repo-split.patch`: apply it to `main` from a local clone (`git apply --index fyp-repo-split.patch`, then commit and push). After that, `CLAUDE.md` and this file describe the new layout.

## State and first results (2026-11-24)
- **Solver checks:** quick CPU mode runs in about 30 s and every built-in check passes: uniform and layered boxes exact, interface resistance exact, slice closed form, finite-element honeycomb benchmark (11.155 / 11.141 against 11.17 / 11.18 W/m·K), Hashin–Shtrikman bounds, energy balance. The app's own Pixel FV solver, run on freshly drawn pictures, trends to the same values. Not yet run on a GPU.
- **Headline, and a warning:** with today's guessed inputs the wall comes out at about 60 W/m·K (quick grid, not converged; about 70 at 5 nm voxels). That is 15 times the 4.0 W/m·K worked back from Kit's measured aerogel, so real walls conduct far worse than this ideal model.
- **What drives the wall value (quick sensitivity, swing of the result):** sheet-to-sheet contact resistance 166 %, BN in-plane conductivity 81 %, sheet tilt 61 %, sheet diameter 56 %, empty space in the wall 48 %. Measure these first.
- **Composition:** "B10" dries to a wall of 83 wt% (77 vol%) BN; C2.5 solids are about 56 wt% CNT.
- **Dry vs resin-filled:** with epoxy in the cells the layer conducts about 230 mW/m·K across the channels, against about 61 dry. The formulas are enough there (their bounds are 12 % apart), so the GPU is only needed for dry layers. If resin gets into the BN top layer of L1 or L2, that layer stops insulating.
- **Wall density puzzle:** the app's wall density (20.2 kg/m³ ÷ 0.018 = 1.12 g/cm³) is far below a dense BN/WPU wall (about 1.89 g/cm³). Either the walls are about 40 % hollow, or Chan 2022 used another skeleton density. Unresolved.

## How to carry on (in order)
1. Apply the folder-split patch to `main`, or let a session that can commit do it.
2. Run `K_cond_GPU_solver/colab_k_cond.py` on a GPU (Colab, or the 2 × RTX 2080 Ti machine with one copy per card). Quick mode first for timing, then full mode. Repeat at half the voxel size to show the wall value has converged.
3. Get real values for the top inputs: BN grade sheet size and thickness (datasheet or TEM); SEM of wall cross-sections and of both aerogel sections (this also gives the channel direction); how Chan 2022 computed the porosity 0.982; resin fill from the mass gain after infusion.
4. Report, do not tune: "what sheet contact resistance would bring the wall down to 4 W/m·K" as an analysis (CLAUDE.md honesty rule).
5. Interim report (21 Dec): write simulation section 3.2 (modelling chain, the app's v0.1 results, the solver and its first result). The chapter split with word counts is in `K_cond_GPU_solver/PLAN.md`.
6. January: model the six specimens (40 × 40 mm plate, heater, supports, still air, solar absorbed as 1 − R), calibrate once on P, then predict L1–L5 without retuning.

**Open questions:** does "C" mean CNF (assumed) or CNT? `docs/FUTURE_WORK.md` §A.4 labels contrast 7692 as "4 W/m·K walls, air", but 7692 = 200/0.026 (with 4 W/m·K walls it is 154): fix the label.

**Planning doc:** "FYP simulator: BN/C wall model, GPU plan and report split" (claude.ai doc, the living version); markdown copy in `K_cond_GPU_solver/PLAN.md`.

## Earlier context
**What you wanted to build (verbatim, 29 Oct 2026, spelling tidied)**
> here are some context for my final year project in exchange in polyu, i am build a simulation tool, build that for me, give a plan first. i will steer you when the council AI is available, you have to use the council to debate with gpt and qwen, give them some context a plan first. until the council is ready, u extract and gather information first, after council works, u throw the context, and debate with 6sol (high), and qwen next (max), and tell them to judge you.

So: a simulation tool for the FYP, plan first, then have the plan debated and judged by two other models through the council MCP. The council step stalled on 29 Oct (metadata only, no answer text; "GPT 6.1 sol" not on the server) and was not resumed.

Supervisor guidance (meeting transcript): aerogel alone first, simple idealised geometry, one fixed composition then vary pore size, along and across the alignment, compare trends and not absolute numbers. Plan: `docs/PLAN.md`; physics: `docs/PHYSICS.md`.

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
| 11-19 | help text | "⚠ Accuracy" sentence added to every method's `HELP` (shown on hover); no change to `web/` |
| 11-24 | hub | `K_cond_GPU_solver/`: `README.md` (inputs and outputs), `colab_k_cond.py` (one-file wall + honeycomb conduction solver, CuPy or NumPy, built-in checks), `PLAN.md` (BN/C wall plan, GPU plan, re-aim at the six laminates, report split); this handover and `CLAUDE.md` updated |
| 11-24 | pending | Folder split into `aerosim_html/` and `report/`: patch only, not pushed |

## Sessions
`session_0143oVsKsbxuFFSfjRSorAqD` PolyU exchange simulation tool (10-29, blocked on council) ·
`session_0143oVsH2r1sHdcV9Yt4RkuJ` PolyU exchange project setup and pore-size study plan (10-29, blocked on council) ·
`session_0143oVsJAkHdZm66bSpB3Fny` UBX data processing and 3D visualization (10-30, pushed here and to AAE-4004-lab) ·
`session_0143oVsGXh4V8fwmnWfhskgN` Repository memory search (11-12) ·
`session_0143oVsGteeUsNh4d62pg2o3` BN/C wall model, GPU plan, K_cond Colab solver, folder split (11-24).

## Branches
GitHub's default branch is still `claude/compassionate-lamport-ff9nt6` (plan only). Set the default to `main` in Settings, Branches. The old `claude/*` branches (`admiring-pascal`, `quirky-thompson`, `compassionate-lamport`, `beautiful-tesla`, `gifted-volta`) are merged and can be deleted. `quirky-thompson` and `beautiful-tesla` still contain the removed GNSS lab folder.
