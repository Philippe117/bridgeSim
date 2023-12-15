from link import Link
from node import Node
import pygame


class JackLink(Link):
    maxLength = 3
    minLength = 0.5
    extentionSpeed = 1

    def __init__(self, node1, node2, world, extention=1.5):
        super().__init__(node1, node2, world, collisionGroup=1, density=2,
                         KP=40000, KD=150, KI=0, friction=2, brakePoint=8000, color="#1144aa", radius=0.15,
                         indestructible=False, locked=False, drawingGroup=5, N=25, mu=0.6, startDelay=5)
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
        pct = min(abs(self.load) / self.brakePoint, 1)
        #        color = pygame.Color(int(pct * 255), int((1 - pct) * 255), 0)  # GN to RD
        color = pygame.Color(int(pct * 255), 0, 0)  # BK to RD

        pos1 = camera.posToScreen(self.node1.pos + self.norm * self.radius, self.world.screen)
        pos2 = camera.posToScreen(self.node2.pos + self.norm * self.radius, self.world.screen)
        pos3 = camera.posToScreen(self.node2.pos - self.norm * self.radius, self.world.screen)
        pos4 = camera.posToScreen(self.node1.pos - self.norm * self.radius, self.world.screen)

        pygame.draw.polygon(self.world.screen, "#888888", [pos1, pos2, pos3, pos4])
        pygame.draw.polygon(self.world.screen, color, [pos1, pos2, pos3, pos4], 2)

        pos = self.node2.pos - self.unit * (self.minLength - self.radius)
        pos1 = camera.posToScreen(self.node2.pos + self.norm * 0.2, self.world.screen)
        pos2 = camera.posToScreen(pos + self.norm * 0.2, self.world.screen)
        pos3 = camera.posToScreen(pos - self.norm * 0.2, self.world.screen)
        pos4 = camera.posToScreen(self.node2.pos - self.norm * 0.2, self.world.screen)
        pygame.draw.polygon(self.world.screen, self.color, [pos1, pos2, pos3, pos4])
        pygame.draw.polygon(self.world.screen, color, [pos1, pos2, pos3, pos4], 2)

    def sclollAction(self, direction):
        self.cmdLength = max(self.minLength, min(self.maxLength, self.curLength + direction * JackLink.extentionSpeed/4))
        return True


class JackNode(Node):
    def __init__(self, pos, world):
        super().__init__(pos, world, collisionGroup=1, collideWithGroups=[], mass=4,
                         radius=0.2, color="#888888", indestructible=False, locked=False, drawingGroup=9, N=25,
                         mu=0.6)


class PullerLink(JackLink):
    def __init__(self, node1, node2, world, extention=0.5):
        super().__init__(node1, node2, world, extention)
