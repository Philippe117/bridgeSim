from classes.abstract.link import Link
from classes.abstract.node import Node
from classes.abstract.destructible import Destructible


class PaveLink(Link, Destructible):
    maxLength = 2
    minLength = 0.5

    def __init__(self, node1, node2, world):
        super().__init__(node1=node1, node2=node2, world=world, collisionGroup=2, density=1600,
                         KP=1, KD=1, friction=1, brakePoint=80000,
                         color="#222222", radius=0.2, drawGroup=5, N=1, mu=1, thickness=2)



class PaveNode(Node, Destructible):
    def __init__(self, pos, world):
        super().__init__(pos, world, collisionGroup=-1, collideWith=[0], density=1600,
                      radius=0.2, locked=False, color="#333333", drawGroup=9, N=1, mu=1, thickness=2)

    def update(self, dt):
        super().update(dt)
        self.torque += -self.angle * self.momentInertia * 150 - self.spin * self.momentInertia * 150

