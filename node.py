# Example file showing a basic pygame "game loop"
import pygame
from object import object

#font = pygame.font.SysFont("silomttf", 48)

class Node(object):

    def __init__(self, pos=pygame.Vector2(0, 0), physic=True):
        # pos: pygame.Vector2
        # links: Link[]

        super().__init__()
        self.physic = physic
        self.pos = pos
        self.links = []
        self.vel = pygame.Vector2(0, 0)
        self.acc = pygame.Vector2(0, 0)
        self.force = pygame.Vector2(0, 0)
        self.mass = 20
        self.size = 0.3

    def addLink(self, link):
        self.links.append(link)

    def update(self, world, dt):
        if self.physic:
            self.force += world.gravity * self.mass
            self.force -= self.vel * (world.friction*self.size*self.size) / dt
            self.acc = self.force / self.mass
            self.vel += self.acc * dt
            self.pos += self.vel * dt

        self.force = pygame.Vector2(0, 0)

    def draw(self, screen, camera):
        pos = camera.posToScreen(self.pos, screen)

        color = "#0000ff"

        # Dessine le node
        pygame.draw.circle(screen, color, pos, self.size * camera.zoom)

        # Dessine le id
        font = pygame.font.SysFont("silomttf", 24)
        img = font.render(str(self.id), True, "#000000")
        screen.blit(img, pos)

    #def delete(self):
    #    for link in self.links:
   #         link.delete = True

    def delete(self):
        self.deleteFlag = True
        for link in self.links:
            link.delete()