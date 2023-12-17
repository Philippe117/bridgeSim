from abc import ABC, abstractmethod
from classes.abstract.base import Base


class Selector(ABC, Base):
    def __init__(self):
        self.selectables = []

    def getHovered(self, pos, maxDist=10):
        minDist = maxDist
        hovered = None
        for selectable in self.selectables:
            dist = selectable.getDistance(pos, maxDist)
            if dist < minDist:
                hovered = selectable
                minDist = dist
        return hovered


class Selectable(ABC, Base):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        world = kwargs.get("world")

        self.selectables = world.selectables
        self.selectables.append(self)

    @abstractmethod
    def getDistance(self, pos, maxDist=10):
        raise NotImplementedError("Must override getDistance")

    def delete(self):
        super().delete()
        if self in self.selectables:
            self.selectables.remove(self)

