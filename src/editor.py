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
        self.available = None

    def bind(self):
        tk.draw_circle(self.x, self.y, 10, color=tk.palette.green)

    def draw(self):
        if self.available is not None:
            if self.available:
                tk.draw_circle(self.x, self.y, 10, color=tk.palette.yellow)
            else:
                tk.draw_circle(self.x, self.y, 10, color=tk.palette.red)

        elif self.active:
            tk.draw_circle(self.x, self.y, 10, color=tk.palette.light_grey)
        else:
            tk.draw_circle(self.x, self.y, 2, color=tk.palette.black)


class EPoint(tk.Sprite):
    def __init__(self):
        self.radius = 20
        super().__init__(x=420, y=420, hitbox=tk.hitbox_circle(self.radius))

    def draw(self):
        if self.window.view.board.mode == 'P':
            tk.draw_circle(self.x, self.y, self.radius, color=tk.palette.light_peach)
        else:
            tk.draw_circle(self.x, self.y, self.radius, color=tk.palette.light_grey)


class EConnect(tk.Sprite):
    def __init__(self):
        self.width = 80
        self.height = 20
        self.radius = 20
        self.lx = 530
        self.rx = 650
        super().__init__(x=590, y=420, hitbox=tk.hitbox_rect(self.width, self.height))
        [self.hitbox.add((x + self.rx, y + self.y)) for (x, y) in tk.hitbox_circle(self.radius)]
        [self.hitbox.add((x + self.lx, y + self.y)) for (x, y) in tk.hitbox_circle(self.radius)]

    def draw(self):
        if self.window.view.board.mode == 'C':
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

        self.point = EPoint()
        self.connect = EConnect()
        self.bind = None
        self.avl = None
        self.mode = None
        self._connects = list()

    @property
    def points(self):
        return [point.name for point in self if point.active]

    @property
    def connects(self):
        return [p1.name + p2.name for (p1, p2) in self._connects]

    def _connect(self, point):
        dx = self.bind.gx - point.gx
        dy = self.bind.gy - point.gy
        return {'point': point, 'angle': dx / dy, 'distance': dx ** 2 + dy ** 2}

    def set_avl(self):
        self.avl = set()
        for point in self:
            if point.active:
                pass

    def click(self, x, y):
        if self.point.collides_with_point(x, y):
            for point in self:
                if point.active:
                    point.available = None
            if self.mode == 'P':
                self.mode = None
                for grid in self:
                    grid.available = None
            else:
                self.bind = None
                self.avl = None
                for grid in self:
                    if grid.active:
                        grid.available = False
                    else:
                        grid.available = True
                self.mode = 'P'
        elif self.connect.collides_with_point(x, y):
            for point in self:
                if point.active:
                    point.available = None

            if self.mode == 'C':
                self.mode = None
                self.bind = None
            else:
                for grid in self:
                    if grid.active:
                        grid.available = True
                    else:
                        grid.available = None
                self.mode = 'C'
        else:
            for grid in self:
                if grid.collides_with_point(x, y):
                    if self.mode == 'P':
                        grid.active = not grid.active
                        grid.available = not grid.available
                    elif self.mode == 'C':
                        if self.bind is None:
                            self.bind = grid
                            self.set_avl()
                            for point in self:
                                if point in self.avl:
                                    point.available = True
                                else:
                                    point.available = False
                        else:
                            if grid in self.avl:
                                self._connects.append([self.bind, grid])
                                self.bind = None
                                self.avl = None
                                for point in self:
                                    if point.active:
                                        point.available = True

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
            w = self.window.view
            board = {
                'name': str(w.name),
                'size': int(w.size),
                'points': list(),
                'connects': list(),
                'badges': int(w.badges),
                'unite': bool(w.unite),
                'skip': bool(w.skip)
            }
            json.dump(json.load(open('data/boards.json')) + board, open('data/boards.json', 'w'), indent=4)


class Confirm(tk.Button):
    def on_click(self):
        if self.color == tk.palette.yellow:
            pass


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

    # def on_update(self, delta_time: float):
    #     cond = True
    #     if cond:
    #         self.save.color = tk.palette.light_peach
    #         self.confirm.color = tk.palette.yellow
    #     else:
    #         self.save.color = tk.palette.light_grey
    #         self.confirm.color = tk.palette.light_grey

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
