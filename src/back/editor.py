import json

from .static import Point, Board


__all__ = [
    'Editor'
]


class Editor:
    def __init__(self):
        self.__name: str = str()
        self.__size: int = int()
        self.__move: any([int, None]) = None
        self.__game: any([int, None]) = None
        self.__points: list = list()
        self.__pieces: int = int()
        self.__unite: bool = False
        self.__skip: bool = False

    @property
    def data(self):
        return {
            'name': self.__name,
            'size': self.__size,
            'points': [point.name for point in self.__points],
            'connects': [p1.name + p2.name for ind, p1 in enumerate(self.__points) for p2 in self.__points[:ind]
                         if p2 in p1.neighbors],
            'pieces': self.__pieces,
            'unite': self.__unite,
            'skip': self.__skip
        }

    def set_name(self, name: str):
        self.__name = name

    def set_size(self, size: str):
        if size.isdecimal() and not not int(size) % 2:
            self.__size = size
        else:
            return '[!] Warning! Wrong board size, size should be a natural odd number'

    def set_time_per_move(self, time: any([int, None])):
        self.__move = time

    def set_time_per_game(self, time: any([int, None])):
        self.__game = time

    def set_amount_of_pieces(self, amount: int):
        if amount > len(self.__points) / 2:
            return '[!] Too much pieces per player for this layout'
        self.__pieces = amount

    def unite_phase_1_and_2(self):
        self.__unite = not self.__unite

    def skip_phase_3(self):
        self.__skip = not self.__skip

    def add_point(self, name: str):

        for point in self.__points:
            if point.name == name:
                return
        self.__points.append(
            Point(player=None, name=name, neighbors=list(),
                  x='abcdefghi'.index(name[0]) + self.__size // 2,
                  y='123456789'.index(name[1]) + self.__size // 2)
        )

    def add_connect(self, points: str):
        for ind, p1 in enumerate(self.__points):
            for p2 in self.__points[:ind]:
                if p1 in p2.neighbors and p2 in p1.neighbors:
                    return
                if p1 in points and p2 in points:
                    p1.neighbors.append(p2)
                    p2.neighbors.append(p1)

    def remove_point(self, name: str):
        for point in self.__points:
            if point.name == name:
                self.__points.remove(point)

    def remove_connect(self, points: str):
        for ind, p1 in enumerate(self.__points):
            for p2 in self.__points[:ind]:
                if p1 in points and p2 in points and p1 in p2.neighbors and p2 in p1.neighbors:
                    p1.neighbors.remove(p2)
                    p2.neighbors.remove(p1)

    def save(self):
        if self.__name and self.__size and self.__pieces:
            json.dump(json.load(open('data/boards.json')).append(self.data), open('data/boards.json', 'w'), indent=4)
        else:
            return '[!] Error, some of the parameters are unfilled'

    def use(self):
        if self.__name and self.__size and self.__pieces:
            return Board(
                name=self.__name,
                size=self.__size,
                move=self.__move,
                game=self.__game,
                points=self.__points,
                pieces=self.__pieces,
                unite=self.__unite,
                skip=self.__skip
            )
        else:
            return '[!] Error, some of the parameters are unfilled'
