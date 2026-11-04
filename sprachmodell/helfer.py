"""Hilfsfunktionen für die Notebooks zum kleinen Sprachmodell.

Gerät und Modellgrösse wählen, Modelle laden, Text erzeugen und lesbar ausgeben,
Verteilungen zeichnen. Die Notebooks sollen die Modelle zeigen, nicht transformers.
"""

import os
import textwrap
import time
from pathlib import Path

import torch
from huggingface_hub import snapshot_download
from transformers import AutoModelForCausalLM, AutoTokenizer

ORDNER = Path(__file__).parent

# Gezogen wird wie in der Ollama-Demo mit Llama 3.1 8B: Temperatur 0,8, dazu die
# Standardwerte von Ollama für top_k, top_p und repeat_penalty. Für beide Modelle gleich,
# damit nur das Post-Training den Unterschied macht. Ohne diese Angaben brächte das
# Instruct-Modell eigene Werte aus seiner generation_config mit.
ZIEHEN = {"do_sample": True, "temperature": 0.8, "top_k": 40, "top_p": 0.9, "repetition_penalty": 1.1}


def zahl(x, stellen=1):
    """Deutsche Schreibweise mit Komma."""
    return f"{x:.{stellen}f}".replace(".", ",")


def waehle_variante():
    """Mit GPU (Colab T4) 1,5 Mrd. Parameter in float16, sonst 0,5 Mrd. auf der CPU.

    MODELL_GROESSE=1.5B erzwingt die grosse Variante ohne CUDA, auf dem Mac dann auf MPS,
    ebenfalls in float16 (in float32 brauchen die zwei Modelle rund 12 GB Speicher).
    """
    if torch.cuda.is_available():
        return "1.5B", "cuda", torch.float16
    groesse = os.environ.get("MODELL_GROESSE", "0.5B")
    if groesse == "1.5B" and torch.backends.mps.is_available():
        return groesse, "mps", torch.float16
    return groesse, "cpu", torch.float32


class Modell:
    def __init__(self, name, geraet="cpu", dtype=torch.float32):
        self.name = name.split("/")[-1]
        self.geraet = geraet
        self.instruct = name.endswith("Instruct")
        self.tokenizer = AutoTokenizer.from_pretrained(name)
        self.modell = AutoModelForCausalLM.from_pretrained(name, dtype=dtype).to(geraet).eval()
        self.parameter = sum(p.numel() for p in self.modell.parameters())

    def _erzeuge(self, text, max_token, stopp=None):
        eingabe = self.tokenizer(text, return_tensors="pt").to(self.geraet)
        extra = {"stop_strings": [stopp], "tokenizer": self.tokenizer} if stopp else {}
        start = time.perf_counter()
        with torch.no_grad():
            ausgabe = self.modell.generate(**eingabe, max_new_tokens=max_token, **ZIEHEN,
                                           pad_token_id=self.tokenizer.eos_token_id, **extra)
        sekunden = time.perf_counter() - start
        neu = ausgabe[0, eingabe["input_ids"].shape[1]:]
        fertig = int(neu[-1]) in (self.tokenizer.eos_token_id, self.tokenizer.convert_tokens_to_ids("<|im_end|>"))
        antwort = self.tokenizer.decode(neu, skip_special_tokens=True)
        if stopp and antwort.endswith(stopp):
            ende = f"hört bei „{stopp.strip()}“ auf"
        elif fertig:
            ende = "hört von selbst auf"
        else:
            ende = f"nach {max_token} Token abgeschnitten"
        kopf = f"{len(neu)} Token in {zahl(sekunden)} s, {ende}"
        return antwort, kopf

    def fortsetzen(self, text, max_token=50, stopp=None):
        """Base Model: Der Text geht so, wie er ist, ans Modell. Es schreibt ihn weiter."""
        antwort, kopf = self._erzeuge(text, max_token, stopp)
        print(f"{self.name} setzt fort ({kopf}):\n")
        _drucke(f"»{text}«{antwort}")
        return antwort

    def chat(self, nachrichten, max_token=50):
        """Instruct-Modell: Die Nachrichten gehen durch das Chat-Template, das Modell antwortet."""
        text = self.tokenizer.apply_chat_template(nachrichten, tokenize=False, add_generation_prompt=True)
        antwort, kopf = self._erzeuge(text, max_token)
        print(f"{self.name} antwortet auf „{_kurz(nachrichten[-1]['content'])}“ ({kopf}):\n")
        _drucke(antwort)
        return antwort


