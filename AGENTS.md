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

The file is a teaching framework, not a finished robot. Its job is to give students working examples of each building block so they can design their own solution. Do not turn it into a solution to the game unless a person asks for one, and keep the `CHANGE ME` and `EXAMPLE` markers honest: remove one only when the value has been confirmed on the real robot.

1. **Devices** — module-level globals: `brain`, `controller`, four `Motor55` motors, the `AiVision` sensor, the IR sensor, an example servo, microswitch and potentiometer, and the `ALL_MOTORS` list that `stop_all()` uses. New devices are declared here and new motors added to `ALL_MOTORS`.
2. **Settings** — named constants (deadband, powers, camera numbers) that students tune on the robot. New timings and powers go here, not inline.
3. **Motor helpers** — `set_power(motor, percent)`, `drive(forward, turn)`, `stop_all()`. All motor movement goes through `set_power`.
4. **Sensor helpers** — `read_ir()`, `find_tag(id)`, `visible_tag_ids()`, and `show_sensors()`, which prints live readings on the brain screen so students can see what the sensors report.
5. **Autonomous building blocks** — `auto_wait`, `auto_drive`, `auto_turn_to_tag`, `auto_run_until_switch`, `auto_move_to_angle`, an `example_routine`, and `run_autonomous(routine)`, which runs a routine and always stops every motor afterwards.
6. **`driver_control()`** — an infinite loop: arcade drive, buttons for the two extra motors and the example servo, a button that starts the autonomous routine, and the sensor display.
7. **`autonomous()` and `competition = Competition(driver_control, autonomous)`** — `autonomous()` is intentionally empty (see "Autonomous in this game"). The `Competition` line must stay the last statement; with no field control attached, running the program goes straight to `driver_control()`.

## Robot hardware

Open questions and unverified guesses about the hardware and code are tracked in `TODO.md`. Check it before relying on a `CHANGE ME` value, and update it when one is settled.

**The robot is not built yet and the design is undecided.** Every port, every reversed flag, and the job of each motor in `src/main.py` is a placeholder marked `CHANGE ME`. Ask the person you are working with what is actually plugged in before adding or changing a device, and never present a guessed port as real.

**Kit parts only.** BEST Robotics rules limit the robot to the parts supplied in the team's kit. Never suggest buying or adding hardware and never write code for a device unless a person has confirmed it came in the kit. If a problem would normally be solved with a sensor the team does not have, solve it in software with what is there or say it cannot be done.

What the team has confirmed is in the kit:

- **Four 2-wire DC motors, two large and two small**, each driven through a VEX Motor Controller 55 (MC55). An MC55 plugs into a numbered Smart Port. Declare it with `Motor55(Ports.PORT1, reversed)`, not `Motor`.
- **One AI Vision Sensor** (Smart Port, `AiVision`). It detects the field's fiducials, which are AprilTags from the Circle21h7 family (`AiVision.TAG_CIRCLE21H7`).
- **One BEST IR Sensor Kit**: two small boards, each with three pins (one with female pins, one with male). How it wires to the brain and what it reports have not been worked out. The code reads it as `AnalogIn` on a 3-wire port as a first guess so students can watch the value on the brain screen.

- **Servos, microswitches and potentiometers.** All use the 3-wire ports (A-H): `Servo` (`set_position`, -50 to 50 degrees; the BEST servos may not reach the full range), `Limit` (`pressing()`), and `Potentiometer` (`angle(DEGREES)`, about 0 to 250). How many of each the team has is not recorded; ask before assuming more than one. The servo, switch and potentiometer in `src/main.py` are examples on placeholder ports, not real mechanisms.

What this means for the code:

