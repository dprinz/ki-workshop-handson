# Worktrees

Kleines Jupyter-Notebook für den KI-Workshop: zwei Worktrees eines Repos, eine Änderung, die
der andere Worktree nicht sieht, und die Fehlermeldung, wenn derselbe Branch ein zweites Mal
ausgecheckt werden soll. Alles mit Git in `%%bash`-Zellen, ohne Agent und ohne Modell.

Geplant als Übung zur Wahl am zweiten Tag, direkt nach der Live-Demo mit zwei Ständen von
AstroPlanner im Block zu parallelen Agents, 10 min zu zweit in Colab. Für alle sind die fünf
Schritte, Bonus ist die Änderung zu committen und im anderen Worktree zu mergen. Branches
(`demo/a`, `demo/b`) und Befehle sind dieselben wie in der Live-Demo.

## Starten

```bash
uv sync
```

```bash
uv run jupyter lab worktrees.ipynb --LabApp.user_settings_dir=../einstellungen-jupyterlab
```

Danach im Menü *Kernel → Restart Kernel and Run All Cells*. Das Notebook braucht Git und Netz
für den Klon.

## Was das Notebook anlegt

Das Notebook klont das öffentliche Repo `dprinz/ki-workshop-handson` ein zweites Mal, in Colab
nach `/content/uebung-worktrees`, lokal in den temporären Ordner des Systems
(`tempfile.gettempdir()`, auf dem Mac unter `/var/folders/…`). Der Klon, in dem das Notebook
selbst liegt, bleibt unberührt. Die Git-Identität für den Commit im Bonus setzt
`git config` ohne `--global`, sie gilt nur für diesen Klon. Die letzte Zelle entfernt die
Worktrees mit `git worktree remove` und löscht danach den ganzen Übungsordner.

## Was im Ordner liegt

| Datei | Inhalt |
|---|---|
| `worktrees.ipynb` | das Notebook mit fünf Schritten und dem Bonus, Ausgaben aus einem echten Lauf |

## Gemessen

Lokal auf dem MacBook Pro mit M3 Pro, Git 2.56.0, am 4. November 2026:

| Schritt | lokal | Colab-CPU, geschätzt |
|---|---|---|
| Klonen (rund 10 MB) | 192 s, langsames WLAN | wenige Sekunden |
| Worktrees anlegen, ändern, Branch doppelt, Bonus, Aufräumen | je unter 0,2 s | je unter 1 s |

Die Zeit hängt fast nur am Klon. In Colab (frische Laufzeit, Gratis-CPU, „Alle ausführen“, 2026-11-04) lief das Notebook ohne Fehler; pro Zelle nicht gemessen.

## Bekannte Grenzen

- Die gespeicherten Ausgaben stammen von einem Mac, auf dem Git deutsch meldet:
  „Schwerwiegend: 'demo/a' wird bereits von Arbeitsverzeichnis in … verwendet“. Colab meldet
  auf Englisch. Je nach Git-Version lautet die Meldung „is already used by worktree at …“ oder
  „is already checked out at …“; das Notebook nennt beide.
- Die Pfade in `git worktree list` sind lokal lang (`/private/var/folders/…`), in Colab kurz.
- `ls` färbt die Ordnernamen lokal ein, in den gespeicherten Ausgaben stehen deshalb
  Farbcodes; Jupyter zeigt sie als Farbe.
- Läuft *Alle ausführen*, läuft auch die Lösung des Bonus. Der Worktree `handson-a` ist dann
  beim Aufräumen sauber; ohne Commit löscht die letzte Zelle ihn mit `--force`.
