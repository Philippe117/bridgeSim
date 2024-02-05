from classes.abstract.building import Building
from time import time
from classes.cars import Pickup
from pygame import Vector2 as Vec
from myGL import loadImage, drawImage
from OpenGL.GL import *


# font = pygame.font.SysFont("silomttf", 48)

class Warehouse(Building):
    image = None


    def __init__(self, pos, world):

        super().__init__(pos=pos, world=world, drawingGroup=0, updateGroup=1)

        if not Warehouse.image:
            Warehouse.image = loadImage("ressources/warehouse.png")

    def update(self, dt):
        pass

    def draw(self, camera):

        glColor3f(1, 1, 1)  # Couleur blanche (la texture fournit la couleur)
        drawImage(Warehouse.image, camera.posToScreen(self.pos+Vec(0, 5)), Vec(6, 3)*4*camera.zoom, 0)

    def delete(self):
        if not self.deleteFlag:
            super().delete()



