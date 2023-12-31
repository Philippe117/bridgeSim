from abc import ABC, abstractmethod
from mymath import newGroups
from classes.abstract.base import Base

class Drawer():
    def __init__(self, nb=10):
        self.drawGroups = newGroups(nb)

    def draw(self, camera):
        for drawGroup in self.drawGroups:
            for drawable in drawGroup:
                drawable.draw(camera)


class Drawable(ABC, Base):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        world = kwargs.get("world")
        drawGroup = kwargs.get("drawGroup")

        self.drawGroup = world.drawGroups[drawGroup]
        self.drawGroup.append(self)

    @abstractmethod
    def draw(self, camera):
        raise NotImplementedError("Must override draw")

    def delete(self):
        super().delete()
        if self in self.drawGroup:
            self.drawGroup.remove(self)
