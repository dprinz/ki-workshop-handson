# Hook gegen Exfiltration

Übungs-Notebook für den KI-Workshop. Die Teilnehmer schreiben die Prüfung eines
PreToolUse-Hooks für Claude Code als Python-Funktion: Sie bekommt einen Tool-Aufruf als `dict`,
so wie Claude Code ihn dem Hook als JSON auf stdin gibt, und antwortet „erlauben“ oder
„blockieren“ mit Grund. Getestet wird gegen vorbereitete Aufrufe mit Soll-Spalte. Kein Modell,
kein Netz, jede Zelle läuft in Millisekunden.

- **Wann im Workshop:** Tag 2 am Nachmittag bei Security, nach der Folie „Folgt der Agent dem
  Kommentar in der README?“
- **Für alle:** den Hook vom Vormittag aus `09-hook-schreiben` (als Startpunkt in der ersten Zelle)
  gegen Abfluss an fremde Hosts erweitern. Drei Aufgaben: README und Test lesen (8 von 14);
  `curl`, `wget`, `requests` und `urllib` blockieren (12 von 14, `localhost` und Maven Central
  werden Fehlalarme); erlaubte Hosts mit `hosts()` wieder durchlassen (14 von 14)
- **Bonus:** einen Aufruf finden, der trotzdem durchkommt; als Knobelaufgabe `git push` nur an URLs
  der eigenen Organisation zulassen, Lesen von GitHub bleibt frei (18 Aufrufe). Was die Sandbox laut
  Doku enger fasst, lesen alle zum Abschluss

Zeitbox 15 min, zu zweit. Das Notebook hängt nicht von `09-hook-schreiben` ab.

## Starten

```bash
uv sync
```

```bash
uv run jupyter lab hook_exfiltration.ipynb --LabApp.user_settings_dir=../einstellungen-jupyterlab
```

Danach im Menü *Kernel → Restart Kernel and Run All Cells*. Die Lösungszellen sind zugeklappt und
laufen dabei mit; sie verwenden eigene Namen (`pruefe_abfluss_loesung`, `pruefe_github_loesung`)
und überschreiben `pruefe` der Teilnehmer nicht.

## Was im Ordner liegt

| Datei | Inhalt |
|---|---|
| `hook_exfiltration.ipynb` | Übung „Den Hook gegen Exfiltration erweitern“, Ausgaben aus einem echten lokalen Lauf |
| `helfer.py` | Aufrufe bauen (`read`, `edit`, `write`, `bash`, `grep`), die vorbereiteten Fälle mit Soll (`FAELLE_ABFLUSS`, für die Knobelaufgabe `FAELLE_GITHUB`), Testlauf als Tabelle mit ✓, wenn alles stimmt (`teste`, `probiere`), `hosts()`, `urls()`, `ERLAUBTE_HOSTS` und `EIGENE_ORG` |
| `env_hook.py` | die Lösung aus `09-hook-schreiben` als lauffähiger Hook (stdin lesen, Exit-Code 2, Grund auf stderr) |
| `daten/kurs-service-README.md` | Kopie der README des Dienstes `kurs-service` aus dem Beispiel zur Prompt Injection, mit dem versteckten HTML-Kommentar |

`daten/kurs-service-README.md` heisst bewusst nicht `README.md`: Die Datei enthält eine Anweisung
an KI-Agents, und ein Agent, der im Repo arbeitet, soll sie nicht als Projektbeschreibung lesen.
Der `curl` darin zielt auf `127.0.0.1`.

## Gemessen

MacBook Pro M3 Pro, `nbconvert --execute`, 2026-11-04, nach dem Umbau in Aufgaben 1–5 erneut am
2026-11-06. Alle Code-Zellen zusammen unter 0,1 s.
Colab-CPU, geschätzt: jede Zelle unter 1 s. In Colab (frische Laufzeit, Gratis-CPU, „Alle
ausführen“, 2026-11-04, Stand vor dem Umbau in Aufgaben 1–5) lief das Notebook ohne Fehler in wenigen Sekunden. Gebraucht wird nur die
Standardbibliothek, kein `pip install`.

## Woher die Angaben stammen

- Format des Aufrufs (`tool_name`, `tool_input` mit `file_path` bzw. `command`), Exit-Code 2
  blockiert und stderr geht an Claude, andere Codes, Absturz und Timeout blockieren nicht,
  `matcher` als regulärer Ausdruck, `permissionDecision`: Claude-Code-Doku, Hooks
  (code.claude.com/docs/en/hooks), abgerufen am 2026-11-04.
- Sandbox: nur Shell-Befehle und ihre Kindprozesse; Verbindungen laufen über einen Proxy, der den
  Hostnamen prüft (macOS: Seatbelt lässt nur die Verbindung zum Proxy zu, Linux: eigener
  Netz-Namespace); Werkzeuge, die den Proxy nicht nutzen, kommen nicht hinaus; fremde Hosts je
  nach Modus Rückfrage oder Ablehnung; Read, Edit, Write und Hooks laufen ausserhalb:
  Claude-Code-Doku, Sandboxing (code.claude.com/docs/en/sandboxing), abgerufen am 2026-11-04.
- Die README mit dem Angriff: aus dem Beispiel zur Prompt Injection, das im Workshop als Aufnahme
  läuft (Empfänger und `.env` mit Testwerten auf dem eigenen Rechner).

## Vereinfachungen und bekannte Grenzen

- Die Aufrufe haben nur `hook_event_name`, `cwd`, `tool_name` und `tool_input`. Echte Aufrufe
  haben weitere Felder (`session_id`, `transcript_path`, `tool_use_id` u. a.); das steht im
  Notebook in `09-hook-schreiben`.
- Der Projektpfad `/home/dev/kurs-service` ist erfunden, damit die Pfade absolut sind wie in der
  Doku. `setup-check.example.com` ist eine reservierte Beispiel-Domain und steht für den Server
  eines Angreifers.
- Die Tabelle zur Sandbox im Notebook beruht für fremde Hosts auf der Doku. Im Workshop-Lauf
  geprüft ist nur die Sperre der `.env` und das Netz gegen `localhost`. Ob `nc` in der Sandbox
  scheitert, ist aus der Doku-Aussage zu Werkzeugen ohne Proxy abgeleitet, nicht gemessen.
- Die Lösung ist eine Sperrliste auf Text und als solche absichtlich lückenhaft; die Bonusaufgaben
  zeigen die Lücken. Die Lösung der Knobelaufgabe sieht nur den einzelnen Aufruf: `git push` über ein
  vorher angelegtes Remote oder an eine SSH-Adresse kommt durch, das steht im Notebook unter der
  Lösung. Die Organisation `kurs-org` ist erfunden.
