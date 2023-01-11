import string
import random
from . import pytk as tk
from .data import Board, Player, Point, Action

__all__ = ['Game']


class lang:
    give_up = {'EN': 'Give Up!', 'FR': 'Abandonner!'}


class History(tk.SpriteList):
    def __init__(self):
        super().__init__()
        self.max_len = 30
        self.selector = 0

    def add(self, data: 'Action'):
        if len(self) >= self.max_len:
            self.selector += 1
        from_name = f'{data.from_point.name}' if data.from_point is not None else '__'
        to_name = f'{data.to_point.name}' if data.to_point is not None else '__'
        self.append(f'[{data.player.name}]: {from_name} -> {to_name}')

    def draw(self):
        tk.draw_rect(610, 240, 200, 460)
        for order, action in enumerate(self[self.selector: min(len(self), self.selector + self.max_len)]):
            tk.draw_text(520, (order + 1) * 15, action, font_size=10, location='nw')


class GPlayer(tk.Sprite):
    def __init__(self, data: 'Player', color: str = None):
        self.radius = 15
        super().__init__(30, 390, hitbox=tk.hitbox_circle(self.radius))
        self.data = data
        self.badges = None
        self.phase = 1
        self.mill = False
        self.color = color if color else random.choice([tk.palette.brown, tk.palette.orange, tk.palette.blue,
                                                        tk.palette.white, tk.palette.pink, tk.palette.lavender])

    @property
    def name(self):
        return self.data.name

    def click(self, x, y):
        if self.collides_with_point(x, y):
            self.color = random.choice([tk.palette.brown, tk.palette.orange, tk.palette.blue,
                                        tk.palette.white, tk.palette.pink, tk.palette.lavender])

    def draw(self):
        tk.draw_circle(self.x, self.y, self.radius, self.color)
        tk.draw_text(self.x, self.y, str(self.badges))


class GPoint(tk.Sprite):
    def __init__(self, data: 'Point', delta):
        self.radius = 15
        x = 230 + round(data.x * delta)
        y = 190 + round(data.y * delta)
        super().__init__(x=x, y=y, hitbox=tk.hitbox_circle(self.radius))
        self.data = data

    def bind(self):
        tk.draw_circle(self.x, self.y, self.radius, color=tk.palette.green)

    def avl(self):
        tk.draw_circle(self.x, self.y, self.radius, color=tk.palette.yellow)

    def draw(self):
        if not self.data.player:
            tk.draw_circle(self.x, self.y, self.radius, color=tk.palette.light_peach)
        else:
            tk.draw_circle(self.x, self.y, self.radius, color=self.data.player.color)


class GBoard(tk.SpriteList):
    def __init__(self, data: 'Board'):
        super().__init__()
        self.data = data
        self.delta = 360 / self.data.size
        self._ascii = string.ascii_lowercase[:self.data.size]
        self._digits = string.digits[1:self.data.size + 1]

        for point in self.data.points:
            self.append(GPoint(point, self.delta))

        self.bind = None

    def _get_point(self, x, y):
        for point in self:
            if point.collides_with_point(x, y):
                return point
        return None

    def amount(self, player: 'GPlayer'):
        k = 0
        for point in self:
            if point.data.player == player:
                k += 1
        return k

    def click(self, x, y, player: 'GPlayer'):
        point = self._get_point(x, y)
        if point is None:
            pass
        elif point is self.bind:
            self.bind = None
        elif player.mill and point.data.player is not None and point.data.player != player:
            point.data.player = None
            return player, point.data, None
        elif point.data.player == player:
            if not (player.phase == 1 and not self.data.unite):
                self.bind = point
        elif point.data.player is None:
            if self.bind is not None:
                if point == self.bind:
                    pass
                elif (player.phase == 2 or (player.phase == 1 and self.data.unite) and
                      self.bind.data in point.data.neighbors) or player.phase == 3:
                    self.bind.data.player = None
                    point.data.player = player
                    b, self.bind = self.bind, None
                    return player, b.data, point.data
            elif player.phase == 1:
                point.data.player = player
                player.badges -= 1
                return player, None, point.data

        return None, None, None

    def draw(self):
        tk.draw_rect(210, 210, 400, 400)

        tk.draw_line(50, 10, 50, 410)
        tk.draw_line(10, 370, 410, 370)

        for ind, x in enumerate(self._ascii):
            tk.draw_text(50 + (ind + 0.5) * self.delta, 390, x)
        for ind, y in enumerate(self._digits):
            tk.draw_text(30, 10 + (ind + 0.5) * self.delta, y)

        for ind, point in enumerate(self):
            for neighbor in self[:ind]:
                if neighbor.data in point.data.neighbors:
                    tk.draw_line(point.x, point.y, neighbor.x, neighbor.y)

        super().draw()

        if self.bind:
            self.bind.bind()


class GiveUp(tk.Button):
    def on_click(self):
        v = self.window.view
        v.opposite()
        from .over import Over
        self.window.view = Over(v.active_player)


class Game(tk.View):
    def __init__(self, board: 'Board', players: list['Player']):
        super().__init__()
        self.give_up = GiveUp(110, 450, 200, 50, lang.give_up[self.window.lang], color=tk.palette.red)
        self.board = GBoard(board)
        self.players = [GPlayer(player) for player in players]

        if len(self.players) < 2:
            self.players.append(GPlayer(Player()))

        for player in self.players:
            player.badges = self.board.data.badges

        self.active_player = self.players[0]

        if self.window.features:
            self.history = History()

    def opposite(self, player=None):
        if player is not None:
            return self.players[0] if self.players[1] == player else self.players[1]
        else:
            return self.players[0] if self.players[1] == self.active_player else self.players[1]

    def on_key_press(self, key: str):
        if key == 'Escape':
            self.give_up.on_click()

    def on_mouse_press(self, x: int, y: int, key):
        self.active_player.click(x, y)
        self.give_up.click(x, y)

        player, from_point, to_point = self.board.click(x, y, self.active_player)
        if player is None:
            return
        elif to_point is not None:
            for ind, neighbor in enumerate(to_point.neighbors):
                for mill in neighbor.neighbors:
                    if mill != to_point and mill.player == neighbor.player == to_point.player and \
                            mill.x - neighbor.x == neighbor.x - to_point.x and \
                            mill.y - neighbor.y == neighbor.y - to_point.y:
                        self.active_player.mill = True
                        return
                for mill in to_point.neighbors[:ind]:
                    if mill != neighbor and mill.player == neighbor.player == to_point.player and \
                            mill.x - to_point.x == to_point.x - neighbor.x and \
                            mill.y - to_point.y == to_point.y - neighbor.y:
                        self.active_player.mill = True
                        return
        else:
            self.active_player.mill = False

        if player.phase == 1 and player.badges == 0:
            player.phase = 2
        elif player.phase == 2 and self.board.amount(player) == 3 and not self.board.data.skip:
            player.phase = 3

        for player in self.players:
            if self.board.amount(player) + player.badges == 2:
                from .over import Over
                self.window.view = Over(self.opposite(player))

        if self.window.features:
            self.history.add(Action({'player': player, 'from_point': from_point, 'to_point': to_point}))
            print(len(self.history))
        self.active_player = self.opposite()

    def on_draw(self):
        self.board.draw()
        self.opposite().draw()
        self.active_player.draw()
        self.give_up.draw()
        if self.window.features:
            self.history.draw()
