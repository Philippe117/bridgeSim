from abc import ABC, abstractmethod
from classes.abstract.updatable import Updatable


class Object(Updatable):
    id = 0

    def __init__(self, world, updateGroup, startDelay=5):
        Updatable.__init__(self, world, updateGroup)
        self.world = world
        self.deleteFlag = False
        self.id = Object.id
        Object.id += 1
        self.age = -startDelay

    def update(self, dt):
        self.age += dt


    def delete(self):
        if not self.deleteFlag:
            self.deleteFlag = True
            return True
        return False
