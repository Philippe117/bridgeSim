
class object:
    id = 0

    def __init__(self):
        self.real = True
        self.physic = True
        self.mass = 1
        self.deleteFlag = False
        self.id = object.id
        object.id += 1

    def update(self, world, dt):
        pass

    def draw(self, screen, camera):
        pass

    def delete(self):
        pass