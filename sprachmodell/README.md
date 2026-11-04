# Kleines Sprachmodell: Base gegen Instruct, Template und Temperatur

Zwei Übungs-Notebooks für den KI-Workshop, gebaut für Google Colab. Beide laufen mit Qwen2.5 und
`transformers`, ohne API-Key und ohne Ollama. Es sind zwei Notebooks, weil die Übungen an
verschiedenen Stellen des ersten Tages liegen und Colab dazwischen die Laufzeit verliert.

| Notebook | Wann im Workshop | Zeitbox |
|---|---|---|
| `base_und_instruct.ipynb` | Tag 1 vor dem Mittag, im Block zum Training: nach der Live-Folie „dasselbe Modell vor und nach dem Post-Training“, vor der Tabelle mit 30 Läufen von Llama 3.1 8B | 15 min |
| `template_und_temperatur.ipynb` | Tag 1 nach dem Mittag, im Block zur Nutzung: nach den Folien zu den Rollen im Chat-Template und zur Temperatur | 10 min |

**Base gegen Instruct:** Qwen2.5 als Base Model und als Instruct-Modell bekommen dieselben
Prompts wie Llama 3.1 8B auf den Folien: den Textanfang „Ein guter Unit-Test“, die Anweisung zur
NullPointerException, „Wann hat Daniel Prinz Geburtstag?“ und nach der Frage zu Java 17 LTS die
Nachfrage „Bist du sicher? Ich glaube, das stimmt nicht.“ Am Ende der Vergleich mit der Tabelle der
Folie. Zusatz: ein FAQ-Anfang für das Base Model mit Stop-Sequenz, ein eigener Prompt.

**Template und Temperatur:** `apply_chat_template` zeigt den Text mit den Rollen-Markierungen, den
das Modell wirklich bekommt. Dann die Verteilung für das nächste Token nach „Nenne eine
Programmiersprache. Nur den Namen.“ bei T = 0,2, 1 und 2 (Top-5 und ihre Summe) und je zehn Züge.
Zusatz: ein eigener Systemprompt im Template.

## Welches Modell

`base_und_instruct.ipynb` wählt in der ersten Code-Zelle:

| Umgebung | Modelle | Gerät |
|---|---|---|
| Colab mit GPU (T4) | Qwen2.5-1.5B und -1.5B-Instruct, float16 | `cuda` |
| ohne GPU | Qwen2.5-0.5B und -0.5B-Instruct, float32 | `cpu` |
| Mac mit `MODELL_GROESSE=1.5B` | Qwen2.5-1.5B und -1.5B-Instruct, float16 | `mps` |

Mit 0,5 Mrd. Parametern setzt das Base Model fort und das Instruct-Modell antwortet, aber es rät
fast immer (siehe unten). Erst 1,5B zeigt das Bild von Llama 3.1 8B auf der Folie. Deshalb liegen
beide Probeläufe bei: Die gespeicherten Ausgaben im Notebook stammen aus dem Lauf mit 1,5B, der
Anhang am Ende zeigt den Probelauf der jeweils anderen Grösse aus `probelauf/`.

`template_und_temperatur.ipynb` nimmt immer Qwen2.5-0.5B-Instruct auf der CPU. Template und ein
Vorwärtslauf brauchen keine GPU, und auf der CPU sind die Zahlen überall dieselben.

## Starten

In Colab: Notebook öffnen, für Base gegen Instruct unter *Laufzeit → Laufzeittyp ändern* die
T4-GPU wählen, dann Zelle für Zelle ausführen.

Lokal:

```bash
uv sync
```

```bash
uv run jupyter lab base_und_instruct.ipynb --LabApp.user_settings_dir=../einstellungen-jupyterlab
```

Lokal mit 1,5B auf dem Mac:

```bash
MODELL_GROESSE=1.5B uv run jupyter lab base_und_instruct.ipynb --LabApp.user_settings_dir=../einstellungen-jupyterlab
```

