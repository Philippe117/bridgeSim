from abc import ABC, abstractmethod


class Object(ABC):
    id = 0

    def __init__(self, pos, world, collisionGroup, collideWithGroups, drawingGroup, updateGroup, radius=1, locked=False,
                 indestructible=False, N=1, mu=1, mass=1, startDelay=5):
        self.real = True
        self.physic = True
        self.mass = mass
        self.world = world
        self.deleteFlag = False
        self.id = Object.id
        self.locked = locked
        self.indestructible = indestructible
        Object.id += 1
        self.pos = pos
        self.age = -startDelay
        self.collideWithGroups = collideWithGroups
        if collisionGroup >= 0:
            self.collisionGroup = self.world.collisionGroups[collisionGroup]
            self.collisionGroup.append(self)
        else:
            self.collisionGroup = None
        if drawingGroup >= 0:
            self.drawingGroup = self.world.drawingGroups[drawingGroup]
            self.drawingGroup.append(self)
        else:
            self.drawingGroup = None
        if updateGroup >= 0:
            self.updateGroup = self.world.updateGroups[updateGroup]
            self.updateGroup.append(self)
        else:
            self.updateGroup = None
        self.radius = radius
        self.N = N
        self.mu = mu

    @abstractmethod
    def getDistance(self, pos, maxDist=10):
        # Retourne la position et la velocité du point de contact
        raise NotImplementedError("Must override collideCheck")

    @abstractmethod
    def getContactPos(self, pos, radius):
        # Retourne la position et la velocité du point de contact
        raise NotImplementedError("Must override collideCheck")

    @abstractmethod
    def collide(self, pos, force, vel, friction):
        raise NotImplementedError("Must override collide")

    # Routine qui permet de faire des actions si requis
    def sclollAction(self, direction):
        return None

    def update(self, dt):
        if not self.deleteFlag:
            for collideWithGroup in self.collideWithGroups:
                for other in self.world.collisionGroups[collideWithGroup]:
                    pos, force = other.getContactPos(self.pos, self.radius)
                    if pos:
                        vel1 = self.getVelAtPoint(pos)
                        vel2 = other.getVelAtPoint(pos)
                        velDiff = vel1 - vel2
                        friction = self.mu * other.mu
                        restitution = force * self.N * other.N
                        self.collide(pos, restitution, velDiff, friction)
                        other.collide(pos, -restitution, -velDiff, friction)

        self.age += dt

    @abstractmethod
    def draw(self, camera):
        raise NotImplementedError("Must override draw")

    @abstractmethod
    def getVelAtPoint(self, pos):
        raise NotImplementedError("Must override getVelAtPoint")

    def delete(self):
        self.deleteFlag = True
        if self in self.collisionGroup:
            self.collisionGroup.remove(self)
        if self in self.drawingGroup:
            self.drawingGroup.remove(self)
        if self in self.updateGroup:
            self.updateGroup.remove(self)
