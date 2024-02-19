from abc import ABC, abstractmethod
from classes.abstract.base import Base

class RessourceHolder(ABC, Base):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        ressources = kwargs.get("ressources")

        self.ressources = {}
        if ressources != None:
            self.addRessources(ressources)

    def pushRessources(self, other, ressources: dict):
        other.addRessources(self.removeRessources(ressources))

    def checkIfEnough(self, ressources):
        for ressource in ressources.keys():
            if ressource not in self.ressources or self.ressources[ressource] < ressources[ressource]:
                return False
        return True

    def addRessources(self, ressources: dict):
        for ressource in ressources.keys():
            if ressource in self.ressources:
                self.ressources[ressource] += ressources[ressource]
            else:
                self.ressources[ressource] = ressources[ressource]

    def removeRessources(self, ressources: dict):
        out = {}
        for ressource in ressources.keys():
            if ressource in self.ressources:
                out[ressource] = min(self.ressources[ressource], ressources[ressource])
                self.ressources[ressource] -= out[ressource]
        return out

    def convertRessources(self, input: dict, output: dict):
        if self.checkIfEnough(input):
            self.removeRessources(input)
            self.addRessources(output)
            return True
        else:
            return False

