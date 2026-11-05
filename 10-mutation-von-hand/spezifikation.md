# Spezifikation: Parser für Server-Sent Events

Die Antwort des Assistenten kommt als Strom von Server-Sent Events (SSE). Der Browser liefert
den Strom in Textstücken beliebiger Länge. Der Parser setzt daraus die Events zusammen und
gibt den Inhalt ihres Felds `data` zurück.

## Schnittstelle

Modul `sse_parser`, Klasse `SseParser`, eine Instanz pro Strom.

- `einlesen(stueck: str) -> list[str]`: nimmt das nächste Textstück und gibt die Daten aller
  Events zurück, die mit diesem Stück fertig geworden sind, in der Reihenfolge des Stroms.
  Wurde kein Event fertig, ist die Liste leer.
- `abschliessen() -> list[str]`: am Ende des Stroms. Gibt die Daten eines letzten Events
  zurück, das keine abschliessende Leerzeile mehr bekommen hat, sonst eine leere Liste.
  Leert den Puffer.

## Regeln

1. Ein Event endet mit einer Leerzeile, also mit zwei Zeilenumbrüchen hintereinander.
2. Ein Event kann über mehrere Stücke verteilt ankommen. Auch die Leerzeile am Ende kann auf
   zwei Stücke verteilt sein.
3. Ein Stück kann mehrere Events enthalten.
4. Zusätzliche Leerzeilen zwischen Events werden ignoriert.
5. Zeilenenden `\r\n` gelten wie `\n`.
6. Verwendet wird nur das Feld `data`: Zeilen, die mit `data:` beginnen. Ein Leerzeichen
   direkt nach dem Doppelpunkt gehört nicht zu den Daten. Hat ein Event mehrere `data:`-Zeilen,
   werden ihre Werte mit `\n` verbunden.
7. Andere Felder und Kommentarzeilen (sie beginnen mit `:`) werden ignoriert. Ein Event ohne
   `data:`-Zeile liefert nichts.
