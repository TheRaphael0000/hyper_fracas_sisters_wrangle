import pygame
from pygame.locals import *
from pygame.math import Vector2

from inputs import Inputs, Movements


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

        # state
        self.grounded = False

        # physics
        self.fric = -0.12
        self.mass = 100

        # jumps
        self.jumps_air_max = 1
        self.jumps = self.jumps_air_max
        self.jumps_air_strength = -9
        self.jumps_short_strength = -8
        self.jumps_full_strength = -13
        self.jumps_selection_t = 0

        # fast fall
        self.gravity_multiplier = 1
        self.fast_fall_gravity_multiplier = 1.7
        self.fast_fall_y_vel_threshold = 2.5

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
        self.handle_fast_fall()
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
        if inputs.press(Movements.LEFT):
            self.apply_force(-self.walk_F)
        if inputs.press(Movements.RIGHT):
            self.apply_force(self.walk_F)

    def handle_platforms(self):
        inputs = self.world.inputs
        interact_platforms = pygame.sprite.spritecollide(
            self, self.world.platforms(), False)
        self.grounded = False
        for platform in interact_platforms:
            self.grounded |= platform.interact(
                self, inputs.press(Movements.FALL))

    def handle_jumps(self):
        inputs = self.world.inputs
        if inputs.pressed(Movements.JUMP) and self.jumps > 0:
            # grounded jumps
            if self.grounded:
                self.vel.y = self.jumps_full_strength
                self.jumps_selection_t = self.HOP_SELECTION_TIME
            # aerial jumps
            else:
                self.vel.y = self.jumps_air_strength
                # only remove jumps when in aerial, to always allow grounded jumps
                self.jumps -= 1

        # when released early convert the fullhop into a short hop
        if self.jumps_selection_t > 0:
            self.jumps_selection_t -= 1
            if self.jumps_selection_t <= 0 and inputs.unpressed(Movements.JUMP):
                self.vel.y = self.jumps_short_strength

    def handle_fast_fall(self):
        if self.world.inputs.pressed(Movements.FALL) \
                and not self.grounded \
                and abs(self.vel.y) < self.fast_fall_y_vel_threshold:
            self.gravity_multiplier = self.fast_fall_gravity_multiplier
        # stop fast falling when the ground is reached
        if self.grounded:
            self.gravity_multiplier = 1

    def handle_physics(self):
        # gravity
        self.apply_force(self.gravity_F * self.gravity_multiplier)
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
