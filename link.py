# Example file showing a basic pygame "game loop"
import pygame
from object import Object


class Link(Object):
    maxLength = 2
    minLength = 0.5

    def __init__(self, node1, node2, world, collisionGroup=0, density=1,
                 KP=100000, KD=10000, KI=4000, friction=2000, brakePoint=15000, color="#888888", radius=0.1,
                 locked=False, indestructible=True,
                 drawingGroup=0, N=50, mu=10, startDelay=0):
        # node1: Node
        # node2: Node

        pos = (node1.pos + node2.pos) / 2
        diff = node1.pos - node2.pos
        self.density = density
        self.length = (diff.x ** 2 + diff.y ** 2) ** 0.5
        mass = self.length * self.density
        super().__init__(pos=pos, world=world, collisionGroup=collisionGroup, collideWithGroups=[],
                         drawingGroup=drawingGroup, updateGroup=0, radius=radius, locked=locked,
                         indestructible=indestructible, N=N, mu=mu,
                         mass=mass, startDelay=startDelay)

        self.connectNode1(node1)
        self.connectNode2(node2)
        self.KP = KP
        self.KD = KD
        self.KI = KI
        self.friction = friction
        self.brakePoint = brakePoint
        self.i = 0
        self.load = 0
        self.oldErr = 0
        self.color = color

    def connectNode1(self, node):
        self.node1 = node
        self.node1.addLink(self)
        self.node1.mass += self.mass / 2

    def connectNode2(self, node):
        self.node2 = node
        self.node2.addLink(self)
        self.node1.mass += self.mass / 2

    def draw(self, camera):

        diff = self.node2.oldPos - self.node1.oldPos
        if abs(diff.x) < 100000 and abs(diff.y) < 100000:
            norm = pygame.Vector2(diff.y, -diff.x)
            norm /= (norm.x ** 2 + norm.y ** 2) ** 0.5

            pct = min(abs(self.load) / self.brakePoint, 1)
            #        color = pygame.Color(int(pct * 255), int((1 - pct) * 255), 0)  # GN to RD
            color = pygame.Color(int(pct * 255), 0, 0)  # BK to RD

            pos1 = camera.posToScreen(self.node1.oldPos + norm * self.radius, self.world.screen)
            pos2 = camera.posToScreen(self.node2.oldPos + norm * self.radius, self.world.screen)
            pos3 = camera.posToScreen(self.node2.oldPos - norm * self.radius, self.world.screen)
            pos4 = camera.posToScreen(self.node1.oldPos - norm * self.radius, self.world.screen)

            pygame.draw.polygon(self.world.screen, self.color, [pos1, pos2, pos3, pos4])
            pygame.draw.polygon(self.world.screen, color, [pos1, pos2, pos3, pos4], 2)

    def update(self, dt):
        super().update(dt)
        diff = self.node1.pos - self.node2.pos
        if abs(diff.x) < 100000 and abs(diff.y) < 100000:
            length = (diff.x ** 2 + diff.y ** 2) ** 0.5
            unit = diff / length
            err = length - self.length

            delta = abs(err) * (err - self.oldErr) / dt
            self.oldErr = err
            self.i += err * dt

            self.load = err * self.KP + delta * self.KD + self.i * self.KI

            if not self.indestructible and abs(self.load) > self.brakePoint or not self.node1 or not self.node2:
                load = self.load
                brakePoint = self.brakePoint
                self.delete()
            else:
                self.node1.force -= unit * self.load
                self.node2.force += unit * self.load

            self.node1.force += (self.node2.vel - self.node1.vel) * self.friction * dt
            self.node2.force += (self.node1.vel - self.node2.vel) * self.friction * dt

    def delete(self):
        super().delete()
        if not self.node1.deleteFlag:
            if self in self.node1.links:
                self.node1.mass -= self.mass / 2
                self.node1.links.remove(self)
        if not self.node2.deleteFlag:
            if self in self.node2.links:
                self.node2.mass -= self.mass / 2
                self.node2.links.remove(self)

    def getContactPos(self, pos, radius):

        contactPos = None
        force = None
        if pos != self.node1.pos and pos != self.node1.pos:

            if (max(self.node1.pos.x, self.node2.pos.x) + radius + self.radius) > pos.x > (
                min(self.node1.pos.x, self.node2.pos.x) - radius - self.radius) \
                and (max(self.node1.pos.y, self.node2.pos.y) + radius + self.radius) > pos.y > (
                min(self.node1.pos.y, self.node2.pos.y) - radius - self.radius):

                # Calcul de la distance
                diff1 = self.node1.pos - pos
                diff2 = self.node2.pos - pos

                diff21 = self.node2.pos - self.node1.pos
                length = (diff21.x ** 2 + diff21.y ** 2) ** 0.5

                # Calcul du vecteur normal et des coefficients de l'équation de la droite
                unit = diff21 / length
                norm = pygame.Vector2(unit.y, -unit.x)
                c = -(norm.x * self.node1.pos.x + norm.y * self.node1.pos.y)

                # Calcul de la distance entre le point et la droite
                dist = abs(norm.x * pos.x + norm.y * pos.y + c) / (norm.x ** 2 + norm.y ** 2) ** 0.5

                if abs(dist) < self.radius + radius:
                    dist1 = abs(diff1 * unit)
                    dist2 = abs(diff2 * unit)
                    if dist1 < length and dist2 < length:
                        contactPos = pos + norm * radius * sign(diff1 * norm)
                        force = norm * (dist - (self.radius + radius)) * sign(diff1 * norm) * self.N
                        ok = 0

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
