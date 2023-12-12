from link import Link
from node import Node
import pygame
from math import cos, sin




class Car:
    def __init__(self, pose, size, world):

        self.wheel1 = TireNode(pygame.Vector2(pose.x-size.x/2, pose.y), world)
        self.wheel2 = TireNode(pygame.Vector2(pose.x+size.x/2, pose.y), world)
        self.top1 = CarNode(pygame.Vector2(pose.x-size.x/2, pose.y-size.y), world)
        self.top2 = CarNode(pygame.Vector2(pose.x+size.x/2, pose.y-size.y), world)
        CarLink(self.wheel1, self.wheel2, world)
        CarLink(self.top1, self.top2, world)
        CarLink(self.wheel1, self.top1, world)
        CarLink(self.wheel2, self.top2, world)
        CarLink(self.wheel1, self.top2, world)
        CarLink(self.wheel2, self.top1, world)






class CarLink(Link):
    maxLength = 2
    minLength = 0.5

    def __init__(self, node1, node2, world):
        super().__init__(node1, node2, world, collisionGroup=3, density=1,
                         KP=20000, KD=500, KI=0, friction=1000, brakePoint=17500, color="#aa0000", radius=0.2,
                         indestructible=False, locked=False, N=25, mu=2, drawingGroup=2)
        self.Speed = 1


class CarNode(Node):
    def __init__(self, pos, world):
        super().__init__(pos, world, collisionGroup=3, collideWithGoups=[0, 2], mass=2,
                         radius=0.2, color="#880000", indestructible=False, locked=False, N=25, mu=2, startDelay=0, drawingGroup=3)


class TireNode(Node):
    def __init__(self, pos, world):
        super().__init__(pos, world, collisionGroup=3, collideWithGoups=[0, 2], mass=2,
                         radius=0.5, color="#111111", indestructible=False, locked=False, N=15, mu=1, startDelay=0, drawingGroup=4)

    def update(self, dt):
        super().update(dt)
        self.torque += (10 - self.spin) * 0.1
