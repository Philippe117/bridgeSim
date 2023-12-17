class Base:
    def __init__(self, world,
                 N: float, mu: float, radius: float, pos: object, collisionGroup: int, drawGroup: int, updateGroup: int, collideWith: list = None):
        # world, N, mu, radius, pos, collisionGroup, drawGroup, updateGroup, collideWith
        self.deleteFlag = False




        pass

    def update(self, dt):
        pass

    def delete(self):
        if not self.deleteFlag:
            self.deleteFlag = True

    def draw(self, camera):
        pass
