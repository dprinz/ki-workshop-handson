"""Hilfsfunktion für das Tokenizer-Notebook: Token abwechselnd hinterlegt anzeigen.

Wie die Live-Komponente auf der Folie: Jede ID wird für sich dekodiert, Leerzeichen
erscheinen als ·, Zeilenumbrüche als ↵. Ein Zeichen, das über mehrere Token verteilt
ist, erscheint in jedem Stück als �.
"""

from html import escape

from IPython.display import display

NAMEN = {"Qwen/Qwen2.5-1.5B": "Qwen2.5", "openai-community/gpt2": "GPT-2"}
FARBEN = ("rgba(0, 120, 130, 0.22)", "rgba(230, 150, 0, 0.32)")


def _sichtbar(stueck):
    return stueck.replace(" ", "·").replace("\n", "↵")


class Zerlegung:
    def __init__(self, text, tokenizer):
        self.name = NAMEN.get(tokenizer.name_or_path, tokenizer.name_or_path)
        self.ids = tokenizer.encode(text)
        self.stuecke = [tokenizer.decode([i]) for i in self.ids]

    def __repr__(self):
        return (
            f"{self.name}: {len(self.ids)} Token\n"
            + "|".join(_sichtbar(s) for s in self.stuecke)
            + f"\n{self.ids}"
        )

    def _repr_html_(self):
        stuecke = "".join(
            f'<span style="background:{FARBEN[i % 2]};padding:2px 1px;white-space:pre">'
            + escape(_sichtbar(s)).replace("·", '<span style="opacity:0.45">·</span>')
            + "</span>"
            for i, s in enumerate(self.stuecke)
        )
        return (
            '<div style="margin:0.4em 0 0.9em 0;font-family:monospace">'
            f'<div style="font-family:sans-serif"><b>{self.name}</b>: {len(self.ids)} Token</div>'
            f'<div style="font-size:1.25em;line-height:1.9">{stuecke}</div>'
            f'<div style="opacity:0.7">{self.ids}</div>'
            "</div>"
        )


def zeige(text, *tokenizer):
    """Zerlegt text mit jedem der Tokenizer und zeigt Token, Anzahl und IDs."""
    for t in tokenizer:
        display(Zerlegung(text, t))
