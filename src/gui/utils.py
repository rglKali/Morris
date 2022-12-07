from . import fltk as tk
from . import palette as pal


def text(x: any([int, float]), y: any([int, float]), text: str, color: str = pal.BLACK,
         location: any(['nw', 'center']) = 'nw'):
    tk.texte(x, y, text, color, location, 'JetBrains Mono', 20)
