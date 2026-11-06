# Ähnlichkeitssuche

Jupyter-Notebook für den KI-Workshop, Python-Fassung des Java-Programms aus der Live-Demo:
dasselbe Embedding-Modell `multilingual-e5-small`, dieselben 643 Chunks aus AstroPlanners
Wissensbasis, die Suche als Schleife über alle Chunks. Die Vektoren der Chunks sind vorberechnet
und liegen im Ordner. Im Notebook wird nur der Suchtext eingebettet.

- **Wann:** Tag 1 am Nachmittag, direkt nach der Live-Demo der Java-Suche im Block zu RAG
- **Für alle:** 1. ein Text wird ein Vektor (Einstieg), 2. zwei Texte vergleichen: Distanz
  vorbereiteter Paare erst vermuten, dann eigene Paare, 3. die Suchen der Live-Demo (Dämmerung,
  Alter des Universums, zweimal OIII-Filter) und eine eigene Suche
- **Bonus:** 4. ohne die Präfixe `query: ` und `passage: ` suchen, 5. Knobelaufgabe: die Suche um
  einen Schwellwert ergänzen; kein fester Wert ordnet vier Fragen richtig ein

15 min, zu zweit. Wo Code zu ergänzen ist, prüft eine Zelle das Ergebnis (✓ oder ✗ mit Sollwert).
Danach folgen gestufte Tipps und die Lösung, zugeklappt und mit eigenen Namen
(`suche_mit_grenze_loesung`), damit sie beim *Alle ausführen* nichts überschreibt. Gemessen wird
diese Suche am zweiten Tag in `08-suche-messen`.

## Starten

```bash
uv sync
```

```bash
uv run jupyter lab aehnlichkeitssuche.ipynb --LabApp.user_settings_dir=../einstellungen-jupyterlab
```

Danach *Kernel → Restart Kernel and Run All Cells*. Beim ersten Start lädt `transformers` das
Modell `intfloat/multilingual-e5-small` von Hugging Face (Revision `614241f…`, 471 MB Gewichte
plus 17 MB Tokenizer) in den Cache unter `~/.cache/huggingface/`; danach braucht es kein Netz.

## Was im Ordner liegt

| Datei | Inhalt |
|---|---|
| `aehnlichkeitssuche.ipynb` | Übung am ersten Tag, Ausgaben aus einem echten Lauf (die Aufgabenzelle der Knobelaufgabe zeigt die Suche ohne Schwellwert) |
| `helfer.py` | Modell laden, Text einbetten (Mean Pooling, Normierung), Daten laden, Treffer drucken |
| `index/mit_praefix.npy` | Vektoren der 643 Chunks mit `passage: `, 643 × 384, float16, 494 KB |
| `index/ohne_praefix.npy` | dieselben Chunks ohne Präfix, für den Bonus |
| `index_bauen.py` | berechnet die beiden Dateien unter `index/` neu, nur lokal |
| `daten/chunks.json` | die 643 Chunks: Dokument-Id, Titel, Abschnitt, Thema, Text |
| `daten/questions.json` | 20 Testfragen mit Fundstellen und 3 ohne, Stand 2026-10-05 |
| `daten/manifest.json` | die 48 Dokumente mit Quelle (Wikipedia-URL), Revision und Lizenz |
| `daten/LICENSE-CC-BY-SA-4.0.txt`, `daten/HERKUNFT-ASTROPLANNER.md` | Lizenz und Herkunft der Texte |

## Gemessen

MacBook Pro mit M3 Pro, `OMP_NUM_THREADS=2` wie die zwei vCPU in Colab, Modell schon im Cache.
In Colab gemessen ist nur das ganze Notebook (siehe unten); die Schätzung pro Schritt nimmt den
Faktor 6 aus dem Vergleich bei Qwen2.5-0.5B (26 gegen 4,3 Token/s bei gleich vielen Threads) und
für den Download 15 bis 50 MB/s.

| Schritt | lokal | Colab-CPU, geschätzt |
|---|---|---|
| erste Zelle: Import, Modell laden, Index laden | 7 bis 11 s | 15 bis 30 s, beim ersten Mal plus Download 10 bis 30 s |
| eine Suche (Embedding und Schleife über 643 Chunks) | rund 10 ms, die erste 74 ms | unter 0,5 s |
| zwei Texte vergleichen: 14 Texte einzeln einbetten | 80 ms | unter 1 s |
| alle übrigen Zellen zusammen | unter 1 s | wenige Sekunden |
| `index_bauen.py`: 1'286 Embeddings, ohne Download | rund 2 min | nicht nötig |

Der Download dauerte beim Bau lokal 7 min, weil parallel ein anderes Modell geladen wurde; das
ist kein Richtwert.

## Abgleich mit dem Java-Lauf vom 2026-10-31

