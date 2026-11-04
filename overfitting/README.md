# Auswendig gelernt

Kleines Jupyter-Notebook für den KI-Workshop: Ein Netz mit einer Hidden Layer lernt 1'000
MNIST-Ziffern auswendig. Es zeigt Overfitting als Live-Lauf, die Probe mit zufälligen Labels und
was dagegen hilft.

Gebaut, im Workshop nicht eingeplant. Passen würde es zur Folie mit den echten Loss-Kurven
im Grundlagenblock.

## Starten

```bash
uv sync
```

```bash
uv run jupyter lab overfitting.ipynb --LabApp.user_settings_dir=../einstellungen-jupyterlab
```

Die Schriftgrössen für den Beamer stehen in `../einstellungen-jupyterlab/`, gemeinsam für alle Workshop-Labs.

Danach im Menü *Kernel → Restart Kernel and Run All Cells*. Ein Lauf mit 150 Epochen dauert auf
dem MacBook Pro mit M3 Pro rund 7 Sekunden, alle Zellen zusammen rund 30 Sekunden. Das Notebook
rechnet auf der CPU: Das kleine Netz ist dort so schnell wie auf der GPU, und der Lauf ist
reproduzierbar. Es braucht kein Netz.

## Was im Ordner liegt

| Datei | Inhalt |
|---|---|
| `overfitting.ipynb` | das Notebook mit den vier Schritten, Ausgaben aus einem echten Lauf |
| `helfer.py` | Ziffern und Kurven zeigen, damit das Notebook das Training zeigt und nicht Matplotlib |
| `daten/mnist-auszug.npz` | die ersten 10'000 Trainingsbilder und die letzten 10'000 als Validierung, aus dem MNIST-Trainingsset |

MNIST: Yann LeCun, Corinna Cortes, Christopher J. C. Burges, CC BY-SA 3.0.

## Gemessen

Mittelwerte über fünf Seeds, 150 Epochen mit 1'000 Bildern oder 15 Epochen mit 10'000, also gleich
viele gesehene Bilder. Im Notebook steht ein Seed, die Zahlen weichen dort leicht ab.

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
