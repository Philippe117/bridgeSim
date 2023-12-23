from abc import ABC, abstractmethod

import pygame

from mymath import newGroups
from classes.abstract.base import Base


class Collidor(ABC):
    def __init__(self, nb=10):
        self.collisionGroups = newGroups(nb)

    def computeCollisions(self, dt):
        for collisionGroup in self.collisionGroups:
            for collidable in collisionGroup:
                collidable.computeCollisions(dt)


class Collidable(ABC, Base):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        world = kwargs.get("world")
        collideWith = kwargs.get("collideWith")
        collisionGroup = kwargs.get("collisionGroup")
        N = kwargs.get("N")
        mu = kwargs.get("mu")
        radius = kwargs.get("radius")
        mass = kwargs.get("mass")
        momentInertia = kwargs.get("momentInertia")

        if collideWith is None:
            collideWith = []
        if not world.collisionGroups:
            world.collisionGroups = newGroups(10)
        self.collisionGroup = world.collisionGroups[collisionGroup]
        self.collisionGroups = world.collisionGroups
        self.collideWith = collideWith
        self.N = N
        self.mu = mu
        self.collisionGroup.append(self)
        self.mass = mass
        self.momentInertia = momentInertia
        self.radius = radius

    def computeCollisions(self, dt):
        for collide in self.collideWith:
            for other in self.collisionGroups[collide]:
                pos, force = other.getContactPos(self.pos, self.radius)
                if pos:
                    restitution = min(self.N*self.mass, other.N*other.mass)
                    forceSum = force*restitution*10000

                    vel1 = self.getVelAtPoint(pos)
                    vel2 = other.getVelAtPoint(pos)
                    velDiff = vel1 - vel2
                    friction = min(self.mu*self.momentInertia, other.mu*other.momentInertia)

                    forceLength = (force.x ** 2 + force.y ** 2) ** 0.5
                    unit = force/forceLength
                    norm = pygame.Vector2(unit.y, -unit.x)

                    velDiffLength = velDiff*norm
                    if abs(velDiffLength) > 1:
                        friction /= 2

                    forceSum -= norm * velDiff * norm * friction * 2000
                    forceSum -= unit * velDiff * unit * restitution * 100

                    self.applyForce(pos, forceSum, dt)
                    other.applyForce(pos, -forceSum, dt)

    @abstractmethod
    def getContactPos(self, pos, radius):
        raise NotImplementedError("Must override getContactPos")

    @abstractmethod
    def getVelAtPoint(self, pos):
        raise NotImplementedError("Must override getVelAtPoint")

    @abstractmethod
    def applyForce(self, pos, force, dt):
        raise NotImplementedError("Must override collide")

    def delete(self):
        if not self.deleteFlag:
            super().delete()
            if self in self.collisionGroup:
                self.collisionGroup.remove(self)
