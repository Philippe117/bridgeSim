from abc import ABC, abstractmethod
from classes.abstract.base import Base


class Destructor(ABC):
    def __init__(self):
        self.destructibles = []


class Destructible(ABC, Base):
    def __init__(self, world: Destructor, N: float, mu: float, radius: float, pos: object, collisionGroup: int, drawGroup: int, updateGroup: int, collideWith: list = None):
        super().__init__(world, N, mu, radius, pos, collisionGroup, drawGroup, updateGroup, collideWith)
        self.destructible = world.destructibles
        self.destructible.append(self)
        self.deleteFlag = False

    @abstractmethod
    def getContactPos(self, pos, radius):
        raise NotImplementedError("Must override getContactPos")

    def delete(self):
        super().delete()
        if not self.deleteFlag and self in self.destructible:
            self.destructible.remove(self)
        self.deleteFlag = True