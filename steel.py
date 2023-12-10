from link import Link
from node import Node


class SteelLink(Link):
    maxLength = 4
    minLength = 0.5

    def __init__(self, node1, node2, world):
        super().__init__(node1, node2, world, collisionGroup=1, density=2,
                         KP=20000, KD=10, KI=0, friction=2000, brakePoint=2000, color="#883333", radius=0.2, indestructible=False, locked=False, drawingGroup=2, N=25, mu=1)


class SteelNode(Node):
    def __init__(self, pos, world):
        super().__init__(pos, world, collisionGroup=1, collideWithGoups=[], mass=4,
                         radius=0.2, color="#883333", indestructible=False, locked=False, drawingGroup=3, N=25, mu=1)
