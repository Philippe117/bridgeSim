# Example file showing a basic pygame "game loop"
import pygame
from classes.world import World
from classes.camera import Camera
from classes.interface import Interface
from OpenGL.GL import glClearColor, glOrtho, glClear, GL_COLOR_BUFFER_BIT
from myGL import hexToColor

# pygame setup
pygame.init()

pygame.display.set_caption('Bridging sim')
# Setting a custom icon for the game window
icon = pygame.image.load('ressources/tire.png')
pygame.display.set_icon(icon)

# Définition de la taille de la fenêtre
width, height = 1600, 900
screen = pygame.display.set_mode((width, height), pygame.DOUBLEBUF | pygame.OPENGL)

clock = pygame.time.Clock()
running = True

# Initialisation de OpenGL
glOrtho(0, width, height, 0, -1, 1)


from levels.river import config
world = World(pygame.Vector2(0, -9.81), config)
camera = Camera(world, screen, pygame.Vector2(0, 0), 50)
interface = Interface(camera)

fps = 60
world.start(1 / fps, camera)

backgroundColor = hexToColor("#115577")
glClearColor(backgroundColor[0], backgroundColor[1], backgroundColor[2], 1)
fpsAvg = 0
i = 0
while running:
    i = (i+1)%50

    running = interface.update(world, camera, running)
    world.update(1 / fps)

    # screen.fill("#115577")
    glClear(GL_COLOR_BUFFER_BIT)
    world.draw(camera)
    interface.draw(camera)

    # flip() the display to put your work on screen
    pygame.display.flip()
    clock.tick(fps)  # limits FPS to 60
    fpsAvg += (clock.get_fps()-fpsAvg)*0.01
    if i==0:
        print("Framerate:", fpsAvg)

pygame.quit()
