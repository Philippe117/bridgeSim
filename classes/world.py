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
        self.friction = 10000
        self.level = level
        self.level(self)
        self.downLimit = 20

    def start(self, dt, camera):
        # settle physic (Undestructible)
        overcompute = 1
        for i in range(overcompute):
            self.update(dt)

    # def draw(self, camera):
    #     Drawer.draw(self, camera)

    def update(self, dt):
        overcompute = 2
        overcompute2 = 2
        for i in range(overcompute):
            for j in range(overcompute2):
                Updator.update(self, dt/overcompute/overcompute2)
            Collidor.computeCollisions(self, dt/overcompute)
        #Collidor.computeCollisions(self, dt)
        for destructible in self.destructibles:
            if destructible.pos.y > self.downLimit:
                destructible.delete()

    # def draw(self, camera):
    #     super().draw(camera)
    #
    #     # Position initiale du carré
    #     glColor3f(1, 0, 0)
    #     drawSquare(camera.posToScreen(pygame.Vector2(0, 0)), 1*camera.zoom)
    #     glColor3f(1, 1, 0)
    #     drawCircle(camera.posToScreen(pygame.Vector2(2, 0)), 1*camera.zoom, num_segments=6)

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
