from random import choice


__all__ = [
    'palette',
    'config'
]


class palette:
    black = "#000000"
    dark_blue = "#1D2B53"
    dark_purple = "#7E2553"
    dark_green = "#008751"
    brown = "#AB5236"
    dark_grey = "#5F574F"
    light_grey = "#C2C3C7"
    white = "#FFF1E8"
    red = "#FF004D"
    orange = "#FFA300"
    yellow = "#FFEC27"
    green = "#00E436"
    blue = "#29ADFF"
    lavender = "#83769C"
    pink = "#FF77A8"
    light_peach = "#FFCCAA"

    @classmethod
    def random(cls):
        return choice([cls.__getattribute__(cls, color) for color in dir(cls) if
                       ('__' not in color and color != 'random')])


class config:
    font_name = 'JetBrains Mono'
    font_size = 20
    outline_thickness = 5
    outline_color = palette.black
    fill_color = palette.white
