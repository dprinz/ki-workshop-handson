# Python für Java-Entwickler, am Neuron

Übungs-Notebook für den KI-Workshop: so viel Python, wie die übrigen Notebooks brauchen, für
Entwickler, die Java kennen. Sechs kurze Abschnitte zeigen je eine Java-Zeile und das Python
dazu (Variablen ohne Typ, Einrückung statt Klammern, Listen und Slices, `for` und `range`, `def`
mit Defaultwerten, f-Strings). Danach wird das Neuron von der Folie „Ein Neuron multipliziert,
addiert und vergleicht“ als Funktion nachgerechnet und ein Gewicht geändert. Als Zusatz rechnen
die Teilnehmer das XOR-Netz von der Folie „XOR braucht eine zweite Schicht“ für alle vier
Eingaben nach, erst mit einer Schleife, dann mit NumPy als Matrixmultiplikation in einer Zeile.

Im Workshop am ersten Vormittag direkt nach der Folie zum XOR-Netz, 15 Minuten zu zweit an
einem Laptop: Pflicht (Python und Neuron) rund 10 Minuten, Zusatz (XOR) für die restliche Zeit.
Zusätzlich geht das Notebook mit der Einladung als freiwillige Vorbereitung hinaus; es erklärt
deshalb das Neuron und XOR selbst und setzt die Folien nicht voraus.

## Starten

```bash
uv sync
```

```bash
uv run jupyter lab python_am_neuron.ipynb --LabApp.user_settings_dir=../einstellungen-jupyterlab
```

In Colab braucht es nichts ausser dem Notebook: NumPy ist dort installiert, Daten gibt es keine.

## Was im Ordner liegt

| Datei | Inhalt |
|---|---|
| `python_am_neuron.ipynb` | das Notebook, Ausgaben aus einem echten lokalen Lauf |
| `pyproject.toml`, `uv.lock` | Python 3.12, JupyterLab, NumPy |

Die Aufgabenzellen enthalten ein lauffähiges Gerüst. Die gespeicherten Ausgaben dieser Zellen
zeigen deshalb das unfertige Gerüst (zum Beispiel `0` statt der erwarteten `1`), die
zugeklappten Lösungszellen darunter das richtige Ergebnis. Die Lösungen arbeiten mit eigenen
Namen (`neuron_loesung`, `x_folie`, `y_loesung`), damit sie beim „Alle ausführen“ nichts
überschreiben, was die Teilnehmer geschrieben haben.

## Werte aus dem Deck

- **Neuron:** Eingaben 1, 3, 2, Gewichte 2, −1, 0.5, Bias 0.5, Ausgabe 1 bei Summe grösser als
  null. Ohne Bias ist die Summe genau 0, also Ausgabe 0. Alles wie auf der Folie.
- **XOR:** Die Folie zeigt die Grenzen von h₁ und h₂ nur als Geraden. Aus der Grafik abgelesen
  liegen sie bei x₁ + x₂ = 0.5 und x₁ + x₂ = 1.5, daraus h₁ mit w = (1, 1), b = −0.5 und h₂
  mit w = (1, 1), b = −1.5. Für den Ausgang (h₁ ja, h₂ nein) ist w = (1, −1), b = −0.5 gewählt.
  Als Aktivierung dient die Stufe des Neurons, nicht ReLU, damit h₁ und h₂ genau 0 oder 1
  melden; das Notebook sagt das.

## Gemessen

Lokal auf dem MacBook Pro mit M3 Pro, `nbconvert --execute`: alle Zellen zusammen 0,6 s
Rechenzeit (mit Start des Kernels rund 11 s). Jede Zelle braucht unter 5 ms, ausser der
NumPy-Zelle mit dem Import (0,5 s).

Geschätzt für Colab-CPU: jede Zelle unter 1 s, der NumPy-Import rund 1 bis 3 s. Rechenzeit
spielt hier keine Rolle; die 15 Minuten gehen ins Lesen und Schreiben.

## Bekannte Grenzen

- Die Zeitbox ist geschätzt, nicht mit Teilnehmern gemessen. Wird es knapp, ist der
  Python-Teil zum Überfliegen gedacht: Die Zellen laufen ohne Änderung.
- Die Gewichte des XOR-Netzes stehen so nicht auf der Folie, siehe oben.
