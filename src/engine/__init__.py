from .objects import Board, Point
import random as rd
import json
import time


class TooMuchPlayers(Exception):
    pass


class Player:
    def __init__(self, turn: int):
        self.turn = turn
        self.key = ''.join([rd.choice('0123456789ABCDEF') for i in range(8)])
        self.game_time = None
        self.move_time = None

    @property
    def token(self):
        return self.key


class Engine:
    def __init__(self):
        self.players = list()
        self.turn = 0
        self.objects = None

    def new_board(self, data: dict):
        pass

    def _get_mills(self, connects: list):
        pass

    def new_player(self):
        if len(self.players) > 2:
            raise TooMuchPlayers
        else:
            self.players.append(Player(len(self.players) + 1))
            return self.players[-1].token

    def get_current_status(self):
        return (-1, 1)
