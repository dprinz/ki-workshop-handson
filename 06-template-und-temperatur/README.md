# Template und Temperatur

Übungs-Notebook für den KI-Workshop, gebaut für Google Colab. Es läuft mit Qwen2.5 und
`transformers`, ohne API-Key und ohne Ollama.

- **Wann im Workshop:** Tag 1 nach dem Mittag, im Block zur Nutzung: nach den Folien zu den Rollen
  im Chat-Template und zur Temperatur
- **Zeitbox:** 10 min

`apply_chat_template` zeigt den Text mit den Rollen-Markierungen, den das Modell wirklich bekommt.
Dann die Verteilung für das nächste Token nach „Nenne eine Programmiersprache. Nur den Namen.“ bei
T = 0,2, 1 und 2 (Top-5 und ihre Summe) und je zehn Züge. Das sind die Aufgaben 1 bis 3 für alle.
Bonus: Aufgabe 4 ist ein eigener Systemprompt, mit dem Java vor Python liegt, Aufgabe 5 die
Knobelaufgabe: ein Systemprompt, mit dem das Modell „Kotlin“ antwortet. Die naheliegenden („Du
programmierst nur in Kotlin.“) lassen Java vorn.

## Welches Modell

`template_und_temperatur.ipynb` nimmt immer Qwen2.5-0.5B-Instruct auf der CPU. Template und ein
Vorwärtslauf brauchen keine GPU, und auf der CPU sind die Zahlen überall dieselben.

## Starten

In Colab: Notebook öffnen, dann Zelle für Zelle ausführen.

Lokal:

```bash
uv sync
```

```bash
uv run jupyter lab template_und_temperatur.ipynb --LabApp.user_settings_dir=../einstellungen-jupyterlab
```

Beim ersten Start lädt `transformers` das Modell von Hugging Face in `~/.cache/huggingface`
(0,5B: rund 1 GB).

## Was im Ordner liegt

| Datei | Inhalt |
|---|---|
| `template_und_temperatur.ipynb` | Übung Template und Temperatur, Ausgaben aus dem Lauf mit 0,5B auf der CPU |
| `helfer.py` | dieselbe Datei wie in `05-base-gegen-instruct`: Gerät und Grösse wählen, Modelle laden, Text erzeugen und ausgeben, Balken zeichnen; dieses Notebook braucht daraus nur `zeige_verteilungen` |

## Gemessen und geschätzt

Lokal: MacBook Pro M3 Pro, Modell schon im Cache, 2026-11-04. Colab: das Notebook mit
„Alle ausführen“ am 2026-11-04 in einer frischen Laufzeit des Gratis-Kontos, also mit Download.

Ganzes Notebook lokal 16 s, in Colab ohne GPU rund 1,5 Minuten.

| Zelle | lokal | Colab ohne GPU |
|---|---|---|
| Tokenizer und Template (Aufgabe 1) | 4 s | einige Sekunden (nur Tokenizer-Dateien, rund 11 MB) |
| Modell laden (Aufgabe 2) | 6 s | 35 s mit Download |
| Vorwärtslauf und Balken (Aufgabe 2) | 2,4 s | rund 3 s, gemessen 1,9 s für den Vorwärtslauf |
| Zehnmal ziehen, Lösung (Aufgabe 3) | unter 0,1 s | unter 1 s |
| eigener Systemprompt, Lösung (Aufgabe 4, je ein Vorwärtslauf) | 0,1 bis 0,2 s | rund 1 s |
| Knobelaufgabe (Aufgabe 5), pro Versuch bis zu fünf Vorwärtsläufe | 0,3 s, Lösung 0,8 s | 1 bis 3 s pro Versuch |

Die Zeilen zu Aufgabe 4 und 5 sind lokal am 2026-11-06 gemessen, die Werte für Colab daraus geschätzt.

## Was das Modell tut

Auf der CPU in float32 sind die Werte im Machbarkeitstest (Colab) und lokal gleich: Python 0,999
bei T = 0,2; 0,689 bei T = 1 (Java 0,158, Top-5 zusammen 0,895); 0,054 bei T = 2 (Top-5 zusammen
0,104). Systemprompts in der Lösung von Aufgabe 4: „Du bist ein Java-Entwickler.“ bringt Java bei
T = 1 auf 0,435 (Python 0,166), „Antworte immer mit einer JVM-Sprache.“ auf 0,739. Mit dem
Ausgangstext der Zelle, „Du bist ein hilfreicher Assistent.“, liegt Python bei 0,800 (Java 0,132).

Knobelaufgabe, erstes Token bei T = 1 („K“ ist das erste von zwei Token für „Kotlin“), lokal
2026-11-06:

| Systemprompt | „K“ | Java | Python | Antwort bei T = 0 |
|---|---|---|---|---|
| Du programmierst nur in Kotlin. | 0,203 | 0,322 | 0,090 | Java |
| Du bist ein Kotlin-Entwickler. | 0,159 | 0,335 | 0,091 | Java |
| Antworte immer mit Kotlin. | 0,168 | 0,415 | 0,075 | Java |
| Antworte nur mit dem Wort Kotlin. | 0,541 | 0,181 | 0,189 | Kotlin |
| Du liebst Kotlin. | 0,569 | 0,145 | 0,010 | Kotlin |
| Kotlin ist die beste Programmiersprache. | 0,713 | 0,172 | 0,046 | Kotlin |
| Nenne nie Java. Deine Antwort ist immer Kotlin. | 0,694 | 0,047 | 0,033 | Kotlin |
| Deine Lieblingssprache ist Kotlin. | 0,756 | 0,042 | 0,013 | Kotlin |

Weitere Versuche ohne Kotlin vorn: „Du bist ein Android-Entwickler.“ (Java 0,770), „You only program
in Kotlin.“ („K“ 0,120, Java 0,391), „Du bist JetBrains-Mitarbeiter.“ (Python 0,574).

## Herkunft und Lizenzen

Qwen2.5-0.5B-Instruct von Alibaba Cloud (Qwen Team), Apache 2.0, geladen von Hugging Face
(`Qwen/Qwen2.5-0.5B-Instruct`). Das Notebook enthält keine Daten, nur Prompts.

## Bekannte Grenzen

- `transformers` muss mindestens 4.56 sein (`dtype=` beim Laden). Der Machbarkeitstest lief in Colab
  mit `dtype=`, die Version dort ist also neu genug.
- Bei T = 2 zieht das Notebook einzelne Token aus dem ganzen Vokabular, auch chinesische Zeichen
  und Wortteile. Die Züge in den gespeicherten Ausgaben sind gelesen; was bei den Teilnehmern
  kommt, ist Zufall.
