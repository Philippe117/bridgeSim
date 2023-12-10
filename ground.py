from link import Link
from node import Node


class GroundLink(Link):
    maxLength = 2
    minLength = 0.5

    def __init__(self, node1, node2, world):
        super().__init__(node1, node2, world, collisionGroup=0, density=0.5,
                         KP=100000, KD=50, KI=0, friction=2000, brakePoint=2000, color="#004411", radius=0.2,
                         indestructible=True, locked=True, drawingGroup=0, N=30, mu=1)


class GroundNode(Node):
    def __init__(self, pos, world):
        super().__init__(pos, world, collisionGroup=0, collideWithGoups=[], mass=1,
                         radius=0.2, color="#004411", indestructible=True, locked=True, drawingGroup=1, N=30, mu=1)
