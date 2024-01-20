from abc import ABC, abstractmethod
from time import time

import pygame

from mymath import newGroups
from classes.abstract.base import Base
import math


class Collidor(ABC):
    def __init__(self, nb=10):
        self.collisionGroups = newGroups(nb)

    def computeCollisions(self, dt):
        for collisionGroup in self.collisionGroups:
            for collidable in collisionGroup:
                collidable.computeCollisions(dt)


class Collidable(ABC, Base):
    restitution = 50000
    friction =1400
    absorbsion = 500


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        world = kwargs.get("world")
        collideWith = kwargs.get("collideWith")
        collisionGroup = kwargs.get("collisionGroup")
        N = kwargs.get("N")
        mu = kwargs.get("mu")
        radius = kwargs.get("radius")
        mass = kwargs.get("mass")
        pos = kwargs.get("mass")
        momentInertia = kwargs.get("momentInertia")

        if collideWith is None:
            collideWith = []
        if not world.collisionGroups:
            world.collisionGroups = newGroups(10)
        self.collisionGroup = world.collisionGroups[collisionGroup]
        self.pos = pos
        self.collisionGroups = world.collisionGroups
        self.collideWith = collideWith
        self.N = N
        self.mu = mu
        self.collisionGroup.append(self)
        self.mass = mass
        self.momentInertia = momentInertia
        self.radius = radius
        self.forces = []

    def computeCollisions(self, dt):
        for collide in self.collideWith:
            for other in self.collisionGroups[collide]:
                pos, force = other.getContactPos(self.pos, self.radius)
                if pos:
                    restitution = min(self.getRestitution(), other.getRestitution())
                    forceSum = force*restitution*Collidable.restitution

                    vel1 = self.getVelAtPoint(pos)
                    vel2 = other.getVelAtPoint(pos)
                    velDiff = vel1 - vel2
                    friction = min(self.mu*self.momentInertia, other.mu*other.momentInertia)

                    forceLength = math.hypot(force.x, force.y)
                    if forceLength > 0:
                        unit = force/forceLength
                        norm = pygame.Vector2(unit.y, -unit.x)

                        velDiffLength = velDiff*norm
                        if abs(velDiffLength) > 10:
                            friction /= 2

                        forceSum -= norm * velDiff * norm * friction * Collidable.friction
                        forceSum -= unit * velDiff * unit * restitution * Collidable.absorbsion

                        now = time()
                        self.addForce(other, pos, forceSum, now+dt)
                        #other.addForce(self, pos, -forceSum, now)

    def addForce(self, other, pos, force, endTime):
        self.forces.append({"force": force, "pos": pos, "endTime": endTime, "other": other})

    # def update(self, dt):
    #     now = time()
    #     super(Collidable, self).update(dt)
    #     for force in self.forces:
    #         self.applyForce(force["pos"], force["force"], dt)
    #         if now > force["endTime"]:
    #             self.forces.remove(force)


    # def update(self, dt):
    #     super(Collidable, self).update(dt)
    #     div = len(self.forces)
    #     if div > 0:
    #         posSum = pygame.Vector2(0, 0)
    #         forceSum = pygame.Vector2(0, 0)
    #         for force in self.forces:
    #             posSum += force["pos"]
    #             forceSum += force["force"]
    #         self.forces = []
    #         posSum /= div
    #         forceSum /= div
    #         self.applyForce(posSum, forceSum, dt)


    def update(self, dt):
        div = len(self.forces)
        if div > 0:
            now = time()
            for force in self.forces:
                if force["other"] != None:
                    self.applyForce(force["pos"], force["force"]/div, dt)
                    force["other"].applyForce(force["pos"], -force["force"]/div, dt)
                    #if now > force["endTime"]:
                    self.forces.remove(force)
        super(Collidable, self).update(dt)


    @abstractmethod
    def getContactPos(self, pos, radius):
        raise NotImplementedError("Must override getContactPos")

    @abstractmethod
    def getVelAtPoint(self, pos):
        raise NotImplementedError("Must override getVelAtPoint")

    @abstractmethod
    def applyForce(self, pos, force, dt):
        raise NotImplementedError("Must override collide")

    @abstractmethod
    def getRestitution(self):
        raise NotImplementedError("Must override getRestitution")

    def delete(self):
        if not self.deleteFlag:
            super().delete()
            if self in self.collisionGroup:
                self.collisionGroup.remove(self)
