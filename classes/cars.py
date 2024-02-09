import pygame
from classes.materials.carParts import *
from pygame import Vector2 as Vec
from classes.abstract.updatable import Updatable
from classes.abstract.ressourceHolder import RessourceHolder

class Car(Updatable):
    body = None
    wheels = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs, updateGroup=3)
        pos = kwargs.get("pos")
        world = kwargs.get("world")
        maxSpeed = kwargs.get("maxSpeed")
        torque = kwargs.get("torque")
        size = kwargs.get("size")
        body = kwargs.get("body")
        wheels = kwargs.get("wheels")
        destination = kwargs.get("destination")

        if not body:
            if not Car.body:
                Car.body = loadImage("ressources/carTemplate.png")
            body = Car.body

        if not wheels:
            if not Car.wheels:
                Car.wheels = loadImage("ressources/wheelTemplate.png")
            wheels = Car.wheels

        self.wheel1 = TireNode(pygame.Vector2(pos.x - size.x / 2.2, pos.y + 0.5), world, image=wheels)
        self.wheel2 = TireNode(pygame.Vector2(pos.x + size.x / 2.2, pos.y + 0.5), world, image=wheels)
        self.top1 = CarNode(pygame.Vector2(pos.x - size.x / 2, pos.y + size.y + 0.5), world)
        self.top2 = CarNode(pygame.Vector2(pos.x + size.x / 2, pos.y + size.y + 0.5), world)
        self.chuck1 = CarSuspention(self.wheel1, self.top1, world)
        self.chuck2 = CarSuspention(self.wheel2, self.top2, world)
        self.destination = destination
        CarSuspention(self.wheel1, self.top2, world)
        CarSuspention(self.wheel2, self.top1, world)
        CarSuspention(self.wheel1, self.wheel2, world)
        self.speed = 0


        self.body = CarLink(self.top1, self.top2, world, image=body)
        self.torque = torque
        self.maxSpeed = maxSpeed
        self.targetSpeed = 0

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
        else:
            self.pos = self.body.pos

            targetSpin = -self.speed/self.chuck1.node1.radius
            torque = min(self.torque, max(-self.torque, (targetSpin-self.chuck1.node1.spin)*10000))
            self.chuck1.node1.applyTorqueToLink(self.chuck1, torque)

            targetSpin = -self.speed/self.chuck2.node1.radius
            torque = min(self.torque, max(-self.torque, (targetSpin-self.chuck2.node1.spin)*10000))
            self.chuck2.node1.applyTorqueToLink(self.chuck2, torque)

class Pickup(Car, RessourceHolder):
    body = None
    wheels = None
    def __init__(self, **kwargs):

        if not Pickup.body:
            Pickup.body = loadImage("ressources/pickup.png")
        if not Pickup.wheels:
            Pickup.wheels = loadImage("ressources/tire.png")

        super().__init__(**kwargs, maxSpeed=5, torque=4000, size=Vec(4, 0.8), body=Pickup.body, wheels=Pickup.wheels)


    def update(self, dt):
        super().update(dt)

        if self.destination:
            dist = self.destination.pos.x-self.pos.x
            self.speed = min(self.maxSpeed, max(-self.maxSpeed, dist))

            if abs(dist < 0.1):
                self.pushRessources(self.destination, self.ressources)
                self.body.delete()
                self.chuck1.delete()
                self.chuck2.delete()
                self.wheel1.delete()
                self.wheel2.delete()
                self.top1.delete()
                self.top2.delete()
                self.delete()

