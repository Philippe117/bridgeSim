import pygame
from classes.materials.carParts import *
from pygame import Vector2 as Vec
from classes.abstract.updatable import Updatable

class Car(Updatable):
    def __init__(self, pose, world, speed=4, torque=4200, size=Vec(4, 0.8), body="ressources/carTemplate.png", wheels="ressources/wheelTemplate.png"):
        super().__init__(world=world, updateGroup=3)

        self.wheel1 = TireNode(pygame.Vector2(pose.x - size.x / 2.2, pose.y - 0.5), world, path=wheels)
        self.wheel2 = TireNode(pygame.Vector2(pose.x + size.x / 2.2, pose.y - 0.5), world, path=wheels)
        self.top1 = CarNode(pygame.Vector2(pose.x - size.x / 2, pose.y - size.y - 0.5), world)
        self.top2 = CarNode(pygame.Vector2(pose.x + size.x / 2, pose.y - size.y - 0.5), world)
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

        force = -(self.speed/self.chuck1.node1.radius-self.chuck1.node1.spin)*(self.torque/self.chuck1.length)*self.chuck1.norm
        self.chuck1.node1.applyForce(self.chuck1.node2.pos, force, dt)
        self.chuck1.node2.applyForce(self.chuck1.node2.pos, -force, dt)

        force = -(self.speed/self.chuck2.node2.radius-self.chuck2.node1.spin)*(self.torque/self.chuck2.length)*self.chuck2.norm
        self.chuck2.node1.applyForce(self.chuck2.node2.pos, force, dt)
        self.chuck2.node2.applyForce(self.chuck2.node2.pos, -force, dt)

class Pickup(Car):
    def __init__(self, pose, size, world):
        super().__init__(pose, Vec(4, 0.8), world, body="ressources/pickup.png", wheels="ressources/tire.png")

