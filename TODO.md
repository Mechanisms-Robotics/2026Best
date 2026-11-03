# TODO

Open questions and unverified guesses, written 2026-10-03. Nothing in `src/main.py` or `examples/example.py` has run on a robot yet. The functions, constants and ports named below are in `examples/example.py`; `src/main.py` has no devices yet. Delete an item once it is settled, and move anything agents need to know into `AGENTS.md`.

## Confirm on the robot

- [ ] **Motor power.** Partly settled on 2026-10-05 with one large motor free on the bench: `get_max_voltage()` returned 8000, so 100% is 8 V, and the motor ran from the stick through `set_power()`, one way with the stick pushed forward and the other way with it pulled back. At a 50% cap it was very slow. Still to check: that full stick at 100% is clearly faster, that half stick gives about half speed, and that a small motor reports the same 8000.
- [ ] **Speed as the battery drains.** 8 V is well below the 12.8 V battery, so the motor may run at the same speed on a full and a part-used battery. Not confirmed. Time a motor on both; if it holds, timed autonomous moves will drift less with battery level than `AGENTS.md` warns.
- [ ] **`spin` with `PERCENT`.** The VEX API page for the MC55 says `spin(FORWARD, 50, PERCENT)` works; the SDK comments only mention volts. Low priority, since `set_power()` works. If someone tries it, record the result in `AGENTS.md`.
- [ ] **AI Vision setup.** `AiVision(Ports.PORT5, AiVision.ALL_TAGS)` plus `set_tag_family(AiVision.TAG_CIRCLE21H7)` is untested. Confirm tag IDs show on the brain screen when the camera sees a printed fiducial.
- [ ] **Fiducial ID 0.** The fiducial sheet includes an ID 0, but the SDK comment for tag descriptions says IDs are "not 0". Check whether tag 0 is detected. This matters: ID 0 is the fiducial on the corner table nearest the blue corner.
- [ ] **Camera picture size.** `CAMERA_CENTER_X = 160` assumes a 320-pixel-wide picture. Confirm a tag held dead ahead reads a `centerX` near 160.
- [ ] **Turn direction in `auto_turn_to_tag`.** It assumes positive turn power turns the robot right. Swap if it turns away from the tag.
- [ ] **Servo range.** Partly settled on 2026-10-05: one servo, on the bench with nothing attached, followed commands across the full -50 to 50 degrees with no straining at either end. Still to do: measure how far it really turns, check it under load once it is on a mechanism, and set `SERVO_POSITION_1` / `SERVO_POSITION_2` in the example for the real mechanism.
- [ ] **Potentiometer direction in `auto_move_to_angle`.** It assumes positive power raises the angle.
- [ ] **Cancel button.** Confirm pressing B mid-routine stops every motor immediately.

## Find out

- [ ] **IR sensor.** How do the two boards of the BEST IR Sensor Kit wire to the brain (one port or two? which board carries the signal?), and is the output on/off or a range? The code reads it as `AnalogIn` on 3-wire port A as a first guess. Replace `read_ir()` once known.
- [ ] **Can the motors run above 8 V?** The MC55 defaults to an 8 V maximum, the API allows up to 12 V, and the battery is 12.8 V. VEX publishes the motor figures at 7.2 V (confirmed for the small motor 276-1610; assumed the same for the large motor 276-1611), which suggests 8 V is already the intended ceiling. Ask the hub whether running the kit motors above 8 V is allowed and safe. Also unknown: whether Python's `Motor55` accepts a maximum voltage the way the C++ `motor55(index, maxv, reverse)` does. Do not try it before the hub answers.
- [ ] **Real ports and motor roles.** Every port in the Devices section of `examples/example.py` is a placeholder, and which of the two large and two small motors drive is undecided. Fill in the tables in `AGENTS.md` when wired.
- [ ] **How many servos, microswitches and potentiometers** are in the kit. Record the counts in `AGENTS.md`.
- [ ] **Check the fiducial map on a real field.** `docs/fiducial-map.md` lists every ID and position from the Field Drawings (Aug 23 2026 revision). The x/y positions, the long-wall spacing and the heights were worked out from the drawings rather than read off them. Measure a built field, and find out how far away the camera can read a tag.
- [ ] **Does the robot have to return on its own?** The rules say the driver may drive the robot out of the Dining Room by hand after a run or after abandoning one. Confirm with the hub whether a self-return is required or just the team's plan.
- [ ] **Field control.** Does BEST plug the controller into a field control system? The `Competition(driver_control, autonomous)` line is kept from the VEX starter, with `autonomous()` left empty. If there is no field control it could be simplified.
- [ ] **Hands-free and the cancel button.** The driver must be hands-free during a Dining Room run. Decide how a cancel works in practice (picking the controller up to press B ends the run by rule anyway) and whether stick movement should also cancel.

## Project setup

- [ ] **Rule summary can go stale.** `AGENTS.md` summarizes the autonomous rules from the game rules dated Sep 10, 2026, and the rules PDFs are not in this repo. Re-check the summary when BEST publishes a revision.
- [ ] **Gemini CLI is untested.** Codex read `AGENTS.md` correctly; the Gemini run failed because its API account was out of credits. Ask it "what commit convention does this repo use?" once it works.
- [ ] **`tools/check.sh` on Windows.** It needs `bash`, `python`, `curl`, `unzip` and `npx`. It has only been run on Linux and in GitHub Actions; try it in Git Bash on a student laptop.
- [ ] **PR check is not required.** The "Check" workflow runs on every PR but a PR can merge while it is failing. Making it required means editing the organization ruleset "Protect main, master, develop".
