import pygame
from pygame.locals import *
from enum import Enum, auto


class Movements(Enum):
    LEFT = auto()
    RIGHT = auto()
    FALL = auto()
    JUMP = auto()


class Inputs():
    mapping = {
        Movements.LEFT: K_LEFT,
        Movements.RIGHT: K_RIGHT,
        Movements.FALL: K_DOWN,
        Movements.JUMP: K_j,
    }

    def __init__(self):
        self.previous = None
        self.current = pygame.key.get_pressed()

    def update(self):
        self.previous = self.current
        self.current = pygame.key.get_pressed()

    def pressed(self, move):
        key = Inputs.mapping[move]
        return not self.previous[key] and self.current[key]

    def press(self, move):
        key = Inputs.mapping[move]
        return self.current[key]

    def unpressed(self, move):
        key = Inputs.mapping[move]
        return not self.current[key]

    def released(self, move):
        key = Inputs.mapping[move]
        return self.previous[key] and not self.current[key]
