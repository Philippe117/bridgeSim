import pygame
from node import Node
from link import Link
from camera import Camera

class World:
    def __init__(self, camera, gravity=pygame.Vector2(0, 9.81), level=None):
        self.gravity = gravity
        super().__init__()
        self.nodes = []
        self.links = []
        self.level = level
        self.level(self)
        self.camera = camera
        self.friction = 1

    def start(self):
        # settle physic (Undestructible)
        for i in range(2000):
            for node in self.nodes:
                node.update(self, 0.0001)
            for link in self.links:
                link.update(self, 0.0001)

        # Revive les objets
        for node in self.nodes:
            node.deleteFlag = False
        for link in self.links:
            link.deleteFlag = False

    def draw(self, screen):

        screen.fill("#115577")
        for link in self.links:
            link.draw(screen, self.camera)
        for node in self.nodes:
            node.draw(screen, self.camera)

    def update(self, dt):

        # RENDER YOUR GAME HERE
        overcompute = 6
        for i in range(overcompute):
            for node in self.nodes:
                node.update(self, dt / overcompute)
            for link in self.links:
                link.update(self, dt / overcompute)

        for node in self.nodes:
            if node.pos.y > 20:
                node.delete()

        # Retire les éléments à retirer
        for link in self.links:
            if link.deleteFlag:
                self.links.remove(link)
        for node in self.nodes:
            if node.deleteFlag:
                self.nodes.remove(node)

    # Retourne une liste des nodes en ordre de distance
    # return [{"node": node, "dist": dist},..]
    def getNodesInRange(self, pos, range):
        proximities = []
        for node in self.nodes:
            diff = node.pos - pos
            dist = (diff.x ** 2 + diff.y ** 2) ** 0.5
            if dist < range:
                proximities.append({"node": node, "dist": dist})
        proximities.sort(key=sortProximity)
        return proximities


# Sert pour trier les nodes
def sortProximity(linkable):
    return linkable["dist"]
