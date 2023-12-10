import pygame


class Camera:
    def __init__(self, pos=pygame.Vector2(0, 0), zoom=1):
        self.zoom = zoom
        self.pos = pos

    def posToScreen(self, pos, screen):
        screenDim = pygame.Vector2(screen.get_width(), screen.get_height())
        return (pos - self.pos) * self.zoom + screenDim / 2

    def screenToPos(self, pos, screen):
        screenDim = pygame.Vector2(screen.get_width(), screen.get_height())
        return (pos - screenDim / 2) / self.zoom + self.pos