def _kurz(text, laenge=60):
    text = " ".join(text.split())
    return text if len(text) <= laenge else text[: laenge - 1] + "…"


def _drucke(text, breite=100):
    for zeile in text.strip("\n").split("\n"):
        print(textwrap.fill(zeile, breite) if zeile.strip() else "")
    print()


def lade_base_und_instruct():
    """Lädt Base und Instruct derselben Grösse, misst Download und Laden."""
    groesse, geraet, dtype = waehle_variante()
    namen = [f"Qwen/Qwen2.5-{groesse}", f"Qwen/Qwen2.5-{groesse}-Instruct"]
    karte = f" ({torch.cuda.get_device_name(0)})" if geraet == "cuda" else ""
    print(f"Gerät: {geraet}{karte}. Modelle: {namen[0]} und {namen[1]}, {str(dtype).split('.')[-1]}.")

    start = time.perf_counter()
    gigabyte = 0
    for name in namen:
        ordner = Path(snapshot_download(name, allow_patterns=["*.json", "*.safetensors", "*.txt"]))
        gigabyte += sum(f.stat().st_size for f in ordner.glob("*.safetensors")) / 1e9
    download = time.perf_counter() - start

    start = time.perf_counter()
    base, instruct = (Modell(name, geraet, dtype) for name in namen)
    laden = time.perf_counter() - start

    print(f"{zahl(base.parameter / 1e9, 2)} Mrd. Parameter pro Modell, zusammen {zahl(gigabyte)} GB Dateien.")
    print(f"Download {zahl(download, 0)} s (fällt weg, wenn die Dateien schon da sind), Laden {zahl(laden, 0)} s.")
    return base, instruct


def zeige_probelauf(modell):
    """Zeigt den gespeicherten Probelauf der jeweils anderen Grösse."""
    from IPython.display import Markdown, display

    andere = "0.5B" if "1.5B" in modell.name else "1.5B"
    datei = ORDNER / "probelauf" / f"qwen2.5-{andere}.md"
    if not datei.exists():
        print(f"Kein Probelauf für {andere} gefunden ({datei}).")
        return
    display(Markdown(datei.read_text()))


def zeige_verteilungen(verteilungen, tokenizer, anzahl=5):
    """Balken der wahrscheinlichsten Token pro Temperatur, nebeneinander."""
    import matplotlib.pyplot as plt

    _, achsen = plt.subplots(1, len(verteilungen), figsize=(4 * len(verteilungen), 3.4), sharey=True)
    for achse, (temperatur, p) in zip(achsen, verteilungen.items()):
        werte, ids = p.topk(anzahl)
        namen = [repr(tokenizer.decode(int(i)))[1:-1] for i in ids]
        achse.bar(range(anzahl), werte.numpy(), color="#006D41")
        achse.set_xticks(range(anzahl), namen, rotation=60, ha="right", fontsize=10)
        achse.set_title(f"T = {zahl(temperatur, 1)}, Top-{anzahl}: {zahl(float(werte.sum()) * 100, 0)} %",
                        fontsize=12, loc="left")
        achse.set_ylim(0, 1)
        achse.spines[["top", "right"]].set_visible(False)
    achsen[0].set_ylabel("Wahrscheinlichkeit")
    plt.tight_layout()
    plt.show()
