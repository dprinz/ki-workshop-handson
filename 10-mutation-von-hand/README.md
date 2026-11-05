# Mutation von Hand

Übungs-Notebook für den KI-Workshop: Ein kleiner Parser für Server-Sent Events hat 61 Tests, die
ein Agent test-first aus der Spezifikation geschrieben hat. Alle sind grün. Die Teilnehmer bauen
absichtlich Fehler in den Parser ein und prüfen, ob ein Test rot wird. Die Fehler an der
Obergrenze von 64 KiB fängt kein Test, weil die Grenze im Code steht, aber nicht in der
Spezifikation.

Eingeplant am zweiten Tag am frühen Nachmittag, im Block zur Verifikation direkt nach der Folie
„Würde der Test rot, wenn die Logik fehlt?“. Die folgende Folie „Ein grüner Test prüft nur, was
in der Spezifikation steht“ geht in der Übung auf. 15 min zu zweit.

## Starten

```bash
uv sync
```

```bash
uv run jupyter lab mutation_von_hand.ipynb --LabApp.user_settings_dir=../einstellungen-jupyterlab
```

Die Schriftgrössen für den Beamer stehen in `../einstellungen-jupyterlab/`, gemeinsam für alle Workshop-Labs.

Danach *Kernel → Restart Kernel and Run All Cells*. Das Notebook braucht kein Netz, und ausser
JupyterLab nur die Standardbibliothek.

## Was im Ordner liegt

| Datei | Inhalt |
|---|---|
| `mutation_von_hand.ipynb` | das Notebook mit drei Schritten und Zusatz, Ausgaben aus einem echten Lauf |
| `spezifikation.md` | die Spezifikation des Parsers, aus der der Agent die Tests geschrieben hat; keine Obergrenze |
| `sse_parser.py` | der Parser; das Notebook schreibt ihn mit `%%writefile` aus der Zelle, in der die Teilnehmer die Fehler einbauen |
| `test_sse_parser.py` | die 61 generierten Tests, unverändert aus dem Lauf unten |
| `helfer.py` | Tests in einem eigenen Prozess starten und die acht Mutationen automatisch durchprobieren |

`test_grenze.py` und `test_grenze_loesung.py` entstehen beim Ausführen des Zusatzes und stehen in `.gitignore`.

## Woher die Tests stammen

Erzeugt am 2026-11-04 um 14:38 mit Claude Code 2.1.318, Modell `claude-opus-5-5`, in einem leeren
Ordner ohne Werkzeuge, also ohne Zugriff auf den Code:

```bash
claude -p --tools "" --model opus --no-session-persistence --output-format json "$(cat prompt.txt)"
```

Prompt (`prompt.txt`), darunter folgte wörtlich der Inhalt von `spezifikation.md`:

```text
Wir arbeiten test-first. Schreibe die Unit-Tests für das Python-Modul `sse_parser` nach der Spezifikation unten. Den Code gibt es noch nicht.

- Eine Datei `test_sse_parser.py`, nur `unittest` aus der Standardbibliothek, Python 3.12.
- Decke die Spezifikation vollständig ab, eine Testmethode pro Fall, sprechende Namen.
- Gib nur den Inhalt der Datei aus, ohne Erklärung und ohne Markdown-Zaun.
```

Laufzeit 3 min 23 s, 24'122 Output-Tokens (davon 17'326 Thinking). Die Antwort ist ohne Änderung
als `test_sse_parser.py` gespeichert.

Im ersten Lauf gegen den Parser waren 3 der 61 Tests rot: Kam ein `\r\n` genau zwischen zwei
Stücken getrennt an, blieb das `\r` in den Daten, weil der Parser nur das neue Stück umwandelte.
Korrigiert wurde der Parser (Umwandlung nach dem Zusammensetzen mit dem Puffer), nicht die Tests.

## Bezug zu AstroPlanner

