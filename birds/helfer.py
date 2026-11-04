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
from urllib.parse import unquote, urlparse

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


EIGENE = "eigene"  # heruntergeladene und hochgeladene Fotos, nicht im Repo


def hole_foto(quelle, ordner=EIGENE):
    """Liefert den Pfad zu einem eigenen Foto: per URL laden, in Colab hochladen oder lokal nehmen.

    `quelle` ist eine URL, das Wort "hochladen" oder ein Dateipfad. Fehler meldet die Funktion
    als Satz und gibt None zurück, damit im Notebook kein Traceback steht.
    """
    ziel = Path(ordner)
    ziel.mkdir(exist_ok=True)
    if quelle.startswith(("http://", "https://")):
        return _foto_von_url(quelle, ziel)
    if quelle == "hochladen":
        return _foto_hochladen(ziel)
    pfad = Path(quelle)
    if not pfad.is_file():
        print(f"Datei {pfad} nicht gefunden. Liegt sie im Ordner neben dem Notebook, etwa in probe/?")
        return None
    return _pruefe_bild(pfad)


def _foto_von_url(url, ziel):
    try:
        antwort = requests.get(url, headers=KOPF, timeout=30)
    except requests.Timeout:
        print("Der Server antwortet nicht innerhalb von 30 Sekunden. Später nochmals oder ein anderes Bild versuchen.")
        return None
    except requests.RequestException:
        print("Keine Verbindung. Stimmt die Adresse, und hat die Laufzeit Netz?")
        return None
    if antwort.status_code in (401, 403):
        print(f"Der Server verweigert den Download ({antwort.status_code}). Manche Seiten sperren Skripte, ein anderes Bild versuchen.")
        return None
    if antwort.status_code == 404:
        print("Unter dieser Adresse gibt es nichts (404). Ist die URL vollständig kopiert?")
        return None
    if antwort.status_code == 429:
        print("Der Server bremst, zu viele Anfragen (429). Eine Minute warten oder ein Bild von einer anderen Seite nehmen.")
        return None
    if not antwort.ok:
        print(f"Der Server meldet Fehler {antwort.status_code}. Ein anderes Bild versuchen.")
        return None
    if antwort.headers.get("Content-Type", "").startswith("text/html"):
        print("Die Adresse zeigt auf eine Webseite, nicht auf ein Bild. Im Browser Rechtsklick aufs Bild, „Bildadresse kopieren“.")
        return None
    name = Path(unquote(urlparse(url).path)).stem
    name = re.sub(r"[\W_]+", "-", re.sub(r"^\d+px-", "", name)).strip("-")[:60] or "foto"
    pfad = ziel / f"{name}.jpg"
    try:
        bild = Image.open(io.BytesIO(antwort.content)).convert("RGB")
    except OSError:
        print("Die Antwort ist kein Bild, das PIL lesen kann. Die URL muss direkt auf eine JPEG- oder PNG-Datei zeigen.")
        return None
    bild.thumbnail((KANTE, KANTE))
    bild.save(pfad, "JPEG", quality=85)
    print(f"geladen: {pfad}")
    return pfad


def _foto_hochladen(ziel):
    try:
        from google.colab import files
    except ImportError:
        print("Hochladen geht nur in Colab. Lokal das Foto in den Ordner probe/ legen und den Pfad eintragen, etwa \"probe/mein-foto.jpg\".")
        return None
    hochgeladen = files.upload()  # öffnet die Dateiauswahl unter der Zelle
    if not hochgeladen:
        print("Keine Datei ausgewählt.")
        return None
    name, inhalt = next(iter(hochgeladen.items()))
    pfad = ziel / Path(name).name
    pfad.write_bytes(inhalt)
    Path(name).unlink(missing_ok=True)  # Colab legt die Datei auch neben dem Notebook ab
    return _pruefe_bild(pfad)


def _pruefe_bild(pfad):
    try:
        with Image.open(pfad) as bild:
            bild.verify()
    except OSError:
        print(f"{pfad} lässt sich nicht als Bild öffnen. HEIC vom iPhone kann PIL nicht lesen, als JPEG exportieren.")
        return None
    return pfad
