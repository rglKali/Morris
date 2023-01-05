from threading import Thread

from ..pytk import run

__all__ = [
    'thrun'     # Still in development
]


def thrun():
    t = Thread(target=run)
    t.start()
