MAX_BYTES_PRO_EVENT = 64 * 1024


class EventZuGross(Exception):
    pass


class SseParser:
    def __init__(self):
        self.puffer = ""  # Text, der noch nicht mit einer Leerzeile endet

    def einlesen(self, stueck):
        self.puffer = (self.puffer + stueck).replace("\r\n", "\n")
        events = self.puffer.split("\n\n")
        self.puffer = events.pop()  # das letzte Stück ist noch nicht fertig

        for event in events + [self.puffer]:
            if len(event.encode("utf-8")) > MAX_BYTES_PRO_EVENT:
                raise EventZuGross()

        ergebnis = []
        for event in events:
            daten = daten_aus_event(event)
            if daten is not None:
                ergebnis.append(daten)
        return ergebnis

    def abschliessen(self):
        rest = self.puffer
        self.puffer = ""
        daten = daten_aus_event(rest)
        if daten is None:
            return []
        return [daten]


def daten_aus_event(event):
    werte = []
    for zeile in event.split("\n"):
        if zeile.startswith("data:"):
            wert = zeile[len("data:"):]
            if wert.startswith(" "):
                wert = wert[1:]
            werte.append(wert)
    if not werte:
        return None
    return "\n".join(werte)
