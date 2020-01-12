import pygame
import os
from models.Tool import Tool


class Eraser(Tool):

    def __init__(self):
        super().__init__()

    def draw(self, screen, position):
        eraser_icon = pygame.image.load(os.path.join('images', 'eraser.png'))
        self._position = position
        screen.blit(eraser_icon, (position[0], position[1]))

    # TODO create eraser functionality
    def do_functionality(self, event, canvas, color_picker):
        print('Doing functionality!')