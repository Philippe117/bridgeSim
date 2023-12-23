from classes.abstract.link import Link
from classes.abstract.node import Node
import pygame
from math import cos, sin
from classes.abstract.destructible import Destructible


class Car:
    def __init__(self, pose, size, world):
        self.wheel1 = TireNode(pygame.Vector2(pose.x - size.x / 2, pose.y - 0.5), world)
        self.wheel2 = TireNode(pygame.Vector2(pose.x + size.x / 2, pose.y - 0.5), world)
        self.top1 = CarNode(pygame.Vector2(pose.x - size.x / 2, pose.y - size.y - 0.5), world)
        self.top2 = CarNode(pygame.Vector2(pose.x + size.x / 2, pose.y - size.y - 0.5), world)
        CarLink(self.wheel1, self.wheel2, world)
        CarLink(self.top1, self.top2, world)
        CarLink(self.wheel1, self.top1, world)
        CarLink(self.wheel2, self.top2, world)
        CarLink(self.wheel1, self.top2, world)
        CarLink(self.wheel2, self.top1, world)

        pos = (self.wheel1.pos + self.wheel2.pos) / 2


class CarLink(Link, Destructible):
    maxLength = 2
    minLength = 0.5

    def __init__(self, node1, node2, world):
        super().__init__(node1, node2, world, collisionGroup=3, density=6000,
                         KP=20000, KD=150, KI=0, friction=1, brakePoint=200000, color="#aa0000", radius=0.2,
                         N=1, mu=1, drawGroup=2)

        self.Speed = 1

    def delete(self):
        super().delete()

class CarNode(Node, Destructible):
    def __init__(self, pos, world):
        super().__init__(pos=pos, world=world, collisionGroup=3, collideWith=[0, 2], density=6000,
                         radius=0.2, color="#880000", locked=False, N=1, mu=1, startDelay=0, drawGroup=3)


class TireNode(Node, Destructible):
    def __init__(self, pos, world):
        super().__init__(pos=pos, world=world, collisionGroup=3, collideWith=[0, 2], density=1200,
                      radius=0.5, color="#111111", locked=False, N=0.1, mu=0.9, startDelay=0, drawGroup=4)

    def update(self, dt):
        super().update(dt)
        self.torque += (80 - self.spin) * 40

    def draw(self, camera):
        super().draw(camera)

        pos = camera.posToScreen(self.pos)

        # Dessine le node
        pygame.draw.circle(camera.screen, "#444444", pos, self.radius * camera.zoom * 0.7)
        pygame.draw.circle(camera.screen, "#000000", pos, self.radius * camera.zoom * 0.7, 2)
        X1 = pygame.Vector2(self.radius * cos(self.angle), self.radius * sin(self.angle)) * camera.zoom
        X2 = pygame.Vector2(X1.y, -X1.x)
        pygame.draw.line(camera.screen, "#000000", pos - X1, pos + X1)
        pygame.draw.line(camera.screen, "#000000", pos - X2, pos + X2)

