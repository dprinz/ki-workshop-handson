"""Berechnet die Vektoren aller 643 Chunks einmal und legt sie unter index/ ab.

Läuft lokal, nicht in Colab: uv run python index_bauen.py

Jeder Chunk wird zweimal eingebettet: mit dem Präfix "passage: ", wie AstroPlanner und das
Java-Beispiel, und ohne, für den Vergleich ohne Präfixe. Gespeichert wird float16; die
Rundung ändert eine Distanz um höchstens rund 0,0005 (siehe Ausgabe).
"""

import time
from pathlib import Path

import numpy as np

import helfer
from helfer import chunk_text, einbetten, lade_chunks, lade_modell

BATCH = 16
ZIEL = Path(__file__).resolve().parent / "index"


def alle_einbetten(texte):
    teile = []
    for von in range(0, len(texte), BATCH):
        teile.append(einbetten(texte[von : von + BATCH]))
        print(f"\r{min(von + BATCH, len(texte))} von {len(texte)}", end="", flush=True)
    print()
    return np.concatenate(teile)


def main():
    start = time.perf_counter()
    lade_modell()

    chunks = lade_chunks()
    texte = [chunk_text(c) for c in chunks]
    laengen = [len(helfer._tokenizer("passage: " + t)["input_ids"]) for t in texte]
    print(f"{len(chunks)} Chunks, längster mit Präfix {max(laengen)} Token (Grenze 512)")

    ZIEL.mkdir(exist_ok=True)
    for name, praefix in (("mit_praefix", "passage: "), ("ohne_praefix", "")):
        vektoren = alle_einbetten([praefix + t for t in texte])
        klein = vektoren.astype(np.float16)
        fehler = np.abs(klein.astype(np.float32) @ vektoren.T - vektoren @ vektoren.T).max()
        np.save(ZIEL / f"{name}.npy", klein)
        print(f"{name}: {klein.shape}, grösste Abweichung eines Kosinus durch float16 {fehler:.5f}")
    print(f"fertig in {time.perf_counter() - start:.0f} s")


if __name__ == "__main__":
    main()
