from classes.abstract.link import Link
from classes.abstract.node import Node
from classes.abstract.destructible import Destructible


class WoodLink(Link, Destructible):
    maxLength = 2
    minLength = 0.5

    def __init__(self, node1, node2, world):
        super().__init__(node1=node1, node2=node2, world=world, collisionGroup=1, density=500,
                         KP=20000, KD=8000, KI=0, friction=200, brakePoint=50000, color="#BA8E4A", radius=0.15,
                         drawGroup=7, N=1, mu=1)

class WoodNode(Node, Destructible):
    def __init__(self, pos, world):
        super().__init__(pos=pos, world=world, collisionGroup=1, collideWith=[], density=500,
                         radius=0.2, color="#63462D", locked=False, drawGroup=9, N=1, mu=1)

