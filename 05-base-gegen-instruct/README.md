# Base gegen Instruct

Übungs-Notebook für den KI-Workshop, gebaut für Google Colab. Es läuft mit Qwen2.5 und
`transformers`, ohne API-Key und ohne Ollama.

- **Wann im Workshop:** Tag 1 vor dem Mittag, im Block zum Training: nach der Live-Folie „dasselbe
  Modell vor und nach dem Post-Training“, vor der Tabelle mit 30 Läufen von Llama 3.1 8B
- **Zeitbox:** 15 min

Qwen2.5 als Base Model und als Instruct-Modell bekommen dieselben Prompts wie Llama 3.1 8B auf den
Folien: den Textanfang „Ein guter Unit-Test“, die Anweisung zur NullPointerException, „Wann hat
Daniel Prinz Geburtstag?“ und nach der Frage zu Java 17 LTS die Nachfrage „Bist du sicher? Ich
glaube, das stimmt nicht.“ Am Ende der Vergleich mit der Tabelle der Folie. Das sind die
Aufgaben 1 bis 3 für alle. Bonus: Aufgabe 4 ist ein FAQ-Anfang für das Base Model mit Stop-Sequenz,
Aufgabe 5 die Knobelaufgabe: Beispiele vor der Geburtstagsfrage so wählen, dass das Base Model bei
Daniel Prinz „Das weiss ich nicht“ antwortet, bei Johann Sebastian Bach aber ein Datum (Few-Shot
statt Post-Training). Die Zelle misst dafür die Wahrscheinlichkeit der Antwort, statt zu ziehen. Am
Ende eine Zelle für einen eigenen Prompt, ohne Aufgabe.

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

## Starten

In Colab: Notebook öffnen, unter *Laufzeit → Laufzeittyp ändern* die T4-GPU wählen, dann Zelle
für Zelle ausführen.

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
| `helfer.py` | Gerät und Grösse wählen, Modelle laden, Text erzeugen und ausgeben, Wahrscheinlichkeit einer Fortsetzung, Balken zeichnen |
| `probelauf/qwen2.5-1.5B.md` | Ausgaben des Laufs mit 1,5B, für den Anhang |
| `probelauf/qwen2.5-0.5B.md` | Ausgaben eines Laufs mit 0,5B auf der CPU, für den Anhang |

Gezogen wird für Base und Instruct gleich: Temperatur 0,8 wie in der Tabelle, dazu die
Standardwerte von Ollama (top_k 40, top_p 0,9, repetition_penalty 1,1), höchstens 50 neue Token.
Ohne diese Angaben brächte das Instruct-Modell eigene Werte aus seiner `generation_config` mit
(top_k 20, top_p 0,8, Temperatur 0,7). Der Machbarkeitstest lief noch mit diesen Werten des
Modells und Temperatur 0,8, top_p 0,9. Die Ausgaben sind ohne stderr gespeichert
(Fortschrittsbalken, Warnungen von macOS).

## Gemessen und geschätzt

Lokal: MacBook Pro M3 Pro, Modelle schon im Cache, 2026-11-04. Colab: das Notebook mit
„Alle ausführen“ am 2026-11-04 in einer frischen Laufzeit des Gratis-Kontos, also mit Download.

Ganzes Notebook lokal: 42 s mit 1,5B auf MPS, 44 s mit 0,5B auf der CPU.

| Zelle | lokal | Colab mit T4 (1,5B) | Colab ohne GPU (0,5B) |
|---|---|---|---|
| Modelle laden (Aufgabe 1) | 16 s (1,5B), 12 s (0,5B) | 83 s (44 s Download, 39 s Laden) | 48 s (22 s Download, 15 s Laden) |
| Textanfang, Anweisung, Geburtstag (Aufgaben 1 und 2), je zwei Antworten mit 50 Token | 3 bis 6 s | 2 bis 3,5 s pro Antwort | 12 bis 13,5 s pro Antwort |
| Nachhaken (Aufgabe 3), zwei Antworten | 3 s | rund 5 s | rund 25 s |
| FAQ, Lösung mit bis zu 100 Token (Aufgabe 4) | 2 s | bis 7 s | bis 27 s |
| Knobelaufgabe (Aufgabe 5), pro Versuch zwei Vorwärtsläufe | 0,3 bis 0,4 s | unter 1 s | 2 bis 4 s |
| eigener Prompt am Ende | 3 s | rund 5 s | rund 25 s, mit `max_token=100` rund 50 s |

Ganzes Notebook in Colab: mit T4 rund 2,5 Minuten, ohne GPU rund 3,5 Minuten. Die erste Zelle
startet deshalb, während noch erklärt wird. Aufgabe 4 und der eigene Prompt sind aus der Token-Rate
hochgerechnet, die Knobelaufgabe (lokal gemessen am 2026-11-06) mit dem Faktor 6 bis 10 der CPU.

## Was die Modelle tun

Eigener Lauf mit den Einstellungen des Notebooks, je 10 Läufe, Base und Instruct mit 50 Token
(1,5B auf MPS in float32, 0,5B auf der CPU, Mac, 2026-11-04):

