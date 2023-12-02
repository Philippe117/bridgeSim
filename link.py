# Example file showing a basic pygame "game loop"
import pygame
from object import Object


class Link(Object):
  def __init__(self, node1, node2, world, collisionGroup, drawingGroup, updateGroup, physic=True):
    # node1: Node
    # node2: Node

    pos = (node1.pos + node2.pos) / 2
    super().__init__(pos, world, collisionGroup, [], drawingGroup, updateGroup)
    self.connectNode1(node1)
    self.connectNode2(node2)
    diff = self.node1.pos - self.node2.pos
    self.length = (diff.x ** 2 + diff.y ** 2) ** 0.5
    self.length2 = self.length*1
    self.physic = physic
    self.KP = 120000
    self.KD = 1000
    self.KI = 4000
    self.friction = 1000
    # self.KP = 60000
    # self.KD = 2000
    # self.KI = 50000
    # self.friction = 20
    self.i = 0
    self.mass = self.length*1
    self.load = 0
    self.load2 = 0
    self.brakePoint = 40000
    self.maxForce = (self.node1.mass + self.node2.mass)*2
    self.oldLoad = 0
    self.oldErr = 0
    self.delta = 0
    self.err = 0

  def connectNode1(self, node):
    self.node1 = node
    self.node1.addLink(self)

  def connectNode2(self, node):
    self.node2 = node
    self.node2.addLink(self)

  def draw(self, camera):
    pos1 = camera.posToScreen(self.node1.oldPos, self.world.screen)
    pos2 = camera.posToScreen(self.node2.oldPos, self.world.screen)

    pct = min(abs(self.load) / self.brakePoint, 1)
    color = pygame.Color(int(pct * 255), int((1 - pct) * 255), 0)
    pygame.draw.line(self.world.screen, color, pos1, pos2)

  def update(self, dt):
    if self.physic:
      diff = self.node1.pos - self.node2.pos
      length = (diff.x ** 2 + diff.y ** 2) ** 0.5
      unit = diff / length
      self.err = length - self.length

      self.err = self.err - sign(self.err)*0.0
      # if err > 0:
      #   err -=


      if abs(self.err) > 0.0:

        #delta = self.node1.vel.dot(unit) - self.node2.vel.dot(unit)
        self.delta = abs(self.err)*(self.err-self.oldErr)/dt
        #self.delta += ((self.err-self.oldErr)/dt-self.delta)*1
        self.oldErr = self.err
        self.i += self.err * dt

        self.load = self.err * self.KP + self.delta * self.KD + self.i * self.KI

        if abs(self.load) > self.brakePoint*0.5:
          self.length += (length - self.length) * 0.8
        self.length += (self.length2 - self.length) * 0.1

        if abs(self.load) > self.brakePoint or not self.node1 or not self.node2:
          load = self.load
          brakePoint = self.brakePoint
          self.delete()
        else:
          self.node1.force -= unit * self.load #/ len(self.node1.links)
          self.node2.force += unit * self.load #/ len(self.node2.links)
      else:
        self.node1.force += (self.node2.vel - self.node1.vel) * self.friction / length * dt
        self.node2.force += (self.node1.vel - self.node2.vel) * self.friction / length * dt

      self.node1.force += (self.node2.vel - self.node1.vel) * self.friction / length * dt
      self.node2.force += (self.node1.vel - self.node2.vel) * self.friction / length * dt


  def delete(self):
    super().delete()
    if not self.node1.deleteFlag:
      self.node1.links.remove(self)
    if not self.node2.deleteFlag:
      self.node2.links.remove(self)

  def collide(self, other):
    print("colliding with : " + str(other.id))


def sign(num):
  return -1 if num < 0 else 1
