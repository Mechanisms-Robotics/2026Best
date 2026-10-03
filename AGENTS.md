# AGENTS.md

This file provides guidance to AI coding agents (Claude Code, Codex, Gemini CLI, Cursor, GitHub Copilot, and others) when working with code in this repository. It is the single source of truth: `CLAUDE.md` and `GEMINI.md` only import this file, so put all agent instructions here and never in those stubs.

## What this is

Baseline robot code for a high school team's (Mechanisms Robotics) 2026 BEST Robotics season. The robot runs on a VEX V5 brain and is programmed in VEX Python. The students who maintain this are mostly coming from FRC Java/WPILib, so keep code plain and heavily commented in the style already in `src/main.py`: explain *why* in terms a new programmer can follow, and say which values they are expected to change (ports, reversed flags, speeds).

## Build, download, test

There is no command-line build or test suite. Downloading goes through the VEX VS Code extension (`vexrobotics.vexcode`):

- **Download to the brain:** connect the brain (or a paired controller) over USB and click **Download** in the VEX toolbar. The program lands in slot 1 (set in `.vscode/vex_project_settings.json`).
- **Check code from a terminal:** `tools/check.sh`. Run it after every change to `src/main.py` and fix what it reports before committing. It confirms `src/main.py` is the only Python file in `src/`, checks syntax, and runs Pyright against the VEX V5 Python SDK, so it catches misspelled `vex` names and wrong arguments. The first run downloads the SDK from VEX into `build/` (gitignored); it needs `bash`, `python`, `curl`, `unzip`, and `npx` (Git Bash on Windows works). GitHub runs the same script on every PR (`.github/workflows/check.yml`).
- **In VS Code:** Pylance in `basic` type-checking mode shows the same errors as red squiggles once the extension has downloaded the SDK.
- **SDK version:** `tools/check.sh` and `tools/pyrightconfig.json` name the same SDK version as `sdkVersion` in `.vscode/vex_project_settings.json`. Change all three together.

The `vex` module does not exist off the brain, so `src/main.py` cannot be run or imported locally. A passing check means the code is well-formed, not that the robot behaves correctly. Say so when handing back changes rather than claiming they were tested.

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

## Robot hardware

**The robot is not built yet and the motor type is unconfirmed.** The devices in `src/main.py` (four V5 Smart Motors on ports 1, 2, 9 and 10) are placeholders from the starter, not the real wiring. BEST kit motors and servos may instead run from the 3-wire ports (A-H) and need different `vex` classes. Until the tables below are filled in, ask the person you are working with what is actually plugged in before adding or changing any device, and never guess a port.

Keep these tables in step with the Devices section of `src/main.py`. When a change adds, removes, or moves a device or a control, update the table in the same commit.

| Port | Device (type) | Mechanism | Reversed? | Notes |
| ---- | ------------- | --------- | --------- | ----- |
| _TBD_ | | | | |

| Controller input | What it does |
| ---------------- | ------------ |
| Axis 3 (left stick up/down) | Drive forward/back |
| Axis 1 (right stick left/right) | Turn |

## Handing back changes

This code moves a physical robot around students, and none of it can be run off the brain. Every PR description and final summary must include a **Test on the robot** list: the specific things a student should do and watch for (e.g. "push the left stick forward; both sides should drive forward"). Call out anything that could move unexpectedly, and suggest testing new mechanisms or autonomous routines with the wheels off the ground first.

## Branches and pull requests

- `develop` is the default branch and where day-to-day work lands. `main` is the known-good code that goes to competition; it only changes through a PR from `develop`.
- Both branches are protected: direct pushes are rejected, and a PR needs an approving review from the team before it can merge.
- Start every change on a new branch off an up-to-date `develop`. Name it like a commit, `type/short-description`, e.g. `feat/arm-control` or `tune/auto-timing`.
- Push the branch and open a PR against `develop`, then stop. A person reviews and merges. Agents do not merge PRs and never use the admin bypass (`gh pr merge --admin`), even if they have permission.

## Commit messages

Use semantic (Conventional Commits) messages: `type: short summary` in the imperative, lowercase, no trailing period. An optional scope names the mechanism, e.g. `feat(drive): add tank drive option`.

- `feat` — new robot behavior or mechanism code
- `fix` — bug fix
- `tune` — changing constants only (ports, speeds, deadband, autonomous timings)
- `refactor` — restructuring with no behavior change
- `docs` — README, comments, or agent instructions
- `chore` — project config and tooling (`.vscode/`, `.gitignore`)

API reference: https://api.vex.com/v5/home/python/index.html
