from classes.abstract.building import Building
from classes.abstract.ressourceHolder import RessourceHolder
from time import time
from classes.cars import Pickup
from pygame import Vector2 as Vec
from myGL import loadImage, drawImage
from OpenGL.GL import *
from classes.abstract.updatable import Updatable
from classes.abstract.drawable import Drawable


# font = pygame.font.SysFont("silomttf", 48)

class Garage(RessourceHolder, Building):
    image = None


    def __init__(self, pos, world, destination):

        super().__init__(pos=pos, world=world, drawGroup=0, updateGroup=1, ressources={"wood": 50, "steel": 10})
        self.delay = 5
        self.NextCarTime = time()+self.delay
        self.greenlight = True
        self.destination = destination

        if not Garage.image:
            Garage.image = loadImage("ressources/garage.png")

    def update(self, dt):
        curTime = time()
        if curTime > self.NextCarTime:
            ressources = {"wood": 10, "steel": 5}

            self.addRessources(ressources)
            if self.checkIfEnough(ressources):
                car = Pickup(pos=self.pos+Vec(0, -0.3), world=self.world, destination=self.destination)
                self.pushRessources(car, ressources)

                self.NextCarTime = curTime+self.delay



    def draw(self, camera):

        glColor3f(1, 1, 1)  # Couleur blanche (la texture fournit la couleur)
        drawImage(Garage.image, camera.posToScreen(self.pos+Vec(0, 3.5)), Vec(6, 4)*2*camera.zoom, 0)

    def delete(self):
        if not self.deleteFlag:
            super().delete()