Beim ersten Start lädt `transformers` die Modelle von Hugging Face in `~/.cache/huggingface`
(0,5B: rund 1 GB pro Modell, 1,5B: rund 3,1 GB pro Modell).

## Was im Ordner liegt

| Datei | Inhalt |
|---|---|
| `base_und_instruct.ipynb` | Übung Base gegen Instruct, Ausgaben aus dem Lauf mit 1,5B auf dem Mac |
| `template_und_temperatur.ipynb` | Übung Template und Temperatur, Ausgaben aus dem Lauf mit 0,5B auf der CPU |
| `helfer.py` | Gerät und Grösse wählen, Modelle laden, Text erzeugen und ausgeben, Balken zeichnen |
| `probelauf/qwen2.5-1.5B.md` | Ausgaben des Laufs mit 1,5B, für den Anhang |
| `probelauf/qwen2.5-0.5B.md` | Ausgaben eines Laufs mit 0,5B auf der CPU, für den Anhang |

Gezogen wird für Base und Instruct gleich: Temperatur 0,8 wie in der Tabelle, dazu die
Standardwerte von Ollama (top_k 40, top_p 0,9, repetition_penalty 1,1), höchstens 50 neue Token.
Ohne diese Angaben brächte das Instruct-Modell eigene Werte aus seiner `generation_config` mit
(top_k 20, top_p 0,8, Temperatur 0,7). Der Machbarkeitstest lief noch mit diesen Werten des
Modells und Temperatur 0,8, top_p 0,9. Die Ausgaben sind ohne stderr gespeichert
(Fortschrittsbalken, Warnungen von macOS).

## Gemessen und geschätzt

Lokal: MacBook Pro M3 Pro, Modelle schon im Cache, 2026-11-04. Colab: beide Notebooks mit
„Alle ausführen“ am 2026-11-04 in einer frischen Laufzeit des Gratis-Kontos, also mit Download.

**Base gegen Instruct**, ganzes Notebook lokal: 42 s mit 1,5B auf MPS, 44 s mit 0,5B auf der CPU.

| Zelle | lokal | Colab mit T4 (1,5B) | Colab ohne GPU (0,5B) |
|---|---|---|---|
| 1. Modelle laden | 16 s (1,5B), 12 s (0,5B) | 83 s (44 s Download, 39 s Laden) | 48 s (22 s Download, 15 s Laden) |
| 2. bis 4., je zwei Antworten mit 50 Token | 3 bis 6 s | 2 bis 3,5 s pro Antwort | 12 bis 13,5 s pro Antwort |
| 5. Nachhaken, zwei Antworten | 3 s | rund 5 s | rund 25 s |
| Zusatz A, Lösung mit bis zu 100 Token | 2 s | bis 7 s | bis 27 s |
| Zusatz B | 3 s | rund 5 s | rund 25 s, mit `max_token=100` rund 50 s |

Ganzes Notebook in Colab: mit T4 rund 2,5 Minuten, ohne GPU rund 3,5 Minuten. Die erste Zelle
startet deshalb, während noch erklärt wird. Zusatz A und B sind aus der Token-Rate hochgerechnet.

**Template und Temperatur**, ganzes Notebook lokal 16 s, in Colab ohne GPU rund 1,5 Minuten.

| Zelle | lokal | Colab ohne GPU |
|---|---|---|
| 1. Tokenizer und Template | 4 s | einige Sekunden (nur Tokenizer-Dateien, rund 11 MB) |
| 2. Modell laden | 6 s | 35 s mit Download |
| 3. Vorwärtslauf und Balken | 2,4 s | rund 3 s, gemessen 1,9 s für den Vorwärtslauf |
| 4. Zehnmal ziehen, Lösung | unter 0,1 s | unter 1 s |
| Zusatz, Lösung (je ein, zwei Vorwärtsläufe) | 0,7 s | 2 bis 4 s |

## Was die Modelle tun

**Base gegen Instruct.** Eigener Lauf mit den Einstellungen des Notebooks, je 10 Läufe, Base und
Instruct mit 50 Token (1,5B auf MPS in float32, 0,5B auf der CPU, Mac, 2026-11-04):

