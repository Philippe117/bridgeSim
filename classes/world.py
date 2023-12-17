import pygame
from classes.abstract.collidable import Collidor
from classes.abstract.updatable import Updator
from classes.abstract.drawable import Drawer
from classes.abstract.selectable import Selector
from classes.abstract.interactible import Interactor
from classes.abstract.destructible import Destructor
from classes.abstract.linkable import Linker


class World(Updator, Collidor, Drawer, Interactor, Destructor, Linker):
    def __init__(self, gravity=pygame.Vector2(0, 9.81), level=None):
        Updator.__init__(self, 10)
        Drawer.__init__(self, 10)
        Collidor.__init__(self, 10)
        Interactor.__init__(self)
        Destructor.__init__(self)
        Linker.__init__(self)

        self.gravity = gravity
        self.friction = 1000
        self.level = level
        self.level(self)
        self.downLimit = 20

    def start(self, dt, camera):
        # settle physic (Undestructible)
        overcompute = 2
        for i in range(overcompute):
            self.update(dt)

    def draw(self, camera):
        Drawer.draw(self, camera)

    def update(self, dt):
        overcompute = 5
        for i in range(overcompute):
            Updator.update(self, dt/overcompute)
        Collidor.computeCollisions(self, dt/overcompute)
        for destructible in self.destructibles:
            if destructible.pos.y > self.downLimit:
                destructible.delete()


    # Retourne une liste des nodes en ordre de distance
    # return [{"node": node, "dist": dist},..]
    def getNodesInRange(self, pos, range):
        proximities = []
        # for node in self.nodes:
        #     diff = node.pos - pos
        #     dist = (diff.x ** 2 + diff.y ** 2) ** 0.5
        #     if dist < range:
        #         proximities.append({"node": node, "dist": dist})
        # proximities.sort(key=sortProximity)
        return proximities


# Sert pour trier les nodes
def sortProximity(linkable):
    return linkable["dist"]
