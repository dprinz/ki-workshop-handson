# Token sind keine Wörter

Übungs-Notebook für den KI-Workshop: Die Teilnehmer zerlegen Text selbst mit denselben zwei
Tokenizern wie auf der Folie „Token sind keine Wörter“, Qwen2.5 und GPT-2. Geladen werden nur die
Tokenizer-Dateien, kein Modell. Zu zweit, 10 Minuten, direkt nach dieser Folie in der LLM-Mechanik
am ersten Vormittag.

- **Pflicht:** Tokenizer laden, die Beispiele der Folie wiedererkennen, eine eigene Java-Zeile,
  derselbe Satz auf Deutsch und Englisch, eine lange Zahl.
- **Zusatz:** Warum zählt ein Modell die Buchstaben in einem Wort schlecht? Vorgriff auf die
  Folie zu den Grenzen eines LLM im Block zur Nutzung, dort steht es in der Reserve: Das Modell
  sieht Token-IDs, Modelle mit Zwischenschritten schaffen es oft, ein Tool sicher.

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
| `tokenizer.ipynb` | das Notebook mit sechs Schritten, Ausgaben aus einem echten Lauf vom 2026-11-04 |
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

## Gemessen

MacBook Pro mit M3 Pro, Heimnetz, 2026-11-04. Nur die erste Code-Zelle braucht Zeit, alle
anderen laufen in unter 0,1 Sekunden.

| Zelle | lokal, leerer Cache | lokal, Cache warm | Colab-CPU, geschätzt |
|---|---|---|---|
| 1 · Tokenizer laden (Import, Download 14 MB, Aufbau) | 19 s | 9 s | 15 bis 30 s |
| alle übrigen | unter 0,1 s | unter 0,1 s | unter 1 s |

Die Schätzung für Colab ist nicht gemessen. Sie nimmt an, dass der Import von `transformers` auf
zwei vCPU einige Sekunden länger dauert und der Download aus dem Rechenzentrum mindestens so
schnell ist wie lokal. Ohne Netz, mit Cache, lädt die Zelle beide Tokenizer in 0,2 s
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
  der Regex des Pre-Tokenizers in `tokenizer.json` (`\p{N}`).
