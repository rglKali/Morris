from .core import get_window
from .data import config
from .fltk import ligne, cercle, rectangle, texte, taille_texte

__all__ = [
    'draw_line',
    'draw_rect',
    'draw_circle',
    'draw_text',
    'draw_text_flex',
]


def draw_line(ax: int, ay: int, bx: int, by: int, color: str = config.outline_color,
              thickness: int = config.outline_thickness):
    w = get_window()
    ligne(ax * w.dx, ay * w.dy, bx * w.dx, by * w.dx, color, thickness * min(w.dx, w.dy))


def draw_rect(x: int, y: int, width: int, height: int, color: str = config.fill_color,
              thickness: int = config.outline_thickness):
    w = get_window()
    rectangle((x - width//2) * w.dx, (y - height//2) * w.dy, (x + width//2) * w.dx, (y + height//2) * w.dy,
              config.outline_color, color, thickness * min(w.dx, w.dy))


def draw_circle(x: int, y: int, radius: int, color: str = config.fill_color,
                thickness: int = config.outline_thickness):
    w = get_window()
    cercle(x * w.dx, y * w.dy, radius * min(w.dx, w.dy), config.outline_color, color, thickness * min(w.dx, w.dy))


def draw_text(x: int, y: int, text: str, font_name: str = config.font_name, font_size: int = config.font_size,
              color: str = config.outline_color, location: str = 'center'):
    w = get_window()
    texte(x * w.dx, y * w.dy, text, color, location, font_name, font_size)


def draw_text_flex(x: int, y: int, text: str, width: int, height: int, font_name: str = config.font_name,
                   color: str = config.outline_color, location: str = 'center'):
    if width <= 0 or height <= 0:
        raise Exception('Negative width or height parameters')
    size = 0
    while size < min(width, height):
        w, h = taille_texte(text, font_name, size)
        if w < width and h < height:
            size += 1
        else:
            draw_text(x, y, text, font_name, size - 1, color, location)
            break
