"""Hilfsfunktionen für die Notebooks zur Ähnlichkeitssuche: Daten laden, Modell laden, Treffer zeigen.

Die Notebooks sollen die Suche und die Messung zeigen, nicht das Laden von Dateien.
Das Modell und das Pooling sind dieselben wie im Java-Beispiel und in AstroPlanner:
multilingual-e5-small, Mittelwert über alle Token-Vektoren, danach auf Länge 1 normiert.
"""

import json
import logging as _logging
from pathlib import Path

# Nur auf macOS: torch meldet beim Import, dass es Ausgaben nicht umleiten kann. Für die Suche ohne Belang.
_logging.getLogger("torch.distributed.elastic.multiprocessing.redirects").setLevel(_logging.ERROR)

import numpy as np
import torch
from transformers import AutoModel, AutoTokenizer
from transformers.utils import logging

logging.set_verbosity_error()
logging.disable_progress_bar()

ORDNER = Path(__file__).resolve().parent
MODELL = "intfloat/multilingual-e5-small"
# Fester Stand des Modells auf Hugging Face, damit der vorberechnete Index dazu passt.
REVISION = "614241f622f53c4eeff9890bdc4f31cfecc418b3"
TEXTANFANG = 70

_tokenizer = None
_modell = None


def lade_modell():
    """Lädt Tokenizer und Modell (rund 490 MB beim ersten Mal, danach aus dem Cache)."""
    global _tokenizer, _modell
    if _modell is None:
        _tokenizer = AutoTokenizer.from_pretrained(MODELL, revision=REVISION)
        _modell = AutoModel.from_pretrained(MODELL, revision=REVISION).eval()
    return _modell


def einbetten(texte):
    """Macht aus einem Text einen Vektor mit 384 Zahlen, aus einer Liste von Texten eine Matrix.

    Das Präfix ("query: " oder "passage: ") gehört schon in den Text.
    """
    lade_modell()
    einzeln = isinstance(texte, str)
    if einzeln:
        texte = [texte]
    eingabe = _tokenizer(texte, padding=True, truncation=True, max_length=512, return_tensors="pt")
    with torch.no_grad():
        token_vektoren = _modell(**eingabe).last_hidden_state  # ein Vektor pro Token
    # Mean Pooling: Mittelwert über alle echten Token (ohne Auffüllung), wie PoolingMode.MEAN in Java.
    maske = eingabe["attention_mask"].unsqueeze(-1).float()
    mittel = (token_vektoren * maske).sum(1) / maske.sum(1)
    # Auf Länge 1 normieren: Dann ist das Skalarprodukt zweier Vektoren schon der Kosinus.
    mittel = torch.nn.functional.normalize(mittel, dim=-1)
    vektoren = mittel.numpy()
    return vektoren[0] if einzeln else vektoren


def chunk_text(chunk):
    """Der Text, den das Modell für einen Chunk bekommt: erste Zeile Titel und Abschnitt, dann der Text."""
    return f"{chunk['dokument']} – {chunk['abschnitt']}\n{chunk['text']}"


def lade_chunks():
    """Die 643 Chunks aus AstroPlanners Wissensbasis, ohne Vektoren."""
    return json.loads((ORDNER / "daten" / "chunks.json").read_text(encoding="utf-8"))


def lade_index(praefix=True):
    """Die vorberechneten Vektoren der Chunks, eine Zeile pro Chunk, in derselben Reihenfolge."""
    name = "mit_praefix.npy" if praefix else "ohne_praefix.npy"
    return np.load(ORDNER / "index" / name).astype(np.float32)


def lade_fragen():
    """Die Testfragen aus AstroPlanner, jede Fundstelle als Paar (Dokument-Id, Abschnitt)."""
    daten = json.loads((ORDNER / "daten" / "questions.json").read_text(encoding="utf-8"))
    return [
        {
            "id": frage["id"],
            "frage": frage["question"],
            "fundstellen": {(stelle["documentId"], stelle["section"]) for stelle in frage["relevant"]},
        }
        for frage in daten["questions"]
    ]


def zeige_dokumente(chunks):
    """Druckt die Dokumente pro Thema, mit der Id, die in den Fundstellen steht."""
    themen = {}
    for chunk in chunks:
        themen.setdefault(chunk["thema"], {})[chunk["id"]] = chunk["dokument"]
    for thema, dokumente in themen.items():
        print(f"{thema}: " + ", ".join(sorted(dokumente)))


def zeige_abschnitte(chunks, dokument_id):
    """Druckt die Abschnitte eines Dokuments mit dem Textanfang ihres ersten Chunks."""
    gesehen = set()
    for chunk in chunks:
        if chunk["id"] == dokument_id and chunk["abschnitt"] not in gesehen:
            gesehen.add(chunk["abschnitt"])
            print(f"{chunk['abschnitt']}\n          {_anfang(chunk['text'])}")


def _anfang(text):
    return text if len(text) <= TEXTANFANG else text[:TEXTANFANG].strip() + " …"


def zeige(treffer, fundstellen=None):
    """Druckt die Treffer wie das Java-Programm: Rang, Distanz, Dokument – Abschnitt, Textanfang.

    Mit `fundstellen` steht vor jedem Treffer, der eine Fundstelle ist, ein ✓.
    """
    for rang, (distanz, chunk) in enumerate(treffer, start=1):
        marke = ""
        if fundstellen is not None:
            marke = "✓ " if (chunk["id"], chunk["abschnitt"]) in fundstellen else "  "
        print(f"{marke}{rang}  {distanz:.3f}  {chunk['dokument']} – {chunk['abschnitt']}")
        print(f"{' ' * len(marke)}          {_anfang(chunk['text'])}")
