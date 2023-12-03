# Example file showing a basic pygame "game loop"
import pygame
from node import Node
from world import World
from link import Link
from camera import Camera
from math import cos, sin
from interface import Interface

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True


def config(self, nb=5, h=2):
  node1 = Node(pygame.Vector2(-10, 0), self, 0, [1, 2, 3], 0, 0, physic=False)
  node2 = Node(pygame.Vector2(-10, h), self, 0, [1, 2, 3], 0, 0, physic=False)

  Link(node1, node2, self, 0, 1, 1)
  # truss
  oldNode1 = node1
  oldNode2 = node2
  for i in range(nb * 2 + 1):
    node1 = Node(oldNode1.pos + pygame.Vector2(2, 0 * cos(i / nb * 3.14 / 2)), self, 0, [1, 2, 3], 0, 0)
    node2 = Node(oldNode2.pos + pygame.Vector2(2, -((h - 0.5) / nb) * cos(i / nb * 3.14 / 2)), self, 0, [1, 2, 3], 0, 0)
    Link(node1, oldNode1, self, 0, 1, 1)
    Link(node2, oldNode2, self, 0, 1, 1)
    Link(node1, oldNode2, self, 0, 1, 1)
    Link(node2, oldNode1, self, 0, 1, 1)
    Link(node1, node2, self, 0, 1, 1)
    oldNode1 = node1
    oldNode2 = node2

  oldNode1.physic = False
  oldNode2.physic = False


camera = Camera(pygame.Vector2(1, 1), 50)
world = World(camera, screen, pygame.Vector2(0, 9.81), config)
interface = Interface()

fps = 60
world.start(1 / fps, camera)

while running:

  mousePos = world.camera.screenToPos(pygame.mouse.get_pos(), screen)
  # poll for events
  # pygame.QUIT event means the user clicked X to close your window
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False
    elif event.type == pygame.MOUSEWHEEL:
      # Zoom
      world.camera.zoom *= 1 + event.y * 0.1
      world.camera.pos += (mousePos - world.camera.pos) * (event.y * 0.1)

  interface.update(world)
  world.update(1 / fps)

  screen.fill("#115577")
  world.draw(camera)
  interface.draw(world)

  # flip() the display to put your work on screen
  pygame.display.flip()

  clock.tick(fps)  # limits FPS to 60

pygame.quit()
