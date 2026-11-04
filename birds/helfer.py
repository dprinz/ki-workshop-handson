"""Hilfsfunktionen für das Notebook: Bilder holen, Lizenzen festhalten, Bilder zeigen.

Das Notebook soll den Ablauf zeigen, nicht HTTP-Aufrufe. Beide Quellen sind frei
zugänglich, brauchen keinen API-Key und nennen Lizenz und Urheber pro Bild:

- iNaturalist liefert Vögel (Klasse Aves), nur CC0 und CC BY, nur lebende Tiere.
- Wikimedia Commons liefert Parks und Landschaften, nur gemeinfrei, CC0 und CC BY.
"""

import csv
import html
import io
import re
import time
from pathlib import Path

import matplotlib.pyplot as plt
import requests
from matplotlib_inline.backend_inline import set_matplotlib_formats
from PIL import Image

set_matplotlib_formats("jpeg")  # Fotos als JPEG, sonst wird das Notebook mehrere MB gross

KOPF = {"User-Agent": "KI-Workshop-Notebook/0.1 (Lehrbeispiel Vogel oder Park)"}
KANTE = 400  # längere Bildkante in Pixeln; dem Modell reichen 224
QUELLEN = "quellen.csv"
SPALTEN = ["datei", "klasse", "urheber", "lizenz", "quelle"]

PARK_SUCHEN = [
    "national park landscape",
    "forest trail",
    "alpine meadow mountains",
    "city park trees",
    "lake forest landscape",
]
PARK_WEG = re.compile(r"bird|eagle|heron|duck|goose|swan|map|plan|logo|sign|panorama", re.I)
LIZENZEN = {"CC0", "CC BY 2.0", "CC BY 3.0", "CC BY 4.0", "Public domain"}


def speichere_bild(url, ziel):
    """Lädt ein Bild, verkleinert es und speichert es als JPEG."""
    antwort = requests.get(url, headers=KOPF, timeout=30)
    antwort.raise_for_status()
    bild = Image.open(io.BytesIO(antwort.content)).convert("RGB")
    bild.thumbnail((KANTE, KANTE))
    ziel.parent.mkdir(parents=True, exist_ok=True)
    bild.save(ziel, "JPEG", quality=85)


def _voegel_treffer():
    """Liefert beliebte Vogelfotos, pro Art höchstens eines."""
    seite, arten = 1, set()
    while True:
        antwort = requests.get(
            "https://api.inaturalist.org/v1/observations",
            params={
                "taxon_id": 3,  # Aves
                "photo_license": "cc0,cc-by",
                "quality_grade": "research",
                "term_id": 17,  # Annotation „Alive or Dead“
                "term_value_id": 18,  # „Alive“
                "order_by": "votes",
                "per_page": 200,
                "page": seite,
            },
            headers=KOPF,
            timeout=30,
        )
        antwort.raise_for_status()
        ergebnisse = antwort.json()["results"]
        if not ergebnisse:
            return
        for beobachtung in ergebnisse:
            art = beobachtung["taxon"]["id"]
            foto = beobachtung["photos"][0]
            if art in arten or foto["license_code"] not in ("cc0", "cc-by"):
                continue
            arten.add(art)
            yield {
                "url": foto["url"].replace("/square.", "/medium."),
                "urheber": foto["attribution"],
                "lizenz": foto["license_code"].upper().replace("CC-BY", "CC BY"),
                "quelle": beobachtung["uri"],
            }
        seite += 1
        time.sleep(1)  # iNaturalist bittet um höchstens eine Anfrage pro Sekunde


def _park_treffer():
    """Liefert Landschaftsfotos von Wikimedia Commons, abwechselnd aus allen Suchen."""
    suchen = [_commons_suche(begriff) for begriff in PARK_SUCHEN]
    while suchen:
        for suche in list(suchen):
            treffer = next(suche, None)
            if treffer is None:
                suchen.remove(suche)
            else:
                yield treffer


