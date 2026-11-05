#!/usr/bin/env python3
"""PreToolUse-Hook für Claude Code: blockiert Lesen und Schreiben der .env.

Die Prüfung ist die Lösung der Übung „Einen Hook schreiben“. Eintrag in .claude/settings.json:

    "hooks": {"PreToolUse": [{"matcher": "Read|Edit|Write|Bash",
        "hooks": [{"type": "command", "command": "python3 \"$CLAUDE_PROJECT_DIR/.claude/hooks/env_hook.py\""}]}]}
"""

import json
import re
import sys
from pathlib import PurePosixPath

# .env als eigenes Wort: davor und danach kein Buchstabe, keine Ziffer, kein Punkt, kein Bindestrich.
ENV_IM_BEFEHL = re.compile(r"(?<![\w.-])\.env(?![\w.-])")


def pruefe(aufruf):
    werkzeug = aufruf["tool_name"]
    eingabe = aufruf["tool_input"]

    if werkzeug in ("Read", "Edit", "Write"):
        if PurePosixPath(eingabe["file_path"]).name == ".env":
            return "blockieren", "Die .env enthält Secrets. Vorlage: .env.example"

    if werkzeug == "Bash":
        if ENV_IM_BEFEHL.search(eingabe["command"]):
            return "blockieren", "Der Befehl greift auf die .env zu. Sie enthält Secrets. Vorlage: .env.example"

    return "erlauben", ""


if __name__ == "__main__":
    aufruf = json.load(sys.stdin)        # Claude Code schreibt den Aufruf als JSON auf stdin
    entscheid, grund = pruefe(aufruf)
    if entscheid == "blockieren":
        print(grund, file=sys.stderr)    # stderr geht als Begründung an Claude
        sys.exit(2)                      # Exit-Code 2 blockiert den Aufruf
    sys.exit(0)                          # 0: weiter
