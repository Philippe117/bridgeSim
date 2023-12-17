from abc import ABC, abstractmethod
from classes.abstract.base import Base


class Interactor(ABC, Base):
    def __init__(self):
        self.interactibles = []

    def interact(self, pos, maxDist=10):
        minDist = maxDist
        hovered = None
        for interactible in self.interactibles:
            dist = interactible.getDistance(pos, maxDist)
            if dist < minDist:
                hovered = interactible
                minDist = dist
        return hovered


class Interactible(ABC, Base):
    def __init__(self, world:Interactor, N: float, mu: float, radius: float, pos: object, collisionGroup: int, drawGroup: int, updateGroup: int, collideWith: list = None):
        super().__init__(world, N, mu, radius, pos, collisionGroup, drawGroup, updateGroup, collideWith)
        self.interactibles = world.interactibles
        self.interactibles.append(self)

    @abstractmethod
    def getContactPos(self, pos, radius):
        raise NotImplementedError("Must override getContactPos")

    def delete(self):
        super().delete()
        if self in self.interactibles:
            self.interactibles.remove(self)
