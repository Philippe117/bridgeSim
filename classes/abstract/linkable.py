from abc import ABC, abstractmethod
from classes.abstract.base import Base


class Linker(ABC, Base):
    def __init__(self):
        self.linkables = []

    def getLinkables(self, pos, maxDist=10):
        proximities = []
        for linkable in self.linkables:
            dist = linkable.getDistance(pos, maxDist)
            if dist and dist < maxDist:
                proximities.append({"node": linkable, "dist": dist})
        proximities.sort(key=sortProximity)
        return proximities

# Sert pour trier les elements
def sortProximity(proximities):
    return proximities["dist"]

class Linkable(ABC, Base):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        world = kwargs.get("world")

        self.linkables = world.linkables
        self.linkables.append(self)

    @abstractmethod
    def getDistance(self, pos, maxDist=10):
        raise NotImplementedError("Must override getDistance")

    def delete(self):
        if not self.deleteFlag:
            super().delete()
            if self in self.linkables:
                self.linkables.remove(self)
