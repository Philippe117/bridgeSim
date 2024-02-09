import pygame
from copy import copy
from math import cos, sin
from abc import ABC, abstractmethod
from classes.abstract.updatable import Updatable
from classes.abstract.drawable import Drawable


# font = pygame.font.SysFont("silomttf", 48)

class Building(Updatable, Drawable):

    def __init__(self, **kwargs):
        pos = kwargs.get("pos")
        world = kwargs.get("world")

        super().__init__(**kwargs)

        # world, N, mu, radius, pos, collisionGroup, drawGroup, updateGroup, collideWith
        self.pos = pos
        self.world = world

    def delete(self):
        if not self.deleteFlag:
            super().delete()


