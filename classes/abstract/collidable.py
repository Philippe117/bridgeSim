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
    restitution = 2000
    friction = 2000
    absorbsion = 100

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        world = kwargs.get("world")
        collideWith = kwargs.get("collideWith")
        collisionGroup = kwargs.get("collisionGroup")
        N = kwargs.get("N")
        mu = kwargs.get("mu")
        radius = kwargs.get("radius")
        mass = kwargs.get("mass")
        pos = kwargs.get("pos")
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
        pos_self, radius_self = self.pos, self.radius
        get_restitution_self = self.getRestitution
        get_vel_at_point_self = self.getVelAtPoint
        mu_self, moment_inertia_self = self.mu, self.momentInertia

        for collide in self.collideWith:
            for other in self.collisionGroups[collide]:
                get_restitution_other = other.getRestitution
                get_vel_at_point_other = other.getVelAtPoint
                mu_other, moment_inertia_other = other.mu, other.momentInertia

                pos, force = other.getContactPos(pos_self, radius_self)
                if pos:
                    restitution = min(get_restitution_self(), get_restitution_other())
                    force_sum = force * restitution * Collidable.restitution

                    vel1 = get_vel_at_point_self(pos)
                    vel2 = get_vel_at_point_other(pos)
                    vel_diff = vel1 - vel2
                    friction = min(mu_self * moment_inertia_self, mu_other * moment_inertia_other)

                    force_length = force.length()
                    if force_length > 0:
                        unit = force / force_length
                        norm = pygame.Vector2(unit.y, -unit.x)

                        vel_diff_length = vel_diff * norm
                        if abs(vel_diff_length) > 10:
                            friction /= 2

                        friction_force = norm * (vel_diff * norm) * (friction * Collidable.friction)
                        restitution_force = unit * (vel_diff * unit) * (restitution * Collidable.absorbsion)

                        force_sum -= friction_force + restitution_force

                        # Utilisation d'une opération vectorielle pour appliquer la force
                        self.applyForce(pos, force_sum, dt)
                        other.applyForce(pos, -force_sum, dt)


    def addForce(self, other, pos, force, endTime):
        self.forces.append({"force": force, "pos": pos, "endTime": endTime, "other": other})

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
