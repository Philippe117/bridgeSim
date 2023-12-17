from abc import ABC, abstractmethod
from classes.abstract.base import Base


class Interactor(ABC, Base):
    def __init__(self):
        self.interactibles = []

    def getInteractibles(self, pos):
        hovereds = []
        for interactible in self.interactibles:
            pos2, force = interactible.getContactPos(pos, 0.01)
            if pos2:
                hovereds.append(interactible)
        return hovereds


class Interactible(ABC, Base):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        world = kwargs.get("world")

        self.interactibles = world.interactibles
        self.interactibles.append(self)

    @abstractmethod
    def getContactPos(self, pos, radius):
        raise NotImplementedError("Must override getContactPos")

    @abstractmethod
    def sclollAction(self, scroll):
        raise NotImplementedError("Must override scrollWheel")

    def delete(self):
        if not self.deleteFlag:
            super().delete()
            if self in self.interactibles:
                self.interactibles.remove(self)
