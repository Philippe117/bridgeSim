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
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        world = kwargs.get("world")

        updateGroup = kwargs.get("updateGroup")
        self.updateGroup = world.updateGroups[updateGroup]
        self.updateGroup.append(self)

    def update(self, dt):
        super(Updatable, self).update(dt)

    def delete(self):
        super().delete()
        if self in self.updateGroup:
            self.updateGroup.remove(self)
