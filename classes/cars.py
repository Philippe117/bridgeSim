import pygame
from classes.materials.carParts import *
from pygame import Vector2 as Vec
from classes.abstract.updatable import Updatable

class Car(Updatable):
    def __init__(self, pose, world, speed=4, torque=2000, size=Vec(3.5, 1), body="ressources/carTemplate.png", wheels="ressources/wheelTemplate.png"):
        super().__init__(world=world, updateGroup=3)

        self.wheel1 = TireNode(pygame.Vector2(pose.x - size.x / 2.2, pose.y + 0.5), world, path=wheels)
        self.wheel2 = TireNode(pygame.Vector2(pose.x + size.x / 2.2, pose.y + 0.5), world, path=wheels)
        self.top1 = CarNode(pygame.Vector2(pose.x - size.x / 2, pose.y + size.y + 0.5), world)
        self.top2 = CarNode(pygame.Vector2(pose.x + size.x / 2, pose.y + size.y + 0.5), world)
        self.chuck1 = CarSuspention(self.wheel1, self.top1, world)
        self.chuck2 = CarSuspention(self.wheel2, self.top2, world)
        CarSuspention(self.wheel1, self.top2, world)
        CarSuspention(self.wheel2, self.top1, world)
        CarSuspention(self.wheel1, self.wheel2, world)
        self.body = CarLink(self.top1, self.top2, world, path=body)
        self.torque = torque
        self.speed = speed

        self.pos = (self.top1.pos + self.top2.pos) / 2
    def update(self, dt):
        super().update(dt)
        if (self.body.deleteFlag or
            self.chuck1.deleteFlag or
            self.chuck2.deleteFlag or
            self.wheel1.deleteFlag or
            self.wheel2.deleteFlag or
            self.top1.deleteFlag or
            self.top2.deleteFlag):
            self.delete()

        targetSpin = -self.speed/self.chuck1.node1.radius
        torque = (targetSpin-self.chuck1.node1.spin)*self.torque
        self.chuck1.node1.applyTorqueToLink(self.chuck1, torque)

        targetSpin = -self.speed/self.chuck2.node1.radius
        torque = (targetSpin-self.chuck2.node1.spin)*self.torque
        self.chuck2.node1.applyTorqueToLink(self.chuck2, torque)

class Pickup(Car):
    def __init__(self, pose, world):
        super().__init__(pose, world, 3, 2000, Vec(4, 0.8), body="ressources/pickup.png", wheels="ressources/tire.png")