Vorbild ist `frontend/src/app/assistant/sse-parser.ts` in AstroPlanner (Stand `6c16d1c`): gleiche
Zerlegung an Leerzeilen, gleicher Umgang mit `data:`, gleiche Grenze von 64 KiB pro Event,
geprüft für fertige Events und den wachsenden Rest. Laut `docs/block-2/veto-notiz.md` (Zeile 24)
waren dort alle generierten Parser-Tests grün, die Spezifikation kannte keine Obergrenze, und
der `security-reviewer` fand den unbegrenzten Puffer (SR-2). Danach kam die Regel „Antwort zu
lang“ (20'000 Zeichen, 64 KiB je Frame) in die Spezifikation, erst dann die Tests.

Unterschied zur Übung: In AstroPlanner fehlte die Grenze zuerst auch im Code. In der Übung steht
sie im Code, aber nicht in der Spezifikation, damit man sie löschen und dabei zusehen kann, dass
kein Test rot wird. Die Aussage ist dieselbe: Die Tests sind so gut wie die Spezifikation.

## Gemessen

MacBook Pro M3 Pro, `nbconvert --execute`: alle Zellen zusammen 1,3 s (mit Kernelstart 7 s).

| Zelle | lokal | Colab-CPU, geschätzt |
|---|---|---|
| Tests laufen lassen (eigener Python-Prozess) | 0,04 s | unter 1 s |
| alle acht Mutationen (neun Prozesse) | 0,4 s | 2 bis 10 s |
| Zusatz mit eigenem Test und Lösung | je 0,5 s | 2 bis 10 s |

Die Zeit geht fast ganz in den Start der Python-Prozesse, nicht in die Tests. In Colab (frische Laufzeit, Gratis-CPU, „Alle ausführen“, 2026-11-04) lief das Notebook ohne Fehler, die 61 Tests grün, die Mutationen wie in der Tabelle unten; pro Zelle nicht gemessen.

Ergebnis der Mutationen mit den generierten Tests:

| Nr | Mutation | Ergebnis |
|---|---|---|
| 1 | `\r\n` nicht mehr umwandeln | rot, 10 von 61 |
| 2 | Rest nicht im Puffer behalten | rot, 9 von 61 |
| 3 | Leerzeichen nach `data:` nicht entfernen | rot, 48 von 61 |
| 4 | Datenzeilen ohne Zeilenumbruch verbinden | rot, 11 von 61 |
| 5 | Puffer beim Abschliessen nicht leeren | rot, 2 von 61 |
| 6 | Grenze nicht durchsetzen (`raise` → `pass`) | grün |
| 7 | nur fertige Events prüfen, nicht den Rest | grün |
| 8 | Zeichen statt Bytes zählen | grün |

Mit den drei Tests der Zusatz-Lösung werden auch 6, 7 und 8 rot.

## Bekannte Grenzen

- `unittest` statt `pytest`: gehört zur Standardbibliothek, läuft also sicher in Colab, und sieht
  für Java-Entwickler aus wie JUnit. Ob `pytest` in Colab vorinstalliert ist, ist nicht geprüft.
- Die Tests laufen in einem eigenen Prozess, damit nach jeder Änderung die neue `sse_parser.py`
  gilt. Ein `import` im Kernel würde den alten Stand behalten.
- Zurücksetzen geht mit Cmd+Z bzw. Ctrl+Z in der Parser-Zelle. Die Zelle überschreibt
  `sse_parser.py`; wer den Stand ganz verliert, öffnet das Notebook neu aus dem Repo.
- Ein zweiter Lauf des Prompts schreibt andere Tests. Dass ein Test zur Grenze fehlt, folgt aus
  der Spezifikation; dass es genau 61 Tests sind und welche, gilt nur für diesen Lauf.
- Der Fehler mit `\r\n` über zwei Stücke steckt in derselben Form auch in `sse-parser.ts` von
  AstroPlanner (`chunk.replace` vor dem Anhängen an den Puffer). Ob der Server dort je `\r\n`
  sendet, ist nicht geprüft; AstroPlanner wurde nicht geändert.
