# Token sind keine Wörter

Übungs-Notebook für den KI-Workshop: Die Teilnehmer zerlegen Text selbst mit denselben zwei
Tokenizern wie auf der Folie „Token sind keine Wörter“, Qwen2.5 und GPT-2. Geladen werden nur die
Tokenizer-Dateien, kein Modell. Zu zweit, 10 Minuten, direkt nach dieser Folie in der LLM-Mechanik
am ersten Vormittag.

Fünf Aufgaben, jede steht im Notebook an der Stelle, an der man sie macht; sie werden von der
ersten zur letzten etwas schwieriger.

- **Für alle, rund 7 Minuten:** (1) Tokenizer laden und die Beispiele der Folie wiedererkennen,
  (2) eine eigene Java-Zeile, (3) derselbe Satz auf Deutsch und Englisch, mit Schätzung vorher
  und dem Faktor als Ausgabe.
- **Bonus:** (4) eine lange Zahl und „strawberry“: Was sieht das Modell, wenn es rechnen oder
  Buchstaben zählen soll? Vorgriff auf die Folie zu den Grenzen eines LLM im Block zur Nutzung,
  dort steht es in der Reserve: Das Modell sieht Token-IDs, Modelle mit Zwischenschritten
  schaffen es oft, ein Tool sicher. (5) Knobelaufgabe: einen Text ohne Ziffern finden, den GPT-2
  in weniger Token zerlegt als Qwen2.5, mit Selbstkontrolle, zwei Tipps und Lösung (siehe unten).

Die Lösungen stehen zugeklappt direkt nach jeder Aufgabe.

## Starten

```bash
uv sync
```

```bash
uv run jupyter lab tokenizer.ipynb --LabApp.user_settings_dir=../einstellungen-jupyterlab
```

Die Schriftgrössen für den Beamer stehen in `../einstellungen-jupyterlab/`, gemeinsam für alle
Workshop-Labs. Beim ersten Lauf lädt das Notebook die Tokenizer von Hugging Face, danach liegen
sie im Cache. Ein Konto oder `HF_TOKEN` braucht es nicht.

In Colab läuft es ohne Installation: `transformers`, `tokenizers` und `torch` sind dort
vorhanden. `torch` steht in `pyproject.toml` nur, damit `transformers` lokal nicht warnt, und
`ipywidgets` für den Fortschrittsbalken beim Download, wie in Colab.

## Was im Ordner liegt

| Datei | Inhalt |
|---|---|
| `tokenizer.ipynb` | das Notebook mit fünf Aufgaben, Ausgaben aus einem echten Lauf |
| `helfer.py` | `zeige(text, *tokenizer)`: Token abwechselnd hinterlegt, Leerzeichen als ·, Anzahl und IDs, wie die Live-Komponente auf der Folie |

## Tokenizer

| Name im Notebook | Hugging Face | Vokabular | Download |
|---|---|---|---|
| `qwen` | `Qwen/Qwen2.5-1.5B` | 151'665 Token | 11,5 MB (`tokenizer.json` 7,0 MB, `vocab.json` 2,8 MB, `merges.txt` 1,7 MB, zwei Configs) |
| `gpt2` | `openai-community/gpt2` | 50'257 Token | 2,9 MB (`tokenizer.json` 1,4 MB, `vocab.json` 1,0 MB, `merges.txt` 0,5 MB, zwei Configs) |

Die beiden `tokenizer.json` sind byte-gleich mit den Dateien, die die Folie „Token sind keine
Wörter“ live verwendet (MD5 verglichen). Qwen2.5 1.5B ist das Modell, dessen Zahlen
die Folie zum nächsten Token zeigt; 0.5B, 1.5B und 7B haben denselben Tokenizer. Lizenzen: Qwen2.5
1.5B Apache 2.0, GPT-2 MIT.

Die Zahlen der Folie stimmen im Lauf: Qwen2.5 zerlegt den deutschen Satz in 14 Token
(„fehlgeschlagen“ in vier Stücken), den englischen in 9, die Java-Zeile in 12, „Thurgauer
Kantonalbank“ in sechs, „ strawberry“ ist ein Token. GPT-2 braucht für den deutschen Satz 20.

## Knobelaufgabe

