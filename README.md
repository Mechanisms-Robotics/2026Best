# 2026Best

Mechanisms Robotics robot code for the 2026 BEST season. The robot uses a VEX V5 brain, and the code is written in Python.

## Setup (Windows)

1. Install [VS Code](https://code.visualstudio.com/). If WPILib's VS Code is already on your machine, you can use that.
2. Clone this repo and open the folder in VS Code (**File → Open Folder**).
3. When VS Code asks whether to install the recommended extensions, click **Install**. That installs:
   - **VEX Robotics** (`vexrobotics.vexcode`): builds and downloads code to the brain
   - **Python** (`ms-python.python`): autocomplete and error checking
4. The first time you open the project, the VEX extension downloads the V5 Python SDK. Wait for that to finish before downloading code.

## Downloading to the robot

1. Plug the V5 brain (or the controller, if it's paired) into your computer with USB.
2. Click the **Download** button in the VEX toolbar at the bottom of VS Code.
3. The program appears in slot 1 on the brain. Run it from the brain screen or the controller.

## Project layout

```
src/main.py                       <- all robot code lives here
.vscode/vex_project_settings.json <- tells the VEX extension this is a V5 Python project
```

Everything has to be in `src/main.py`. VEX Python downloads one file, so you can't split code across files the way you do in WPILib. Classes and functions inside the one file work fine.

## Coming from FRC Java

- **Indentation matters.** Python uses indentation instead of `{ }` to mark blocks.
- **No compiler.** Type mistakes only show up when the code runs, so watch for red squiggles in VS Code before you download.
- **It's MicroPython.** The brain runs a small version of Python, so most of the standard library isn't available and you can't `pip install` anything.
- **No command-based framework.** The code is plain functions. `driver_control()` runs a loop for the whole match. There is no autonomous period in this year's game: the driver presses a button and the robot runs a routine on its own (see the "Autonomous building blocks" section of `src/main.py`).
- **Docs:** [VEX V5 Python API](https://api.vex.com/v5/home/python/index.html)

## Autocomplete not working?

The VEX extension adds `python.analysis.stubPath` to `.vscode/settings.json` on each machine, and that path is specific to your computer. **Don't commit that line.** If autocomplete for `vex` stops working, reopen the folder so the extension can set the path again.
