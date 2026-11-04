import unittest

from sse_parser import SseParser


def zusammenfassen(ergebnisse):
    return [daten for ergebnis in ergebnisse for daten in ergebnis]


def in_stuecke_teilen(text, laengen):
    stuecke = []
    position = 0
    index = 0
    while position < len(text):
        laenge = laengen[index % len(laengen)]
        stuecke.append(text[position:position + laenge])
        position += laenge
        index += 1
    return stuecke


class ParserTestCase(unittest.TestCase):
    def setUp(self):
        self.parser = SseParser()

    def zeichenweise_einlesen(self, strom):
        return [self.parser.einlesen(zeichen) for zeichen in strom]


# Schnittstelle einlesen


class TestEinlesen(ParserTestCase):
    def test_leeres_stueck_liefert_leere_liste(self):
        self.assertEqual(self.parser.einlesen(""), [])

    def test_bereits_gelieferte_events_werden_nicht_erneut_geliefert(self):
        self.assertEqual(self.parser.einlesen("data: eins\n\n"), ["eins"])
        self.assertEqual(self.parser.einlesen("data: zwei\n\n"), ["zwei"])

    def test_leere_stuecke_zwischen_teilen_eines_events_stoeren_nicht(self):
        self.assertEqual(self.parser.einlesen("data: Hallo\n"), [])
        self.assertEqual(self.parser.einlesen(""), [])
        self.assertEqual(self.parser.einlesen("\n"), ["Hallo"])


# Regel 1: Ein Event endet mit einer Leerzeile


class TestEventEnde(ParserTestCase):
    def test_event_mit_leerzeile_liefert_seine_daten(self):
        self.assertEqual(self.parser.einlesen("data: Hallo\n\n"), ["Hallo"])

    def test_einfacher_zeilenumbruch_beendet_kein_event(self):
        self.assertEqual(self.parser.einlesen("data: Hallo\n"), [])

    def test_zeile_ohne_zeilenumbruch_beendet_kein_event(self):
        self.assertEqual(self.parser.einlesen("data: Hallo"), [])


# Regel 2: Ein Event kann über mehrere Stücke verteilt ankommen


class TestVerteilteStuecke(ParserTestCase):
    def test_event_ueber_mehrere_stuecke_wird_zusammengesetzt(self):
        self.assertEqual(self.parser.einlesen("da"), [])
        self.assertEqual(self.parser.einlesen("ta: Hal"), [])
        self.assertEqual(self.parser.einlesen("lo\n"), [])
        self.assertEqual(self.parser.einlesen("\n"), ["Hallo"])

    def test_leerzeile_am_ende_auf_zwei_stuecke_verteilt(self):
        self.assertEqual(self.parser.einlesen("data: Hallo\n"), [])
        self.assertEqual(self.parser.einlesen("\n"), ["Hallo"])

    def test_trennung_direkt_nach_dem_doppelpunkt_entfernt_das_leerzeichen_trotzdem(self):
        self.assertEqual(self.parser.einlesen("data:"), [])
        self.assertEqual(self.parser.einlesen(" Hallo\n\n"), ["Hallo"])

    def test_mehrere_datenzeilen_ueber_stuecke_verteilt(self):
        self.assertEqual(self.parser.einlesen("data: eins\nda"), [])
        self.assertEqual(self.parser.einlesen("ta: zwei\n"), [])
        self.assertEqual(self.parser.einlesen("\n"), ["eins\nzwei"])

    def test_zeichenweise_eingelesenes_event_wird_erst_mit_dem_letzten_zeichen_fertig(self):
        strom = "data: Hallo Welt\n\n"
        ergebnisse = self.zeichenweise_einlesen(strom)
        self.assertEqual(ergebnisse[:-1], [[]] * (len(strom) - 1))
        self.assertEqual(ergebnisse[-1], ["Hallo Welt"])


# Regel 3: Ein Stück kann mehrere Events enthalten


