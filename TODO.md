# TODO

Open questions and unverified guesses, written 2026-10-03. Nothing in `src/main.py` has run on a robot yet. Delete an item once it is settled, and move anything agents need to know into `AGENTS.md`.

## Confirm on the robot

- [ ] **Motor power.** `set_power()` converts percent to volts using `Motor55.get_max_voltage()`, based only on the SDK's own comments (the VEX docs site was unreachable). Check that half stick gives about half speed and full stick gives full speed. If `get_max_voltage()` returns 0 or something odd, the motors will not move.
- [ ] **AI Vision setup.** `AiVision(Ports.PORT5, AiVision.ALL_TAGS)` plus `set_tag_family(AiVision.TAG_CIRCLE21H7)` is untested. Confirm tag IDs show on the brain screen when the camera sees a printed fiducial.
- [ ] **Fiducial ID 0.** The fiducial sheet includes an ID 0, but the SDK comment for tag descriptions says IDs are "not 0". Check whether tag 0 is detected. This matters: ID 0 is the fiducial on the corner table nearest the blue corner.
- [ ] **Camera picture size.** `CAMERA_CENTER_X = 160` assumes a 320-pixel-wide picture. Confirm a tag held dead ahead reads a `centerX` near 160.
- [ ] **Turn direction in `auto_turn_to_tag`.** It assumes positive turn power turns the robot right. Swap if it turns away from the tag.
- [ ] **Servo range.** The BEST servos may not reach the full -50 to 50 degrees. Find the real limits and set `SERVO_POSITION_1` / `SERVO_POSITION_2`.
- [ ] **Potentiometer direction in `auto_move_to_angle`.** It assumes positive power raises the angle.
- [ ] **Cancel button.** Confirm pressing B mid-routine stops every motor immediately.

## Find out

- [ ] **IR sensor.** How do the two boards of the BEST IR Sensor Kit wire to the brain (one port or two? which board carries the signal?), and is the output on/off or a range? The code reads it as `AnalogIn` on 3-wire port A as a first guess. Replace `read_ir()` once known.
- [ ] **Real ports and motor roles.** Every port in the Devices section is a placeholder, and which of the two large and two small motors drive is undecided. Fill in the tables in `AGENTS.md` when wired.
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
