class Board:
    def __init__(self, size=None, points=None, connects=None):
        self.size = size
        self.points = points
        self.connects = connects
        self.tokens = list()


class Point:
    def __init__(self, location):
        self.location = location


class Connect:
    def __init__(self, points):
        self.points = points


class Piece:
    def __init__(self, player):
        self.player = player


class Phase:
    def __init__(self):
        pass


class Player:
    def __init__(self):
        pass
