# Auswendig gelernt

Kleines Jupyter-Notebook für den KI-Workshop: Ein Netz mit einer Hidden Layer lernt 1'000
MNIST-Ziffern auswendig. Es zeigt Overfitting als Live-Lauf, die Probe mit zufälligen Labels und
was dagegen hilft.

Geplant als Übung zur Wahl am ersten Tag, nach der Folie zum Gradienten, 15 min zu zweit in
Colab. Pflicht: Grundfall und zufällige Labels, danach rechnet jedes Paar ein Gegenmittel. Dafür
steht in Abschnitt 4 die Variable `VARIANTE` (`"dropout"`, `"weight_decay"` oder `"mehr_daten"`),
der Raum vergleicht danach die Endwerte per Handzeichen. Alle Gegenmittel nacheinander wären in
Colab zu lang. Zusatz: Endwerte mit der Tabelle im Notebook vergleichen, eine zweite Variante
oder eigene Werte.

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
reproduzierbar. Es braucht kein Netz.

## Was im Ordner liegt

| Datei | Inhalt |
|---|---|
| `overfitting.ipynb` | das Notebook mit den vier Schritten, Ausgaben aus einem echten Lauf mit `VARIANTE = "weight_decay"` |
| `helfer.py` | Ziffern und Kurven zeigen, damit das Notebook das Training zeigt und nicht Matplotlib |
| `daten/mnist-auszug.npz` | die ersten 10'000 Trainingsbilder und die letzten 10'000 als Validierung, aus dem MNIST-Trainingsset |

MNIST: Yann LeCun, Corinna Cortes, Christopher J. C. Burges, CC BY-SA 3.0.

## Gemessen

Mittelwerte über fünf Seeds, 150 Epochen mit 1'000 Bildern oder 15 Epochen mit 10'000, also gleich
viele gesehene Bilder. Im Notebook steht ein Seed, die Zahlen weichen dort leicht ab. Die Tabelle
steht auch im Notebook unter Abschnitt 4, damit die Paare ihre Variante mit den anderen
vergleichen können.

| Lauf | Loss-Minimum | Loss am Ende | richtig am Ende |
|---|---|---|---|
| 1'000 Bilder | 0.365 | 0.570 | 90,0 % |
| Dropout 0.5 | 0.347 | 0.590 | 90,3 % |
| Weight Decay 0.1 | 0.364 | 0.468 | 90,2 % |
| Weight Decay 1.0 | 0.332 | 0.381 | 90,2 % |
| 10'000 Bilder | 0.138 | 0.151 | 96,5 % |
| 1'000 Bilder, Labels zufällig | 2.316 | 7.146 | 10,6 % |

Der Lauf mit zufälligen Labels erreicht im Training 100 %.

## Bekannte Grenzen

- Die Gegenmittel sind mit je einer Einstellung geprüft. Dass Dropout hier kaum hilft, gilt für
  dieses Netz und diesen Wert, nicht allgemein.
- Die Folie im Deck zeigt einen Lauf mit Keras (Batch-Grösse 128, Minimum in Epoche 13). Hier ist
  die Batch-Grösse 32, das Minimum liegt bei Epoche 5 bis 7; die Aussage bleibt dieselbe.
- Die Gegenprobe mit zufälligen Labels stammt aus Zhang et al. 2017, „Understanding deep learning
  requires rethinking generalization“.
