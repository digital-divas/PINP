import pygame
import os
from models.Tool import Tool


class PaintBucket(Tool):

    def __init__(self):
        super().__init__()

    def draw(self, screen, position):
        pencil_icon = pygame.image.load(os.path.join('images', 'paint_bucket.png'))
        self._position = position
        screen.blit(pencil_icon, (position[0], position[1]))

    def do_functionality(self, event, canvas, color_picker):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            canvas.draw_fill(event.pos, color_picker.primary_color)

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            canvas.draw_fill(event.pos, color_picker.secondary_color)