# Vogel oder Park

Kleines Jupyter-Notebook für den KI-Workshop: Ein vortrainiertes Bildmodell lernt, Fotos mit
Vögeln von Fotos von Parks und Landschaften zu unterscheiden. Es läuft am ersten Workshop-Tag
direkt nach dem xkcd-Comic „Tasks“, bevor die Grundlagen erklärt sind. Geplant als erste Übung:
Die Teilnehmer führen es zu zweit in Colab aus, 15 min. Pflicht ist alles ausführen, die
Trefferquote ablesen und die schwierigen Fälle ansehen, Zusatz ein eigenes Foto per URL oder
Upload; beides steht oben im Notebook. Die Idee
stammt aus dem fast.ai-Tutorial [„Is it a bird?“](https://www.kaggle.com/code/jhoward/is-it-a-bird-creating-a-model-from-your-own-data)
von Jeremy Howard (Lektion 1 von [Practical Deep Learning](https://course.fast.ai/Lessons/lesson1.html)).

## Starten

```bash
uv sync
```

```bash
uv run jupyter lab vogel_oder_park.ipynb --port 8891 --ServerApp.port_retries=0 --IdentityProvider.token=ki-workshop --LabApp.user_settings_dir=../einstellungen-jupyterlab
```

Die Schriftgrössen für den Beamer stehen in `../einstellungen-jupyterlab/`, gemeinsam für alle Workshop-Labs.
Port und Token sind fest, weil das Live-Etikett auf den Folien das Notebook über
`http://localhost:8891/lab/tree/…?token=ki-workshop` öffnet (`NotebookLive.vue` im Deck). Ist der
Port belegt, bricht der Start ab, statt einen anderen zu nehmen. Das Lab hört nur auf localhost.

Läuft das Deck mit `pnpm dev`, geht es auch ohne Terminal: Der Knopf links vom Etikett
startet das Lab (Play) und fährt es samt Kernel wieder herunter (Stop), ein Klick aufs Etikett
startet ein gestopptes Lab ebenfalls. Endet das Deck, enden die Labs, die es gestartet hat.

Danach im Menü *Kernel → Restart Kernel and Run All Cells*. Alle Zellen zusammen laufen auf dem
MacBook Pro mit M3 Pro in rund 10 Sekunden, Training samt Prüfen in unter zwei Sekunden.
In Colab auf der Gratis-CPU dauert das Training 55 Sekunden (gemessen). Das eigene Foto per URL
braucht lokal unter einer Sekunde, in Colab geschätzt wenige Sekunden.

## Was im Ordner liegt

| Datei | Inhalt |
|---|---|
| `vogel_oder_park.ipynb` | das Notebook mit den fünf Schritten, Ausgaben aus einem echten Lauf |
| `kreuzvalidierung.ipynb` | Wie viel die 39 von 40 wert sind: 100 Splits, Kreuzvalidierung, Varianten vergleichen. Nicht im Workshop eingeplant |
| `was_hat_es_gelernt.ipynb` | Worauf das Modell schaut, Verdecken, Zoom, Unschärfe, kleiner Vogel im Park. Live am Ende der Grundlagen |
| `helfer.py` | Bilder laden und anzeigen, ein eigenes Foto holen, damit das Notebook den Ablauf zeigt und nicht HTTP-Aufrufe |
| `daten/` | 100 Vögel, 100 Parks, verkleinert auf 400 Pixel |
| `probe/` | acht schwierige Fälle, die weder im Training noch in der Validierung vorkommen; lokal kann hier auch ein eigenes Foto liegen |
| `eigene/` | Fotos aus der letzten Zelle, per URL geladen oder in Colab hochgeladen; nicht im Repo |
| `daten/quellen.csv` | Urheber, Lizenz und Quelle jedes Bildes, auch der schwierigen Fälle |

## Modell

ResNet-18 aus torchvision, auf ImageNet vortrainiert. Das ist ein Bildklassifikator; er sagt, was
auf dem Bild ist, nicht wo (das wäre Object Detection). Das Notebook friert die 11,2 Millionen
übernommenen Parameter ein, auch die BatchNorm-Statistiken bleiben fest, und trainiert nur die
neue letzte Schicht mit 1'026 Parametern.

ImageNet enthält viele Vogelklassen, das Modell bringt also fast alles mit. Die hohe Trefferquote
zeigt, was vortrainierte Modelle leisten, nicht, dass Vogelerkennung in zwei Sekunden lernbar ist.

## Daten

Vögel stammen von iNaturalist (die Fotos mit den meisten Stimmen, pro Art eines, CC0 oder CC BY),
Parks und Landschaften von Wikimedia Commons (gemeinfrei, CC0 oder CC BY). Beide brauchen keinen
API-Key.

Die Bilder sind vorab geladen und von Hand durchgesehen. Von 280 geladenen Bildern flogen 61
raus: Bei den Vögeln stehen unter den beliebtesten Fotos viele Witzbilder, Schilder und Fotos mit
kaum sichtbarem Tier, bei den Parks Gemälde, Postkarten, Blumen und Bildserien desselben Motivs.
Acht wurden schwierige Fälle für den Schluss, die restlichen elf fielen beim Kürzen auf 100 pro Klasse weg. Fotos aus
dem Netz gehören nicht ungesehen auf den Beamer. Das Laden dauert ausserdem rund drei Minuten,
also nichts für den Live-Teil.

Das Beispiel in der Zelle für ein eigenes Foto ist „Kohlmeise (April 2025)“ von Romzig auf
Wikimedia Commons, gemeinfrei (CC0):
<https://commons.wikimedia.org/wiki/File:Kohlmeise_(April_2025).jpg>. Das Notebook lädt die
Vorschau mit 960 Pixeln Breite; das Modell sagt Vogel mit 99 %.

Die Download-Zelle lädt nichts, solange die Bilder im Ordner liegen. Das Notebook läuft deshalb
ohne Netz, wenn die Modellgewichte einmal geladen sind (`~/.cache/torch/hub/checkpoints/`). Nur
die letzte Zelle mit der Beispiel-URL braucht Netz; ohne meldet sie „Keine Verbindung“.
Wer den Download sehen will, entfernt `daten/` und lässt die Zelle laufen; die Bilder sind dann
ungeprüft. `git restore daten` holt den durchgesehenen Stand zurück.

## Vor dem Workshop

1. Notebook einmal komplett laufen lassen, damit die Gewichte im Cache liegen.
2. In JupyterLab *View → Appearance → Presentation Mode* einschalten und die Schrift prüfen.
3. Das Notebook ohne WLAN testen.

## Bekannte Grenzen

- Vögel und Parks kommen aus verschiedenen Quellen. Das Modell hat dadurch mehr gelernt als Vogel
  gegen Park: Stark unscharfe Parks gelten fast immer als Vogel (19 von 20 bei Radius 8), eine
  graue Fläche mit 70 %. Der Widder, der mit 54 % bei Vogel landet, passt dazu. Mehr in
  `was_hat_es_gelernt.ipynb`, gemessen an je 20 Bildern.
- 40 Validierungsbilder sind wenig, ein Bild verschiebt die Trefferquote um 2,5 Prozentpunkte. Über
  100 Splits streut das Ergebnis zwischen 38 und 40 von 40, siehe `kreuzvalidierung.ipynb`.
- Es gibt nur zwei Klassen. Ein Foto ohne Vogel und ohne Park bekommt trotzdem eine der beiden
  Antworten.
- Eigenes Foto: Die URL muss direkt auf das Bild zeigen, nicht auf eine Seite. Manche Server
  sperren Skripte (403) oder bremsen (429, bei Wikimedia beobachtet für eine nicht vorhandene
  Datei); die Zelle meldet das als Satz. HEIC-Fotos vom iPhone liest PIL nicht. Der Upload in
  Colab (`google.colab.files.upload()`) ist lokal nicht geprüft.
