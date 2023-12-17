from abc import ABC, abstractmethod
from mymath import newGroups
from classes.abstract.base import Base


class Updator(ABC, Base):
    def __init__(self, nb=10):
        self.updateGroups = newGroups(nb)

    def update(self, dt):
        for updateGroup in self.updateGroups:
            for updatable in updateGroup:
                updatable.update(dt)


class Updatable(ABC, Base):
    def __init__(self, world: Updator, N: float, mu: float, radius: float, pos: object, collisionGroup: int, drawGroup: int, updateGroup: int, collideWith: list = None):
        super().__init__(world, N, mu, radius, pos, collisionGroup, drawGroup, updateGroup, collideWith)
        self.updateGroup = world.updateGroups[updateGroup]
        self.updateGroup.append(self)

    @abstractmethod
    def update(self, dt):
        raise NotImplementedError("Must override update")

    def delete(self):
        super().delete()
        if self in self.updateGroup:
            self.updateGroup.remove(self)
