import pygame

# Constraints
COLOR_PICKER_HEIGHT = 55

class ColorPicker:
    DEFAULT_COLORS = [
        (0, 0, 0),
        (255, 255, 255),
        (128, 128, 128),
        (192, 192, 192),
        (128, 0, 0),
        (255, 0, 0),
        (128, 128, 0),
        (255, 255, 0),
        (0, 128, 0),
        (0, 255, 0),
        (0, 128, 128),
        (0, 255, 255),
        (0, 0, 128),
        (0, 0, 255),
        (128, 0, 128),
        (255, 0, 255),
        (128, 128, 64),
        (255, 255, 128),
        (0, 64, 64),
        (0, 255, 128),
        (0, 128, 255),
        (128, 255, 255),
        (0, 64, 128),
        (128, 128, 255),
        (64, 0, 255),
        (255, 0, 128),
        (128, 64, 0),
        (255, 128, 64),
    ]
    BLOCK_SIZE = 20

    def __init__(self):
        self._primary_color = (0, 0, 0)
        self._secondary_color = (255, 255, 255)
        self._color_positions = []

    @property
    def primary_color(self):
        return self._primary_color

    def __set_primary_color(self, color):
        self._primary_color = color

    @property
    def secondary_color(self):
        return self._secondary_color

    def __set_secondary_color(self, color):
        self._secondary_color = color

    def draw(self, screen):
        left_margin = 85
        top_margin = screen.get_height() - COLOR_PICKER_HEIGHT

        pygame.draw.rect(screen, (212, 208, 200), (0, top_margin, screen.get_width(), COLOR_PICKER_HEIGHT), 0)
        pygame.draw.rect(screen, (255, 255, 255), (left_margin - 3, screen.get_height() - 52, 352, 49), 0)

        for index, default_color in enumerate(self.DEFAULT_COLORS):
            if index % 2 == 0:
                start_point = (left_margin + (index / 2 * 5) + (index / 2 * self.BLOCK_SIZE),
                               screen.get_height() - 5 - self.BLOCK_SIZE - self.BLOCK_SIZE - 5)

                pygame.draw.rect(
                    screen,
                    default_color,
                    (start_point[0], start_point[1], self.BLOCK_SIZE, self.BLOCK_SIZE),
                    0,
                )
            else:
                start_point = (
                left_margin + ((index - 1) / 2 * 5) + ((index - 1) / 2 * self.BLOCK_SIZE), screen.get_height() - 5 - self.BLOCK_SIZE)

                pygame.draw.rect(
                    screen,
                    default_color,
                    (start_point[0], start_point[1], self.BLOCK_SIZE, self.BLOCK_SIZE),
                    0,
                )

            self._color_positions.append(
                (start_point[0], start_point[1], start_point[0] + self.BLOCK_SIZE, start_point[1] + self.BLOCK_SIZE))

            pygame.draw.line(screen, (0, 0, 0), start_point, (start_point[0], start_point[1] + self.BLOCK_SIZE))
            pygame.draw.line(screen, (0, 0, 0), start_point, (start_point[0] + self.BLOCK_SIZE, start_point[1]))

            pygame.draw.line(screen, (212, 208, 200), (start_point[0] + self.BLOCK_SIZE, start_point[1] + self.BLOCK_SIZE),
                             (start_point[0], start_point[1] + self.BLOCK_SIZE))
            pygame.draw.line(screen, (212, 208, 200), (start_point[0] + self.BLOCK_SIZE, start_point[1] + self.BLOCK_SIZE),
                             (start_point[0] + self.BLOCK_SIZE, start_point[1]))

        pygame.draw.rect(screen, self.secondary_color,
                         (25 + (self.BLOCK_SIZE // 2), screen.get_height() - 45 + (self.BLOCK_SIZE // 2), self.BLOCK_SIZE, self.BLOCK_SIZE), 0)
        pygame.draw.rect(screen, self.primary_color, (25, screen.get_height() - 45, self.BLOCK_SIZE, self.BLOCK_SIZE), 0)

        pygame.draw.line(screen, (255, 255, 255), (0, top_margin), (screen.get_width(), top_margin))
        pygame.draw.line(screen, (128, 128, 128), (0, screen.get_height() - 1), (screen.get_width(), screen.get_height() - 1))

    def __check_positions(self, pos, color_method):
        for index, color_position in enumerate(self._color_positions):
            if color_position[0] < pos[0] < color_position[2] and color_position[1] < pos[1] < color_position[3]:
                color_method(self.DEFAULT_COLORS[index])
                print(self.primary_color)
                print(self.secondary_color)
                break

    def check_picked_color(self, event):
        if event.button == 1:
            self.__check_positions(event.pos, self.__set_primary_color)

        if event.button == 3:
            self.__check_positions(event.pos, self.__set_secondary_color)