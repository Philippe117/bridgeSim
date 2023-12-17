from abc import ABC, abstractmethod
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
    def __init__(self, world: Collidor, N: float, mu: float, radius: float, pos: object, collisionGroup: int, drawGroup: int, updateGroup: int, collideWith: list = None):
        super().__init__(world, N, mu, radius, pos, collisionGroup, drawGroup, updateGroup, collideWith)
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
        self.radius = radius

    def computeCollisions(self, dt):
        for collide in self.collideWith:
            for other in self.collisionGroups[collide]:
                pos, force = other.getContactPos(self.pos, self.radius)
                if pos:
                    vel1 = self.getVelAtPoint(pos)
                    vel2 = other.getVelAtPoint(pos)
                    velDiff = vel1 - vel2
                    friction = self.mu * other.mu
                    restitution = force * self.N * other.N
                    self.collide(pos, restitution, velDiff, friction, dt)
                    other.collide(pos, -restitution, -velDiff, friction, dt)

    @abstractmethod
    def getContactPos(self, pos, radius):
        raise NotImplementedError("Must override getContactPos")

    @abstractmethod
    def getVelAtPoint(self, pos):
        raise NotImplementedError("Must override getVelAtPoint")

    @abstractmethod
    def collide(self, pos, force, vel, friction, dt):
        raise NotImplementedError("Must override collide")

    def delete(self):
        if not self.deleteFlag:
            super().delete()
            if self in self.collisionGroup:
                self.collisionGroup.remove(self)
