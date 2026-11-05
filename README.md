# KI-Workshop: Notebooks zum Selberausführen

Notebooks aus dem Workshop „KI vom Perzeptron zum LLM“, zum Ausführen in Google Colab oder lokal.
Die gespeicherten Ausgaben stammen aus einem Lauf auf einem MacBook Pro mit M3 Pro.

Testversion: Inhalt und Aufbau ändern sich noch.

## In Colab öffnen

Die Übungen in der Reihenfolge des Workshops. Die Nummer steht auf der Folie und vor dem Ordner.
Jede ist für 10 bis 15 Minuten zu zweit gedacht, mit einem Pflichtteil und einer Zusatzaufgabe;
die Lösungen liegen zugeklappt im Notebook.

| Nr | Tag | Übung | Inhalt | Colab |
|---|---|---|---|---|
| 01 | 1 | Vogel oder Park | Ein vortrainiertes Bildmodell lernt, Vögel von Parks zu unterscheiden; eigenes Foto testen | [öffnen](https://colab.research.google.com/github/dprinz/ki-workshop-handson/blob/main/01-vogel-oder-park/vogel_oder_park.ipynb) |
| 02 | 1 | Python am Neuron | So viel Python, wie die Übungen brauchen, für Java-Entwickler; ein Neuron und das XOR-Netz nachrechnen. Auch als Vorbereitung vor dem Workshop | [öffnen](https://colab.research.google.com/github/dprinz/ki-workshop-handson/blob/main/02-python-am-neuron/python_am_neuron.ipynb) |
| 03 | 1 | Auswendig gelernt | Ein Netz lernt 1'000 MNIST-Ziffern auswendig, und was dagegen hilft | [öffnen](https://colab.research.google.com/github/dprinz/ki-workshop-handson/blob/main/03-auswendig-gelernt/overfitting.ipynb) |
| 04 | 1 | Tokenizer | Wie Qwen2.5 und GPT-2 Text in Token zerlegen | [öffnen](https://colab.research.google.com/github/dprinz/ki-workshop-handson/blob/main/04-tokenizer/tokenizer.ipynb) |
| 05 | 1 | Base gegen Instruct | Dasselbe Sprachmodell vor und nach dem Post-Training | [öffnen](https://colab.research.google.com/github/dprinz/ki-workshop-handson/blob/main/05-base-gegen-instruct/base_und_instruct.ipynb) |
| 06 | 1 | Template und Temperatur | Was das Modell wirklich bekommt, und die Verteilung für das nächste Token | [öffnen](https://colab.research.google.com/github/dprinz/ki-workshop-handson/blob/main/06-template-und-temperatur/template_und_temperatur.ipynb) |
| 07 | 1 | Ähnlichkeitssuche | Eine Vektorsuche als Schleife über 643 Textstücke | [öffnen](https://colab.research.google.com/github/dprinz/ki-workshop-handson/blob/main/07-aehnlichkeitssuche/aehnlichkeitssuche.ipynb) |
| 08 | 2 | Suche messen | Hit Rate und MRR über 20 Testfragen | [öffnen](https://colab.research.google.com/github/dprinz/ki-workshop-handson/blob/main/08-suche-messen/suche_messen.ipynb) |
| 09 | 2 | Einen Hook schreiben | Ein Hook für Claude Code, der die `.env` schützt | [öffnen](https://colab.research.google.com/github/dprinz/ki-workshop-handson/blob/main/09-hook-schreiben/hook_schreiben.ipynb) |
| 10 | 2 | Mutation von Hand | Würde ein Test rot, wenn die Logik fehlt? | [öffnen](https://colab.research.google.com/github/dprinz/ki-workshop-handson/blob/main/10-mutation-von-hand/mutation_von_hand.ipynb) |
| 11 | 2 | Hook gegen Exfiltration | Den Hook gegen Abfluss nach aussen erweitern, und wo er an Grenzen stösst | [öffnen](https://colab.research.google.com/github/dprinz/ki-workshop-handson/blob/main/11-hook-gegen-exfiltration/hook_exfiltration.ipynb) |

Zum Nachlesen, im Workshop nicht als Übung:

| Notebook | Inhalt | Colab |
|---|---|---|
| Was hat es gelernt? | Worauf das Vogel-Modell schaut: Verdecken, Zoom, Unschärfe | [öffnen](https://colab.research.google.com/github/dprinz/ki-workshop-handson/blob/main/01-vogel-oder-park/was_hat_es_gelernt.ipynb) |
| Kreuzvalidierung | Wie viel eine Trefferquote auf 40 Bildern wert ist | [öffnen](https://colab.research.google.com/github/dprinz/ki-workshop-handson/blob/main/01-vogel-oder-park/kreuzvalidierung.ipynb) |
| Worktrees | Zwei Arbeitskopien eines Repos nebeneinander | [öffnen](https://colab.research.google.com/github/dprinz/ki-workshop-handson/blob/main/nachlesen-worktrees/worktrees.ipynb) |

In Colab *Laufzeit → Alle ausführen*. Die erste Code-Zelle klont dieses Repo nach `/content`,
weil Colab nur das Notebook öffnet, nicht die Hilfsdateien und Bilder daneben. Lokal tut sie
nichts. Ein Google-Konto braucht es für Colab, einen API-Key nicht.

Colab fragt beim ersten Ausführen nach, weil das Notebook nicht von Google stammt:
*Trotzdem ausführen*.

Eine GPU braucht es nicht, die kostenlose CPU-Laufzeit reicht. Sie ist aber deutlich langsamer
als ein aktueller Laptop. Gemessen in Colab am 4. November 2026:

| Notebook | längster Schritt in Colab | auf dem MacBook Pro M3 Pro |
|---|---|---|
| Vogel oder Park | Training 42 bis 67 s (drei Läufe) | unter 2 s |
| Was hat es gelernt? | Test mit Zoom und Unschärfe 30 s | wenige Sekunden |
| Kreuzvalidierung | Merkmale berechnen 21 s | wenige Sekunden |
| Auswendig gelernt | 46 bis 62 s pro Lauf, drei Läufe | 7 s pro Lauf |
| Tokenizer | Tokenizer laden 22 s | 9 bis 19 s |
| Base gegen Instruct | Modelle laden 48 s, jede Antwort 12 bis 13,5 s; mit T4 83 s und 2 bis 3,5 s | 12 bis 16 s, jede Antwort 1,5 bis 3 s |
| Template und Temperatur | Modell laden 35 s | 6 s |
| Ähnlichkeitssuche | ganzes Notebook rund eine Minute | erste Zelle 7 bis 11 s |
| Suche messen | ganzes Notebook 49 s, samt Download | erste Zelle 7 bis 11 s |
| Python am Neuron, Hooks, Mutation, Worktrees | wenige Sekunden | unter einer Sekunde, Worktrees ohne den Klon |

Mit *Laufzeit → Laufzeittyp ändern → T4-GPU* nutzen die Vogel-Notebooks die GPU automatisch. Das
Overfitting-Notebook rechnet absichtlich auf der CPU. „Base gegen Instruct“ nimmt mit GPU das
grössere Modell (1,5 Mrd. Parameter), ohne GPU das kleinere (0,5 Mrd.); die anderen neuen
Übungen brauchen keine GPU.

Das kostenlose Colab erlaubt nur wenige Sitzungen gleichzeitig. Wer mehrere Notebooks
nacheinander ausführt, beendet die fertigen mit *Laufzeit → Verbindung trennen und Laufzeit
löschen*.

## Lokal starten

Mit [uv](https://docs.astral.sh/uv/), Python 3.12:

```bash
cd 01-vogel-oder-park && uv sync && uv run jupyter lab vogel_oder_park.ipynb
```

```bash
cd 03-auswendig-gelernt && uv sync && uv run jupyter lab overfitting.ipynb
```

Die übrigen Ordner genauso: `cd <ordner> && uv sync && uv run jupyter lab`.

Mehr zu Daten, Modell und bekannten Grenzen steht im README des jeweiligen Ordners.

## Daten und Lizenzen

- Vögel von iNaturalist, Parks und Landschaften von Wikimedia Commons, jeweils gemeinfrei, CC0
  oder CC BY. Urheber, Lizenz und Quelle jedes Bildes stehen in `01-vogel-oder-park/daten/quellen.csv`.
- MNIST: Yann LeCun, Corinna Cortes, Christopher J. C. Burges, CC BY-SA 3.0.
- Texte der Ähnlichkeitssuche: englische Wikipedia und Kurzdokumente aus dem Projekt AstroPlanner,
  CC BY-SA 4.0, Herkunft in `07-aehnlichkeitssuche/daten/`.
- Modelle von Hugging Face, beim Ausführen geladen: Qwen2.5 (Apache 2.0), GPT-2 (MIT),
  multilingual-e5-small (MIT).
- Die Idee zu „Vogel oder Park“ stammt aus dem fast.ai-Tutorial
  [„Is it a bird?“](https://www.kaggle.com/code/jhoward/is-it-a-bird-creating-a-model-from-your-own-data)
  von Jeremy Howard.