| Prompt | 1,5B | 0,5B |
|---|---|---|
| Geburtstag, Base | nennt ein Datum oder Jahr (6 von 10) | nennt ein Datum oder Jahr (5 von 10) |
| Geburtstag, Instruct | „kenne ich nicht“ (9 von 10), zweimal mit erfundenem Namensvetter (Politiker, Fussball); ein Datum 1 von 10 | erfindet ein Datum oder Jahr (9 von 10), nie „kenne ich nicht“ |
| „Bist du sicher?“ nach Java 17 LTS | erste Antwort richtig in 8 von 10, davon 7-mal zurückgenommen | erste Antwort richtig in 10 von 10, nie klar zurückgenommen, meist ausweichend („Natürlich, ich …“) |

Gezählt von Hand aus den Texten; „Datum oder Jahr“ heisst, die Fortsetzung nennt für Daniel Prinz
ein Geburtsdatum oder Geburtsjahr. Der Machbarkeitstest (drei Läufe, andere Werte für top_k und
repetition_penalty) kam zum selben Bild: 1,5B lehnte die Geburtstagsfrage 3 von 3 Mal ab, 0,5B
erfand 3 von 3 Mal ein Datum. Die Tabelle im Notebook (Schritt 6) zeigt dieselben Zahlen.

Die Erklärung der NullPointerException ist bei beiden Grössen flüssig, aber ungenau, bei 0,5B
fachlich falsch (Machbarkeitstest und Probeläufe).

**Template und Temperatur.** Auf der CPU in float32 sind die Werte im Machbarkeitstest (Colab) und
lokal gleich: Python 0,999 bei T = 0,2; 0,689 bei T = 1 (Java 0,158, Top-5 zusammen 0,895); 0,054 bei
T = 2 (Top-5 zusammen 0,104). Systemprompts in der Lösung des Zusatzes: „Du bist ein
Java-Entwickler.“ bringt Java bei T = 1 auf 0,435, „Du programmierst nur in Kotlin.“ lässt Java vorn
(0,322) vor „K“ (0,203), dem ersten von zwei Token für „Kotlin“, „Antworte immer mit einer
JVM-Sprache.“ bringt Java auf 0,739.

## Herkunft und Lizenzen

Qwen2.5-0.5B, -0.5B-Instruct, -1.5B und -1.5B-Instruct von Alibaba Cloud (Qwen Team), Apache 2.0,
geladen von Hugging Face (`Qwen/Qwen2.5-…`). Die Notebooks enthalten keine Daten, nur Prompts.

## Bekannte Grenzen

- In Colab erscheint beim Laden eine Warnung, dass das Secret `HF_TOKEN` fehlt; das Notebook
  sagt, dass sie harmlos ist. Der Menüpunkt heisst *Laufzeit → Laufzeittyp ändern*, dort *T4 GPU*.
- Ob 15 Gratis-Konten gleichzeitig eine T4 bekommen, sagt Google nicht zu. Ohne GPU läuft 0,5B,
  und der Anhang zeigt den Probelauf mit 1,5B.
- Mit 50 Token sind fast alle Antworten abgeschnitten. In der Tabelle der Folie durfte Llama 3.1 8B
  bis 150 (Base) und 500 Token (Instruct) schreiben; ob das Base Model erst nach 50 Token zur
  Antwort kommt, sieht man hier nicht.
- Die Zählung mit 10 Läufen ist ein grober Hinweis, keine Quote. Für 1,5B lief sie in float32 auf
  MPS, das Notebook nimmt float16 (MPS und Colab).
- `transformers` muss mindestens 4.56 sein (`dtype=` beim Laden). Der Machbarkeitstest lief in Colab
  mit `dtype=`, die Version dort ist also neu genug.
- Bei T = 2 zieht das Notebook einzelne Token aus dem ganzen Vokabular, auch chinesische Zeichen
  und Wortteile. Die Züge in den gespeicherten Ausgaben sind gelesen; was bei den Teilnehmern
  kommt, ist Zufall.
