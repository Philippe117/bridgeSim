# Example file showing a basic pygame "game loop"
import pygame
from classes.abstract.object import Object
from mymath import getDiffLengthUnitNorm
from classes.abstract.collidable import Collidable
from classes.abstract.updatable import Updatable
from classes.abstract.drawable import Drawable
from classes.abstract.node import Node


class Link(Collidable, Updatable, Drawable):
    maxLength = 2
    minLength = 0.5

    def __init__(self, node1: Node, node2: Node, world: object, collisionGroup=0, density=1,
                 KP=100000, KD=10000, KI=4000, friction=2000, brakePoint=15000, color="#888888", radius=0.1,
                 drawGroup=0, N=50, mu=10, updateGroup=0):
        pos = (node1.pos + node2.pos) / 2
        super().__init__(world, N, mu, radius, pos, collisionGroup, drawGroup, updateGroup, [])

        self.radius = radius
        self.node1 = node1
        self.node2 = node2
        self.updateValues()
        self.curLength = self.length
        self.density = density
        self.mass = self.length * self.density
        self.pos = pos

        self.connectNode1(node1)
        self.connectNode2(node2)
        self.KP = KP
        self.KD = KD
        self.KI = KI
        self.friction = friction
        self.brakePoint = brakePoint
        self.i = 0
        self.load = 0
        self.color = color

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
            pct = min(abs(self.load) / self.brakePoint, 1)
            #        color = pygame.Color(int(pct * 255), int((1 - pct) * 255), 0)  # GN to RD
            color = pygame.Color(int(pct * 255), 0, 0)  # BK to RD

            pos1 = camera.posToScreen(self.node1.pos + self.norm * self.radius)
            pos2 = camera.posToScreen(self.node2.pos + self.norm * self.radius)
            pos3 = camera.posToScreen(self.node2.pos - self.norm * self.radius)
            pos4 = camera.posToScreen(self.node1.pos - self.norm * self.radius)

            pygame.draw.polygon(camera.screen, self.color, [pos1, pos2, pos3, pos4])
            pygame.draw.polygon(camera.screen, color, [pos1, pos2, pos3, pos4], 2)

    def update(self, dt):
        self.updateValues()
        if abs(self.diff.x) < 100000 and abs(self.diff.y) < 100000:
            mass = (self.node1.mass + self.node2.mass) * 0.2
            err = self.length - self.curLength
            velDiff = self.node2.vel - self.node1.vel
            delta = velDiff * self.unit
            self.i += err * dt
            self.load = (err * self.KP + delta * self.KD + self.i * self.KI) * mass

            if abs(self.load) > self.brakePoint or not self.node1 or not self.node2:
                self.delete()
            else:
                self.node1.force += self.unit * self.load
                self.node2.force -= self.unit * self.load

                self.node1.force += self.norm * velDiff * self.norm * self.friction
                self.node2.force -= self.norm * velDiff * self.norm * self.friction

    def updateValues(self):
        self.diff, self.length, self.unit, self.norm = getDiffLengthUnitNorm(self.node1.pos, self.node2.pos)
        self.pos = (self.node1.pos + self.node2.pos) / 2

    def delete(self):
        if self in self.node1.links:
            self.node1.mass -= self.mass / 2
        if self in self.node2.links:
            self.node2.mass -= self.mass / 2
        Collidable.delete(self)
        Updatable.delete(self)
        Drawable.delete(self)

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

    def collide(self, pos, force, vel, friction):

        diff1 = self.node1.pos - pos
        diff2 = self.node2.pos - pos

        diff21 = self.node2.pos - self.node1.pos
        length = (diff21.x ** 2 + diff21.y ** 2) ** 0.5
        unit = diff21 / length
        norm = pygame.Vector2(unit.y, -unit.x)

        dist1 = abs(diff1 * unit)
        dist2 = abs(diff2 * unit)

        # N
        self.node1.force += force * (dist2 / length)
        self.node2.force += force * (dist1 / length)
        self.node1.force -= norm * vel * norm * 100 * (dist2 / length)
        self.node2.force -= norm * vel * norm * 100 * (dist2 / length)

        # mu
        self.node1.force += unit * vel * unit * friction
        self.node2.force += unit * vel * unit * friction


def sign(num):
    return -1 if num < 0 else 1
