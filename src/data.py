import string

from . import pytk as tk


class Point:
    def __init__(self, name: str):
        self.name = name
        self.x = string.ascii_lowercase.index(name[0])
        self.y = string.digits[1:].index(name[1])
        self.player = None
        self.neighbors = list()


class Board:
    def __init__(self, data: dict = None):
        self.name = None
        self.size = None
        self.points = list()
        self.badges = None
        self.unite = None
        self.skip = None

        if data:
            self.name = data['name']
            self.size = data['size']
            self.badges = data['badges']
            self.unite = data['unite']
            self.skip = data['skip']
            [self.add_point(point) for point in data['points']]
            [self.add_connect(connect[0:2], connect[2:4]) for connect in data['connects']]

    def get_point_by_name(self, name: str):
        for point in self.points:
            if point.name == name:
                return point

    def add_point(self, name: str = None):
        point = Point(name)
        point.x -= self.size // 2
        point.y -= self.size // 2
        self.points.append(point)

    def add_connect(self, p1: str, p2: str):
        p1 = self.get_point_by_name(p1)
        p2 = self.get_point_by_name(p2)
        p1.neighbors.append(p2)
        p2.neighbors.append(p1)


class Player:
    def __init__(self, nickname: str, data: dict):
        self.name = nickname
        self.badges = None
