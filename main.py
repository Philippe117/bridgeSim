# Example file showing a basic pygame "game loop"
import pygame
from classes.world import World
from classes.camera import Camera
from classes.interface import Interface
from levels.river import config

# pygame setup
pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
clock = pygame.time.Clock()
running = True




camera = Camera(screen, pygame.Vector2(1, 1), 50)
world = World(pygame.Vector2(0, 9.81), config)
interface = Interface(camera)

fps = 60
world.start(1 / fps, camera)

while running:


    running = interface.update(world, camera, running)
    world.update(1 / fps)

    screen.fill("#115577")
    world.draw(camera)
    interface.draw(camera)

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(fps)  # limits FPS to 60

pygame.quit()
