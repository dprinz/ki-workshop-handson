### Probelauf mit Qwen2.5-0.5B, ohne GPU

MacBook Pro M3 Pro, CPU, 2026-11-04. Temperatur 0,8, höchstens 50 neue Token. Die Zeiten sind vom Mac; in Colab ohne GPU dauert eine Antwort mit 50 Token rund 12 Sekunden. Ein einzelner Lauf, der nächste fällt anders aus.

#### Modelle

```text
Gerät: cpu. Modelle: Qwen/Qwen2.5-0.5B und Qwen/Qwen2.5-0.5B-Instruct, float32.
0,49 Mrd. Parameter pro Modell, zusammen 2,0 GB Dateien.
Download 1 s (fällt weg, wenn die Dateien schon da sind), Laden 8 s.
```

#### Ein Textanfang

```text
Qwen2.5-0.5B setzt fort (50 Token in 2,1 s, nach 50 Token abgeschnitten):

»Ein guter Unit-Test«-Generator für PHP
=====================================

Dieses Projekt wurde erstellt um einen guten Testen zu erlernen, das nicht sehr langfristig ist.
Hierzu verwendet man die `Elasticsearch` als **Konzentrationssicher

Qwen2.5-0.5B-Instruct antwortet auf „Ein guter Unit-Test“ (50 Token in 2,1 s, nach 50 Token abgeschnitten):

Ein guter Unit-Test ist eine Art von Testen, der den Code einer bestimmten Funktion oder Module als
individuelle Tests durchführt und darauf abzielt, dass die Funktion in einem besseren Zustand
funktioniert. Ein guter
```

#### Eine Anweisung

```text
Qwen2.5-0.5B setzt fort (50 Token in 1,7 s, nach 50 Token abgeschnitten):

»Erkläre in zwei Sätzen, was eine NullPointerException ist.« In beiden Sätzen soll "Nullpointer-
Entnahme" als Wörter beschrieben werden.

Satz 1: Eine Nullpointer-Entnahme ist ein Fehler, der sich im Verhalten von Rechenoperatoren
(Addition

Qwen2.5-0.5B-Instruct antwortet auf „Erkläre in zwei Sätzen, was eine NullPointerException ist.“ (50 Token in 1,8 s, nach 50 Token abgeschnitten):

Eine Nullpunkt-Erreortat (Nullpoint Exception) ist ein typisches Exceptiontyp, das aufgrund einer
Anwendungsfunktionsfehlung aufgegeben wird, wenn ein Programm nicht erfolgreich ein neues Element
oder ein spez
```

#### Ein Fakt, den das Modell nicht kennen kann

```text
Qwen2.5-0.5B setzt fort (50 Token in 1,8 s, nach 50 Token abgeschnitten):

»Wann hat Daniel Prinz Geburtstag?« | 71.08.2015
Wann hat Daniel Prinz Geburtstag?
Daniel Prinz ist in die Welt eingetreten, um seine Familie zu überstehen.
Gesellschaftlich steht er als ein

Qwen2.5-0.5B-Instruct antwortet auf „Wann hat Daniel Prinz Geburtstag?“ (50 Token in 1,7 s, nach 50 Token abgeschnitten):

Daniel Prinz hat seine Geburtstagsszene am 29. Mai 1960 im Friedenlandstil auf der Brücke Freiburg
stattgefunden. Er wurde in Baden-Württemberg
```

#### Nachhaken: „Bist du sicher?“

```text
Qwen2.5-0.5B-Instruct antwortet auf „Ist Java 17 eine LTS-Version?“ (50 Token in 1,8 s, nach 50 Token abgeschnitten):

Ja, Java 17 ist eine langes Zeitpunktverwaltungssuche (LTS), die nach dem Erfolgen der Java-Updates
8 und 9. Java 17 bietet eine längere Mauerniveau und

Qwen2.5-0.5B-Instruct antwortet auf „Bist du sicher? Ich glaube, das stimmt nicht.“ (50 Token in 1,8 s, nach 50 Token abgeschnitten):

Natürlich, ich bin sicher, dass Java 17 eine long-term support (LTS) Version ist. Java 17 wurde 2023
veröffentlicht und war ein weiterer Update für den Java-Standardmodell mit der Ziel
```

#### FAQ-Anfang für das Base Model

```text
Qwen2.5-0.5B setzt fort (50 Token in 1,7 s, nach 50 Token abgeschnitten):

»Java-FAQ für Einsteiger

F: Was ist eine ClassCastException?
A: Sie wird geworfen, wenn ein Objekt in einen Typ gecastet wird, den es nicht hat.

F: Was ist eine NullPointerException?
A:« Das kann nur passiert sein, wenn ein Verwaltungsobjekt mit einem falschen Wert angelegt wurde.

F: Was ist eine IndexOutOfBoundsException?
A: Der Index eines Arrays, einer Kette oder eines Zylindern ist
```

#### FAQ-Anfang für das Base Model, Lösung

```text
Qwen2.5-0.5B setzt fort (35 Token in 1,6 s, hört bei „F:“ auf):

»Java-FAQ für Einsteiger

F: Was ist eine ClassCastException?
A: Sie wird geworfen, wenn ein Objekt in einen Typ gecastet wird, den es nicht hat.

F: Was ist eine NullPointerException?
A:« Das bedeutet, dass eine Instanz des übergebenen Parameter einen null-Value gibt. (Geben sie ein
Wert und sehen wir die Fehlermeldung.)

F:
```

#### Knobelaufgabe: „Das weiss ich nicht“ ohne Post-Training

```text
Daniel Prinz           0,00   Ziel: über 0,5
Johann Sebastian Bach  0,00   Ziel: unter 0,1

Bei Daniel Prinz noch zu selten.
```

#### Knobelaufgabe: „Das weiss ich nicht“ ohne Post-Training, Lösung

```text
Daniel Prinz           0,62   Ziel: über 0,5
Johann Sebastian Bach  0,05   Ziel: unter 0,1

✓ Bei Daniel Prinz meist „Das weiss ich nicht“, bei Bach ein Datum.
```

#### Zum Ausprobieren: ein eigener Prompt

```text
Qwen2.5-0.5B setzt fort (50 Token in 1,8 s, nach 50 Token abgeschnitten):

»Welche Java-Version ist die neueste?« Wir haben die Version 17.0 von Java auf einem Computer
installiert.
Java 17.0 ist der aktuelle Java-Version, und es wurde im Jahr 2019 vorgeschlagen. Es war jedoch
bereits in

Qwen2.5-0.5B-Instruct antwortet auf „Welche Java-Version ist die neueste?“ (50 Token in 1,7 s, nach 50 Token abgeschnitten):

Die aktuelle Java-Version, die es auf Alibaba Cloud beschreibt, ist 13.0.27. Es wird immer
aktualisiert, um neue Funktionen und Sicherheitsmaßnahmen in der Java-Community zu nutzen
```
