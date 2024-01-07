import pygame
from copy import copy
from math import cos, sin
from abc import ABC, abstractmethod
from classes.abstract.updatable import Updatable
from classes.abstract.drawable import Drawable


# font = pygame.font.SysFont("silomttf", 48)

class Building(Updatable, Drawable):

    def __init__(self, pos, world, drawingGroup, updateGroup):
        super().__init__(world=world, pos=pos, drawGroup=drawingGroup, updateGroup=updateGroup)

        # world, N, mu, radius, pos, collisionGroup, drawGroup, updateGroup, collideWith
        self.pos = pos
        self.world = world

    def delete(self):
        if not self.deleteFlag:
            super().delete()

    def getDistance(self, pos, maxDist=10):
        dist = None
        if pos != self.pos:
            diff = self.pos - pos
            if abs(diff.x) < (maxDist)*2 and abs(diff.y) < (maxDist)*2:
                dist = math.dist(self.pos, pos)
        return dist


