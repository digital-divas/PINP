import pygame
import os
from Tool import Tool

class Eraser(Tool):

    def __init__(self, screen):
        self.__screen = screen
        # Position on X, Y, Width and Height
        self.__position = (0, 0, 0, 0)

    def draw(self, position):
        eraser_icon = pygame.image.load(os.path.join('images', 'eraser.png'))
        self.__position = position
        self.__screen.blit(eraser_icon, (position[0], position[1]))

    def __is_over_axis_x(self, x_position):
        if x_position >= self.__position[0] and x_position <= self.__position[0] + self.__position[2]:
            return True
        
        return False

    def __is_over_axis_y(self, y_position):
        if y_position >= self.__position[1] and y_position <= self.__position[1] + self.__position[3]:
            return True

        return False

    def is_over(self, position):
        if self.__is_over_axis_x(position[0]) and self.__is_over_axis_y(position[1]):
            return True

    # TODO create eraser functionality
    def do_functionality(self):
        print('Doing functionality!')