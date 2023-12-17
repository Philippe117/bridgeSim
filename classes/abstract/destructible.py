from abc import ABC, abstractmethod
from classes.abstract.base import Base


class Destructor(ABC):
    def __init__(self):
        self.destructibles = []


class Destructible(ABC, Base):
    def __init__(self, world: Destructor, N: float, mu: float, radius: float, pos: object, collisionGroup: int, drawGroup: int, updateGroup: int, collideWith: list = None):
        super().__init__(world, N, mu, radius, pos, collisionGroup, drawGroup, updateGroup, collideWith)
        self.destructibles = world.destructibles
        self.destructibles.append(self)

    @abstractmethod
    def getContactPos(self, pos, radius):
        raise NotImplementedError("Must override getContactPos")

    def delete(self):
        if not self.deleteFlag:
            super().delete()
            if self in self.destructibles:
                self.destructibles.remove(self)
        else:
            raise NotImplementedError("many delete?")
