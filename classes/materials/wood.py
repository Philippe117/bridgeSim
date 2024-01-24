from classes.abstract.link import Link
from classes.abstract.node import Node
from classes.abstract.destructible import Destructible

1
class WoodLink(Link, Destructible):
    maxLength = 2
    minLength = 0.5

    def __init__(self, node1, node2, world):
        super().__init__(node1=node1, node2=node2, world=world, collisionGroup=1, density=800,
                         KP=0.6, KD=0.9, friction=1, brakePoint=0.65, color="#BA8E4A", radius=0.15,
                         drawGroup=7, N=1, mu=1, thickness=0.5)

class WoodNode(Node, Destructible):
    def __init__(self, pos, world):
        super().__init__(pos=pos, world=world, collisionGroup=1, collideWith=[], density=800,
                         radius=0.2, color="#63462D", locked=False, drawGroup=9, N=1, mu=1, thickness=0.5)

