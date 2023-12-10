from link import Link
from node import Node
import pygame
from math import cos, sin


class CarLink(Link):
    maxLength = 2
    minLength = 0.5

    def __init__(self, node1, node2, world):
        super().__init__(node1, node2, world, collisionGroup=3, density=1,
                         KP=100000, KD=10, KI=0, friction=2000, brakePoint=17500, color="#aa0000", radius=0.12,
                         indestructible=False, locked=False, N=25, mu=2)
        self.Speed = 1


class CarNode(Node):
    def __init__(self, pos, world):
        super().__init__(pos, world, collisionGroup=3, collideWithGoups=[0, 2], mass=2,
                         radius=0.32, color="#880000", indestructible=False, locked=False, N=25, mu=2)


class TireNode(Node):
    def __init__(self, pos, world):
        super().__init__(pos, world, collisionGroup=3, collideWithGoups=[0, 2], mass=2,
                         radius=0.5, color="#111111", indestructible=False, locked=False, N=15, mu=1)

    def update(self, dt):
        super().update(dt)
        self.torque += (10 - self.spin) * 0.1
