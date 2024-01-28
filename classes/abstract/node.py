from pygame import Vector2 as Vec
from classes.abstract.collidable import Collidable
from classes.abstract.updatable import Updatable
from classes.abstract.drawable import Drawable
from classes.abstract.linkable import Linkable
from myGL import drawCircle, drawLine, drawDisk, setColorHex
from math import cos, sin

class Node(Collidable, Updatable, Drawable, Linkable):

    def __init__(self, pos, world, density=1000, radius=0.12, locked=False, color="#ffffff", collisionGroup=0,
                 collideWith=None, drawGroup=-1, updateGroup=0, N=10, mu=1, startDelay=5, thickness=0.2):

        # Utilisation de formules directes plutôt que des variables intermédiaires
        self.surface = 3.14159 * radius**2
        mass = self.surface * thickness * density
        momentInertia = (mass * radius**2) / 2

        super().__init__(world=world, mass=mass, momentInertia=momentInertia, N=N, mu=mu, radius=radius, pos=pos,
                         collisionGroup=collisionGroup, drawGroup=drawGroup, updateGroup=updateGroup,
                         collideWith=collideWith)

        self.density = density
        self.thickness = thickness
        self.radius = radius
        self.N = N
        self.mu = mu
        self.locked = locked
        self.age = -startDelay
        self.links = []
        self.world = world
        self.vel = Vec(0, 0)
        self.acc = Vec(0, 0)
        self.force = Vec(0, 0)
        self.pos = pos
        self.color = color
        self.spin = 0
        self.torque = 0
        self.angle = 0

    def getRestitution(self):
        return self.N * self.mass

    def addLink(self, link):
        self.links.append(link)

    def update(self, dt):
        super(Node, self).update(dt)
        if not self.locked:
            if self.age > 0:
                self.force += self.world.gravity * self.mass * min(1, (self.age) * 1)
            maxiForce = self.mass*300
            maxiTorque = self.momentInertia*100

            if self.force.length() > 0:
                self.force.clamp_magnitude_ip(maxiForce)
            self.torque = min(max(self.torque, -maxiTorque), maxiTorque)

            self.force -= self.vel * (self.world.friction * self.surface) * dt
            self.acc = self.force / self.mass
            self.vel += self.acc * dt
            self.pos += self.vel * dt
            self.spin += self.torque / self.momentInertia * dt
            self.angle += self.spin * dt

        # Réinitialisation des forces et torques à la fin de la mise à jour
        self.force = Vec(0, 0)
        self.torque = 0
        self.age += dt

    def draw(self, camera):
        pos = camera.posToScreen(self.pos)

        # Utilisation directe des méthodes de dessin
        setColorHex(self.color)
        drawDisk(pos, self.radius * camera.zoom, 16)
        setColorHex("#000000")
        drawCircle(pos, self.radius * camera.zoom, 16, 2)

        # Calcul direct des vecteurs sans utiliser les variables intermédiaires
        X1 = Vec(self.radius * cos(self.angle), self.radius * sin(self.angle)) * camera.zoom
        X2 = Vec(X1.y, -X1.x)
        drawLine(pos - X1, pos + X1, 2)
        drawLine(pos - X2, pos + X2, 2)

    def delete(self):
        if not self.deleteFlag:
            super().delete()
            # Utilisation de la copie directe plutôt que de la fonction copy
            links = self.links.copy()
            for link in links:
                link.delete()

    def getDistance(self, pos, maxDist=10):
        dist = None
        diff = self.pos - pos
        if abs(diff.x) < maxDist * 2 and abs(diff.y) < maxDist * 2:
            dist = self.pos.distance_to(pos)
        return dist

    def getContactPos(self, pos, radius):
        contactPos = None
        force = None
        maxDist = self.radius + radius
        dist = self.getDistance(pos, maxDist=maxDist)
        if dist is not None:
            if dist > 0:
                diff = self.pos - pos
                unit = diff / dist
                if dist < (self.radius + radius):
                    contactPos = pos + unit * self.radius
                    force = unit * (dist - maxDist) * self.N
            else:
                contactPos = pos
                force = Vec(0, 0)
        return contactPos, force

    def getVelAtPoint(self, pos):
        if pos != self.pos:
            dist = self.pos.distance_to(pos)
            unit = (self.pos - pos).normalize()
            norm = Vec(unit.y, -unit.x)
            vel = self.vel + self.spin * dist * norm
            return vel
        else:
            return self.vel

    def applyForce(self, pos, force, dt):
        self.force += force
        if pos != self.pos:
            dist = self.pos.distance_to(pos)
            unit = (self.pos - pos).normalize()
            norm = Vec(unit.y, -unit.x)
            spin = norm * force * dist
            self.torque += spin

    def replace(self, NewType):
        links = self.links.copy()
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
