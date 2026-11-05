# Template und Temperatur

Übungs-Notebook für den KI-Workshop, gebaut für Google Colab. Es läuft mit Qwen2.5 und
`transformers`, ohne API-Key und ohne Ollama.

- **Wann im Workshop:** Tag 1 nach dem Mittag, im Block zur Nutzung: nach den Folien zu den Rollen
  im Chat-Template und zur Temperatur
- **Zeitbox:** 10 min

`apply_chat_template` zeigt den Text mit den Rollen-Markierungen, den das Modell wirklich bekommt.
Dann die Verteilung für das nächste Token nach „Nenne eine Programmiersprache. Nur den Namen.“ bei
T = 0,2, 1 und 2 (Top-5 und ihre Summe) und je zehn Züge. Zusatz: ein eigener Systemprompt im
Template.

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
| 1. Tokenizer und Template | 4 s | einige Sekunden (nur Tokenizer-Dateien, rund 11 MB) |
| 2. Modell laden | 6 s | 35 s mit Download |
| 3. Vorwärtslauf und Balken | 2,4 s | rund 3 s, gemessen 1,9 s für den Vorwärtslauf |
| 4. Zehnmal ziehen, Lösung | unter 0,1 s | unter 1 s |
| Zusatz, Lösung (je ein, zwei Vorwärtsläufe) | 0,7 s | 2 bis 4 s |

## Was das Modell tut

Auf der CPU in float32 sind die Werte im Machbarkeitstest (Colab) und lokal gleich: Python 0,999
bei T = 0,2; 0,689 bei T = 1 (Java 0,158, Top-5 zusammen 0,895); 0,054 bei T = 2 (Top-5 zusammen
0,104). Systemprompts in der Lösung des Zusatzes: „Du bist ein Java-Entwickler.“ bringt Java bei
T = 1 auf 0,435, „Du programmierst nur in Kotlin.“ lässt Java vorn (0,322) vor „K“ (0,203), dem
ersten von zwei Token für „Kotlin“, „Antworte immer mit einer JVM-Sprache.“ bringt Java auf 0,739.

## Herkunft und Lizenzen

Qwen2.5-0.5B-Instruct von Alibaba Cloud (Qwen Team), Apache 2.0, geladen von Hugging Face
(`Qwen/Qwen2.5-0.5B-Instruct`). Das Notebook enthält keine Daten, nur Prompts.

## Bekannte Grenzen

- `transformers` muss mindestens 4.56 sein (`dtype=` beim Laden). Der Machbarkeitstest lief in Colab
  mit `dtype=`, die Version dort ist also neu genug.
- Bei T = 2 zieht das Notebook einzelne Token aus dem ganzen Vokabular, auch chinesische Zeichen
  und Wortteile. Die Züge in den gespeicherten Ausgaben sind gelesen; was bei den Teilnehmern
  kommt, ist Zufall.