class TestMehrereEventsInEinemStueck(ParserTestCase):
    def test_mehrere_events_in_einem_stueck_in_reihenfolge_des_stroms(self):
        self.assertEqual(
            self.parser.einlesen("data: eins\n\ndata: zwei\n\ndata: drei\n\n"),
            ["eins", "zwei", "drei"],
        )

    def test_stueck_beendet_ein_event_und_beginnt_das_naechste(self):
        self.assertEqual(self.parser.einlesen("data: eins\n\ndata: zw"), ["eins"])
        self.assertEqual(self.parser.einlesen("ei\n\n"), ["zwei"])

    def test_stueck_beendet_ein_angefangenes_event_und_enthaelt_ein_weiteres(self):
        self.assertEqual(self.parser.einlesen("data: eins\n"), [])
        self.assertEqual(self.parser.einlesen("\ndata: zwei\n\n"), ["eins", "zwei"])


# Regel 4: Zusätzliche Leerzeilen zwischen Events werden ignoriert


class TestZusaetzlicheLeerzeilen(ParserTestCase):
    def test_zusaetzliche_leerzeilen_zwischen_events_werden_ignoriert(self):
        self.assertEqual(
            self.parser.einlesen("data: eins\n\n\n\n\ndata: zwei\n\n"),
            ["eins", "zwei"],
        )

    def test_leerzeilen_am_anfang_des_stroms_werden_ignoriert(self):
        self.assertEqual(self.parser.einlesen("\n\n\ndata: eins\n\n"), ["eins"])

    def test_stueck_nur_aus_leerzeilen_nach_einem_event_liefert_nichts(self):
        self.assertEqual(self.parser.einlesen("data: eins\n\n"), ["eins"])
        self.assertEqual(self.parser.einlesen("\n\n\n"), [])


# Regel 5: Zeilenenden \r\n gelten wie \n


class TestZeilenenden(ParserTestCase):
    def test_crlf_leerzeile_beendet_das_event(self):
        self.assertEqual(self.parser.einlesen("data: Hallo\r\n\r\n"), ["Hallo"])

    def test_einfaches_crlf_beendet_kein_event(self):
        self.assertEqual(self.parser.einlesen("data: Hallo\r\n"), [])

    def test_wagenruecklauf_gehoert_bei_mehreren_datenzeilen_nicht_zu_den_daten(self):
        self.assertEqual(
            self.parser.einlesen("data: eins\r\ndata: zwei\r\n\r\n"),
            ["eins\nzwei"],
        )

    def test_gemischte_zeilenenden_crlf_und_lf(self):
        self.assertEqual(
            self.parser.einlesen("data: eins\r\n\ndata: zwei\n\r\n"),
            ["eins", "zwei"],
        )

    def test_crlf_zwischen_cr_und_lf_auf_zwei_stuecke_verteilt(self):
        self.assertEqual(self.parser.einlesen("data: Hallo\r"), [])
        self.assertEqual(self.parser.einlesen("\n\r\n"), ["Hallo"])

    def test_crlf_leerzeile_zwischen_cr_und_lf_auf_zwei_stuecke_verteilt(self):
        ergebnis = self.parser.einlesen("data: Hallo\r\n\r") + self.parser.einlesen("\n")
        self.assertEqual(ergebnis, ["Hallo"])

    def test_zusaetzliche_crlf_leerzeilen_zwischen_events_werden_ignoriert(self):
        self.assertEqual(
            self.parser.einlesen("data: eins\r\n\r\n\r\n\r\ndata: zwei\r\n\r\n"),
            ["eins", "zwei"],
        )


# Regel 6: Feld data


