#!/usr/bin/env bash
# Checks src/main.py without a robot. Run from anywhere: tools/check.sh
#
# This is the same check GitHub runs on every pull request. It catches syntax
# errors, misspelled vex names, and wrong arguments. It cannot tell you whether
# the robot does the right thing - only testing on the robot can.
set -euo pipefail

cd "$(dirname "$0")/.."

# Must match "sdkVersion" in .vscode/vex_project_settings.json.
SDK_VERSION="V5_1_0_1_25"
SDK_URL="https://content.vexrobotics.com/vexos/public/V5/vscode/sdk/python/${SDK_VERSION}.zip"
# Must match the "extraPaths" entry in tools/pyrightconfig.json.
SDK_DIR="build/vex-sdk"
PYRIGHT_VERSION="1.1.414"

echo "== Only src/main.py gets downloaded to the brain"
extra=$(find src -name '*.py' ! -path 'src/main.py')
if [ -n "$extra" ]; then
    echo "Found other Python files in src/. Move this code into src/main.py:"
    echo "$extra"
    exit 1
fi

echo "== Syntax"
python -m py_compile src/main.py

echo "== Types (Pyright with the VEX V5 Python SDK)"
# The VEX SDK is downloaded from VEX rather than committed to this repo.
# build/ is in .gitignore, so it is only downloaded once per machine.
if [ ! -f "$SDK_DIR/$SDK_VERSION/vexv5/stubs/vex.py" ]; then
    mkdir -p "$SDK_DIR"
    curl -fsSL "$SDK_URL" -o "$SDK_DIR/sdk.zip"
    unzip -q -o "$SDK_DIR/sdk.zip" -d "$SDK_DIR"
    rm "$SDK_DIR/sdk.zip"
fi
npx --yes "pyright@${PYRIGHT_VERSION}" -p tools/pyrightconfig.json
