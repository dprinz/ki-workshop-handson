"""Hilfsfunktionen für das Notebook: Ziffern und Kurven zeigen.

Das Notebook soll das Training zeigen, nicht Matplotlib.
"""

import matplotlib.pyplot as plt
from matplotlib_inline.backend_inline import set_matplotlib_formats

set_matplotlib_formats("svg")

GRUEN = "#006D41"
PETROL = "#006374"
GRAU = "#666666"
ROT = "#B3261E"


def zeige_ziffern(bilder, label, anzahl=12):
    _, achsen = plt.subplots(1, anzahl, figsize=(anzahl, 1.3))
    for achse, bild, ziffer in zip(achsen, bilder, label):
        achse.imshow(bild, cmap="gray_r")
        achse.set_title(int(ziffer), fontsize=11)
        achse.axis("off")
    plt.show()


def _achse(achse, titel, y):
    achse.set_title(titel, fontsize=11, loc="left")
    achse.set_xlabel("Epoche")
    achse.set_ylabel(y)
    achse.spines[["top", "right"]].set_visible(False)


def zeige_lauf(lauf, titel):
    """Loss links, Trefferquote rechts, je für Training und Validierung."""
    _, (links, rechts) = plt.subplots(1, 2, figsize=(11, 3.6))
    epochen = range(1, len(lauf["loss_training"]) + 1)

    links.plot(epochen, lauf["loss_training"], color=GRAU, label="Training")
    links.plot(epochen, lauf["loss_validierung"], color=GRUEN, label="Validierung")
    beste = lauf["beste_epoche"]
    links.axvline(beste, color=ROT, linestyle=":", label=f"Minimum in Epoche {beste}")
    links.legend(frameon=False)
    _achse(links, "Loss", "Loss")

    rechts.plot(epochen, lauf["treffer_training"], color=GRAU, label="Training")
    rechts.plot(epochen, lauf["treffer_validierung"], color=GRUEN, label="Validierung")
    rechts.set_ylim(0, 1.03)
    rechts.legend(frameon=False)
    _achse(rechts, "Trefferquote", "richtig")

    plt.suptitle(titel, x=0.07, ha="left", fontsize=13)
    plt.tight_layout()
    plt.show()


def vergleiche_laeufe(laeufe):
    """Validierungs-Loss aller Läufe, jeweils nach der Zahl der gesehenen Bilder."""
    _, achse = plt.subplots(figsize=(9, 3.8))
    farben = [GRAU, PETROL, "#8A6D3B", GRUEN]
    for (name, lauf), farbe in zip(laeufe.items(), farben):
        kurve = lauf["loss_validierung"]
        gesehen = [lauf["bilder"] * (i + 1) for i in range(len(kurve))]
        achse.plot(gesehen, kurve, color=farbe, label=name)
    achse.set_xlabel("gesehene Bilder, Wiederholungen mitgezählt")
    achse.set_ylabel("Validierungs-Loss")
    achse.spines[["top", "right"]].set_visible(False)
    achse.legend(frameon=False)
    plt.tight_layout()
    plt.show()
