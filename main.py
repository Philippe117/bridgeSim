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


def config(self, nb = 5, h = 3):



    node1 = Node(pygame.Vector2(-10, 0), physic=False)
    node2 = Node(pygame.Vector2(-10, h), physic=False)
    self.nodes.append(node1)
    self.nodes.append(node2)

    self.links.append(Link(node1, node2))
    # truss
    oldNode1 = node1
    oldNode2 = node2
    for i in range(nb*2+1):
        node1 = Node(oldNode1.pos+pygame.Vector2(2, 0*cos(i/nb*3.14/2)))
        node2 = Node(oldNode2.pos+pygame.Vector2(2, -((h-1)/nb)*cos(i/nb*3.14/2)))
        self.nodes.append(node1)
        self.nodes.append(node2)
        self.links.append(Link(node1, oldNode1))
        self.links.append(Link(node2, oldNode2))
        self.links.append(Link(node1, oldNode2))
        self.links.append(Link(node2, oldNode1))
        self.links.append(Link(node1, node2))
        oldNode1 = node1
        oldNode2 = node2

    oldNode1.physic = False
    oldNode2.physic = False


camera = Camera(pygame.Vector2(1, 1), 50)
world = World(camera, pygame.Vector2(0, 9.81), config)
interface = Interface()


fps = 30
world.start()

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

    world.update(1/fps)

    interface.update(world, screen)

    world.draw(screen)

    interface.draw(world, screen)

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(fps)  # limits FPS to 60

pygame.quit()
