# Example file showing a basic pygame "game loop"
import pygame
from mymath import getDiffLengthUnitNorm
from classes.abstract.collidable import Collidable
from classes.abstract.updatable import Updatable
from classes.abstract.drawable import Drawable
from classes.abstract.node import Node
from OpenGL.GL import glBegin, GL_QUADS, glVertex2f, glEnd, GL_LINE_LOOP, glColor3f, glLineWidth
from myGL import setColorHex

class Link(Collidable, Updatable, Drawable):
    maxLength = 2
    minLength = 0.5

    KP = 30000
    KD = 3000
    Friction = 1
    breakpoint = 800000

    def __init__(self, node1: Node, node2: Node, world: object, collisionGroup=0, density=1,
                 KP=1, KD=1, friction=1, brakePoint=1, color="#888888", radius=0.1,
                 drawGroup=0, N=1, mu=1, updateGroup=0, thickness=0.2, startDelay=5):
        pos = (node1.pos + node2.pos) / 2
        self.age = -startDelay
        self.density = density
        self.thickness = thickness
        self.world = world
        self.node1 = node1
        self.node2 = node2
        self.updateValues()
        mass = self.density * self.length * radius * 2 * self.thickness
        momentInertia = mass/12*self.length
        super().__init__(world=world, mass=mass, momentInertia=momentInertia, N=N, mu=mu, radius=radius, pos=pos, collisionGroup=collisionGroup,
                         drawGroup=drawGroup, updateGroup=updateGroup, collideWith=[])

        self.radius = radius
        self.curLength = self.length
        self.pos = pos

        self.connectNode1(node1)
        self.connectNode2(node2)
        self.KP = KP
        self.KD = KD
        self.friction = friction
        self.breakePoint = brakePoint
        self.load = 0
        self.color = color

    def getRestitution(self):
        return self.N*self.mass
        # return self.N*(self.node1.mass + self.node2.mass + self.mass)

    def connectNode1(self, node):
        self.node1 = node
        self.node1.addLink(self)
        self.node1.mass += self.mass / 2

    def connectNode2(self, node):
        self.node2 = node
        self.node2.addLink(self)
        self.node2.mass += self.mass / 2

    def draw(self, camera):
        if abs(self.diff.x) < 100000 and abs(self.diff.y) < 100000:
            pct = min(abs(self.load) / (self.breakePoint * Link.breakpoint), 1)

            pos1 = camera.posToScreen(self.node1.pos + self.norm * self.radius)
            pos2 = camera.posToScreen(self.node2.pos + self.norm * self.radius)
            pos3 = camera.posToScreen(self.node2.pos - self.norm * self.radius)
            pos4 = camera.posToScreen(self.node1.pos - self.norm * self.radius)

            #glColor3f(self.color[0], self.color.g, self.color.b)
            setColorHex(self.color)
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



    def update(self, dt):
        super(Link, self).update(dt)
        self.updateValues()
        if abs(self.diff.x) < 100000 and abs(self.diff.y) < 100000:
            mass = min(self.node1.mass, self.node2.mass)
            err = self.length - self.curLength
            velDiff = self.node2.vel - self.node1.vel
            delta = (velDiff * self.unit)*abs(err)
            self.load = err * self.KP * Link.KP * mass

            if abs(self.load) > self.breakePoint*Link.breakpoint or not self.node1 or not self.node2:
                self.delete()
            else:
                self.node1.force += self.unit * (self.load + (delta * self.KD * Link.KD) * mass)
                self.node2.force -= self.unit * (self.load + (delta * self.KD * Link.KD) * mass)

                self.node1.force += self.norm * velDiff * self.norm * self.friction * Link.Friction * mass
                self.node2.force -= self.norm * velDiff * self.norm * self.friction * Link.Friction * mass

                # if self.age > 0:
                #     self.node1.force += self.mass * self.world.gravity * min(1, (self.age) * 1) / 2
                #     self.node2.force += self.mass * self.world.gravity * min(1, (self.age) * 1) / 2

        self.age += dt

    def updateValues(self):
        self.diff, self.length, self.unit, self.norm = getDiffLengthUnitNorm(self.node1.pos, self.node2.pos)
        self.pos = (self.node1.pos + self.node2.pos) / 2

    def delete(self):
        if not self.deleteFlag:
            super().delete()
            if self in self.node1.links:
                if self.node1.mass > 0:
                    self.node1.mass -= self.mass / 2
                else:
                    raise ValueError(str(self.mass) + ":" + str(self.node1.mass))
                self.node1.links.remove(self)

            if self in self.node2.links:
                if self.node2.mass > 0:
                    self.node2.mass -= self.mass / 2
                else:
                    raise ValueError(str(self.mass) + ":" + str(self.node2.mass))
                self.node2.links.remove(self)

    def getDistance(self, pos, maxDist=10):
        dist = None
        if pos != self.node1.pos and pos != self.node1.pos:

            if (max(self.node1.pos.x, self.node2.pos.x) + maxDist) > pos.x > (
                min(self.node1.pos.x, self.node2.pos.x) - maxDist) \
                and (max(self.node1.pos.y, self.node2.pos.y) + maxDist) > pos.y > (
                min(self.node1.pos.y, self.node2.pos.y) - maxDist):

                # Calcul de la distance
                diff1 = self.node1.pos - pos
                diff2 = self.node2.pos - pos
                dist1 = abs(diff1 * self.unit)
                dist2 = abs(diff2 * self.unit)
                if dist1 < self.length and dist2 < self.length:
                    c = -(self.norm.x * self.node1.pos.x + self.norm.y * self.node1.pos.y)

                    # Calcul de la distance entre le point et la droite
                    dist = abs(self.norm.x * pos.x + self.norm.y * pos.y + c) / (
                            self.norm.x ** 2 + self.norm.y ** 2) ** 0.5

        return dist

    def getContactPos(self, pos, radius):
        contactPos = None
        force = None
        if pos != self.node1.pos and pos != self.node1.pos:

            maxDist = radius + self.radius

            if (max(self.node1.pos.x, self.node2.pos.x) + radius + self.radius) > pos.x > (
                min(self.node1.pos.x, self.node2.pos.x) - radius - self.radius) \
                and (max(self.node1.pos.y, self.node2.pos.y) + radius + self.radius) > pos.y > (
                min(self.node1.pos.y, self.node2.pos.y) - radius - self.radius):

                # Calcul de la distance entre le point et la droite
                dist = self.getDistance(pos, maxDist=maxDist)
                if dist and abs(dist) < self.radius + radius:
                    # Calcul de la distance
                    diff1 = self.node1.pos - pos
                    diff2 = self.node2.pos - pos
                    dist1 = abs(diff1 * self.unit)
                    dist2 = abs(diff2 * self.unit)
                    if dist1 < self.length and dist2 < self.length:
                        contactPos = pos + self.norm * radius * sign(diff1 * self.norm)
                        force = self.norm * (dist - (self.radius + radius)) * sign(diff1 * self.norm) * self.N
        if not contactPos:
            contactPos, force = self.node1.getContactPos(pos, radius)

        if not contactPos:
            contactPos, force = self.node2.getContactPos(pos, radius)

        return contactPos, force

    def getVelAtPoint(self, pos):
        # Pourrait être mieu fait. Tenir compte du rayon
        diff1 = self.node1.pos - pos
        diff2 = self.node2.pos - pos
        diff21 = self.node2.pos - self.node1.pos
        length = (diff21.x ** 2 + diff21.y ** 2) ** 0.5
        unit = diff21 / length
        dist1 = abs(diff1 * unit)
        dist2 = abs(diff2 * unit)
        vel = (self.node1.vel * dist2 + self.node2.vel * dist1) / length
        return vel

    def applyForce(self, pos, force, dt):

        diff1 = self.node1.pos - pos
        diff2 = self.node2.pos - pos

        dist1 = abs(diff1 * self.unit)
        dist2 = abs(diff2 * self.unit)

        # N
        self.node1.force += force * (dist2 / self.length)
        self.node2.force += force * (dist1 / self.length)

        # self.node1.force -= self.norm * force * self.norm
        # self.node2.force -= self.norm * force * self.norm


def sign(num):
    return -1 if num < 0 else 1
