import pygame
from copy import copy
from math import cos, sin
from abc import ABC, abstractmethod


# font = pygame.font.SysFont("silomttf", 48)

class Building():

    def __init__(self, pos, world, drawingGroup, updateGroup):
        self.pos = pos
        self.world = world
        self.world.buildings.append(self)
        if drawingGroup >= 0:
            self.drawingGroup = self.world.drawingGroups[drawingGroup]
            self.drawingGroup.append(self)
        else:
            self.drawingGroup = None
        if updateGroup >= 0:
            self.updateGroup = self.world.updateGroups[updateGroup]
            self.updateGroup.append(self)
        else:
            self.updateGroup = None

    @abstractmethod
    def update(self, dt):
        raise NotImplementedError("Must override update")

    @abstractmethod
    def draw(self, camera):
        raise NotImplementedError("Must override draw")

    def delete(self):
        if not self.deleteFlag:
            self.deleteFlag = True
            if self in self.drawingGroup:
                self.drawingGroup.remove(self)
            if self in self.updateGroup:
                self.updateGroup.remove(self)
            return True
        return False


    def getDistance(self, pos, maxDist=10):
        dist = None
        if pos != self.pos:
            diff = self.pos - pos
            if abs(diff.x) < (maxDist)*2 and abs(diff.y) < (maxDist)*2:
                dist = (diff.x ** 2 + diff.y ** 2) ** 0.5
        return dist


