from link import Link
from node import Node
import pygame


class JackLink(Link):
    maxLength = 3
    minLength = 0.5
    extentionSpeed = 0.5

    def __init__(self, node1, node2, world, extention=1.5):
        super().__init__(node1, node2, world, collisionGroup=1, density=2,
                         KP=40000, KD=500, KI=0, friction=2000, brakePoint=8000, color="#1144aa", radius=0.15,
                         indestructible=False, locked=False, drawingGroup=5, N=25, mu=0.6, startDelay=5)
        self.finalLength = self.length*extention
        self.bodyLength = min(self.length, self.length*extention)

    def update(self, dt):
        super().update(dt)
        if self.age > 0:
            self.length += min(JackLink.extentionSpeed, max(-JackLink.extentionSpeed, (
                    self.finalLength - self.length) * 0.5)) * dt

    def draw(self, camera):
        diff = self.node2.oldPos - self.node1.oldPos
        length = (diff.x ** 2 + diff.y ** 2) ** 0.5
        unit = diff / length
        norm = pygame.Vector2(unit.y, -unit.x)

        pct = min(abs(self.load) / self.brakePoint, 1)
        #        color = pygame.Color(int(pct * 255), int((1 - pct) * 255), 0)  # GN to RD
        color = pygame.Color(int(pct * 255), 0, 0)  # BK to RD

        pos1 = camera.posToScreen(self.node1.oldPos + norm * self.radius, self.world.screen)
        pos2 = camera.posToScreen(self.node2.oldPos + norm * self.radius, self.world.screen)
        pos3 = camera.posToScreen(self.node2.oldPos - norm * self.radius, self.world.screen)
        pos4 = camera.posToScreen(self.node1.oldPos - norm * self.radius, self.world.screen)

        pygame.draw.polygon(self.world.screen, "#888888", [pos1, pos2, pos3, pos4])
        pygame.draw.polygon(self.world.screen, color, [pos1, pos2, pos3, pos4], 2)

        pos = self.node2.oldPos - unit * (self.bodyLength - self.radius)
        pos1 = camera.posToScreen(self.node2.oldPos + norm * 0.2, self.world.screen)
        pos2 = camera.posToScreen(pos + norm * 0.2, self.world.screen)
        pos3 = camera.posToScreen(pos - norm * 0.2, self.world.screen)
        pos4 = camera.posToScreen(self.node2.oldPos - norm * 0.2, self.world.screen)
        pygame.draw.polygon(self.world.screen, self.color, [pos1, pos2, pos3, pos4])
        pygame.draw.polygon(self.world.screen, color, [pos1, pos2, pos3, pos4], 2)


class JackNode(Node):
    def __init__(self, pos, world):
        super().__init__(pos, world, collisionGroup=1, collideWithGroups=[], mass=4,
                         radius=0.2, color="#888888", indestructible=False, locked=False, drawingGroup=9, N=25,
                         mu=0.6)


class PullerLink(JackLink):
    def __init__(self, node1, node2, world, extention=0.5):
        super().__init__(node1, node2, world, extention)
