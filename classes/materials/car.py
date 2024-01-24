from classes.abstract.link import Link
from classes.abstract.node import Node
import pygame
from math import cos, sin, atan2
from classes.abstract.destructible import Destructible
from classes.abstract.drawable import Drawable
from classes.abstract.updatable import Updatable
from myGL import loadImage, drawImage
from OpenGL.GL import *


class Car:
    def __init__(self, pose, size, world):
        self.wheel1 = TireNode(pygame.Vector2(pose.x - size.x / 2.2, pose.y - 0.5), world)
        self.wheel2 = TireNode(pygame.Vector2(pose.x + size.x / 2.2, pose.y - 0.5), world)
        self.top1 = CarNode(pygame.Vector2(pose.x - size.x / 2, pose.y - size.y - 0.5), world)
        self.top2 = CarNode(pygame.Vector2(pose.x + size.x / 2, pose.y - size.y - 0.5), world)
        CarSuspention(self.wheel1, self.top1, world)
        CarSuspention(self.wheel2, self.top2, world)
        CarSuspention(self.wheel1, self.top2, world)
        CarSuspention(self.wheel2, self.top1, world)
        CarSuspention(self.wheel1, self.wheel2, world)
        CarLink(self.top1, self.top2, world)

        self.pos = (self.top1.pos + self.top2.pos) / 2


class CarLink(Link, Destructible):
    maxLength = 2
    minLength = 0.5
    pickupImage = None

    def __init__(self, node1, node2, world):
        super().__init__(node1, node2, world, collisionGroup=-1, density=6000,
                         KP=0.1, KD=0.1, friction=1, brakePoint=1, color="#aa0000", radius=0.3,
                         N=1, mu=1, drawGroup=2, thickness=0.5)

        if not CarLink.pickupImage:
            CarLink.pickupImage = loadImage("ressources/pickup.png")


    def draw(self, camera):
        # super().draw(camera)

        angle = atan2(self.diff.y, self.diff.x)
        pos = camera.posToScreen(self.pos)

        glColor3f(1, 1, 1)  # Couleur blanche (la texture fournit la couleur)
        drawImage(CarLink.pickupImage, pos, pygame.Vector2(self.length * camera.zoom * 1.4, 2 * camera.zoom), angle)


class CarSuspention(Link, Destructible):
    maxLength = 1
    minLength = 0.5
    def __init__(self, node1, node2, world):
        super().__init__(node1, node2, world, collisionGroup=-1, density=6000,
                         KP=0.004, KD=0.01, friction=1, brakePoint=1, color="#666666", radius=0.1,
                         N=1, mu=1, drawGroup=1, thickness=0.5)


class CarNode(Node, Destructible):
    def __init__(self, pos, world):
        super().__init__(pos=pos, world=world, collisionGroup=3, collideWith=[], density=6000,
                         radius=0.3, color="#880000", locked=False, N=1, mu=1, startDelay=0, drawGroup=-1, thickness=0.3)


class TireNode(Node, Destructible):
    tireImage = None
    def __init__(self, pos, world):
        super().__init__(pos=pos, world=world, collisionGroup=3, collideWith=[0, 2], density=500,
                      radius=0.5, color="#111111", locked=False, N=0.5, mu=1, startDelay=0, drawGroup=2, thickness=0.5)

        if not TireNode.tireImage:
            TireNode.tireImage = loadImage("ressources/tire.png")

    def update(self, dt):
        super().update(dt)
        self.torque += (3 - self.spin) * 2200

    def draw(self, camera):
        super().draw(camera)
        glColor3f(1, 1, 1)  # Couleur blanche (la texture fournit la couleur)
        drawImage(TireNode.tireImage, camera.posToScreen(self.pos), pygame.Vector2(self.radius, self.radius)*2*camera.zoom, self.angle)


