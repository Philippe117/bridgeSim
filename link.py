# Example file showing a basic pygame "game loop"
import pygame
from object import object


class Link(object):
    def __init__(self, node1=None, node2=None, physic=True):
        # node1: Node
        # node2: Node

        super().__init__()
        self.connectNode1(node1)
        self.connectNode2(node2)
        diff = self.node1.pos - self.node2.pos
        self.length = (diff.x**2+diff.y**2)**0.5
        self.physic = physic
        self.KP = 400000
        self.KD = 200
        self.KI = 10000
        self.friction = 20
        self.i = 0
        self.mass = self.length
        self.load = 0
        self.brakePoint = 10000
        self.maxForce = 4*self.KP / max(self.node1.mass, self.node2.mass)

    def connectNode1(self, node):
        self.node1 = node
        self.node1.addLink(self)

    def connectNode2(self, node):
        self.node2 = node
        self.node2.addLink(self)

    def draw(self, screen, camera):
        pos1 = camera.posToScreen(self.node1.pos, screen)
        pos2 = camera.posToScreen(self.node2.pos, screen)

        pct = min(abs(self.load)/self.brakePoint, 1)
        color = pygame.Color(int(pct*255), int((1-pct)*255), 0)
        pygame.draw.line(screen, color, pos1, pos2)

    def update(self, world, dt):
        if self.physic:
            diff = self.node1.pos - self.node2.pos
            length = (diff.x ** 2 + diff.y ** 2) ** 0.5
            unit = diff/length
            err = length-self.length
            delta = self.node1.vel.dot(unit) - self.node2.vel.dot(unit)
            self.i += err*dt

            self.load = err*self.KP + delta*self.KD + self.i*self.KI
            if self.load > 0:
                self.load *= 0.5

            appliedLoad = self.load #max(-self.maxForce, min(self.maxForce, self.load))

            if abs(self.load) > self.brakePoint or not self.node1 or not self.node2:
                self.delete()
            else:
                self.node1.force -= unit*appliedLoad
                self.node2.force += unit*appliedLoad

                self.node1.force += (self.node2.vel-self.node1.vel)*self.friction/length
                self.node2.force += (self.node1.vel-self.node2.vel)*self.friction/length


    def delete(self):
        self.deleteFlag = True

def sign(num):
    return -1 if num < 0 else 1
