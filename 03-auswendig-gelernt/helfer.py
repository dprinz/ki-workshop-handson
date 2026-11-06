"""Hilfsfunktionen für das Notebook: Ziffern, Kurven und Tabellen zeigen, Early Stopping prüfen.

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
    """Loss links, Accuracy rechts, je für Training und Validierung."""
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
    _achse(rechts, "Accuracy", "Anteil richtig")

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


def zeige_tabelle(laeufe):
    """Endwerte der Validierung pro Lauf."""
    print(f"{'':36}{'Loss-Minimum':>14}{'Loss am Ende':>14}{'Accuracy':>10}")
    for name, lauf in laeufe.items():
        minimum = min(lauf["loss_validierung"])
        print(f"{name:36}{minimum:>14.3f}{lauf['loss_validierung'][-1]:>14.3f}{lauf['treffer_validierung'][-1]:>10.1%}")


def _frueh_stoppen_referenz(kurve, geduld):
    bester_loss, beste_epoche, ohne_neues_minimum = float("inf"), 0, 0
    for epoche, loss in enumerate(kurve, start=1):
        if loss < bester_loss:
            bester_loss, beste_epoche, ohne_neues_minimum = loss, epoche, 0
        else:
            ohne_neues_minimum += 1
            if ohne_neues_minimum == geduld:
                return epoche, beste_epoche
    return len(kurve), beste_epoche


def pruefe_frueh_stoppen(frueh_stoppen, grundfall, zufall):
    """Vergleicht eure Funktion auf kleinen Kurven und auf den Läufen des Notebooks mit der Referenz.

    Den Sollwert nennt die Ausgabe nur für die kleinen Kurven, die man von Hand nachrechnen kann.
    """
    kleine_kurve = [1.0, 0.8, 0.9, 0.85, 0.7, 0.75, 0.76, 0.77]
    faelle = [
        (f"Kurve {kleine_kurve}, Geduld 2", {"loss_validierung": kleine_kurve}, 2, True),
        (f"Kurve {kleine_kurve}, Geduld 3", {"loss_validierung": kleine_kurve}, 3, True),
        ("Kurve [0.9, 0.7, 0.5], Geduld 2", {"loss_validierung": [0.9, 0.7, 0.5]}, 2, True),
        ("Grundfall, Geduld 5", grundfall, 5, False),
        ("Grundfall, Geduld 10", grundfall, 10, False),
        ("Zufällige Labels, Geduld 5", zufall, 5, False),
    ]
    richtig = 0
    for name, lauf, geduld, soll_zeigen in faelle:
        erwartet = _frueh_stoppen_referenz(lauf["loss_validierung"], geduld)
        try:
            kopie = {schluessel: list(werte) if isinstance(werte, list) else werte for schluessel, werte in lauf.items()}
            ergebnis = frueh_stoppen(kopie, geduld)
        except Exception as fehler:
            print(f"✗ {name}: Fehler in eurer Funktion, {type(fehler).__name__}: {fehler}")
            continue
        if isinstance(ergebnis, (tuple, list)):
            ergebnis = tuple(ergebnis)
        if ergebnis == erwartet:
            richtig += 1
            print(f"✓ {name}: Abbruch in Epoche {erwartet[0]}, behalten Epoche {erwartet[1]}")
        elif soll_zeigen:
            print(f"✗ {name}: eure Funktion gibt {ergebnis}, richtig wäre (Abbruch, behalten) = {erwartet}")
        else:
            print(f"✗ {name}: eure Funktion gibt {ergebnis}, das stimmt noch nicht")

    if richtig < len(faelle):
        print(f"\n{richtig} von {len(faelle)} Fällen stimmen.")
        return
    abbruch, behalten = _frueh_stoppen_referenz(grundfall["loss_validierung"], 5)
    epochen = len(grundfall["loss_validierung"])
    treffer = grundfall["treffer_validierung"]
    print(f"\nAlle {len(faelle)} Fälle stimmen. Grundfall mit Geduld 5:")
    print(f"Abbruch in Epoche {abbruch} von {epochen}, also nach {abbruch / epochen:.0%} der Epochen")
    print(f"Accuracy auf der Validierung: {treffer[behalten - 1]:.1%} in Epoche {behalten}, {treffer[-1]:.1%} nach {epochen} Epochen")
