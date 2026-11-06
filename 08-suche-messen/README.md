# Suche messen

Jupyter-Notebook für den KI-Workshop. Es misst die Ähnlichkeitssuche aus `07-aehnlichkeitssuche`,
die Python-Fassung des Java-Programms aus der Live-Demo: dasselbe Embedding-Modell
`multilingual-e5-small`, dieselben 643 Chunks aus AstroPlanners Wissensbasis, die Suche als
Schleife über alle Chunks. Die Vektoren der Chunks sind vorberechnet und liegen im Ordner. Im
Notebook wird nur der Suchtext eingebettet.

- **Wann:** Tag 2 am Vormittag, nach der Folie zum Fragenset im Block zu Eval
- **Für alle:** 1. Ränge der 20 Testfragen ablesen (Einstieg), 2. `hit_rate` ergänzen, 3. `mrr`
  ergänzen, beide mit Selbstkontrolle an vier Beispielen; dann mit dem Java-Lauf vergleichen und
  ohne Präfixe messen
- **Bonus:** 4. eine Testfrage schreiben, die die Suche verfehlt, 5. Knobelaufgabe: für
  Schwellwerte von 0,17 bis 0,24 zählen, wie viele Fragen abgewiesen oder durchgelassen würden

15 min, zu zweit. Das Notebook läuft für sich, ohne `07-aehnlichkeitssuche`, weil Colab über
Nacht die Laufzeit verliert. Wo Code zu ergänzen ist, prüft eine Zelle das Ergebnis (✓ oder ✗ mit
Sollwert). Danach folgen gestufte Tipps und die Lösung, zugeklappt und mit eigenen Namen
(`loesung_hit_rate`, `loesung_mrr`, `fehler_loesung`), damit sie beim *Alle ausführen* nichts
überschreibt.

## Starten

```bash
uv sync
```

```bash
uv run jupyter lab suche_messen.ipynb --LabApp.user_settings_dir=../einstellungen-jupyterlab
```

Danach *Kernel → Restart Kernel and Run All Cells*. Beim ersten Start lädt `transformers` das
Modell `intfloat/multilingual-e5-small` von Hugging Face (Revision `614241f…`, 471 MB Gewichte
plus 17 MB Tokenizer) in den Cache unter `~/.cache/huggingface/`; danach braucht es kein Netz.

## Was im Ordner liegt

| Datei | Inhalt |
|---|---|
| `suche_messen.ipynb` | Übung am zweiten Tag, Ausgaben aus einem echten Lauf (die Aufgabenzellen zu Schritt 4 und zur Knobelaufgabe zeigen 0, weil die Funktionen dort noch leer sind) |
| `helfer.py` | Modell laden, Text einbetten (Mean Pooling, Normierung), Daten laden, Treffer drucken |
| `index/mit_praefix.npy` | Vektoren der 643 Chunks mit `passage: `, 643 × 384, float16, 494 KB |
| `index/ohne_praefix.npy` | dieselben Chunks ohne Präfix, für Schritt 6 |
| `daten/chunks.json` | die 643 Chunks: Dokument-Id, Titel, Abschnitt, Thema, Text |
| `daten/questions.json` | 20 Testfragen mit Fundstellen und 3 ohne, Stand 2026-10-05 |
| `daten/manifest.json` | die 48 Dokumente mit Quelle (Wikipedia-URL), Revision und Lizenz |
| `daten/LICENSE-CC-BY-SA-4.0.txt`, `daten/HERKUNFT-ASTROPLANNER.md` | Lizenz und Herkunft der Texte |

Die Dateien unter `index/` berechnet `index_bauen.py` in `07-aehnlichkeitssuche` neu.

## Gemessen

MacBook Pro mit M3 Pro, `OMP_NUM_THREADS=2` wie die zwei vCPU in Colab, Modell schon im Cache.
In Colab gemessen ist nur das ganze Notebook (siehe unten); die Schätzung pro Schritt nimmt den
Faktor 6 aus dem Vergleich bei Qwen2.5-0.5B (26 gegen 4,3 Token/s bei gleich vielen Threads) und
für den Download 15 bis 50 MB/s.

| Schritt | lokal | Colab-CPU, geschätzt |
|---|---|---|
| erste Zelle: Import, Modell laden, Index laden | 7 bis 11 s | 15 bis 30 s, beim ersten Mal plus Download 10 bis 30 s |
| eine Suche (Embedding und Schleife über 643 Chunks) | rund 10 ms, die erste 74 ms | unter 0,5 s |
| Ränge der 20 Testfragen | 52 ms | unter 1 s |
| Knobelaufgabe: 23 Fragen auf einmal einbetten und suchen | 51 ms | unter 0,5 s |
| alle übrigen Zellen zusammen | unter 1 s | wenige Sekunden |

## Abgleich mit dem Java-Lauf vom 2026-10-31

Gleich sind Modell, Chunk-Text (erste Zeile „Titel – Abschnitt“, dann der Text), Präfixe, Mean
Pooling über alle Token, Normierung auf Länge 1 und das Abschneiden nach 512 Token. Verschieden
ist die Fassung des Modells: Java lädt `Xenova/multilingual-e5-small`, `onnx/model_quantized.onnx`
(118 MB), hier läuft das Original in float32.

