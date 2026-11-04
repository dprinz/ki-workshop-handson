# KI-Workshop: Notebooks zum Selberausführen

Notebooks aus dem Workshop „KI vom Perzeptron zum LLM“, zum Ausführen in Google Colab oder lokal.
Die gespeicherten Ausgaben stammen aus einem Lauf auf einem MacBook Pro mit M3 Pro.

Testversion: Inhalt und Aufbau ändern sich noch.

## In Colab öffnen

| Notebook | Inhalt | Colab |
|---|---|---|
| Vogel oder Park | Ein vortrainiertes Bildmodell lernt, Vögel von Parks zu unterscheiden | [öffnen](https://colab.research.google.com/github/dprinz/ki-workshop-handson/blob/main/birds/vogel_oder_park.ipynb) |
| Was hat es gelernt? | Worauf das Modell schaut: Verdecken, Zoom, Unschärfe | [öffnen](https://colab.research.google.com/github/dprinz/ki-workshop-handson/blob/main/birds/was_hat_es_gelernt.ipynb) |
| Kreuzvalidierung | Wie viel eine Trefferquote auf 40 Bildern wert ist | [öffnen](https://colab.research.google.com/github/dprinz/ki-workshop-handson/blob/main/birds/kreuzvalidierung.ipynb) |
| Auswendig gelernt | Ein Netz lernt 1'000 MNIST-Ziffern auswendig, und was dagegen hilft | [öffnen](https://colab.research.google.com/github/dprinz/ki-workshop-handson/blob/main/overfitting/overfitting.ipynb) |

In Colab *Laufzeit → Alle ausführen*. Die erste Code-Zelle klont dieses Repo nach `/content`,
weil Colab nur das Notebook öffnet, nicht die Hilfsdateien und Bilder daneben. Lokal tut sie
nichts. Ein Google-Konto braucht es für Colab, einen API-Key nicht.

Colab fragt beim ersten Ausführen nach, weil das Notebook nicht von Google stammt:
*Trotzdem ausführen*.

Eine GPU braucht es nicht, die kostenlose CPU-Laufzeit reicht. Sie ist aber deutlich langsamer
als ein aktueller Laptop. Gemessen in Colab am 4. November 2026:

| Notebook | längster Schritt in Colab | auf dem MacBook Pro M3 Pro |
|---|---|---|
| Vogel oder Park | Training 55 s | unter 2 s |
| Was hat es gelernt? | Test mit Zoom und Unschärfe 30 s | wenige Sekunden |
| Kreuzvalidierung | Merkmale berechnen 21 s | wenige Sekunden |
| Auswendig gelernt | 62 s pro Lauf, sechs Läufe | 7 s pro Lauf |

Mit *Laufzeit → Laufzeittyp ändern → T4-GPU* nutzen die Vogel-Notebooks die GPU automatisch. Das
Overfitting-Notebook rechnet absichtlich auf der CPU.

Das kostenlose Colab erlaubt nur wenige Sitzungen gleichzeitig. Wer mehrere Notebooks
nacheinander ausführt, beendet die fertigen mit *Laufzeit → Verbindung trennen und Laufzeit
löschen*.

## Lokal starten

Mit [uv](https://docs.astral.sh/uv/), Python 3.12:

```bash
cd birds && uv sync && uv run jupyter lab vogel_oder_park.ipynb
```

```bash
cd overfitting && uv sync && uv run jupyter lab overfitting.ipynb
```

Mehr zu Daten, Modell und bekannten Grenzen steht im README des jeweiligen Ordners.

## Daten und Lizenzen

- Vögel von iNaturalist, Parks und Landschaften von Wikimedia Commons, jeweils gemeinfrei, CC0
  oder CC BY. Urheber, Lizenz und Quelle jedes Bildes stehen in `birds/daten/quellen.csv`.
- MNIST: Yann LeCun, Corinna Cortes, Christopher J. C. Burges, CC BY-SA 3.0.
- Die Idee zu „Vogel oder Park“ stammt aus dem fast.ai-Tutorial
  [„Is it a bird?“](https://www.kaggle.com/code/jhoward/is-it-a-bird-creating-a-model-from-your-own-data)
  von Jeremy Howard.
