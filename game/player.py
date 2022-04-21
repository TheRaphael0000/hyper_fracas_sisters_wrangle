import pygame
from pygame.locals import *
from pygame.math import Vector2

from inputs import Inputs


class Player(pygame.sprite.Sprite):
    COLOR = (128, 255, 40)
    SIZE = (30, 30)
    G = 0.5

    HOP_SELECTION_TIME = 4

    def __init__(self, world):
        super().__init__()
        self.world = world

        self.previous_keys = None

        self.surf = pygame.Surface(Player.SIZE)
        self.surf.fill(Player.COLOR)
        self.rect = self.surf.get_rect()

        self.fric = -0.12
        self.mass = 100

        # jumps
        self.max_air_jumps = 1
        self.jumps = self.max_air_jumps
        self.air_jump_strength = -9
        self.short_hop_strength = -8
        self.full_hop_strength = -13
        self.hop_selection_t = 0

        self.grounded = False

        # computed forces
        self.gravity_F = Vector2(0, Player.G * self.mass)

        # contante forces
        self.walk_F = Vector2(100, 0)
        self.jump_F = Vector2(0, -20 * Player.G * self.mass)

        self.pos = Vector2(0, 0)
        self.vel = Vector2(0, 0)
        self.acc = Vector2(0, 0)

        self.respawn()

    def update(self):
        self.reset_forces()
        self.handle_blastzones()
        self.handle_platforms()
        self.handle_movements()
        self.handle_jumps()
        self.handle_physics()

    def apply_force(self, f):
        """a = f / m"""
        self.acc += f / self.mass

    def reset_forces(self):
        self.acc = Vector2(0, 0)

    def respawn(self):
        self.pos = Vector2((self.world.size[0] // 2, self.world.size[1] // 2))
        self.vel = Vector2(0, 0)
        self.acc = Vector2(0, 0)

    def handle_movements(self):
        inputs = self.world.inputs
        if inputs.press(K_LEFT):
            self.apply_force(-self.walk_F)
        if inputs.press(K_RIGHT):
            self.apply_force(self.walk_F)

    def handle_platforms(self):
        inputs = self.world.inputs
        interact_platforms = pygame.sprite.spritecollide(
            self, self.world.platforms(), False)
        self.grounded = False
        for platform in interact_platforms:
            self.grounded |= platform.interact(self, inputs.press(K_DOWN))

    def handle_jumps(self):
        inputs = self.world.inputs
        if inputs.pressed(K_UP) and self.jumps > 0:
            # grounded jumps
            if self.grounded:
                self.vel.y = self.full_hop_strength
                self.hop_selection_t = self.HOP_SELECTION_TIME
            # aerial jumps
            else:
                self.vel.y = self.air_jump_strength
                # only remove jumps when in aerial, to always allow grounded jumps
                self.jumps -= 1

        # when released early convert the fullhop into a short hop
        if self.hop_selection_t > 0:
            self.hop_selection_t -= 1
            if self.hop_selection_t <= 0 and inputs.unpressed(K_UP):
                self.vel.y = self.short_hop_strength

    def handle_physics(self):
        # gravity
        self.apply_force(self.gravity_F)
        self.acc.x += self.vel.x * self.fric
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        self.rect.midbottom = self.pos

    def handle_blastzones(self):
        if self.pos.x < 0 or \
                self.pos.x > self.world.size.x or \
                self.pos.y < 0 or \
                self.pos.y > self.world.size.y:
            self.respawn()

    def draw(self, displaysurface):
        self.surf.fill((255, 0, 255))

        if self.grounded:
            self.surf.fill((255, 255, 0))

        displaysurface.blit(self.surf, self.rect)
