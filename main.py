# Example file showing a basic pygame "game loop"
import pygame
from classes.world import World
from classes.materials.wood import WoodLink
from classes.materials.pave import PaveLink, PaveNode
from classes.camera import Camera
from classes.interface import Interface
from classes.materials.ground import GroundNode, GroundLink

# pygame setup
pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
clock = pygame.time.Clock()
running = True


def config(self, nb=5, h=WoodLink.maxLength):
    node1 = GroundNode(pygame.Vector2(-50, 0), self)
    node2 = GroundNode(pygame.Vector2(50, 0), self)
    # GroundNode(pygame.Vector2(-7, 0), self)
    # # GroundNode(pygame.Vector2(-12, -1), self)
    GroundLink(node1, node2, self)
    # GroundNode(pygame.Vector2(-5, 2), self)
    # node3 = GroundNode(pygame.Vector2(-5, 10), self)
    # GroundLink(node2, node3, self)
    #
    # node4 = GroundNode(pygame.Vector2(50, 0), self)
    # node5 = GroundNode(pygame.Vector2(5, 0), self)
    # GroundNode(pygame.Vector2(7, 0), self)
    # GroundLink(node4, node5, self)
    # GroundNode(pygame.Vector2(5, 2), self)
    # node6 = GroundNode(pygame.Vector2(5, 10), self)
    # GroundLink(node5, node6, self)

    # Garage(pygame.Vector2(-18, -0.5), self)


    nodeA = PaveNode(pygame.Vector2(-50, -0.5), self)
    nodeA.age = 0
    for i in range(50):
        nodeB = PaveNode(nodeA.pos+pygame.Vector2(2, 0), self)
        nodeB.age = 0
        PaveLink(nodeA, nodeB, self)
        nodeA = nodeB



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
