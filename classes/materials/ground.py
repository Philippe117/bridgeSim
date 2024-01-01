from classes.abstract.link import Link
from classes.abstract.node import Node


class GroundLink(Link):
    maxLength = 2
    minLength = 0.5

    def __init__(self, node1, node2, world):
        super().__init__(node1, node2, world, collisionGroup=0, density=2000,
                         KP=20000, KD=5000, KI=0, friction=200, brakePoint=2000, color="#004411", radius=0.2,
                         drawGroup=0, N=1, mu=1)


class GroundNode(Node):
    def __init__(self, pos, world):
        super().__init__(pos, world, collisionGroup=0, collideWith=[2, 3], density=2000,
                         radius=0.2, color="#004411", locked=True, drawGroup=9, N=1, mu=1, startDelay=0)
