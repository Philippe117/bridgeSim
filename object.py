from abc import ABC, abstractmethod


class Object(ABC):
  id = 0

  def __init__(self, pos, world, collisionGroup, collideWithGoups, drawingGroup, updateGroup):
    self.real = True
    self.physic = True
    self.mass = 1
    self.world = world
    self.deleteFlag = False
    self.id = Object.id
    Object.id += 1
    self.pos = pos
    self.collideWithGoups = collideWithGoups
    self.collisionGroup = self.world.collisionGroups[collisionGroup]
    self.collisionGroup.append(self)
    self.drawingGroup = self.world.drawingGroups[drawingGroup]
    self.drawingGroup.append(self)
    self.updateGroup = self.world.updateGroups[updateGroup]
    self.updateGroup.append(self)

  @abstractmethod
  def collide(self, other):
    raise NotImplementedError("Must override methodB")

  def update(self, dt):
    for collideWithGroup in self.collideWithGoups:
      for other in collideWithGroup:
        self.collide(other)

  @abstractmethod
  def draw(self, camera):
    raise NotImplementedError("Must override methodB")

  def delete(self):
    self.deleteFlag = True
    self.collisionGroup.remove(self)
    self.drawingGroup.remove(self)
    self.updateGroup.remove(self)
