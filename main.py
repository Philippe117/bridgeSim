# Example file showing a basic pygame "game loop"

from world import World
from wood import *
from camera import *
from interface import Interface
from ground import *

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True


def config(self, nb=5, h=WoodLink.maxLength):
    node1 = GroundNode(pygame.Vector2(-20, 0), self)
    node2 = GroundNode(pygame.Vector2(-10, 0), self)
    GroundLink(node1, node2, self)
    node3 = GroundNode(pygame.Vector2(-10, 2), self)
    GroundLink(node2, node3, self)

    node4 = GroundNode(pygame.Vector2(20, 0), self)
    node5 = GroundNode(pygame.Vector2(10, 0), self)
    GroundLink(node4, node5, self)
    node6 = GroundNode(pygame.Vector2(10, 2), self)
    GroundLink(node5, node6, self)


    # node = PaveNode(pygame.Vector2(-20, 0), self)
    # node.physic = False
    # node1 = PaveNode(pygame.Vector2(-10, 0), self)
    # PaveLink(node, node1, self)
    # node2 = WoodNode(pygame.Vector2(-10, h), self)
    # pilar = WoodNode(pygame.Vector2(0, h), self)
    # pilar.physic = False
    # node1.physic = False
    # node2.physic = False
    #
    # WoodLink(node1, node2, self)
    # # truss
    # oldNode1 = node1
    # oldNode2 = node2
    # for i in range(nb * 2 + 1):
    #     node1 = PaveNode(oldNode1.pos + pygame.Vector2(h, 0 * cos(i / nb * 3.14 / 2)), self)
    #     node2 = WoodNode(oldNode2.pos + pygame.Vector2(h, -((h*1) / nb) * cos(i / nb * 3.14 / 2)), self)
    #     PaveLink(node1, oldNode1, self)
    #     WoodLink(node2, oldNode2, self)
    #     WoodLink(node1, oldNode2, self)
    #     #Wood(node2, oldNode1, self)
    #     WoodLink(node1, node2, self)
    #     oldNode1 = node1
    #     oldNode2 = node2
    #
    # oldNode1.physic = False
    # oldNode2.physic = False
    #
    # node = PaveNode(pygame.Vector2(oldNode1.pos.x+10, 0), self)
    # node.physic = False
    # PaveLink(oldNode1, node, self)

    #
    # node1 = PaveNode(pygame.Vector2(-10, 0), self)
    # node2 = PaveNode(pygame.Vector2(10, 0), self)
    # PaveLink(node1, node2, self)
    # node1.physic = False
    # node2.physic = False
    #
    # top1 = TireNode(pygame.Vector2(-9, -1.5), self)
    # top1.physic = False






camera = Camera(pygame.Vector2(1, 1), 50)
world = World(camera, screen, pygame.Vector2(0, 9.81), config)
interface = Interface()

fps = 60
world.start(1 / fps, camera)

while running:


    running = interface.update(world, screen, running)
    world.update(1 / fps)

    screen.fill("#115577")
    world.draw(camera)
    interface.draw(world)

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(fps)  # limits FPS to 60

pygame.quit()