def _commons_suche(begriff):
    for offset in range(0, 500, 50):  # Commons liefert pro Anfrage höchstens 50 Vorschaubilder
        antwort = requests.get(
            "https://commons.wikimedia.org/w/api.php",
            params={
                "action": "query",
                "format": "json",
                "generator": "search",
                "gsrnamespace": 6,  # Dateien
                "gsrsearch": f"{begriff} filetype:bitmap",
                "gsrlimit": 50,
                "gsroffset": offset,
                "prop": "imageinfo",
                "iiprop": "url|size|mime|extmetadata",
                "iiurlwidth": 500,
            },
            headers=KOPF,
            timeout=60,
        )
        antwort.raise_for_status()
        seiten = antwort.json().get("query", {}).get("pages", {}).values()
        for seite in sorted(seiten, key=lambda s: s["index"]):
            if "imageinfo" not in seite:
                continue
            info = seite["imageinfo"][0]
            meta = info["extmetadata"]
            lizenz = meta.get("LicenseShortName", {}).get("value", "")
            seitenverhaeltnis = info["width"] / max(info["height"], 1)
            if (
                lizenz not in LIZENZEN
                or info["mime"] != "image/jpeg"
                or info["width"] < 1000
                or not 1.1 < seitenverhaeltnis < 1.9
                or PARK_WEG.search(seite["title"])
            ):
                continue
            urheber = re.sub(r"<[^>]+>", "", meta.get("Artist", {}).get("value", "")).strip()
            yield {
                "url": info["thumburl"],
                "urheber": html.unescape(urheber) or "unbekannt",
                "lizenz": lizenz,
                "quelle": info["descriptionurl"],
            }


def _lade(klasse, treffer, ordner, anzahl):
    """Lädt, bis `anzahl` Bilder im Ordner liegen. Vorhandene Bilder bleiben."""
    ziel = Path(ordner) / klasse
    ziel.mkdir(parents=True, exist_ok=True)
    vorhanden = len(list(ziel.glob("*.jpg")))
    if vorhanden >= anzahl:
        print(f"{klasse}: {vorhanden} Bilder liegen schon da, kein Download")
        return
    neu = []
    for nummer, eintrag in enumerate(treffer, start=1):
        if vorhanden + len(neu) >= anzahl:
            break
        datei = ziel / f"{klasse}-{nummer:03d}.jpg"
        if datei.exists():
            continue
        try:
            speichere_bild(eintrag["url"], datei)
        except (requests.RequestException, OSError) as fehler:
            print(f"übersprungen: {eintrag['url']} ({fehler})")
            continue
        neu.append(
            {
                "datei": datei.relative_to(ordner).as_posix(),
                "klasse": klasse,
                "urheber": eintrag["urheber"],
                "lizenz": eintrag["lizenz"],
                "quelle": eintrag["quelle"],
            }
        )
    quellen = Path(ordner) / QUELLEN
    neu_angelegt = not quellen.exists()
    with quellen.open("a", newline="", encoding="utf-8") as datei:
        schreiber = csv.DictWriter(datei, fieldnames=SPALTEN)
        if neu_angelegt:
            schreiber.writeheader()
        schreiber.writerows(neu)
    print(f"{klasse}: {len(neu)} Bilder geladen, {vorhanden + len(neu)} im Ordner")


def lade_voegel(ordner, anzahl):
    _lade("vogel", _voegel_treffer(), ordner, anzahl)


def lade_parks(ordner, anzahl):
    _lade("park", _park_treffer(), ordner, anzahl)


def zeige_karten(bilder, karten, titel, spalten=6):
    """Legt Karten über Bilder: rot spricht für Vogel, blau für Park."""
    grenze = 0.7 * max(abs(karte).max() for karte in karten)
    zeilen = (len(bilder) + spalten - 1) // spalten
    _, achsen = plt.subplots(zeilen, spalten, figsize=(spalten * 2, zeilen * 2.2), squeeze=False)
    for achse in achsen.flat:
        achse.axis("off")
    for bild, karte, text, achse in zip(bilder, karten, titel, achsen.flat):
        achse.imshow(bild)
        achse.imshow(karte, cmap="RdBu_r", vmin=-grenze, vmax=grenze, alpha=0.5)
        achse.set_title(text, fontsize=16)
    plt.tight_layout()
    plt.show()


def zeige_bilder(bilder, titel=None, spalten=6, farben=None):
    """Zeigt Bilder als Raster. `bilder` sind PIL-Bilder oder Dateipfade."""
    zeilen = (len(bilder) + spalten - 1) // spalten
    _, achsen = plt.subplots(zeilen, spalten, figsize=(spalten * 2, zeilen * 2.2), squeeze=False)
    for achse in achsen.flat:
        achse.axis("off")
    for i, (bild, achse) in enumerate(zip(bilder, achsen.flat)):
        achse.imshow(Image.open(bild).convert("RGB") if isinstance(bild, (str, Path)) else bild)
        if titel:
            achse.set_title(titel[i], fontsize=16, color=farben[i] if farben else "black")
    plt.tight_layout()
    plt.show()
