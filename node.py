# Example file showing a basic pygame "game loop"
import pygame
from object import Object
from copy import copy
from math import cos, sin


# font = pygame.font.SysFont("silomttf", 48)

class Node(Object):

    def __init__(self, pos, world, collisionGroup, collideWithGoups, mass=2,
                 radius=0.12, locked=False, indestructible=True, color="#ffffff", drawingGroup=1, N=10, mu=10):
        # pos: pygame.Vector2
        # links: Link[]

        super().__init__(pos, world, collisionGroup, collideWithGoups, drawingGroup, 1, radius, locked, indestructible, N, mu, mass)
        self.links = []
        self.vel = pygame.Vector2(0, 0)  # m/s
        self.acc = pygame.Vector2(0, 0)  # m/s^2
        self.force = pygame.Vector2(0, 0)  # N
        self.mass = mass  # Kg
        self.world.nodes.append(self)
        self.age = 0  # s
        self.oldVel = copy(self.vel)
        self.oldPos = copy(self.pos)
        self.color = color
        self.spin = 0   # rad/s
        self.torque = 0  # Nm
        self.momentInertia = (3.14159*self.radius**4)/4
        self.angle = 0
        self.N = N
        self.mu = mu

    def addLink(self, link):
        self.links.append(link)

    def update(self, dt):
        super().update(dt)
        if not self.locked:
            self.force += self.world.gravity * self.mass * min(1, self.age * 1)
            self.force -= self.vel * (self.world.friction * self.radius * self.radius) * dt
            self.acc = self.force / self.mass
            self.vel += self.acc * dt
            self.pos += self.vel * dt
            self.oldPos += (self.pos - self.oldPos) * 1
            self.spin += self.torque / self.momentInertia * dt
            self.angle += self.spin*dt

        self.force = pygame.Vector2(0, 0)
        self.torque = 0
        self.age += dt

    def draw(self, camera):
        pos = camera.posToScreen(self.oldPos, self.world.screen)

        # Dessine le node
        pygame.draw.circle(self.world.screen, self.color, pos, self.radius * camera.zoom*1.1)
        pygame.draw.circle(self.world.screen, "#000000", pos, self.radius * camera.zoom*1.1, 2)
        X1 = pygame.Vector2(self.radius*cos(self.angle), self.radius*sin(self.angle)) * camera.zoom
        X2 = pygame.Vector2(X1.y, -X1.x)
        pygame.draw.line(self.world.screen, "#000000", pos-X1, pos+X1)
        pygame.draw.line(self.world.screen, "#000000", pos-X2, pos+X2)
        #
        # # Dessine le id
        # font = pygame.font.SysFont("silomttf", 24)
        # img = font.render(str(self.id), True, "#000000")
        # self.world.screen.blit(img, pos)

    # def delete(self):
    #    for link in self.links:
    #         link.delete = True

    def delete(self):
        super().delete()
        self.world.nodes.remove(self)
        for link in self.links:
            link.delete()


    def getContactPos(self, pos, radius):
        contactPos = None
        force = None
        if pos != self.pos:
            #if abs(self.pos.x - pos.x) < (radius + self.radius)*2 and abs(self.pos.y - pos.y) < (radius + self.radius)*2:
            diff = self.pos - pos
            dist = (diff.x ** 2 + diff.y ** 2) ** 0.5
            unit = diff / dist
            if dist < (self.radius + radius):
                contactPos = pos + unit * self.radius
                force = unit*(dist - (self.radius+radius)) * self.N
        return contactPos, force

    def getVelAtPoint(self, pos):
        # Pourrait être mieu fait. Tenir compte du rayon
        if pos != self.pos:
            diff = self.pos - pos
            dist = (diff.x ** 2 + diff.y ** 2) ** 0.5
            unit = diff/dist
            tangent = pygame.Vector2(unit.y, -unit.x)
            return self.vel+self.spin*dist*tangent
        else:
            return self.vel

    def collide(self, pos, force, vel, friction):
        self.force += force
        if pos != self.pos:
            diff = self.pos - pos
            dist = (diff.x ** 2 + diff.y ** 2) ** 0.5
            unit = diff / dist
            norm = pygame.Vector2(unit.y, -unit.x)

            # mu
            #self.force += -norm*(vel)*norm*friction
            self.force += -vel*friction*10
            spin = -(norm*vel)/self.radius
            self.torque += spin*friction*0.1