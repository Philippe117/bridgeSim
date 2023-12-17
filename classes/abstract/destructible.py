from abc import ABC, abstractmethod
from classes.abstract.base import Base


class Destructor(ABC):
    def __init__(self):
        self.destructibles = []


class Destructible(ABC, Base):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        world = kwargs.get("world")

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