| | Java | Python |
|---|---|---|
| Hit Rate@5, MRR@5 | 0.95, 0.90 | 0.95, 0.90 |
| nicht unter den ersten fünf | D-08 | D-08 |
| Rang 2 statt 1 | D-11, D-17 | D-11, D-12 |
| bester Abstand mit Fundstelle, ohne | 0.118 bis 0.205, 0.203 bis 0.229 | 0.127 bis 0.208, 0.206 bis 0.230 |
| ohne Präfixe: Hit Rate@5, MRR@5 | 0.95, 0.89 (D-11 auf Rang 3) | 0.95, 0.925 (D-12 auf Rang 1) |

Die Distanzen liegen in Python um 0,001 bis 0,009 höher. Die Kennzahlen mit Präfixen sind gleich,
ohne Präfixe nicht: Dort hängt der Unterschied an je einer Frage.

Gegenprobe: Mit dem quantisierten ONNX-Modell des Java-Programms in
Python (onnxruntime 1.20.0, Tokenizer aus `tokenizer.json`, nach 512 Token abgeschnitten) stimmen
alle 643 Chunk-Vektoren mit dem Index des Java-Programms überein (Kosinus 1,0000), und
alle Java-Werte der Tabelle kommen exakt heraus, auch 0.89 ohne Präfixe. Die Abweichung oben kommt
also nur von der Quantisierung. Das Prüfskript ist nicht im Ordner, weil es das ONNX-Modell und den
Java-Index braucht.

Zwölf Chunks sind länger als 512 Token, mit Präfix bis 1'276 Token, meist Abschnitte mit
TeX-Formeln (Air mass, Astronomical seeing, Focal length, F-number). Java und Python schneiden sie
gleich nach 512 Token ab; der Rest des Chunks fliesst nicht in den Vektor ein. In Java schneidet der
Tokenizer von DJL ab (Voreinstellung `LONGEST_FIRST`, 512 Token); die Aufteilung langer Texte in
LangChain4j greift deshalb nie.

## Befunde aus der Knobelaufgabe

Schwellwert über das Fragenset, Distanzen aus dem Python-Lauf vom 2026-11-06, abgewiesen mit
Fundstelle / durchgelassen ohne: 0,17: 11/0, 0,18: 7/0, 0,19: 5/0, 0,20: 2/0, 0,21: 0/1, 0,22:
0/1, 0,23: 0/2, 0,24: 0/3. Am wenigsten Fehler bei 0,21 und 0,22, dann kommt das Alter des
Universums durch. Mit drei Fragen ohne Fundstelle hängt das Minimum an einer Frage. Am knappsten
liegt die Frage nach der Temperatur des Erdkerns (N-03) mit 0.2303 über der Stufe 0,23; zeigt
Colab dort eine andere Zahl, ist das der Grund. Alle anderen Fragen liegen mindestens 0,001 neben
einer Stufe.

## Herkunft und Lizenzen

- **Texte und Fragen**: Kopie aus dem Java-Programm, dort aus AstroPlanner, Stand `ea7d554`.
  `daten/chunks.json` ist der Index des Java-Programms ohne Vektoren (Chunker wie AstroPlanner:
  Abschnitte, höchstens 250 Wörter, 40 Wörter Überlappung). Die Texte stammen aus 42 Artikeln der
  englischen Wikipedia und sechs eigenen Kurzdokumenten von AstroPlanner, Lizenz CC BY-SA 4.0
  (`daten/LICENSE-CC-BY-SA-4.0.txt`). Autoren und Bearbeitung beschreibt
  `daten/HERKUNFT-ASTROPLANNER.md`, das unveränderte README der Wissensbasis von AstroPlanner;
  die Quelle jedes Artikels steht in `daten/manifest.json`. Die Vektoren unter `index/` sind aus
  diesen Texten berechnet und stehen unter derselben Lizenz.
- **Modell**: `intfloat/multilingual-e5-small`, MIT-Lizenz, wird nicht mitgeliefert.

## Bekannte Grenzen

- In Colab (frische Laufzeit, Gratis-CPU, „Alle ausführen“, 2026-11-04) lief das Notebook ohne
  Fehler, mit denselben Werten wie lokal (Hit Rate@5 0,95, MRR@5 0,90), samt Verbinden und
  Modell-Download in 49 s. Die Zeiten pro Schritt in der Tabelle oben sind geschätzt. Die Fassung
  mit nummerierten Aufgaben, Selbstkontrollen und Knobelaufgabe (2026-11-06) lief bisher nur
  lokal.
- Die Ergebnisse weichen leicht vom Java-Lauf ab (Tabelle oben). Das Notebook sagt das an der
  Stelle, wo es auffällt.
- `daten/HERKUNFT-ASTROPLANNER.md` verweist auf Dateien und Abschnitte von AstroPlanner, die im
  öffentlichen Repo nicht liegen. Es ist als Herkunftsnachweis unverändert übernommen.
- 20 Fragen sind ein Spike, keine Statistik. Unterschiede von einer Frage (0,025 in der MRR) sind
  kein Befund.
