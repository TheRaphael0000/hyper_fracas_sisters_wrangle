import pygame
from pygame.locals import *
from pygame.math import Vector2

from inputs import Inputs

class Player(pygame.sprite.Sprite):
    COLOR = (128, 255, 40)
    SIZE = (30, 30)
    G = 0.5

    def __init__(self, world):
        super().__init__()
        self.world = world

        self.previous_keys = None

        self.surf = pygame.Surface(Player.SIZE)
        self.surf.fill(Player.COLOR)
        self.rect = self.surf.get_rect()

        self.fric = -0.12
        self.mass = 100

        self.max_jumps = 2
        self.jumps = self.max_jumps

        # computed forces
        self.gravity_F = Vector2(0, Player.G * self.mass)

        # contante forces
        self.walk_F = Vector2(100, 0)
        self.jump_F = Vector2(0, -20 * Player.G * self.mass)

        self.pos = Vector2(0, 0)
        self.vel = Vector2(0, 0)
        self.acc = Vector2(0, 0)

        self.respawn()

    def apply_force(self, f):
        """a = f / m"""
        self.acc += f / self.mass

    def reset_forces(self):
        self.acc = Vector2(0, 0)

    def respawn(self):
        self.pos = Vector2((self.world.size[0] // 2, self.world.size[1] // 2))
        self.vel = Vector2(0, 0)
        self.acc = Vector2(0, 0)

    def update(self):
        self.reset_forces()

        size = self.world.size
        inputs = self.world.inputs

        if inputs.press(K_LEFT):
            self.apply_force(-self.walk_F)
        if inputs.press(K_RIGHT):
            self.apply_force(self.walk_F)

        hits = pygame.sprite.spritecollide(self, self.world.platforms(), False)
        if hits and self.vel.y > 0:
            self.pos.y = hits[0].rect.top + 1
            self.vel.y = 0
            self.jumps = self.max_jumps

        if inputs.pressed(K_UP) and self.jumps > 0:
            self.vel.y = -10
            self.jumps -= 1

        # gravity
        self.apply_force(self.gravity_F)

        self.acc.x += self.vel.x * self.fric
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        # respawn
        if self.pos.x < 0 or \
            self.pos.x > size.x or \
            self.pos.y < 0 or \
            self.pos.y > size.y:
            self.respawn()

        self.rect.midbottom = self.pos
