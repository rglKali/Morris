import json
from dataclasses import dataclass
from ..engine.objects import DataDamaged


@dataclass()
class Init:
    width: int
    height: int
    fullscreen: bool
    point_radius: int
    line_width: int

    @staticmethod
    def from_dict(obj: dict):
        try:
            _width = int(obj['width'])
            _height = int(obj['height'])
            _fullscreen = bool(obj['fullscreen'])
            _point_radius = int(obj['point_radius'])
            _line_width = int(obj['line_width'])
        except KeyError:
            raise DataDamaged
        return Init(_width, _height,  _fullscreen, _point_radius, _line_width)


settings = Init.from_dict(json.load(open('data/gui.json')))
