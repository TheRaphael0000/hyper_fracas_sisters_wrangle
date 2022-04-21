import pygame


class Platform(pygame.sprite.Sprite):
    def __init__(self, width, height, x, y, can_go_though=True):
        super().__init__()
        self.surf = pygame.Surface((width, height))
        self.surf.fill((0, 0, 255))
        self.rect = self.surf.get_rect(center=(x, y))
        self.can_go_though = can_go_though

    def interact(self, player, go_though):
        # allow to go though platforms from below
        if self.can_go_though and player.vel.y < 0:
            return False

        # allow to go though platforms from above if pressed
        if self.can_go_though and go_though:
            return False

        if player.vel.y > 0:
            player.pos.y = self.rect.top + 1
            player.vel.y = 0
            player.jumps = player.max_air_jumps
            return True

        if player.vel.y < 0:
            player.pos.y = self.rect.bottom + player.surf.get_height()
            player.vel.y = 0

        return False

    def draw(self, displaysurface):
        displaysurface.blit(self.surf, self.rect)

class Map(list):
    def __init__(self, world):
        self.world = world


class MapBF(Map):
    def __init__(self, *arg, **args):
        super().__init__(*arg, **args)
        width = self.world.size[0]
        height = self.world.size[1]

        self.extend([
            Platform(width * 0.6, 10, 0.5 * width,  height * 0.6, False),
            Platform(width * 0.15, 3, 0.35 * width,  height * 0.48),
            Platform(width * 0.15, 3, 0.65 * width,  height * 0.48)
        ])


class MapFD(Map):
    def __init__(self, *arg, **args):
        super().__init__(*arg, **args)
        width = self.world.size[0]
        height = self.world.size[1]

        self.extend([
            Platform(width * 0.6, 10, 0.5 * width,  height * 0.65, False),
        ])