- **Use `set_power`, not `spin`.** The SDK documents `Motor55.spin` in volts (`spin(FORWARD, 3, VOLT)`), with `VOLT` as the default unit, so `spin(FORWARD, 50)` asks for 50 volts. `set_power(motor, percent)` converts a -100 to 100 percent into volts using `get_max_voltage()`. Whether `spin` also accepts `PERCENT` is not confirmed; do not rely on it.
- **No built-in feedback.** `Motor55` can set power, reverse, stop, set brake mode, limit current (`set_max_torque`), and report current and temperature. It has no position or velocity, so `spin_for`, `spin_to_position`, and anything measured in degrees or turns do not exist for it. There are no encoders in the kit, so nothing measures wheel travel. A potentiometer on a pivot or a microswitch at the end of travel is how a mechanism knows where it is (`auto_move_to_angle` and `auto_run_until_switch` are the examples).
- **No `MotorGroup`.** It only accepts `Motor` (Smart Motor) objects. Command each `Motor55` individually.
- **Only four motors.** Any design has to split them between driving and mechanisms; do not write code that assumes more.
- **No CAN devices.** The V5 brain has no CAN bus, so parts such as a CTRE CANcoder cannot be used even if available.

Keep these tables in step with the Devices section and the controls comment in `src/main.py`. When a change adds, removes, or moves a device or a control, update the table in the same commit. Everything below is a placeholder until the robot is wired.

| Port | Device (type) | Name in code | Reversed? | Notes |
| ---- | ------------- | ------------ | --------- | ----- |
| Smart 1 | MC55 + motor (`Motor55`) | `left_motor` | No | Placeholder |
| Smart 10 | MC55 + motor (`Motor55`) | `right_motor` | Yes | Placeholder |
| Smart 2 | MC55 + motor (`Motor55`) | `motor_3` | No | Placeholder, job undecided |
| Smart 9 | MC55 + motor (`Motor55`) | `motor_4` | No | Placeholder, job undecided |
| Smart 5 | AI Vision Sensor (`AiVision`) | `ai_vision` | | Placeholder |
| 3-wire A | BEST IR Sensor Kit (`AnalogIn`) | `ir_sensor` | | Placeholder, wiring unconfirmed |
| 3-wire B | Servo (`Servo`) | `example_servo` | | Example only |
| 3-wire C | Microswitch (`Limit`) | `example_switch` | | Example only |
| 3-wire D | Potentiometer (`Potentiometer`) | `example_pot` | | Example only |

| Controller input | What it does |
| ---------------- | ------------ |
| Axis 3 (left stick up/down) | Drive forward/back |
| Axis 1 (right stick left/right) | Turn |
| L1 / L2 | `motor_3` forward / reverse |
| R1 / R2 | `motor_4` forward / reverse |
| X / Y | `example_servo` to position 1 / position 2 |
| A | Start the autonomous routine |
| B | Cancel the autonomous routine |

## Autonomous in this game

The 2026 game is *Byte to Bite*. Matches are three minutes. There is no autonomous period at the start of the match. Instead, the centre of the field is the Dining Room, an autonomous-only zone:

- A robot may only enter the Dining Room under autonomous control while the driver is hands-free (the controller is not in the driver's hands).
- Every scoring task inside the Dining Room must be done autonomously: navigate to an open table and place a completed meal on it.
- Fiducials (AprilTags) are on the Dining Room walls and on the table tops to help the robot navigate. Their sizes, positions and ID numbers are in the *Byte to Bite Field Drawings*.
- A team may abandon an autonomous run at any time, and the driver may then drive the robot out by hand. The rules do not require the robot to return on its own.
- The robot may not run any autonomous or time-delay program while the Spotter is interacting with it in the Robot Start Area.

These points are a summary. The official *2026 BEST Robotics Classic Game Rules* decide any question; ask a person to check them rather than relying on this list, and do not state a rule that is not written here.

What this means for the code:

- **Autonomous is started from `driver_control()`** by a controller button and run through `run_autonomous(routine)`. The `Competition` autonomous callback is unused.
- **Every routine must be cancellable.** Inside autonomous code use `auto_wait()` instead of `wait()`, and call `check_cancel()` in any loop. Both raise `AutoCancelled` when the cancel button is pressed; `run_autonomous` catches it and stops every motor. A plain `wait()` leaves the robot moving with nobody in control.
- **Timed moves drift.** With no encoders, `auto_drive` is set power, wait, stop, and the distance changes with battery level and floor friction. The AI Vision Sensor and the IR sensor are the only ways to correct the robot's position. Say this plainly when asked for an autonomous routine instead of promising accuracy.
- **Keep timings and powers as named constants** in the Settings section so students can tune them on the robot.

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
