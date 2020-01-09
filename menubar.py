import pygame

MENUBAR_HEIGHT = 21

class MenuBar(object):
    def __init__(self):
        self.height = MENUBAR_HEIGHT

    def draw(self, surface):
        pygame.draw.rect(surface, (212,208,200), (0, 0, surface.get_width(), self.height), 0)
        pygame.draw.line(surface, (128,128,128), (0, self.height), (surface.get_width(), self.height))