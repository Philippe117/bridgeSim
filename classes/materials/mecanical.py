from classes.abstract.link import Link
from classes.abstract.node import Node
import pygame
from classes.abstract.destructible import Destructible
from classes.abstract.interactible import Interactible


class JackLink(Link, Destructible, Interactible):
    maxLength = 3
    minLength = 0.5
    extentionSpeed = 1

    def __init__(self, node1, node2, world, extention=1.5):
        super().__init__(node1=node1, node2=node2, world=world, collisionGroup=1, density=6000,
                         KP=30000, KD=5000, KI=0, friction=2, brakePoint=800000, color="#1144aa", radius=0.15,
                         drawGroup=5, N=1, mu=1)

        self.maxLength = max(self.length, self.length * extention)
        self.minLength = min(self.length, self.length * extention)
        self.cmdLength = self.length
        self.cmdSpeed = 0

    def update(self, dt):
        super().update(dt)
        self.cmdSpeed += min(JackLink.extentionSpeed,
                             max(-JackLink.extentionSpeed, (self.cmdLength - self.curLength) * 20)) * dt
        self.curLength += self.cmdSpeed * dt
        self.cmdSpeed += -self.cmdSpeed * 0.02

    def draw(self, camera):
        super().draw(camera)
        pct = min(abs(self.load) / self.brakePoint, 1)
        #        color = pygame.Color(int(pct * 255), int((1 - pct) * 255), 0)  # GN to RD
        color = pygame.Color(int(pct * 255), 0, 0)  # BK to RD

        pos1 = camera.posToScreen(self.node1.pos + self.norm * self.radius)
        pos2 = camera.posToScreen(self.node2.pos + self.norm * self.radius)
        pos3 = camera.posToScreen(self.node2.pos - self.norm * self.radius)
        pos4 = camera.posToScreen(self.node1.pos - self.norm * self.radius)

        pygame.draw.polygon(camera.screen, "#888888", [pos1, pos2, pos3, pos4])
        pygame.draw.polygon(camera.screen, color, [pos1, pos2, pos3, pos4], 2)

        pos = self.node2.pos - self.unit * (self.minLength - self.radius)
        pos1 = camera.posToScreen(self.node2.pos + self.norm * 0.2)
        pos2 = camera.posToScreen(pos + self.norm * 0.2)
        pos3 = camera.posToScreen(pos - self.norm * 0.2)
        pos4 = camera.posToScreen(self.node2.pos - self.norm * 0.2)
        pygame.draw.polygon(camera.screen, self.color, [pos1, pos2, pos3, pos4])
        pygame.draw.polygon(camera.screen, color, [pos1, pos2, pos3, pos4], 2)

    def sclollAction(self, scroll):
        self.cmdLength = max(self.minLength,
                             min(self.maxLength, self.curLength + scroll * JackLink.extentionSpeed / 4))
        return True


class JackNode(Node, Destructible):
    def __init__(self, pos, world):
        super().__init__(pos=pos, world=world, collisionGroup=1, collideWith=[], density=6000,
                         radius=0.2, color="#888888", drawGroup=9, N=1, mu=1)


class PullerLink(JackLink):
    def __init__(self, node1, node2, world, extention=0.5):
        super().__init__(node1, node2, world, extention)


class SpringLink(Link, Destructible):
    maxLength = 3
    minLength = 0.5

    def __init__(self, node1, node2, world, extention=1.5):
        super().__init__(node1=node1, node2=node2, world=world, collisionGroup=1, density=6000,
                         KP=300, KD=10, KI=0, friction=2, brakePoint=800000, color="#ff8800", radius=0.15,
                         drawGroup=5, N=1, mu=1)
