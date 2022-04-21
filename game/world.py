from player import Player
from maps import Platform
from inputs import Inputs

class World(list):
    def __init__(self, size):
        self.size = size
        self.inputs = Inputs()

    def players(self):
        return [i for i in self if type(i) == Player]

    def platforms(self):
        return [i for i in self if type(i) == Platform]
