import pygame


class Platform(pygame.sprite.Sprite):
    def __init__(self, width, height, x, y):
        super().__init__()
        self.surf = pygame.Surface((width, height))
        self.surf.fill((255, 0, 0))
        self.rect = self.surf.get_rect(center=(x, y))


class Map(list):
    def __init__(self, world):
        self.world = world


class MapBF(Map):
    def __init__(self, *arg, **args):
        super().__init__(*arg, **args)
        width = self.world.size[0]
        height = self.world.size[1]

        self.extend([
            Platform(width * 0.75, 3, 0.5 * width,  height * 0.75),
            Platform(width * 0.15, 3, 0.30 * width,  height * 0.65),
            Platform(width * 0.15, 3, 0.70 * width,  height * 0.65)
        ])


class MapFD(Map):
    def __init__(self, *arg, **args):
        super().__init__(*arg, **args)
        width = self.world.size[0]
        height = self.world.size[1]

        self.extend([
            Platform(width * 0.75, 3, 0.5 * width,  height * 0.75),
        ])
