# 2026Best

Mechanisms Robotics robot code for the 2026 BEST season. The robot uses a VEX V5 brain, and the code is written in Python.

## Setup (Windows)

1. Install [VS Code](https://code.visualstudio.com/). If WPILib's VS Code is already on your machine, you can use that.
2. In VS Code, open the Extensions view (**Ctrl+Shift+X**) and install:
   - **VEX Robotics** (`vexrobotics.vexcode`): builds and downloads code to the brain
   - **Python** (`ms-python.python`): autocomplete and error checking
3. Clone this repo.
4. In the repo, make a folder called `.vscode` and save this as `.vscode/vex_project_settings.json`. It tells the VEX extension that the folder is a V5 Python project. It is not in Git: `.gitignore` leaves out the whole `.vscode` folder, because the VEX extension writes paths there that only exist on your computer.

   ```json
   {
   	"extension": {
   		"version": "0.7.2025041600",
   		"json": 2
   	},
   	"project": {
   		"name": "2026Best",
   		"description": "Mechanisms Robotics 2026 BEST robot (VEX V5, Python)",
   		"creationDate": "9/29/2026, 12:00:00 PM",
   		"platform": "V5",
   		"language": "python",
   		"slot": 1,
   		"sdkVersion": "V5_1_0_1_25",
   		"python": {
   			"main": "src/main.py"
   		}
   	}
   }
   ```

5. Open the folder in VS Code (**File → Open Folder**). The first time, the VEX extension downloads the V5 Python SDK. Wait for that to finish before downloading code.

## Downloading to the robot

1. Plug the V5 brain (or the controller, if it's paired) into your computer with USB.
2. Click the **Download** button in the VEX toolbar at the bottom of VS Code.
3. The program appears in slot 1 on the brain. Run it from the brain screen or the controller.

## Project layout

```
src/main.py                       <- all robot code lives here
examples/example.py               <- working examples to copy from (not downloaded)
.vscode/vex_project_settings.json <- tells the VEX extension this is a V5 Python project (not in Git; see Setup)
docs/fiducial-map.md              <- where each fiducial is on the field, and its ID
```

Everything has to be in `src/main.py`. VEX Python downloads one file, so you can't split code across files the way you do in WPILib. Classes and functions inside the one file work fine.

`src/main.py` starts out nearly empty. `examples/example.py` has a working example of each building block: motors, sensors, driving and autonomous. Copy the parts you need into `src/main.py`. It is never downloaded to the brain and can't be imported.

## Coming from FRC Java

- **Indentation matters.** Python uses indentation instead of `{ }` to mark blocks.
- **No compiler.** Type mistakes only show up when the code runs, so watch for red squiggles in VS Code before you download.
- **It's MicroPython.** The brain runs a small version of Python, so most of the standard library isn't available and you can't `pip install` anything.
- **No command-based framework.** The code is plain functions. `driver_control()` runs a loop for the whole match. There is no autonomous period in this year's game: the driver presses a button and the robot runs a routine on its own (see the "Autonomous building blocks" section of `examples/example.py`).
- **Docs:** [VEX V5 Python API](https://api.vex.com/v5/home/python/index.html)
- **Field:** [`docs/fiducial-map.md`](docs/fiducial-map.md) shows where each fiducial (AprilTag) is in the Dining Room and its ID number.

## Autocomplete not working?

The VEX extension adds `python.analysis.stubPath` to `.vscode/settings.json` on each machine, pointing at the SDK it downloaded. That path is specific to your computer, which is why `.vscode` is not in Git. If autocomplete for `vex` stops working, reopen the folder so the extension can set the path again.

To see the same errors as `tools/check.sh` as red squiggles, add `"python.analysis.typeCheckingMode": "basic"` to that file.
