from pygame import Vector2 as Vec
from classes.abstract.updatable import Updatable


class Camera(Updatable):
    def __init__(self, world, screen, pos=Vec(0, 0), zoom=1):
        super().__init__(world=world, updateGroup=1)
        self.zoom = zoom
        self.pos = pos
        self.screen = screen
        self.update(0.01)

    def update(self, dt):
        self.screenDim = Vec(self.screen.get_width(), self.screen.get_height())/2

    def posToScreen(self, pos: Vec):
        pos2 = (pos - self.pos) * self.zoom + self.screenDim
        pos2.y = self.screen.get_height()-pos2.y
        return pos2

    def screenToPos(self, pos: Vec):
        return (Vec(pos.x, self.screen.get_height()-pos.y) - self.screenDim) / self.zoom + self.pos

    def zoomInOut(self, pos, zoom):
        self.zoom *= 1+zoom
        self.pos += (pos-self.pos)*(1-1/(1+zoom))
