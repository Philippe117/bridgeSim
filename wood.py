from link import Link
from node import Node


class WoodLink(Link):
    maxLength = 2
    minLength = 0.5

    def __init__(self, node1, node2, world):
        super().__init__(node1, node2, world, collisionGroup=1, density=0.5,
                         KP=20000, KD=200, KI=0, friction=2, brakePoint=2000, color="#BA8E4A", radius=0.2,
                         indestructible=False, locked=False, drawingGroup=7, N=25, mu=1)

class WoodNode(Node):
    def __init__(self, pos, world):
        super().__init__(pos, world, collisionGroup=1, collideWithGroups=[], mass=1,
                         radius=0.2, color="#63462D", indestructible=False, locked=False, drawingGroup=9, N=25, mu=1)