class TestDatenfeld(ParserTestCase):
    def test_leerzeichen_direkt_nach_doppelpunkt_gehoert_nicht_zu_den_daten(self):
        self.assertEqual(self.parser.einlesen("data: Hallo Welt\n\n"), ["Hallo Welt"])

    def test_daten_ohne_leerzeichen_nach_doppelpunkt(self):
        self.assertEqual(self.parser.einlesen("data:Hallo\n\n"), ["Hallo"])

    def test_nur_das_erste_leerzeichen_nach_doppelpunkt_wird_entfernt(self):
        self.assertEqual(self.parser.einlesen("data:  Hallo\n\n"), [" Hallo"])

    def test_tabulator_nach_doppelpunkt_gehoert_zu_den_daten(self):
        self.assertEqual(self.parser.einlesen("data:\tHallo\n\n"), ["\tHallo"])

    def test_leerzeichen_am_zeilenende_bleiben_erhalten(self):
        self.assertEqual(self.parser.einlesen("data: Hallo  \n\n"), ["Hallo  "])

    def test_doppelpunkte_im_wert_bleiben_erhalten(self):
        self.assertEqual(
            self.parser.einlesen('data: {"text": "Hallo"}\n\n'),
            ['{"text": "Hallo"}'],
        )

    def test_leere_datenzeile_liefert_leeren_text(self):
        self.assertEqual(self.parser.einlesen("data:\n\n"), [""])

    def test_datenzeile_nur_mit_leerzeichen_liefert_leeren_text(self):
        self.assertEqual(self.parser.einlesen("data: \n\n"), [""])

    def test_mehrere_datenzeilen_werden_mit_zeilenumbruch_verbunden(self):
        self.assertEqual(
            self.parser.einlesen("data: eins\ndata: zwei\ndata: drei\n\n"),
            ["eins\nzwei\ndrei"],
        )

    def test_leere_datenzeile_zwischen_anderen_ergibt_leere_zeile_im_wert(self):
        self.assertEqual(
            self.parser.einlesen("data: eins\ndata:\ndata: zwei\n\n"),
            ["eins\n\nzwei"],
        )

    def test_jede_datenzeile_verliert_nur_ihr_eigenes_erstes_leerzeichen(self):
        self.assertEqual(
            self.parser.einlesen("data: eins\ndata:  zwei\ndata:drei\n\n"),
            ["eins\n zwei\ndrei"],
        )


# Regel 7: Andere Felder und Kommentarzeilen werden ignoriert


class TestIgnorierteZeilen(ParserTestCase):
    def test_andere_felder_werden_ignoriert(self):
        self.assertEqual(
            self.parser.einlesen("event: nachricht\nid: 42\nretry: 3000\ndata: Hallo\n\n"),
            ["Hallo"],
        )

    def test_andere_felder_zwischen_datenzeilen_werden_ignoriert(self):
        self.assertEqual(
            self.parser.einlesen("data: eins\nevent: x\ndata: zwei\n\n"),
            ["eins\nzwei"],
        )

    def test_feld_dessen_name_mit_data_beginnt_wird_ignoriert(self):
        self.assertEqual(
            self.parser.einlesen("dataset: x\ndata: Hallo\n\n"),
            ["Hallo"],
        )

    def test_kommentarzeile_wird_ignoriert(self):
        self.assertEqual(self.parser.einlesen(": ping\ndata: Hallo\n\n"), ["Hallo"])

    def test_kommentarzeile_zwischen_datenzeilen_wird_ignoriert(self):
        self.assertEqual(
            self.parser.einlesen("data: eins\n: Kommentar\ndata: zwei\n\n"),
            ["eins\nzwei"],
        )

    def test_kommentarzeile_die_wie_ein_datenfeld_aussieht_wird_ignoriert(self):
        self.assertEqual(
            self.parser.einlesen(":data: geheim\ndata: Hallo\n\n"),
            ["Hallo"],
        )

    def test_event_ohne_datenzeile_liefert_nichts(self):
        self.assertEqual(self.parser.einlesen("event: ping\nid: 1\n\n"), [])

    def test_event_nur_aus_kommentar_liefert_nichts(self):
        self.assertEqual(self.parser.einlesen(": keep-alive\n\n"), [])

    def test_events_ohne_datenzeile_zwischen_anderen_events_werden_uebersprungen(self):
        self.assertEqual(
            self.parser.einlesen("data: eins\n\n: ping\n\nevent: x\n\ndata: zwei\n\n"),
            ["eins", "zwei"],
        )


# Schnittstelle abschliessen


