# AGENTS.md

This file provides guidance to AI coding agents (Claude Code, Codex, Gemini CLI, Cursor, GitHub Copilot, and others) when working with code in this repository. It is the single source of truth: `CLAUDE.md` and `GEMINI.md` only import this file, so put all agent instructions here and never in those stubs.

## What this is

Baseline robot code for a high school team's (Mechanisms Robotics) 2026 BEST Robotics season. The robot runs on a VEX V5 brain and is programmed in VEX Python. The students who maintain this are mostly coming from FRC Java/WPILib, so keep code plain and heavily commented in the style already in `src/main.py`: explain *why* in terms a new programmer can follow, and say which values they are expected to change (ports, reversed flags, speeds).

## Build, download, test

There is no command-line build, linter, or test suite. Everything goes through the VEX VS Code extension (`vexrobotics.vexcode`):

- **Download to the brain:** connect the brain (or a paired controller) over USB and click **Download** in the VEX toolbar. The program lands in slot 1 (set in `.vscode/vex_project_settings.json`).
- **Checking code:** Pylance in `basic` type-checking mode is the only static check, and it only works inside VS Code once the extension has downloaded the V5 Python SDK stubs. The `vex` module does not exist off the brain, so `src/main.py` cannot be run or imported locally.
- **Syntax-only check from a terminal:** `python -m py_compile src/main.py` (does not resolve `vex` names, so it catches syntax errors only).

Code can only really be verified on the physical robot. Say so when handing back changes rather than claiming they were tested.

## Constraints that shape the code

- **Single file.** The VEX extension downloads only `src/main.py` (`project.python.main`). Do not split code into modules or add imports of local files; organize with functions and classes inside the one file.
- **MicroPython on the brain.** Most of the standard library is missing and nothing can be `pip install`ed. Stick to `from vex import *` and language built-ins.
- **Every loop must yield.** Long-running loops need a `wait(20, MSEC)` (or similar) so the brain can service other tasks.
- **Don't commit `python.analysis.stubPath`.** The VEX extension writes this machine-specific path into `.vscode/settings.json` on each computer. Leave it out of commits.

## Structure of `src/main.py`

1. **Devices** — module-level globals (`brain`, `controller`, motors, `MotorGroup`s). Port numbers and the reversed flag on each `Motor` reflect physical wiring; new mechanisms get their devices declared here.
2. **Helpers** — small pure functions such as `apply_deadband`.
3. **`autonomous()`** — runs once when field control starts the autonomous period.
4. **`driver_control()`** — an infinite loop reading the controller (currently arcade drive: axis 3 forward/back, axis 1 turn).
5. **`competition = Competition(driver_control, autonomous)`** — must stay the last statement. It hands both functions to the field control system; with no field control attached, running the program goes straight to `driver_control()`.

## Commit messages

Use semantic (Conventional Commits) messages: `type: short summary` in the imperative, lowercase, no trailing period. An optional scope names the mechanism, e.g. `feat(drive): add tank drive option`.

- `feat` — new robot behavior or mechanism code
- `fix` — bug fix
- `tune` — changing constants only (ports, speeds, deadband, autonomous timings)
- `refactor` — restructuring with no behavior change
- `docs` — README, comments, or agent instructions
- `chore` — project config and tooling (`.vscode/`, `.gitignore`)

API reference: https://api.vex.com/v5/home/python/index.html
