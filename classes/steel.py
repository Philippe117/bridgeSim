from classes.abstract.link import Link
from classes.abstract.node import Node
from classes.abstract.destructible import Destructible


class SteelLink(Link, Destructible):
    maxLength = 4
    minLength = 0.5

    def __init__(self, node1, node2, world):
        super().__init__(node1=node1, node2=node2, world=world, collisionGroup=1, density=2,
                         KP=30000, KD=100, KI=0, friction=2, brakePoint=8000, color="#883333", radius=0.2,
                         drawGroup=7, N=30, mu=0.6)


class SteelNode(Node, Destructible):
    def __init__(self, pos, world):
        super().__init__(pos=pos, world=world, collisionGroup=1, collideWith=[], mass=4,
                         radius=0.2, color="#883333", locked=False, drawGroup=9, N=30, mu=0.6)
