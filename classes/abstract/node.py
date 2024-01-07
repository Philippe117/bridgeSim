# Example file showing a basic pygame "game loop"
import pygame
from copy import copy
from math import cos, sin
from classes.abstract.collidable import Collidable
from classes.abstract.updatable import Updatable
from classes.abstract.drawable import Drawable
from classes.abstract.linkable import Linkable
import math


class Node(Collidable, Updatable, Drawable, Linkable):

    def __init__(self, pos, world, density=1000, radius=0.12, locked=False, color="#ffffff", collisionGroup=0,
                 collideWith=None, drawGroup=0, updateGroup=0, N=10, mu=1, startDelay=5, thickness=0.2):

        self.density = density
        self.thickness = thickness
        self.radius = radius
        self.surface = 3.14159*self.radius**2
        mass = self.surface * self.thickness * self.density  # Kg
        momentInertia = (mass*self.radius**2)/2
        super().__init__(world=world, mass=mass, momentInertia=momentInertia, N=N, mu=mu, radius=radius, pos=pos, collisionGroup=collisionGroup,
                         drawGroup=drawGroup, updateGroup=updateGroup, collideWith=collideWith)

        self.N = N
        self.mu = mu
        self.locked = locked
        self.age = -startDelay
        self.links = []
        self.world = world
        self.vel = pygame.Vector2(0, 0)  # m/s
        self.acc = pygame.Vector2(0, 0)  # m/s^2
        self.force = pygame.Vector2(0, 0)  #
        self.pos = pos
        self.color = color
        self.spin = 0  # rad/s
        self.torque = 0  # Nm
        self.angle = 0

    def getRestitution(self):
        return self.N*self.mass

    def addLink(self, link):
        self.links.append(link)

    def update(self, dt):
        super(Node, self).update(dt)
        if not self.locked:
            if self.age > 0:
                self.force += self.world.gravity * self.mass * min(1, (self.age) * 1)
            self.force -= self.vel * (self.world.friction * self.surface) * dt
            self.acc = self.force / self.mass
            self.vel += self.acc * dt
            self.pos += self.vel * dt
            self.spin += self.torque / self.momentInertia * dt
            self.angle += self.spin * dt

        self.force = pygame.Vector2(0, 0)
        self.torque = 0
        self.age += dt

    def draw(self, camera):
        pos = camera.posToScreen(self.pos)

        # Dessine le node
        pygame.draw.circle(camera.screen, self.color, pos, self.radius * camera.zoom * 1.1)
        pygame.draw.circle(camera.screen, "#000000", pos, self.radius * camera.zoom * 1.1, 2)
        X1 = pygame.Vector2(self.radius * cos(self.angle), self.radius * sin(self.angle)) * camera.zoom
        X2 = pygame.Vector2(X1.y, -X1.x)
        pygame.draw.line(camera.screen, "#000000", pos - X1, pos + X1)
        pygame.draw.line(camera.screen, "#000000", pos - X2, pos + X2)

        # Dessine l'age'
        if self.age < 0:
            font = pygame.font.SysFont("silomttf", 24)
            img = font.render(str(int(-self.age)) + "s", True, "#000000")
            camera.screen.blit(img, pos + pygame.Vector2(20, -20))
        #
        # # Dessine la masse
        # font = pygame.font.SysFont("silomttf", 24)
        # img = font.render(str(self.mass), True, "#000000")
        # camera.screen.blit(img, pos)

    # def delete(self):
    #    for link in self.links:
    #         link.delete = True

    def delete(self):
        if not self.deleteFlag:
            super().delete()
            links = copy(self.links)
            for link in links:
                link.delete()

    def getDistance(self, pos, maxDist=10):
        dist = None
        diff = self.pos - pos
        if abs(diff.x) < maxDist * 2 and abs(diff.y) < maxDist * 2:
            dist = math.dist(self.pos, pos)
        return dist

    def getContactPos(self, pos, radius):
        contactPos = None
        force = None
        maxDist = self.radius + radius
        dist = self.getDistance(pos, maxDist=maxDist)
        if dist != None:
            if dist > 0:
                diff = self.pos - pos
                unit = diff / dist
                if dist < (self.radius + radius):
                    contactPos = pos + unit * self.radius
                    force = unit * (dist - maxDist) * self.N
            else:
                contactPos = pos
                force = pygame.Vector2(0, 0)
        return contactPos, force

    def getVelAtPoint(self, pos):
        # Pourrait être mieu fait. Tenir compte du rayon
        if pos != self.pos:
            diff = self.pos - pos
            dist = math.dist(self.pos, pos)
            unit = diff / dist
            tangent = pygame.Vector2(unit.y, -unit.x)
            vel = self.vel + self.spin * dist * tangent
            return vel
        else:
            return self.vel

    def applyForce(self, pos, force, dt):

        self.force += force
        if pos != self.pos:
            diff = self.pos - pos
            dist = math.dist(self.pos, pos)
            unit = diff / dist
            norm = pygame.Vector2(unit.y, -unit.x)

            spin = norm * force * dist
            self.torque += spin

    def replace(self, NewType):
        links = copy(self.links)
        self.links = []
        newNode = NewType(self.pos, self.world)
        newNode.age = self.age
        for link in links:
            if link.node1 == self:
                link.connectNode1(newNode)
            if link.node2 == self:
                link.connectNode2(newNode)
        self.delete()
        return newNode
