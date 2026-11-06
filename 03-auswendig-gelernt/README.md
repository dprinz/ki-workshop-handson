# Auswendig gelernt

Kleines Jupyter-Notebook für den KI-Workshop: Ein Netz mit einer Hidden Layer lernt 1'000
MNIST-Ziffern auswendig. Es zeigt Overfitting als Live-Lauf, die Probe mit zufälligen Labels und
was dagegen hilft.

Geplant als Übung zur Wahl am ersten Tag, nach der Folie zum Gradienten, 15 min zu zweit in
Colab. Die fünf Aufgaben stehen im Notebook an der Stelle, an der man sie macht, und werden
von der ersten zur letzten etwas schwieriger. Für alle (Aufgaben 1 bis 3): Grundfall und
zufällige Labels, jeweils zuerst vermuten, dann ablesen; danach rechnet jedes Paar ein
Gegenmittel und vergleicht es mit der Tabelle im Notebook. Dafür steht in Abschnitt 4 die
Variable `VARIANTE` (`"dropout"`, `"weight_decay"` oder `"mehr_daten"`), der Raum vergleicht
danach die Endwerte per Handzeichen. Alle Gegenmittel nacheinander wären in Colab zu lang.
Bonus: eine zweite Variante oder eigene Werte (Aufgabe 4) und als Knobelaufgabe Early Stopping
auf den gespeicherten Kurven nachrechnen, ohne neu zu trainieren (Aufgabe 5, mit
Selbstkontrolle, zwei Tipps und Lösung).

## Starten

```bash
uv sync
```

```bash
uv run jupyter lab overfitting.ipynb --LabApp.user_settings_dir=../einstellungen-jupyterlab
```

Die Schriftgrössen für den Beamer stehen in `../einstellungen-jupyterlab/`, gemeinsam für alle Workshop-Labs.

Danach im Menü *Kernel → Restart Kernel and Run All Cells*. Ein Lauf mit 150 Epochen dauert auf
dem MacBook Pro mit M3 Pro rund 7 Sekunden, alle Zellen zusammen mit einer Variante rund 20
Sekunden. In Colab auf der Gratis-CPU dauert ein Lauf 46 bis 62 Sekunden, das ganze
Notebook mit Grundfall, zufälligen Labels und einer Variante rund drei Minuten (gemessen am
4. November 2026 mit `"weight_decay"`; `"mehr_daten"` ist etwas schneller, weil es nur 15-mal misst). Das Notebook
rechnet auf der CPU: Das kleine Netz ist dort so schnell wie auf der GPU, und der Lauf ist
reproduzierbar. Es braucht kein Netz. Die Zelle zu Early Stopping trainiert nicht und läuft
sofort, die Zelle mit eigenen Werten so lange wie ein Lauf.

## Was im Ordner liegt

| Datei | Inhalt |
|---|---|
| `overfitting.ipynb` | das Notebook mit fünf Abschnitten und fünf Aufgaben, Ausgaben aus einem echten Lauf mit `VARIANTE = "weight_decay"`; die Zelle zu Aufgabe 5 zeigt das leere Gerüst, die Lösung darunter das Ergebnis |
| `helfer.py` | Ziffern, Kurven und Endwerte zeigen, damit das Notebook das Training zeigt und nicht Matplotlib, und die Funktion aus Aufgabe 5 gegen eine Referenz prüfen |
| `daten/mnist-auszug.npz` | die ersten 10'000 Trainingsbilder und die letzten 10'000 als Validierung, aus dem MNIST-Trainingsset |

MNIST: Yann LeCun, Corinna Cortes, Christopher J. C. Burges, CC BY-SA 3.0.

## Gemessen

Mittelwerte über fünf Seeds, 150 Epochen mit 1'000 Bildern oder 15 Epochen mit 10'000, also gleich
viele gesehene Bilder. Im Notebook steht ein Seed, die Zahlen weichen dort leicht ab. Die Tabelle
steht auch im Notebook unter Abschnitt 4, damit die Paare ihre Variante mit den anderen
vergleichen können.

| Lauf | Loss-Minimum | Loss am Ende | Accuracy am Ende |
|---|---|---|---|
| 1'000 Bilder | 0.365 | 0.570 | 90,0 % |
| Dropout 0.5 | 0.347 | 0.590 | 90,3 % |
| Weight Decay 0.1 | 0.364 | 0.468 | 90,2 % |
| Weight Decay 1.0 | 0.332 | 0.381 | 90,2 % |
| 10'000 Bilder | 0.138 | 0.151 | 96,5 % |
| 1'000 Bilder, Labels zufällig | 2.316 | 7.146 | 10,6 % |

Der Lauf mit zufälligen Labels erreicht im Training 100 %.

Early Stopping mit Geduld 5 auf den Kurven des Grundfalls, Seeds 0 bis 4, nachgerechnet am
6. November 2026: Das Minimum des Validierungs-Loss liegt in Epoche 5 bis 10, abgebrochen wird in
Epoche 10 bis 15, also nach höchstens einem Zehntel der 150 Epochen. Die behaltene Epoche ist
jedes Mal das Minimum über alle 150 Epochen. Ihre Accuracy liegt jedes Mal 0,7 bis 1,1
Prozentpunkte unter der nach 150 Epochen (88,6 bis 89,5 % gegen 89,7 bis 90,5 %); die höchste
Accuracy erreichen die Läufe erst in Epoche 109 bis 149. Die Lösung im Notebook nennt das als
Nebenbefund: Early Stopping auf den Loss hält nicht bei der besten Accuracy an.

## Bekannte Grenzen

- Die Gegenmittel sind mit je einer Einstellung geprüft. Dass Dropout hier kaum hilft, gilt für
  dieses Netz und diesen Wert, nicht allgemein.
- Die Folie im Deck zeigt einen Lauf mit Keras (Batch-Grösse 128, Minimum in Epoche 13). Hier ist
  die Batch-Grösse 32, das Minimum liegt bei Epoche 5 bis 10 (Seeds 0 bis 4); die Aussage bleibt
  dieselbe.
- Die Prüfung in Aufgabe 5 rechnet die Sollwerte zur Laufzeit mit einer Referenz in `helfer.py`
  nach und nicht gegen feste Zahlen, weil die Kurven auf einer anderen CPU numerisch leicht
  anders ausfallen können. Den Sollwert nennt sie nur für die kleinen Kurven, die man von Hand
  nachrechnen kann, damit die Ausgabe des leeren Gerüsts die Antwort nicht vorwegnimmt.
- Für Keras nennt die Lösung `EarlyStopping` mit `monitor`, `patience` und
  `restore_best_weights` (Keras-Dokumentation): Ohne `restore_best_weights=True` behält Keras die
  Gewichte der letzten Epoche.
- Die Gegenprobe mit zufälligen Labels stammt aus Zhang et al. 2017, „Understanding deep learning
  requires rethinking generalization“.
