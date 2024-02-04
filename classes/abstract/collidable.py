from abc import ABC, abstractmethod
from mymath import newGroups
from classes.abstract.base import Base
from pygame import Vector2 as Vec
from myGL import setColorHex, drawDisk, setColorHex, drawLine


class Collidor(ABC):
    def __init__(self, nb=10):
        self.collisionGroups = newGroups(nb)

    def computeCollisions(self, dt):
        for collisionGroup in self.collisionGroups:
            for collidable in collisionGroup:
                collidable.computeCollisions(dt)


class Collidable(ABC, Base):
    restitution = 8000
    friction = 4000
    absorbsion = 200000

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
        if collisionGroup >= 0:
            self.collisionGroup = world.collisionGroups[collisionGroup]
            self.collisionGroup.append(self)
        else:
            self.collisionGroup = None
        self.pos = pos
        self.collisionGroups = world.collisionGroups
        self.collideWith = collideWith
        self.N = N
        self.mu = mu
        self.mass = mass
        self.momentInertia = momentInertia
        self.radius = radius
        self.forces = []

    def computeCollisions(self, dt):
        maxSquish = Vec(0, 0)
        maxPos = 0
        maxlen = 0
        maxOther = None
        for collide in self.collideWith:
            for other in self.collisionGroups[collide]:
                pos, squish = other.getContactPos(self.pos, self.radius)
                if pos and pos != self.pos:
                    lenght = squish.length()
                    if lenght > maxlen:
                        maxlen = lenght
                        maxSquish = squish
                        maxPos = pos
                        maxOther = other

        if maxlen > 0:
            pos, squish, other = maxPos, maxSquish, maxOther

            vel1 = self.getVelAtPoint(pos)
            vel2 = other.getVelAtPoint(pos)
            velDiff = vel2 - vel1
            friction = min(self.mu * self.momentInertia, other.mu * other.momentInertia)
            restitution = min(self.N * self.mass, other.N * other.mass)
            unit = squish.normalize()
            norm = Vec(-unit.y, unit.x)
            slip = velDiff * norm
            if abs(slip) > 10:
                friction /= 2

            frictionForce = norm * slip * (friction * Collidable.friction)
            absorbForce = max(0, unit * velDiff) * unit * (1 * Collidable.absorbsion)
            squishForce = squish * (restitution * Collidable.restitution)

            # applique la friction
            force = frictionForce + absorbForce + squishForce

            torque = force * (pos - self.pos).rotate(90)

            other.applyForceTorque(-force, -torque)
            self.applyForceTorque(force, torque)

    @abstractmethod
    def getContactPos(self, pos, radius) -> (Vec, Vec):
        raise NotImplementedError("Must override getContactPos")

    @abstractmethod
    def getVelAtPoint(self, pos):
        raise NotImplementedError("Must override getVelAtPoint")

    @abstractmethod
    def applyForceTorque(self, force, torque):
        raise NotImplementedError("Must override applyForceTorque")

    def delete(self):
        if not self.deleteFlag:
            super().delete()
            if self.collisionGroup and self in self.collisionGroup:
                self.collisionGroup.remove(self)
