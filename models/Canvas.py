import pygame
from cv2 import cv2 as cv

from models.ToolPicker import TOOLPICKER_WIDTH
from models.Menubar import MENUBAR_HEIGHT
from models.ColorPicker import COLOR_PICKER_HEIGHT

def cvimage_to_pygame(image):
    """Convert cvimage into a pygame image"""

    return pygame.image.frombuffer(image.tostring(), image.shape[1::-1], "RGB")

class Canvas(object):

    def __init__(self):
        self.image = None
        self.surface = None
        self.left_margin = TOOLPICKER_WIDTH + 1
        self.top_margin = MENUBAR_HEIGHT + 1
        
    def __draw_resizeble_dots(self):

        height, width, _ = self.image.shape

        # 1 = margin
        top_margin = self.top_margin + 1
        # 1 = margin
        left_margin = self.left_margin + 1

        pygame.draw.rect(self.surface, (28, 36, 56), (left_margin, top_margin + 0, 3, 3), 0)
        pygame.draw.rect(self.surface, (255, 255, 255), (left_margin + 1, top_margin + 1, 2, 2), 0)

        pygame.draw.rect(self.surface, (28, 36, 56), (width + left_margin + 3, top_margin+ 0, 3, 3), 0)
        pygame.draw.rect(
            self.surface, (255, 255, 255), (width + left_margin + 4, top_margin+1, 2, 2), 0
        )

        pygame.draw.rect(self.surface, (28, 36, 56), (left_margin, top_margin + height + 3, 3, 3), 0)
        pygame.draw.rect(
            self.surface, (255, 255, 255), (left_margin + 1, top_margin + height + 3 + 1, 2, 2), 0
        )

        pygame.draw.rect(self.surface, (28, 36, 56), (width // 2 + left_margin + 3, top_margin + 0, 3, 3), 0)
        pygame.draw.rect(
            self.surface, (255, 255, 255), (width // 2 + left_margin + 4, top_margin + 1, 2, 2), 0
        )

        pygame.draw.rect(
            self.surface, (28, 36, 56), (left_margin, height // 2 + 3 + top_margin, 3, 3), 0
        )
        pygame.draw.rect(
            self.surface, (255, 255, 255), (left_margin + 1, height // 2 + 3 + 1 + top_margin, 2, 2), 0
        )

        pygame.draw.rect(
            self.surface, (28, 36, 56), (width + left_margin + 3, height + 3 + top_margin, 3, 3), 0
        )
        pygame.draw.rect(
            self.surface, (28, 36, 56), (width + left_margin + 3, height // 2 + 3 + top_margin, 3, 3), 0
        )
        pygame.draw.rect(
            self.surface, (28, 36, 56), (width // 2 + left_margin + 3, height + 3 + top_margin, 3, 3), 0
        )

    def __draw_image(self):
        # 1 = margin
        # 3 = resizable dots
        top_margin = self.top_margin + 1 + 3


        # 1 = margin
        # 3 = resizable dots
        left_margin = self.left_margin + 1 + 3

        self.surface.blit(cvimage_to_pygame(self.image), (left_margin, top_margin))

    def __draw_margin(self):
        pygame.draw.line(
            self.surface, (64, 64, 64), (TOOLPICKER_WIDTH+1, self.top_margin) , (self.surface.get_width(), self.top_margin)
        )
        pygame.draw.line(
            self.surface, (64, 64, 64), (TOOLPICKER_WIDTH+1, self.top_margin) , (TOOLPICKER_WIDTH+1, self.surface.get_height() - COLOR_PICKER_HEIGHT - 1)
        )
        pygame.draw.line(
            self.surface, (212,208,200), (TOOLPICKER_WIDTH+1, self.surface.get_height() - COLOR_PICKER_HEIGHT - 1) , (self.surface.get_width(), self.surface.get_height() - COLOR_PICKER_HEIGHT - 1)
        )

    def render(self, surface, image):

        self.image = image
        self.surface = surface
        
        self.__draw_resizeble_dots()
        self.__draw_image()
        self.__draw_margin()

    def draw_line(self, last_pos, pos, last_color, thickness):
        last_x, last_y = last_pos
        x, y = pos

        # 1 = margin
        # 3 = resizable dots
        last_x -= 3 + 1 + self.left_margin
        last_y -= 3 + 1 + self.top_margin
        x -= 3 + 1 + self.left_margin
        y -= 3 + 1 + self.top_margin

        cv.line(self.image, (last_x, last_y), (x, y), last_color, thickness)

    def draw_fill(self, pos, color):
        x, y = pos
        # 1 = margin
        # 3 = resizable dots
        x -= 3 + 1 + self.left_margin
        y -= 3 + 1 + self.top_margin

        theStack = [(x, y)]

        height, width, _ = self.image.shape

        try:
            original_color = [self.image[y][x][0], self.image[y][x][1], self.image[y][x][2]]
        except IndexError:
            return

        color = [color[0], color[1], color[2]]

        while len(theStack) > 0:
            x, y = theStack.pop()

            if x < 0 or y < 0:
                continue

            if x >= width or y >= height:
                continue

            if not all(self.image[y][x] == original_color):
                continue

            self.image[y][x] = color

            theStack.append((x + 1, y))  # right
            theStack.append((x - 1, y))  # left
            theStack.append((x, y + 1))  # down
            theStack.append((x, y - 1))  # up