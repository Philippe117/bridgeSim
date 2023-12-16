from link import Link
from node import Node
import pygame
from math import cos, sin


class PaveLink(Link):
    maxLength = 2
    minLength = 0.5

    def __init__(self, node1, node2, world):
        super().__init__(node1, node2, world, collisionGroup=2, density=1,
                         KP=20000, KD=150, KI=0, friction=2, brakePoint=3000, indestructible=False, locked=False,
                         color="#222222", radius=0.2, drawingGroup=5, N=25, mu=1)


class PaveNode(Node):
    def __init__(self, pos, world):
        super().__init__(pos, world, collisionGroup=2, collideWithGroups=[0, 3], mass=2,
                         radius=0.2, color="#333333", indestructible=False, locked=False, drawingGroup=9, N=25, mu=1)

    def update(self, dt):
        super().update(dt)
        self.torque += -self.angle * 0.1 - self.spin * 0.1
