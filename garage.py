from building import Building
from time import time
from car import Car
import pygame
from copy import copy
from math import cos, sin
from abc import ABC, abstractmethod


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

        pos = camera.posToScreen(self.pos, self.world.screen)
        rect = pygame.Rect(pos.x-2*camera.zoom, pos.y-2*camera.zoom, 4*camera.zoom, 2*camera.zoom)
        pygame.draw.rect(self.world.screen, "#000000", rect)

    def delete(self):
        super().delete()



