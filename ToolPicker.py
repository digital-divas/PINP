import pygame
from color_picker import COLOR_PICKER_HEIGHT
from menubar import MENUBAR_HEIGHT

TOOLPICKER_WIDTH = 80

class ToolPicker:

    def __init__(self, screen, tools=[]):
        self.__screen = screen
        self.__tools = tools
        self.top_margin = MENUBAR_HEIGHT + 1

        # Draw on screen the Tool Picker
        self.draw()

    def draw(self):
        # Define the size and margin for each Tool
        TOOL_MARGIN = 6
        TOOL_SIZE = 30
        
        # Create the ToolPicker bar
        pygame.draw.rect(self.__screen, (212,208,200), (0, self.top_margin, TOOLPICKER_WIDTH, self.__screen.get_height() - COLOR_PICKER_HEIGHT - 1), 0)
        pygame.draw.line(self.__screen, (255,255,255), (0, self.top_margin), (TOOLPICKER_WIDTH, self.top_margin))
        pygame.draw.line(self.__screen, (128,128,128), (TOOLPICKER_WIDTH, self.top_margin), (TOOLPICKER_WIDTH, self.__screen.get_height() - COLOR_PICKER_HEIGHT - 1))
        pygame.draw.line(self.__screen, (128,128,128), (0, self.__screen.get_height() - COLOR_PICKER_HEIGHT - 1), (TOOLPICKER_WIDTH, self.__screen.get_height() - COLOR_PICKER_HEIGHT - 1))

        # If there is tools to add to ToolPicker
        if len(self.__tools) > 0:
            # Define the first tool initial position
            position = (TOOL_MARGIN, TOOL_MARGIN + self.top_margin, TOOL_SIZE, TOOL_SIZE)

            for index, tool in enumerate(self.__tools):
                # If is not the first tool, we need to change the position
                if index > 0:
                    # If is even, we change the row(height) to insert the tool on a new row
                    if index % 2 == 0:
                        position = (TOOL_MARGIN, (position[1] + TOOL_MARGIN + TOOL_SIZE), TOOL_SIZE, TOOL_SIZE)
                    # If is odd we change the position on X, to add beside the other
                    else:
                        position = ((position[0] + TOOL_SIZE + TOOL_MARGIN), position[1], TOOL_SIZE, TOOL_SIZE)
                # Draw the tool on screen
                tool.draw(position)

    def check_picked_tool(self, event):
        for tool in self.__tools:
            if tool.is_over(event.pos):
                tool.do_functionality()
