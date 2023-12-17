import pygame


class Camera:
    def __init__(self, screen, pos=pygame.Vector2(0, 0), zoom=1):
        self.zoom = zoom
        self.pos = pos
        self.screen = screen

    def posToScreen(self, pos):
        screenDim = pygame.Vector2(self.screen.get_width(), self.screen.get_height())
        return (pos - self.pos) * self.zoom + screenDim / 2

    def screenToPos(self, pos):
        screenDim = pygame.Vector2(self.screen.get_width(), self.screen.get_height())
        return (pos - screenDim / 2) / self.zoom + self.pos
