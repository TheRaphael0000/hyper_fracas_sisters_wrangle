import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

from maps import MapFD, MapBF
from world import World
from player import Player
import sys
from pygame.math import Vector2
from pygame.locals import *
import pygame

pygame.init()

SIZE = Vector2(1280, 720)

FPS = 60

BG_color = (20, 20, 20)

FramePerSec = pygame.time.Clock()

displaysurface = pygame.display.set_mode(SIZE)
pygame.display.set_caption("Game")

world = World(SIZE)
world.extend(MapBF(world))
world.append(Player(world))

all_sprites = pygame.sprite.Group()
for entry in world:
    all_sprites.add(entry)

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    world.inputs.update()

    for player in world.players():
        player.update()

    displaysurface.fill(BG_color)

    for entity in world:
        entity.draw(displaysurface)

    pygame.display.update()
    FramePerSec.tick(FPS)
