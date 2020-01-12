import pygame
import os
from models.Tool import Tool


class Pencil(Tool):

    def __init__(self):
        super().__init__()
        self._drawing = False
        self._last_pos = (0, 0)
        self._last_color = None

    def draw(self, screen, position):
        pencil_icon = pygame.image.load(os.path.join('images', 'pencil.png'))
        self._position = position
        screen.blit(pencil_icon, (position[0], position[1]))

    def do_functionality(self, event, canvas, color_picker):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self._drawing = True
            self._last_pos = event.pos
            self._last_color = color_picker.primary_color
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            self._drawing = True
            self._last_pos = event.pos
            self._last_color = color_picker.secondary_color
        if event.type == pygame.MOUSEBUTTONUP:
            self._drawing = False

        if self._drawing:
            canvas.draw_line(self._last_pos, event.pos, self._last_color, 1)
            self._last_pos = event.pos