class Base:
    def __init__(self, *args, **kargs):
        self.deleteFlag = False

    def update(self, dt):
        pass

    def delete(self):
        if not self.deleteFlag:
            self.deleteFlag = True

    def draw(self, camera):
        pass
