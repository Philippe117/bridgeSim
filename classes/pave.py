from classes.abstract.link import Link
from classes.abstract.node import Node
from classes.abstract.destructible import Destructible


class PaveLink(Link, Destructible):
    maxLength = 2
    minLength = 0.5

    def __init__(self, node1, node2, world):
        super().__init__(node1=node1, node2=node2, world=world, collisionGroup=2, density=1,
                         KP=20000, KD=150, KI=0, friction=2, brakePoint=3000,
                         color="#222222", radius=0.2, drawGroup=5, N=25, mu=1)



class PaveNode(Node, Destructible):
    def __init__(self, pos, world):
        super().__init__(pos, world, collisionGroup=2, collideWith=[0, 3], mass=2,
                      radius=0.2, locked=False, color="#333333", drawGroup=9, N=25, mu=1)

    def update(self, dt):
        super().update(dt)
        self.torque += -self.angle * 0.1 - self.spin * 0.1

