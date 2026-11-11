# Git runs .vscode/settings.json through this script every time the file is
# staged or compared (see .gitattributes; tools/check.sh switches it on).
#
# The VEX extension writes "python.analysis.stubPath" into that file with a
# full path that only exists on your computer. This script swaps that path
# for a relative one, build/vex-sdk/..., so the committed file works on every
# machine. tools/check.sh downloads the same SDK into build/. Your own copy of
# the file on disk is not changed.
#
# The SDK version below must match SDK_VERSION in tools/check.sh.

# Windows line endings would stop the pattern below from matching.
{ sub(/\r$/, "") }

# Replace whatever path the extension wrote with the relative one.
/"python\.analysis\.stubPath"/ {
    sub(/"python\.analysis\.stubPath"[ \t]*:[ \t]*"[^"]*"/,
        "\"python.analysis.stubPath\": \"build/vex-sdk/V5_1_0_1_25/vexv5/stubs\"")
}

{ print }
