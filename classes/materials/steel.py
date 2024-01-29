from classes.abstract.link import Link
from classes.abstract.node import Node
from classes.abstract.destructible import Destructible


class SteelLink(Link, Destructible):
    maxLength = 5
    minLength = 0.5

    def __init__(self, node1, node2, world):
        super().__init__(node1=node1, node2=node2, world=world, collisionGroup=-1, density=800,
                         KP=1, KD=1, friction=1, brakePoint=1, color="#883333", radius=0.1,
                         drawGroup=7, N=1, mu=1, thickness=0.5)


class SteelNode(Node, Destructible):
    def __init__(self, pos, world):
        super().__init__(pos=pos, world=world, collisionGroup=1, collideWith=[], density=800,
                         radius=0.2, color="#883333", locked=False, drawGroup=9, N=1, mu=1, thickness=0.5)
