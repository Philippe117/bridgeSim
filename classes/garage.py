from classes.abstract.building import Building
from time import time
from classes.materials.car import Car
import pygame


# font = pygame.font.SysFont("silomttf", 48)

class Garage(Building):

    def __init__(self, pos, world):

        super().__init__(pos=pos, world=world, drawingGroup=1, updateGroup=1)
        self.delay = 5
        self.NextCarTime = time()+self.delay
        self.greenlight = True
        self.carSize = pygame.Vector2(2.5, 1)

    def update(self, dt):
        curTime = time()
        if curTime > self.NextCarTime:
            Car(self.pos, self.carSize, self.world)
            self.NextCarTime = curTime+self.delay

    def draw(self, camera):

        pos = camera.posToScreen(self.pos)
        rect = pygame.Rect(pos.x-2*camera.zoom, pos.y-2*camera.zoom, 4*camera.zoom, 2*camera.zoom)
        pygame.draw.rect(camera.screen, "#000000", rect)

    def delete(self):
        if not self.deleteFlag:
            super().delete()



