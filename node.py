# Example file showing a basic pygame "game loop"
import pygame
from object import Object
from copy import copy

# font = pygame.font.SysFont("silomttf", 48)

class Node(Object):

  def __init__(self, pos, world, collisionGroup, collideWithGoups, drawingGroup, updateGroup, physic=True):
    # pos: pygame.Vector2
    # links: Link[]

    super().__init__(pos, world, collisionGroup, collideWithGoups, drawingGroup, updateGroup)
    self.physic = physic
    self.links = []
    self.vel = pygame.Vector2(0, 0)
    self.acc = pygame.Vector2(0, 0)
    self.force = pygame.Vector2(0, 0)
    self.mass = 20
    self.size = 0.3
    self.world.nodes.append(self)
    self.age = 0
    self.oldVel = copy(self.vel)
    self.oldPos = copy(self.pos)

  def addLink(self, link):
    self.links.append(link)

  def update(self, dt):
    if self.physic:
      self.force += self.world.gravity * self.mass * min(1, self.age*1)
      self.force -= self.vel * (self.world.friction * self.size * self.size) * dt
      self.acc = self.force / self.mass
      self.vel += self.acc * dt
      # if (self.vel.x > 0 ) != (self.oldVel.x > 0 ):
      #   self.vel *= 0.01
      # if (self.vel.y > 0 ) != (self.oldVel.y > 0 ):
      #   self.vel *= 0.01
      self.pos += self.vel * dt
      self.oldPos += (self.pos-self.oldPos)*0.1


      # diff = self.pos-self.oldPos
      # dist = (diff.x**2+diff.y**2)**0.5
      # if dist < 0.01:
      #   self.pos = self.oldPos
      #   self.vel *= 0.9

    self.force = pygame.Vector2(0, 0)
    self.age += dt

  def draw(self, camera):
    pos = camera.posToScreen(self.oldPos, self.world.screen)

    color = "#0000ff"

    # Dessine le node
    pygame.draw.circle(self.world.screen, color, pos, self.size * camera.zoom)

    # Dessine le id
    font = pygame.font.SysFont("silomttf", 24)
    img = font.render(str(self.id), True, "#000000")
    self.world.screen.blit(img, pos)

  # def delete(self):
  #    for link in self.links:
  #         link.delete = True

  def delete(self):
    super().delete()
    self.world.nodes.remove(self)
    for link in self.links:
      link.delete()

  def collide(self, other):
    print("colliding with : " + str(other.id))
