from classes.abstract.link import Link
from classes.abstract.node import Node
import pygame
from classes.abstract.destructible import Destructible
from classes.abstract.interactible import Interactible
from myGL import setColorHex, drawDisk, setColorHex, drawLine
from OpenGL.GL import glBegin, GL_QUADS, glVertex2f, glEnd, GL_LINE_LOOP, glColor3f, glLineWidth


class JackLink(Link, Destructible, Interactible):
    maxLength = 3
    minLength = 0.5
    extentionSpeed = 1

    def __init__(self, node1, node2, world, extention=1.5):
        super().__init__(node1=node1, node2=node2, world=world, collisionGroup=1, density=6000,
                         KP=1, KD=1, friction=1, brakePoint=1, color="#888888", radius=0.15,
                         drawGroup=5, N=1, mu=1, thickness=0.5)

        self.sleeveColor = "#1144aa"
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
        pct = min(abs(self.load) / (self.breakePoint * Link.breakpoint), 1)

        pos = self.node2.pos - self.unit * (self.minLength - self.radius)
        pos1 = camera.posToScreen(self.node2.pos + self.norm * 0.2)
        pos2 = camera.posToScreen(pos + self.norm * 0.2)
        pos3 = camera.posToScreen(pos - self.norm * 0.2)
        pos4 = camera.posToScreen(self.node2.pos - self.norm * 0.2)

        setColorHex(self.sleeveColor)
        glBegin(GL_QUADS)
        glVertex2f(pos1.x, pos1.y)
        glVertex2f(pos2.x, pos2.y)
        glVertex2f(pos3.x, pos3.y)
        glVertex2f(pos4.x, pos4.y)
        glEnd()

        glColor3f(pct, 0, 0)
        glLineWidth(2)
        glBegin(GL_LINE_LOOP)
        glVertex2f(pos1.x, pos1.y)
        glVertex2f(pos2.x, pos2.y)
        glVertex2f(pos3.x, pos3.y)
        glVertex2f(pos4.x, pos4.y)
        glEnd()

    def sclollAction(self, scroll):
        self.cmdLength = max(self.minLength,
                             min(self.maxLength, self.curLength + scroll * JackLink.extentionSpeed / 4))
        return True


class JackNode(Node, Destructible):
    def __init__(self, pos, world):
        super().__init__(pos=pos, world=world, collisionGroup=-1, collideWith=[], density=6000,
                         radius=0.2, color="#888888", drawGroup=9, N=1, mu=1, thickness=0.5)


class PullerLink(JackLink):
    def __init__(self, node1, node2, world, extention=0.5):
        super().__init__(node1, node2, world, extention)


class SpringLink(Link, Destructible):
    maxLength = 3
    minLength = 0.5

    def __init__(self, node1, node2, world, extention=1.5):
        super().__init__(node1=node1, node2=node2, world=world, collisionGroup=-1, density=6000,
                         KP=0.01, KD=0.001, friction=1, brakePoint=1, color="#ff8800", radius=0.15,
                         drawGroup=5, N=1, mu=1, thickness=0.5)
