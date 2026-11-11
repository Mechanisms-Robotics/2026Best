# Git runs .vscode/settings.json through this script every time the file is
# staged or compared (see .gitattributes; tools/check.sh switches it on).
#
# The VEX extension writes "python.analysis.stubPath" into that file with a
# path that only exists on your computer. This script drops that one line, so
# Git never sees it and the committed file works on every machine. Your own
# copy of the file on disk is not changed.

# Windows line endings would stop the patterns below from matching.
{ sub(/\r$/, "") }

# Skip the machine-specific line.
/"python\.analysis\.stubPath"/ { next }

# Print each line one step late, so that if the removed line was the last
# setting, the comma left on the line before it can be removed too.
{
    if (have_previous) {
        if ($0 ~ /^[ \t]*}[ \t]*$/) {
            sub(/,[ \t]*$/, "", previous)
        }
        print previous
    }
    previous = $0
    have_previous = 1
}

END {
    if (have_previous) {
        print previous
    }
}
