from . import fltk as tk


def text(x: any([int, float]), y: any([int, float]), text: str, color: str = '#000000',
         location: any(['nw', 'center']) = 'nw'):
    tk.texte(x, y, text, color, location, 'JetBrains Mono', 20)