Gleich sind Modell, Chunk-Text (erste Zeile „Titel – Abschnitt“, dann der Text), Präfixe, Mean
Pooling über alle Token, Normierung auf Länge 1 und das Abschneiden nach 512 Token. Verschieden
ist die Fassung des Modells: Java lädt `Xenova/multilingual-e5-small`, `onnx/model_quantized.onnx`
(118 MB), hier läuft das Original in float32.

| | Java | Python |
|---|---|---|
| Dämmerung, bester Treffer | Twilight – Astronomical twilight, 0.165 | dasselbe, 0.173 |
| Alter des Universums, bester Treffer | Galaxy – Super-luminous spiral, 0.203 | Planetary nebula – Introduction, 0.206 (Galaxy auf Rang 3, 0.208) |
| `OIII Filter`, Thema `filters` | Ultra-high contrast filters, 0.156 | dasselbe, 0.159 |
| `narrowband OIII filter oxygen emission`, Thema `filters` | HOO, SHO and LRGB – Narrowband filters, 0.093 | dasselbe, 0.095 |
| ohne Präfixe: Dämmerung | 0.169 | 0.170 |

Die Distanzen liegen in Python um 0,001 bis 0,009 höher.

Gegenprobe: Mit dem quantisierten ONNX-Modell des Java-Programms in
Python (onnxruntime 1.20.0, Tokenizer aus `tokenizer.json`, nach 512 Token abgeschnitten) stimmen
alle 643 Chunk-Vektoren mit dem Index des Java-Programms überein (Kosinus 1,0000), und
alle Java-Werte der Tabelle kommen exakt heraus. Die Abweichung oben kommt also nur von der
Quantisierung. Das Prüfskript ist nicht im Ordner, weil es das ONNX-Modell und den Java-Index
braucht.

Zwölf Chunks sind länger als 512 Token, mit Präfix bis 1'276 Token, meist Abschnitte mit
TeX-Formeln (Air mass, Astronomical seeing, Focal length, F-number). Java und Python schneiden sie
gleich nach 512 Token ab; der Rest des Chunks fliesst nicht in den Vektor ein. In Java schneidet der
Tokenizer von DJL ab (Voreinstellung `LONGEST_FIRST`, 512 Token); die Aufteilung langer Texte in
LangChain4j greift deshalb nie.

## Befunde aus den Aufgaben

Distanzen aus dem Python-Lauf vom 2026-11-06; in Java liegen sie um 0,001 bis 0,009 tiefer (Abgleich oben).

- **Distanz von Textpaaren** (Aufgabe 2, beide Texte mit `query: `): Dämmerung zu Abenddämmerung
  0.039, Sonnenuntergang 0.117, Pizza 0.164, twilight 0.165, NullPointerException 0.202. „Wann
  beginnt die astronomische Dämmerung?“ zu „Wann wird es nachts dunkel genug für Sterne?“ 0.103, zu
  „Wie behebe ich eine NullPointerException?“ 0.261. Teleskop zu Mikroskop 0.079, zu Fernrohr 0.188.
  Bei einzelnen Wörtern ist die Reihenfolge also wenig verlässlich. Alle Werte liegen unter 0,3:
  Laut Modellkarte von `multilingual-e5-small` (FAQ, Frage 3) liegt der Kosinus wegen der tiefen
  Temperatur 0,01 im kontrastiven Training meist zwischen 0,7 und 1, es zählt die Reihenfolge,
  nicht der Wert.
- **Schwellwert an vier Fragen** (Aufgabe 5), bester Treffer: „Wie viel kostet eine Astrokamera?“
  0.172 (Astrophotography – Amateur astrophotography; der Korpus nennt keine Preise), Dämmerung
  0.173, Universum 0.206, „Was ist Seeing?“ 0.230 (Astronomical seeing – Introduction auf Rang 1).
  Kein fester Wert ordnet alle vier richtig ein.

## Index neu bauen

```bash
uv run python index_bauen.py
```

Bettet jeden Chunk zweimal ein, mit `passage: ` und ohne, und speichert float16. Die Rundung
ändert einen Kosinus um höchstens 0.00006. Nötig nur, wenn sich Chunks oder Modell ändern.

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
  Fehler, samt Download in rund einer Minute. Die Zeiten pro Schritt in der Tabelle oben sind
  geschätzt. Die Fassung mit nummerierten Aufgaben, Selbstkontrolle und Knobelaufgabe
  (2026-11-06) lief bisher nur lokal.
- Die Ergebnisse weichen leicht von der Live-Demo ab (Tabelle oben); beim Alter des Universums ist
  der beste Treffer ein anderer. Das Notebook sagt das an der Stelle, wo es auffällt.
- `daten/HERKUNFT-ASTROPLANNER.md` verweist auf Dateien und Abschnitte von AstroPlanner, die im
  öffentlichen Repo nicht liegen. Es ist als Herkunftsnachweis unverändert übernommen.
