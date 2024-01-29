from classes.abstract.building import Building
from time import time
from classes.cars import Car
from pygame import Vector2 as Vec
from myGL import loadImage, drawImage
from OpenGL.GL import *


# font = pygame.font.SysFont("silomttf", 48)

class Garage(Building):
    image = None


    def __init__(self, pos, world):

        super().__init__(pos=pos, world=world, drawingGroup=0, updateGroup=1)
        self.delay = 5
        self.NextCarTime = time()+self.delay
        self.greenlight = True

        if not Garage.image:
            Garage.image = loadImage("ressources/garage.png")

    def update(self, dt):
        curTime = time()
        if curTime > self.NextCarTime:
            Car(self.pos, self.world)
            self.NextCarTime = curTime+self.delay

    def draw(self, camera):

        glColor3f(1, 1, 1)  # Couleur blanche (la texture fournit la couleur)
        drawImage(Garage.image, camera.posToScreen(self.pos+Vec(0, 3.5)), Vec(6, 4)*2*camera.zoom, 0)

    def delete(self):
        if not self.deleteFlag:
            super().delete()



