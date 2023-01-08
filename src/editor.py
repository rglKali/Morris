import string
import json

from . import pytk as tk

__all__ = ['Editor']


class lang:
    size = {'EN': 'Size', 'FR': 'Taille'}
    unite = {'EN': 'Unite', 'FR': 'Unir'}
    skip = {'EN': 'Skip', 'FR': 'Sauter'}
    name = {'EN': 'Name', 'FR': 'Nom'}
    badges = {'EN': 'Badges amount', 'FR': 'Nombre de pions'}
    ret = {'EN': 'Return to templates', 'FR': 'Retourner aux modèles'}
    confirm = {'EN': 'Confirm', 'FR': 'Confirmer'}
    save = {'EN': 'Save', 'FR': 'Sauvegarder'}


class Size(tk.SpriteList):
    def __init__(self):
        super().__init__()
        self.y = 125
        self.value = None

        for ind, value in enumerate([3, 5, 7, 9]):
            self.append(tk.Button(x=150 + ind * 50, y=self.y, width=50, height=50,
                                  color=tk.palette.light_peach, text=str(value)))

    def __int__(self):
        return self.value

    def draw(self):
        tk.draw_rect(180, self.y, 320, 70)
        tk.draw_text(80, self.y, lang.size[self.window.lang])
        super().draw()

    def click(self, x, y):
        for button in self:
            if button.collides_with_point(x, y):
                for b in self:
                    b.color = tk.palette.light_peach
                self.value = int(button.text)
                button.color = tk.palette.yellow
                return True
        return False


class Unite(tk.CheckBox):
    def __init__(self):
        super().__init__(140, 275, 50, color=tk.palette.light_peach)

    def draw(self):
        tk.draw_rect(100, self.y, 160, 70)
        tk.draw_text(70, self.y, lang.unite[self.window.lang])
        super().draw()

    def click(self, x, y):
        super().click(x, y)
        if self.collides_with_point(x, y):
            if self.value:
                self.color = tk.palette.yellow
            else:
                self.color = tk.palette.red


class Skip(tk.CheckBox):
    def __init__(self):
        super().__init__(300, 275, 50, color=tk.palette.light_peach)

    def draw(self):
        tk.draw_rect(260, self.y, 160, 70)
        tk.draw_text(230, self.y, lang.skip[self.window.lang])
        super().draw()

    def click(self, x, y):
        super().click(x, y)
        if self.collides_with_point(x, y):
            if self.value:
                self.color = tk.palette.yellow
            else:
                self.color = tk.palette.red


