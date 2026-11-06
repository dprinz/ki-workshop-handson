# Einen Hook schreiben

Übungs-Notebook für den KI-Workshop. Die Teilnehmer schreiben die Prüfung eines
PreToolUse-Hooks für Claude Code als Python-Funktion: Sie bekommt einen Tool-Aufruf als `dict`,
so wie Claude Code ihn dem Hook als JSON auf stdin gibt, und antwortet „erlauben“ oder
„blockieren“ mit Grund. Getestet wird gegen vorbereitete Aufrufe mit Soll-Spalte. Kein Modell,
kein Netz, jede Zelle läuft in Millisekunden.

- **Wann im Workshop:** Tag 2 vor dem Mittag, nach der Folie „Hooks: Skripte an festen Stellen der
  Tool-Schleife“
- **Für alle:** Lesen und Schreiben der `.env` blockieren, mit jedem Tool und in der Shell;
  `.env.example` bleibt erlaubt. Drei Aufgaben in einer Zelle: Test der Startfunktion lesen
  (7 von 13), erster Versuch `".env" in befehl` (12 von 13, `cat .env.example` wird Fehlalarm),
  Fehlalarm beheben (13 von 13)
- **Bonus:** einen Aufruf finden, den der eigene Hook durchlässt; als Knobelaufgabe das Grep-Tool
  und `cat .e""nv` schliessen, ohne dass einer der 13 Fälle kippt (18 Aufrufe)

Zeitbox 15 min, zu zweit. Am Nachmittag erweitert `11-hook-gegen-exfiltration` diesen Hook.

## Starten

```bash
uv sync
```

```bash
uv run jupyter lab hook_schreiben.ipynb --LabApp.user_settings_dir=../einstellungen-jupyterlab
```

Danach im Menü *Kernel → Restart Kernel and Run All Cells*. Die Lösungszellen sind zugeklappt und
laufen dabei mit; sie verwenden eigene Namen (`pruefe_loesung`, `pruefe_dicht_loesung`) und
überschreiben `pruefe` der Teilnehmer nicht.

## Was im Ordner liegt

| Datei | Inhalt |
|---|---|
| `hook_schreiben.ipynb` | Übung „Einen Hook schreiben“, Ausgaben aus einem echten lokalen Lauf |
| `helfer.py` | Aufrufe bauen (`read`, `edit`, `write`, `bash`, `grep`), die vorbereiteten Fälle mit Soll (`FAELLE_ENV`, für die Knobelaufgabe `FAELLE_UMWEGE`), Testlauf als Tabelle mit ✓, wenn alles stimmt (`teste`, `probiere`); dazu `hosts()`, `urls()` und die Fälle für `11-hook-gegen-exfiltration`, weil beide Übungen dieselbe Datei nutzen |
| `env_hook.py` | die Lösung der Übung als lauffähiger Hook (stdin lesen, Exit-Code 2, Grund auf stderr); das Notebook ruft ihn am Ende mit JSON auf stdin auf |
| `daten/kurs-service-README.md` | Kopie der README des Dienstes `kurs-service` aus dem Beispiel zur Prompt Injection, mit dem versteckten HTML-Kommentar |

`daten/kurs-service-README.md` heisst bewusst nicht `README.md`: Die Datei enthält eine Anweisung
an KI-Agents, und ein Agent, der im Repo arbeitet, soll sie nicht als Projektbeschreibung lesen.
Der `curl` darin zielt auf `127.0.0.1`.

## Gemessen

MacBook Pro M3 Pro, `nbconvert --execute`, 2026-11-04, nach dem Umbau in Aufgaben 1–5 erneut am
2026-11-06. Alle Code-Zellen zusammen unter 0,1 s; die einzige messbare Zelle ist der Aufruf von
`env_hook.py` als Unterprozess (0,05 bis 0,3 s). Colab-CPU, geschätzt: jede Zelle unter 1 s, der
Unterprozess 1 bis 2 s. In Colab (frische Laufzeit,
Gratis-CPU, „Alle ausführen“, 2026-11-04, Stand vor dem Umbau in Aufgaben 1–5) lief das Notebook ohne Fehler in wenigen Sekunden.
Gebraucht wird nur die Standardbibliothek, kein `pip install`.

## Woher die Angaben stammen

- Format des Aufrufs (`tool_name`, `tool_input` mit `file_path` bzw. `command`), Exit-Code 2
  blockiert und stderr geht an Claude, andere Codes, Absturz und Timeout blockieren nicht,
  `matcher` als regulärer Ausdruck, `permissionDecision`: Claude-Code-Doku, Hooks
  (code.claude.com/docs/en/hooks), abgerufen am 2026-11-04.
- Der Hook der Folie (nur `file_path`, `.env.example` erlaubt, Matcher `Edit|MultiEdit|Write`):
  AstroPlanner, `.claude/hooks/protect-files.sh`.

## Vereinfachungen und bekannte Grenzen

- Die Aufrufe haben nur `hook_event_name`, `cwd`, `tool_name` und `tool_input`. Echte Aufrufe
  haben weitere Felder (`session_id`, `transcript_path`, `tool_use_id` u. a.); das steht im
  Notebook.
- Der Projektpfad `/home/dev/kurs-service` ist erfunden, damit die Pfade absolut sind wie in der
  Doku.
- `env_hook.py` ist mit JSON auf stdin geprüft, nicht in einer laufenden Claude-Code-Sitzung. Der
  `settings.json`-Eintrag folgt dem Aufbau von AstroPlanner und der Doku.
- Die Lösung ist eine Sperrliste auf Text und als solche absichtlich lückenhaft; die Bonusaufgaben
  zeigen die Lücken. Auch die Lösung der Knobelaufgabe schliesst nur zwei davon; `cat .en?`, Base64
  und Skripte bleiben offen, das steht im Notebook unter der Lösung.
