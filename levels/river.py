from classes.materials.wood import WoodLink, WoodNode
from classes.materials.pave import PaveLink, PaveNode
from classes.materials.ground import GroundNode, GroundLink
import pygame
from classes.garage import Garage

def config(self):
    nb = 5
    h = WoodLink.maxLength
    node1 = GroundNode(pygame.Vector2(-50, 0), self)
    node2 = GroundNode(pygame.Vector2(-6, 0), self)
    node3 = GroundNode(pygame.Vector2(-6, -10), self)
    GroundLink(node1, node2, self)
    GroundLink(node2, node3, self)
    GroundNode(pygame.Vector2(-6, -2), self)
    GroundNode(pygame.Vector2(-8, 0), self)

    node4 = GroundNode(pygame.Vector2(50, 0), self)
    node5 = GroundNode(pygame.Vector2(6, 0), self)
    node6 = GroundNode(pygame.Vector2(6, -10), self)
    GroundLink(node4, node5, self)
    GroundLink(node5, node6, self)
    GroundNode(pygame.Vector2(6, -2), self)
    GroundNode(pygame.Vector2(8, 0), self)

    Garage(pygame.Vector2(-18, 0.5), self)


    nodeA, nodeB = node2, PaveNode(pygame.Vector2(-3, 0), self)
    nodeC = WoodNode(pygame.Vector2(-4, 2), self)
    WoodLink(nodeA, nodeC, self)
    WoodLink(nodeB, nodeC, self)
    PaveLink(nodeA, nodeB, self)

    nodeA, nodeC = nodeB, nodeC
    nodeB = PaveNode(pygame.Vector2(-1, 0), self)
    nodeD = WoodNode(pygame.Vector2(-2, 2), self)
    WoodLink(nodeC, nodeD, self)
    WoodLink(nodeA, nodeD, self)
    WoodLink(nodeB, nodeD, self)
    PaveLink(nodeA, nodeB, self)

    nodeA, nodeC = nodeB, nodeD
    nodeB = PaveNode(pygame.Vector2(1, 0), self)
    nodeD = WoodNode(pygame.Vector2(0, 2), self)
    WoodLink(nodeC, nodeD, self)
    WoodLink(nodeA, nodeD, self)
    WoodLink(nodeB, nodeD, self)
    PaveLink(nodeA, nodeB, self)

    nodeA, nodeC = nodeB, nodeD
    nodeB = PaveNode(pygame.Vector2(3, 0), self)
    nodeD = WoodNode(pygame.Vector2(2, 2), self)
    WoodLink(nodeC, nodeD, self)
    WoodLink(nodeA, nodeD, self)
    WoodLink(nodeB, nodeD, self)
    PaveLink(nodeA, nodeB, self)

    nodeA, nodeC = nodeB, nodeD
    nodeB = node5
    nodeD = WoodNode(pygame.Vector2(4, 2), self)
    WoodLink(nodeC, nodeD, self)
    WoodLink(nodeA, nodeD, self)
    WoodLink(nodeB, nodeD, self)
    PaveLink(nodeA, nodeB, self)

