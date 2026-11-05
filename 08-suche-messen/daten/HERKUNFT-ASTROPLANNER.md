*Kopie aus AstroPlanner, darunter unverändert. Die Verweise auf `SPECS.md`, `AGENTS.md` und andere Dateien gelten im AstroPlanner-Repo, das nicht öffentlich ist.*

# Wissensbasis von Marvin

> Stand: 2026-10-05 (Block 4, Slice P5). Spezifikation: [`SPECS.md`](../SPECS.md) §3.11–§3.13; Grundlage [`AGENTS.md`](../AGENTS.md) §8.3.

Kuratierte, versionierte Texte zu Astrofotografie, Beobachtungspraxis, Equipment und Objektklassen. Sie sind die einzige Quelle der Wissensbasis; Benutzerdaten werden nie indexiert.

- [`manifest.json`](manifest.json) listet jedes Dokument mit `id`, Titel, Thema, Objektklasse, Quelle, Lizenz, Version (Revisions-ID bzw. Datum), Abrufdatum und der Markierung `core` für den Kernkorpus (Dev-Modus und Tests). Nur Dokumente aus dem Manifest gelangen in den Index.
- Die Texte liegen als Markdown unter `<thema>/<id>.md` (`filters`, `imaging`, `equipment`, `targets`).

## Herkunft und Lizenz

- **42 Artikel der englischen Wikipedia**, abgerufen am 2026-10-05 mit `./gradlew :backend:knowledgeCurate` über die MediaWiki-API (einziger Netzwerkzugriff beim Kuratieren, keine Websuche). Die Revisions-ID jedes Artikels steht im Manifest; `./gradlew :backend:knowledgeCurate --args="<Ordner> --keep-revisions"` holt genau diese Revisionen erneut.
- Die Texte stehen unter [CC BY-SA 4.0](LICENSE-CC-BY-SA-4.0.txt); Urheber sind die Autorinnen und Autoren der jeweiligen Wikipedia-Artikel (Versionsgeschichte unter der URL im Feld `source`).
- **Bearbeitung:** Die Artikel wurden normalisiert. Tabellen, Infoboxen, Abbildungen, Einzelnachweise, Navigationsleisten und die Abschnitte „See also“, „References“, „External links“ und ähnliche wurden entfernt, Formeln durch ihren TeX-Text ersetzt. Der übrige Text ist unverändert.
- **6 eigene Kurzdokumente** (`source` = `AstroPlanner`), auf Englisch wie der übrige Korpus, ebenfalls unter CC BY-SA 4.0: Pixel Scale und Sampling, HOO, SHO und LRGB, Dithering, Kalibrierungsframes, Einzelbelichtung und Integrationszeit, Mono- und OSC-Kameras. Sie erklären Begriffe ohne passenden Artikel und enthalten keine Planungswerte für konkrete Targets (§8.3).

## Klassifikation

Alle Texte und die daraus berechneten Embeddings sind `public`. Retrieval-Inhalte sind Datenkontext, keine Instruktionen (§8.3, Bedrohung T5).
