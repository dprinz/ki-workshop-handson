"""Tests starten und Mutationen automatisch durchprobieren, damit das Notebook den Ablauf zeigt."""

import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ORDNER = Path(__file__).parent
PARSER = ORDNER / "sse_parser.py"

# Nummer, was sich ändert, Text im Parser, Ersatz. Dieselben Mutationen wie in der Tabelle im Notebook.
MUTATIONEN = [
    ("1", "\\r\\n nicht mehr umwandeln",
     '(self.puffer + stueck).replace("\\r\\n", "\\n")', "self.puffer + stueck"),
    ("2", "Rest nicht im Puffer behalten",
     "self.puffer = events.pop()", "events.pop()"),
    ("3", "Leerzeichen nach data: nicht entfernen",
     '            if wert.startswith(" "):\n                wert = wert[1:]\n', ""),
    ("4", "Datenzeilen ohne Zeilenumbruch verbinden",
     'return "\\n".join(werte)', 'return "".join(werte)'),
    ("5", "Puffer beim Abschliessen nicht leeren",
     '        self.puffer = ""\n        daten = daten_aus_event(rest)', "        daten = daten_aus_event(rest)"),
    ("6", "Grenze nicht mehr durchsetzen",
     "raise EventZuGross()", "pass"),
    ("7", "nur fertige Events prüfen, den Puffer nicht",
     "for event in events + [self.puffer]:", "for event in events:"),
    ("8", "Zeichen statt Bytes zählen",
     'len(event.encode("utf-8"))', "len(event)"),
]


def _unittest(ordner, testdateien, ausfuehrlich):
    shutil.rmtree(Path(ordner) / "__pycache__", ignore_errors=True)
    module = [Path(datei).stem for datei in testdateien]
    befehl = [sys.executable, "-B", "-m", "unittest", "-v" if ausfuehrlich else "-q", *module]
    return subprocess.run(befehl, cwd=ordner, capture_output=True, text=True, timeout=60)


def tests_laufen_lassen(*testdateien, ausfuehrlich=False):
    """Startet unittest in einem eigenen Prozess, damit immer die aktuelle sse_parser.py gilt."""
    lauf = _unittest(ORDNER, testdateien or ["test_sse_parser.py"], ausfuehrlich)
    if ausfuehrlich:
        print(lauf.stderr)
    elif "Ran " not in lauf.stderr:
        print("Die Tests sind nicht gestartet, Python kann den Code nicht laden:")
        print(lauf.stderr.strip().splitlines()[-1])
        print("Tipp: Ein Block braucht mindestens eine Zeile. Wer eine Zeile ganz löscht, schreibt pass hin.")
        return
    elif lauf.returncode != 0:
        for zeile in lauf.stderr.splitlines():
            if zeile.startswith(("FAIL:", "ERROR:")):
                print(zeile.split(" (")[0])
            elif zeile.startswith("AssertionError") or "Error:" in zeile and not zeile.startswith(" "):
                print("   ", zeile)
        print()
    print("Ergebnis:", _ergebnis(lauf))


def _ergebnis(lauf):
    anzahl = re.search(r"Ran (\d+) test", lauf.stderr)
    if anzahl is None:
        return "Code lässt sich nicht laden"
    tests = f"{anzahl.group(1)} Test" if anzahl.group(1) == "1" else f"{anzahl.group(1)} Tests"
    if lauf.returncode == 0:
        return f"grün ({tests})"
    rot = sum(int(zahl) for zahl in re.findall(r"(?:failures|errors)=(\d+)", lauf.stderr))
    return f"rot ({rot} von {tests})"


def mutationen_pruefen(*testdateien):
    """Wendet jede Mutation auf die aktuelle sse_parser.py an und lässt die Tests in einer Kopie laufen."""
    testdateien = testdateien or ("test_sse_parser.py",)
    quelle = PARSER.read_text(encoding="utf-8")
    with tempfile.TemporaryDirectory() as tmp:
        for datei in testdateien:
            shutil.copy(ORDNER / datei, tmp)
        (Path(tmp) / "sse_parser.py").write_text(quelle, encoding="utf-8")
        if _unittest(tmp, testdateien, ausfuehrlich=False).returncode != 0:
            print("Die Tests sind schon ohne Mutation rot. Ist der Parser oben noch verändert, oder schlägt ein eigener Test fehl?")
            return
        print(f"Tests: {', '.join(testdateien)}\n")
        for nummer, beschreibung, alt, neu in MUTATIONEN:
            if quelle.count(alt) != 1:
                print(f"{nummer}  {beschreibung:<46} Zeile nicht gefunden, Parser zurücksetzen")
                continue
            (Path(tmp) / "sse_parser.py").write_text(quelle.replace(alt, neu), encoding="utf-8")
            lauf = _unittest(tmp, testdateien, ausfuehrlich=False)
            urteil = "nicht gefangen" if lauf.returncode == 0 else "gefangen"
            print(f"{nummer}  {beschreibung:<46} {urteil:<16} {_ergebnis(lauf)}")
