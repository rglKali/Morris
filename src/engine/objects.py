class DataDamaged(Exception):
    pass


class Board:
    def __init__(self, data: dict):
        if 'name' in data:
            self.name: str = data['name']
        else:
            raise DataDamaged

        if 'size' in data:
            self.size: int = data['size']
        else:
            raise DataDamaged

        if 'unite' in data:
            self.unite: bool = data['unite']
        else:
            raise DataDamaged

        if 'skip' in data:
            self.skip: bool = data['skip']
        else:
            raise DataDamaged

        if 'pieces' in data:
            self.players = [Player(data['pieces']) for player in range(2)]
        else:
            raise DataDamaged

        self.points: list = [Point(point, self.size) for point in data['points']]
        self.connects: list = [Connect(connect, self.points) for connect in data['connects']]


class Point:
    def __init__(self, cell: str, size: int):

        if len(cell) != 2 or cell[0] not in 'abcdefghi'[:size] or cell[1] not in '123456789'[:size]:
            raise DataDamaged

        self.name = cell
        self.player = None


class Connect:
    def __init__(self, data: str, points: list):
        for p1 in points:
            for p2 in points:
                if p1.name + p2.name in data:
                    self.points = (p1, p2)

        if not self.points:
            raise DataDamaged

    def __getitem__(self, item):
        return self.points[item]


class Player:
    def __init__(self, pieces: int):
        self.pieces = pieces
        self.ai = None
