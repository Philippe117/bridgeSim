from mymath import getDiffLengthUnitNorm
from classes.abstract.collidable import Collidable
from classes.abstract.updatable import Updatable
from classes.abstract.drawable import Drawable
from classes.abstract.node import Node
from OpenGL.GL import glBegin, GL_QUADS, glVertex2f, glEnd, GL_LINE_LOOP, glColor3f, glLineWidth
from myGL import setColorHex, drawDisk, setColorHex, drawLine

class Link(Collidable, Updatable, Drawable):
    maxLength = 2
    minLength = 0.5
    KP = 50000
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
        momentInertia = mass / 12 * self.length
        super().__init__(world=world, mass=mass, momentInertia=momentInertia, N=N, mu=mu, radius=radius, pos=pos,
                         collisionGroup=collisionGroup, drawGroup=drawGroup, updateGroup=updateGroup, collideWith=[])
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
        # self.camera = camera

    def update(self, dt):
        super(Link, self).update(dt)
        self.updateValues()
        if abs(self.diff.x) < 100000 and abs(self.diff.y) < 100000:
            mass = min(self.node1.mass, self.node2.mass)
            err = self.length - self.curLength
            velDiff = self.node2.vel - self.node1.vel
            delta = (velDiff * self.unit) * abs(err)
            self.load = err * self.KP * Link.KP * mass

            if abs(self.load) > self.breakePoint * Link.breakpoint or not self.node1 or not self.node2:
                self.delete()
            else:
                kd_factor = delta * self.KD * Link.KD * mass
                self.node1.force += self.unit * (self.load + kd_factor)
                self.node2.force -= self.unit * (self.load + kd_factor)

                friction_force = velDiff * self.norm * self.friction * Link.Friction * mass
                self.node1.force += self.norm * friction_force
                self.node2.force -= self.norm * friction_force

        self.age += dt

    def updateValues(self):
        self.diff, self.length, self.unit, self.norm = getDiffLengthUnitNorm(self.node1.pos, self.node2.pos)
        self.pos = (self.node1.pos + self.node2.pos) / 2

    def delete(self):
        if not self.deleteFlag:
            super().delete()
            for node in [self.node1, self.node2]:
                if self in node.links:
                    if node.mass > 0:
                        node.mass -= self.mass / 2
                    else:
                        raise ValueError(str(self.mass) + ":" + str(node.mass))
                    node.links.remove(self)

    def getDistance(self, pos, maxDist=10):
        if pos in (self.node1.pos, self.node2.pos):
            return None

        # x_min, x_max = min(self.node1.pos.x, self.node2.pos.x), max(self.node1.pos.x, self.node2.pos.x)
        # y_min, y_max = min(self.node1.pos.y, self.node2.pos.y), max(self.node1.pos.y, self.node2.pos.y)
        # if x_max + maxDist <= pos.x <= x_min - maxDist or y_max + maxDist <= pos.y <= y_min - maxDist:
        #     return None

        diff1 = pos - self.node1.pos
        diff2 = pos - self.node2.pos
        dist1 = diff1 * self.unit
        dist2 = diff2 * self.unit
        if dist1 > 0 > dist2:
            diff_to_line = abs(diff1*self.norm)
            return diff_to_line if 0 <= diff_to_line <= self.length else None

        return None

    def getContactPos(self, pos, radius):
        contactPos = None
        squish = None

        if pos in (self.node1.pos, self.node2.pos):
            return None, None

        maxDist = self.radius + radius

        dist = self.getDistance(pos, maxDist=radius + self.radius)
        if dist and abs(dist) < maxDist:
            direction = sign((self.node1.pos - pos) * self.norm)
            contactPos = pos + self.norm * (radius + dist - maxDist) * direction
            squish = self.norm * (dist - maxDist) * direction
        #
        # if not contactPos:
        #     contactPos, squish = self.node1.getContactPos(pos, radius)
        #
        # if not contactPos:
        #     contactPos, squish = self.node2.getContactPos(pos, radius)

        # try:
        #     campos = self.camera.posToScreen(contactPos)
        #     campos2 = self.camera.posToScreen(contactPos+squish*10)
        #     # Utilisation directe des méthodes de dessin
        #     setColorHex("#ff0000")
        #     drawLine(campos, campos2, 1)
        #     drawDisk(campos, 0.05 * self.camera.zoom, 6)
        # except:
        #     pass

        return contactPos, squish

    def sign(num):
        return -1 if num < 0 else 1

    def getVelAtPoint(self, pos):
        # Pourrait être mieu fait. Tenir compte du rayon
        diff1 = self.node1.pos - pos
        diff2 = self.node2.pos - pos
        dist1 = abs(diff1 * self.unit)
        dist2 = abs(diff2 * self.unit)
        vel = (self.node1.vel * dist2 + self.node2.vel * dist1) / self.length
        return vel

    def applyForceTorque(self, force, torque):
        self.node1.applyForceTorque(force-self.norm*torque/(self.length/2), 0)
        self.node2.applyForceTorque(force+self.norm*torque/(self.length/2), 0)


def sign(num):
    return -1 if num < 0 else 1