class EGrid(tk.Sprite):
    def __init__(self, x, y, size):
        self.gx, self.gy = x, y
        self.name = string.ascii_lowercase[x] + string.digits[y + 1]
        x, y = round(540 + 140 * (x / (size // 2) - 1)), round(180 + 140 * (y / (size // 2) - 1))
        super().__init__(x=x, y=y, hitbox=tk.hitbox_circle(10))
        self.active = False

    def __str__(self):
        return self.name

    def __bool__(self):
        return self.active

    def bind(self):
        tk.draw_circle(self.x, self.y, 10, color=tk.palette.green)

    def draw(self):
        if self.active:
            tk.draw_circle(self.x, self.y, 10, color=tk.palette.light_peach)
        else:
            tk.draw_circle(self.x, self.y, 2, color=tk.palette.black)


class EPoint(tk.Sprite):
    def __init__(self):
        self.mode = True
        self.radius = 20
        super().__init__(x=420, y=420, hitbox=tk.hitbox_circle(self.radius))

    def draw(self):
        if self.mode:
            tk.draw_circle(self.x, self.y, self.radius, color=tk.palette.light_peach)
        else:
            tk.draw_circle(self.x, self.y, self.radius, color=tk.palette.light_grey)


class EConnect(tk.Sprite):
    def __init__(self):
        self.mode = False
        self.width = 80
        self.height = 20
        self.radius = 20
        self.lx = 530
        self.rx = 650
        super().__init__(x=590, y=420, hitbox=tk.hitbox_rect(self.width, self.height))
        [self.hitbox.add((x + self.rx, y + self.y)) for (x, y) in tk.hitbox_circle(self.radius)]
        [self.hitbox.add((x + self.lx, y + self.y)) for (x, y) in tk.hitbox_circle(self.radius)]

    def draw(self):
        if self.mode:
            color = tk.palette.light_peach
        else:
            color = tk.palette.light_grey
        tk.draw_rect(self.x, self.y, self.width, self.height, color=color)
        tk.draw_circle(self.lx, self.y, self.radius, color=color)
        tk.draw_circle(self.rx, self.y, self.radius, color=color)


class EBoard(tk.SpriteList):
    def __init__(self, size: int = None):
        super().__init__()
        if size:
            self.extend([EGrid(x, y, size) for x in range(size) for y in range(size)])

        self.size = size
        self.point = EPoint()
        self.connect = EConnect()
        self.bind = None
        self.mode = None
        self.blocked = tk.SpriteList()
        self._connects = list()

    @property
    def unconnected(self):
        unconnected = 0
        for point in [point for point in self if point.active]:
            connected = False
            for connect in self._connects:
                if point in connect:
                    connected = True
            if not connected:
                unconnected += 1
        return unconnected

    @property
    def points(self):
        return [point.name for point in self if point.active]

    @property
    def connects(self):
        return [p1.name + p2.name for (p1, p2) in self._connects]

    @property
    def mills(self):
        for ind, c1 in enumerate(self._connects):
            for c2 in self._connects[:ind]:
                points = sorted(sorted(list(set(c1 + c2)), key=lambda p: p.gy), key=lambda p: p.gx)
                if len(points) == 3:
                    p1, p2, p3 = points
                    if p3.x - p2.x == p2.x - p1.x and p3.y - p2.y == p2.y - p1.y:
                        return True
        return False

    def _get_blocked(self, p1: 'EGrid', p2: 'EGrid'):
        blocked = list()

        if p1.gx == p2.gx:
            for p3 in self:
                if min(p1.gy, p2.gy) < p3.gy < max(p1.gy, p2.gy) and p3.gx == p1.gx == p2.gx:
                    blocked.append(p3)

        elif p1.gy == p2.gy:
            for p3 in self:
                if min(p1.gx, p2.gx) < p3.gx < max(p1.gx, p2.gx) and p3.gy == p1.gy == p2.gy:
                    blocked.append(p3)

        else:
            for p3 in self:
                if p1.gx == p3.gx or p2.gx == p3.gx or p1.gy == p3.gy or p2.gy == p3.gy:
                    continue
                if min(p1.gy, p2.gy) < p3.gy < max(p1.gy, p2.gy) and min(p1.gx, p2.gx) < p3.gx < max(p1.gx, p2.gx) and \
                        (p1.gx - p3.gx) / (p1.gy - p3.gy) == (p2.gx - p3.gx) / (p2.gy - p3.gy):
                    blocked.append(p3)

        return blocked

    def click(self, x, y):
        if self.point.collides_with_point(x, y):
            self.bind = None
            self.point.mode = True
            self.connect.mode = False
        elif self.connect.collides_with_point(x, y):
            self.bind = None
            self.point.mode = False
            self.connect.mode = True
        else:
            for grid in self:
                if grid.collides_with_point(x, y):
                    if self.point.mode:
                        if grid.active:
                            connects = self._connects.copy()
                            for connect in self._connects:
                                if grid in connect:
                                    [self.blocked.remove(point) for point in self._get_blocked(*connect)]
                                    connects.remove(connect)
                            self._connects = connects.copy()
                            grid.active = False
                        elif grid not in self.blocked:
                            grid.active = True
                    elif self.connect.mode and grid.active:
                        if self.bind is None:
                            self.bind = grid
                        else:
                            if grid == self.bind:
                                self.bind = None
                            else:
                                if (grid, self.bind) in self._connects:
                                    [self.blocked.remove(point) for point in self._get_blocked(grid, self.bind)]
                                    self._connects.remove((grid, self.bind))
                                    self.bind = None
                                else:
                                    for point in self._get_blocked(grid, self.bind):
                                        if point.active:
                                            return
                                    [self.blocked.append(point) for point in self._get_blocked(grid, self.bind)]
                                    self._connects.append((grid, self.bind))
                                    self.bind = None
                    return

    def draw(self):
        tk.draw_rect(540, 180, 340, 340)
        self.point.draw()
        self.connect.draw()

        for p1, p2 in self._connects:
            tk.draw_line(p1.x, p1.y, p2.x, p2.y)

        super().draw()
        self.bind.bind() if self.bind is not None else None


class Save(tk.Button):
    def on_click(self):
        if self.color == tk.palette.light_peach:
            json.dump(json.load(open('data/boards.json')) + [self.window.view.json], open('data/boards.json', 'w'), indent=4)

            self.window.view.templates.on_click()


class Confirm(tk.Button):
    def on_click(self):
        if self.color == tk.palette.yellow:
            from .lobby import Lobby
            self.window.view = Lobby(self.window.view.json, None)


class Return(tk.Button):
    def on_click(self):
        from .templates import Choice
        self.window.view = Choice()


class Editor(tk.View):
    def __init__(self):
        super().__init__()
        self.name = tk.InputField(x=180, y=50, width=320, height=50, text=f'{lang.name[self.window.lang]}: ',
                                  max_length=12, color=tk.palette.light_peach)
        self.size = Size()
        self.badges = tk.InputField(x=180, y=200, width=320, height=50, text=f'{lang.badges[self.window.lang]}: ',
                                    max_length=2, color=tk.palette.light_peach, allowed_chars=string.digits)
        self.unite = Unite()
        self.skip = Skip()

        self.confirm = Confirm(x=260, y=380, width=160, height=50,
                               text=lang.confirm[self.window.lang], color=tk.palette.light_grey)
        self.save = Save(x=100, y=380, width=160, height=50,
                         text=lang.save[self.window.lang], color=tk.palette.light_grey)
        self.templates = Return(x=180, y=440, width=320, height=50,
                                text=lang.ret[self.window.lang], color=tk.palette.red)

        self.board = EBoard()

    def create_new_board(self):
        self.board = EBoard(int(self.size))

    @property
    def json(self):
        return {
            'name': str(self.name),
            'size': int(self.size),
            'points': list(self.board.points),
            'connects': list(self.board.connects),
            'badges': int(self.badges),
            'unite': bool(self.unite),
            'skip': bool(self.skip)
        }

    def _check_for_board(self):
        if self.board.mills and len(self.name) >= 4 and \
                3 <= int(self.badges) <= 2 * len(self.board.points) - self.board.unconnected:
            self.save.color = tk.palette.light_peach
            self.confirm.color = tk.palette.yellow
        else:
            self.save.color = tk.palette.light_grey
            self.confirm.color = tk.palette.light_grey

    def on_key_press(self, key: str):
        if key == 'Escape':
            self.templates.on_click()
        elif key == 'Return':
            self.confirm.on_click()
        elif key == 'Left':
            self.name.move_selector_left()
        elif key == 'Right':
            self.name.move_selector_right()
        elif key == 'BackSpace':
            self.name.remove_char()
            self.badges.remove_char()
        else:
            self.name.add_char(key)
            self.badges.add_char(key)

        self._check_for_board()

    def on_mouse_press(self, x: int, y: int, key):
        self.name.click(x, y)
        if self.size.click(x, y):
            self.create_new_board()
        self.badges.click(x, y)
        self.unite.click(x, y)
        self.skip.click(x, y)
        self.save.click(x, y)
        self.confirm.click(x, y)
        self.templates.click(x, y)
        self.board.click(x, y)

        self._check_for_board()

    def on_draw(self):
        self.name.draw()
        self.size.draw()
        self.badges.draw()
        self.unite.draw()
        self.skip.draw()
        self.save.draw()
        self.confirm.draw()
        self.templates.draw()
        self.board.draw()
