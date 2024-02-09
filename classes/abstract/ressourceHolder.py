from abc import ABC, abstractmethod
from classes.abstract.base import Base

class RessourceHolder(ABC, Base):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        ressources = kwargs.get("ressources")
        if ressources != None:
            self.ressources = ressources
        else:
            self.ressources = {}

    def pushRessources(self, other, ressources: dict):
        for ressource in ressources.keys():
            if ressource in self.ressources:
                quantity = min(self.ressources[ressource], ressources[ressource])
                self.ressources[ressource] -= quantity
                if ressource in other.ressources:
                    other.ressources[ressource] += quantity
                else:
                    other.ressources[ressource] = quantity

    def checkIfEnough(self, ressources):
        for ressource in ressources.keys():
            if ressource not in self.ressources or self.ressources[ressource] < ressources[ressource]:
                return False
        return True

