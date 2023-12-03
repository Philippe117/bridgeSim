import pygame
from threading import Thread
from node import Node
from link import Link
from camera import Camera

def funk(objects, dt):
  for object in objects:
    object.update(dt)
    if object.pos.y > 20:
      object.delete()


class World:
  def __init__(self, camera, screen, gravity=pygame.Vector2(0, 9.81), level=None):
    self.gravity = gravity
    super().__init__()
    self.nodes = []
    self.maxLinkLength = 2
    self.minLinkLength = 0.5
    self.camera = camera
    self.screen = screen
    self.friction = 50000
    self.collisionGroups = [[],[],[],[]]
    self.drawingGroups = [[],[],[],[]]
    self.updateGroups = [[],[],[],[]]
    self.level = level
    self.level(self)

  def start(self, dt, camera):
    # settle physic (Undestructible)
    overcompute = 2
    for i in range(overcompute):
      self.update(dt)

  def draw(self, camera):

    for drawingGroup in self.drawingGroups:
      for object in drawingGroup:
        object.draw(camera)

  def update(self, dt):
    overcompute = 20
    for i in range(overcompute):
      for updateGroup in self.updateGroups:
        for object in updateGroup:
          object.update(dt / overcompute)
          if object.pos.y > 20:
            object.delete()

  # Retourne une liste des nodes en ordre de distance
  # return [{"node": node, "dist": dist},..]
  def getNodesInRange(self, pos, range):
    proximities = []
    for node in self.nodes:
      diff = node.pos - pos
      dist = (diff.x ** 2 + diff.y ** 2) ** 0.5
      if dist < range:
        proximities.append({"node": node, "dist": dist})
    proximities.sort(key=sortProximity)
    return proximities


# Sert pour trier les nodes
def sortProximity(linkable):
  return linkable["dist"]