Mit Ziffern wäre sie zu leicht: Qwen2.5 nimmt jede Ziffer einzeln, `1000000` sind dort sieben
Token, bei GPT-2 zwei. Deshalb ist ein Text ohne Ziffern gesucht. Die Zelle prüft es selbst,
Zahlzeichen wie ½ zählen als Ziffern (Unicode-Kategorie N, wie `\p{N}` im Pre-Tokenizer).
Häufige Wörter zerlegen beide gleich: „The build is green.“ ist bei beiden fünf Token, auch
` Massachusetts`, ` Zuckerberg` oder ` cryptocurrency` sind bei beiden ein Token. Seltenere
englische Wörter und Namen kennt oft nur GPT-2 als ein Token (Lauf vom 6. November 2026, Token
Qwen2.5 gegen GPT-2, jeweils mit Leerzeichen davor): ` incomprehensible` 3 gegen 1,
` Schwarzenegger` 4 gegen 1, ` chimpanzees` 3 gegen 1, ` unilaterally` 3 gegen 1; der Satz „The
incomprehensible chimpanzees unilaterally lobbied Schwarzenegger.“ 18 gegen 7.

Die Erklärung in der Lösung: Ein grösseres Vokabular enthält nicht einfach das kleinere. GPT-2
ist auf englischen Webseiten trainiert (Radford et al. 2019). Qwen2.5 verwendet den Tokenizer
von Qwen (Qwen Team 2024, „Qwen2.5 Technical Report“), dessen Vokabular von `cl100k` ausgeht und
für Chinesisch und andere Sprachen erweitert wurde (Bai et al. 2023, „Qwen Technical Report“).
Die Lösung zählt das zur Laufzeit nach: Von den Token aus Buchstaben a bis z kennt nur GPT-2
6'140, meist englische Wörter (` linebackers`, ` resettlement`), nur Qwen2.5 28'170, viele davon
Code-Bezeichner und Wörter anderer Sprachen (` serialVersionUID`, ` XmlDocument`, ` qualquer`,
` commentaire`). 30'701 der 151'665 Token von Qwen2.5 enthalten chinesische, japanische oder
koreanische Zeichen, bei GPT-2 183 von 50'257.

## Gemessen

MacBook Pro mit M3 Pro, Heimnetz, 2026-11-04. Nur die erste Code-Zelle braucht Zeit, alle
anderen laufen in unter 0,1 Sekunden, ausser der Lösung der Knobelaufgabe, die beide Vokabulare
Token für Token dekodiert (gemessen am 6. November 2026, Colab geschätzt).

| Zelle | lokal, leerer Cache | lokal, Cache warm | Colab-CPU |
|---|---|---|---|
| 1 · Tokenizer laden (Import, Download 14 MB, Aufbau) | 19 s | 9 s | 22 s, gemessen |
| Lösung der Knobelaufgabe | 0,5 s | 0,5 s | geschätzt 2 bis 5 s |
| alle übrigen | unter 0,1 s | unter 0,1 s | unter 1 s, gemessen |

Colab: frische Laufzeit, „Alle ausführen“, 2026-11-04. Ohne Netz, mit Cache, lädt die Zelle beide Tokenizer in 0,2 s
(`HF_HUB_OFFLINE=1`).

## Bekannte Grenzen

- In Colab erscheint beim Laden eine Warnung, dass das Secret `HF_TOKEN` fehlt. Das Notebook sagt,
  dass man sie ignorieren kann. Ohne Token gelten tiefere Rate-Limits bei Hugging Face; ob ein
  ganzer Raum gleichzeitig aus demselben Netz daran stösst, ist nicht geprüft.
- `zeige` dekodiert jede ID für sich, wie die Komponente auf der Folie. Ein Zeichen, das über
  zwei Token verteilt ist (selten, etwa bei Emojis), erscheint dann in beiden Stücken als �.
- Quellen in den Lösungen: Petrov et al. 2023 („Language Model Tokenizers Introduce Unfairness
  Between Languages“) für den Unterschied Deutsch und Englisch, wie in den Notizen der Folie; Radford et al.
  2019 (GPT-2, WebText ohne nicht englische Seiten); Chowdhery et al. 2022 (PaLM) und Touvron et
  al. 2023 (Llama) für Zahlen in einzelnen Ziffern. Dass Qwen2.5 Ziffern einzeln trennt, steht in
  der Regex des Pre-Tokenizers in `tokenizer.json` (`\p{N}`) und im Qwen Technical Report (Bai et
  al. 2023), der auch das Vokabular beschreibt; dass Qwen2.5 denselben Tokenizer verwendet, im
  Qwen2.5 Technical Report (Qwen Team 2024).
