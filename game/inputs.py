import pygame

class Inputs():
    def __init__(self):
        self.previous = None
        self.current = pygame.key.get_pressed()

    def update(self):
        self.previous = self.current
        self.current = pygame.key.get_pressed()

    def pressed(self, k):
        return not self.previous[k] and self.current[k]

    def press(self, k):
        return self.current[k]

    def unpressed(self, k):
        return not self.current[k]

    def released(self, k):
        return self.previous[k] and not self.current[k]