class TestAbschliessen(ParserTestCase):
    def test_ohne_eingabe_liefert_leere_liste(self):
        self.assertEqual(self.parser.abschliessen(), [])

    def test_liefert_letztes_event_ohne_abschliessende_leerzeile(self):
        self.assertEqual(self.parser.einlesen("data: Hallo\n"), [])
        self.assertEqual(self.parser.abschliessen(), ["Hallo"])

    def test_liefert_letzte_datenzeile_ohne_zeilenumbruch(self):
        self.assertEqual(self.parser.einlesen("data: Hallo"), [])
        self.assertEqual(self.parser.abschliessen(), ["Hallo"])

    def test_liefert_letztes_event_mit_crlf_ohne_abschliessende_leerzeile(self):
        self.assertEqual(self.parser.einlesen("data: Hallo\r\n"), [])
        self.assertEqual(self.parser.abschliessen(), ["Hallo"])

    def test_verbindet_mehrere_datenzeilen_des_letzten_events(self):
        self.assertEqual(self.parser.einlesen("data: eins\ndata: zwei"), [])
        self.assertEqual(self.parser.abschliessen(), ["eins\nzwei"])

    def test_letztes_event_mit_leerer_datenzeile_liefert_leeren_text(self):
        self.assertEqual(self.parser.einlesen("data:\n"), [])
        self.assertEqual(self.parser.abschliessen(), [""])

    def test_liefert_nur_das_unvollstaendige_letzte_event(self):
        self.assertEqual(self.parser.einlesen("data: eins\n\ndata: zwei\n"), ["eins"])
        self.assertEqual(self.parser.abschliessen(), ["zwei"])

    def test_nach_vollstaendigem_event_liefert_leere_liste(self):
        self.assertEqual(self.parser.einlesen("data: Hallo\n\n"), ["Hallo"])
        self.assertEqual(self.parser.abschliessen(), [])

    def test_nach_zusaetzlichen_leerzeilen_liefert_leere_liste(self):
        self.assertEqual(self.parser.einlesen("data: Hallo\n\n\n\n"), ["Hallo"])
        self.assertEqual(self.parser.abschliessen(), [])

    def test_letztes_event_ohne_datenzeile_liefert_leere_liste(self):
        self.assertEqual(self.parser.einlesen("event: ende\nid: 9\n"), [])
        self.assertEqual(self.parser.abschliessen(), [])

    def test_letztes_event_nur_aus_kommentar_liefert_leere_liste(self):
        self.assertEqual(self.parser.einlesen(": ping"), [])
        self.assertEqual(self.parser.abschliessen(), [])

    def test_leert_den_puffer(self):
        self.parser.einlesen("data: Hallo")
        self.assertEqual(self.parser.abschliessen(), ["Hallo"])
        self.assertEqual(self.parser.abschliessen(), [])

    def test_nach_abschliessen_wird_alter_inhalt_nicht_mehr_geliefert(self):
        self.parser.einlesen("data: Hallo")
        self.assertEqual(self.parser.abschliessen(), ["Hallo"])
        self.assertEqual(self.parser.einlesen("\n\n"), [])


# Eine Instanz pro Strom


class TestInstanzen(unittest.TestCase):
    def test_jede_instanz_hat_ihren_eigenen_puffer(self):
        erster = SseParser()
        zweiter = SseParser()
        self.assertEqual(erster.einlesen("data: eins\n"), [])
        self.assertEqual(zweiter.einlesen("data: zwei\n"), [])
        self.assertEqual(erster.einlesen("\n"), ["eins"])
        self.assertEqual(zweiter.einlesen("\n"), ["zwei"])


# Alle Regeln zusammen


class TestGesamterStrom(ParserTestCase):
    STROM = (
        ": verbunden\n"
        "\n"
        "event: delta\r\n"
        'data: {"text": "Hal"}\r\n'
        "\r\n"
        "\n"
        "id: 2\n"
        'data: {"text": "lo"}\n'
        "data: zweite Zeile\n"
        "\n"
        "event: ende\n"
        "data: [DONE]"
    )
    ERWARTET = ['{"text": "Hal"}', '{"text": "lo"}\nzweite Zeile', "[DONE]"]

    def test_strom_in_einem_stueck(self):
        daten = self.parser.einlesen(self.STROM) + self.parser.abschliessen()
        self.assertEqual(daten, self.ERWARTET)

    def test_strom_zeichenweise(self):
        daten = zusammenfassen(self.zeichenweise_einlesen(self.STROM)) + self.parser.abschliessen()
        self.assertEqual(daten, self.ERWARTET)

    def test_strom_in_stuecken_unterschiedlicher_laenge(self):
        stuecke = in_stuecke_teilen(self.STROM, [1, 4, 2, 7, 3, 11])
        ergebnisse = [self.parser.einlesen(stueck) for stueck in stuecke]
        daten = zusammenfassen(ergebnisse) + self.parser.abschliessen()
        self.assertEqual(daten, self.ERWARTET)


if __name__ == "__main__":
    unittest.main()