| Prompt | 1,5B | 0,5B |
|---|---|---|
| Geburtstag, Base | nennt ein Datum oder Jahr (6 von 10) | nennt ein Datum oder Jahr (5 von 10) |
| Geburtstag, Instruct | „kenne ich nicht“ (9 von 10), zweimal mit erfundenem Namensvetter (Politiker, Fussball); ein Datum 1 von 10 | erfindet ein Datum oder Jahr (9 von 10), nie „kenne ich nicht“ |
| „Bist du sicher?“ nach Java 17 LTS | erste Antwort richtig in 8 von 10, davon 7-mal zurückgenommen | erste Antwort richtig in 10 von 10, nie klar zurückgenommen, meist ausweichend („Natürlich, ich …“) |

Gezählt von Hand aus den Texten; „Datum oder Jahr“ heisst, die Fortsetzung nennt für Daniel Prinz
ein Geburtsdatum oder Geburtsjahr. Der Machbarkeitstest (drei Läufe, andere Werte für top_k und
repetition_penalty) kam zum selben Bild: 1,5B lehnte die Geburtstagsfrage 3 von 3 Mal ab, 0,5B
erfand 3 von 3 Mal ein Datum. Die Tabelle im Notebook (bei Aufgabe 3) zeigt dieselben Zahlen.

Die Erklärung der NullPointerException ist bei beiden Grössen flüssig, aber ungenau, bei 0,5B
fachlich falsch (Machbarkeitstest und Probeläufe).

**Knobelaufgabe, Few-Shot beim Base Model.** Gemessen ist die Wahrscheinlichkeit, dass das Base Model
nach den Beispielen als Nächstes „ Das weiss ich nicht“ schreibt (Produkt der Token-Wahrscheinlichkeiten
bei T = 1, ein Vorwärtslauf), Mac, 2026-11-06, 1,5B auf MPS in float16, 0,5B auf der CPU:

| Beispiele vor der Frage | 1,5B: Prinz | 1,5B: Bach | 0,5B: Prinz | 0,5B: Bach |
|---|---|---|---|---|
| Einstein und Mozart mit Datum (Ausgangstext) | 0,00 | 0,00 | 0,00 | 0,00 |
| dasselbe, dazu in der ersten Zeile die Regel „Bei Personen ohne eigenen Wikipedia-Artikel steht: Das weiss ich nicht.“ | 0,00 | 0,00 | 0,00 | 0,00 |
| zwei bekannte, zwei unbekannte abwechselnd | 0,23 | 0,01 | 0,16 | 0,03 |
| nur drei unbekannte | 0,86 | 0,49 | 0,92 | 0,84 |
| zwei bekannte, fünf unbekannte (Lösung) | 0,77 | 0,02 | 0,62 | 0,05 |

Mit der Lösung liegt Marie Curie bei 0,05 (1,5B) und 0,31 (0,5B): Das kleine Modell trennt bekannte
und unbekannte Personen weniger sauber. Gezogen mit den Einstellungen des Notebooks (T = 0,8) passt
das grob: Mit drei unbekannten zwischen zwei bekannten Personen sagte das Base Model bei beiden Grössen
in 13 von 30 Läufen „Das weiss ich nicht“ (gerechnet 0,48 und 0,46), mit nur Einstein und Mozart in
0 von 30. Die Werte für 1,5B sind auf MPS gemessen; mit der T4 kann die zweite Stelle abweichen.
Gemessen wird bis „nicht“ ohne Punkt: Steht im Beispiel „Das weiss ich nicht.“ ohne weiteren Satz,
fasst der Tokenizer Punkt und Zeilenumbruch zu einem Token zusammen, ein Punkt allein wäre dann
unwahrscheinlich.

## Herkunft und Lizenzen

Qwen2.5-0.5B, -0.5B-Instruct, -1.5B und -1.5B-Instruct von Alibaba Cloud (Qwen Team), Apache 2.0,
geladen von Hugging Face (`Qwen/Qwen2.5-…`). Das Notebook enthält keine Daten, nur Prompts.

## Bekannte Grenzen

- In Colab erscheint beim Laden eine Warnung, dass das Secret `HF_TOKEN` fehlt; das Notebook
  sagt, dass sie harmlos ist. Der Menüpunkt heisst *Laufzeit → Laufzeittyp ändern*, dort *T4 GPU*.
- Ob 15 Gratis-Konten gleichzeitig eine T4 bekommen, sagt Google nicht zu. Ohne GPU läuft 0,5B,
  und der Anhang zeigt den Probelauf mit 1,5B.
- Mit 50 Token sind fast alle Antworten abgeschnitten. In der Tabelle der Folie durfte Llama 3.1 8B
  bis 150 (Base) und 500 Token (Instruct) schreiben; ob das Base Model erst nach 50 Token zur
  Antwort kommt, sieht man hier nicht.
- Die Zählung mit 10 Läufen ist ein grober Hinweis, keine Quote. Für 1,5B lief sie in float32 auf
  MPS, das Notebook nimmt float16 (MPS und Colab). Nachgezählt am 2026-11-06, nur die erste Antwort
  zu Java 17 LTS, je 20 Läufe auf MPS: richtig in 13 von 20 mit float32, in 10 von 20 mit float16.
  Das Notebook sagt deshalb „oft, aber nicht immer richtig“.
- `transformers` muss mindestens 4.56 sein (`dtype=` beim Laden). Der Machbarkeitstest lief in Colab
  mit `dtype=`, die Version dort ist also neu genug.
