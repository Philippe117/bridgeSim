from classes.materials.wood import WoodLink
from classes.materials.pave import PaveLink, PaveNode
from classes.materials.ground import GroundNode, GroundLink
import pygame
from classes.garage import Garage

def config(self):
    nb = 5
    h = WoodLink.maxLength
    node1 = GroundNode(pygame.Vector2(-50, 0), self)
    node2 = GroundNode(pygame.Vector2(-5, 0), self)
    node3 = GroundNode(pygame.Vector2(-5, 10), self)
    GroundLink(node1, node2, self)
    GroundLink(node2, node3, self)
    GroundNode(pygame.Vector2(-5, 2), self)
    GroundNode(pygame.Vector2(-7, 0), self)

    node1 = GroundNode(pygame.Vector2(50, 0), self)
    node2 = GroundNode(pygame.Vector2(5, 0), self)
    node3 = GroundNode(pygame.Vector2(5, 10), self)
    GroundLink(node1, node2, self)
    GroundLink(node2, node3, self)
    GroundNode(pygame.Vector2(5, 2), self)
    GroundNode(pygame.Vector2(7, 0), self)

    Garage(pygame.Vector2(-18, -0.5), self)


    # nodeA = PaveNode(pygame.Vector2(-50, -0.5), self)
    # nodeA.age = 0
    # for i in range(50):
    #     nodeB = PaveNode(nodeA.pos+pygame.Vector2(2, 0), self)
    #     nodeB.age = 0
    #     PaveLink(nodeA, nodeB, self)
    #     nodeA = nodeB

