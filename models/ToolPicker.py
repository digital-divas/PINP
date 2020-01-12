import pygame
from models.ColorPicker import COLOR_PICKER_HEIGHT
from models.Menubar import MENUBAR_HEIGHT

TOOLPICKER_WIDTH = 80

class ToolPicker:

    def __init__(self, tools=[]):
        self._tools = tools
        self.top_margin = MENUBAR_HEIGHT + 1

    def draw(self, screen):
        # Define the size and margin for each Tool
        TOOL_MARGIN = 6
        TOOL_SIZE = 30
        
        # Create the ToolPicker bar
        pygame.draw.rect(screen, (212,208,200), (0, self.top_margin, TOOLPICKER_WIDTH, screen.get_height() - COLOR_PICKER_HEIGHT - 1 - self.top_margin), 0)
        pygame.draw.line(screen, (255,255,255), (0, self.top_margin), (TOOLPICKER_WIDTH, self.top_margin))
        pygame.draw.line(screen, (128,128,128), (TOOLPICKER_WIDTH, self.top_margin), (TOOLPICKER_WIDTH, screen.get_height() - COLOR_PICKER_HEIGHT - 1))
        pygame.draw.line(screen, (128,128,128), (0, screen.get_height() - COLOR_PICKER_HEIGHT - 1), (TOOLPICKER_WIDTH, screen.get_height() - COLOR_PICKER_HEIGHT - 1))

        # If there is tools to add to ToolPicker
        if len(self._tools) > 0:
            # Define the first tool initial position
            position = (TOOL_MARGIN, TOOL_MARGIN + self.top_margin, TOOL_SIZE, TOOL_SIZE)

            for index, tool in enumerate(self._tools):
                # If is not the first tool, we need to change the position
                if index > 0:
                    # If is even, we change the row(height) to insert the tool on a new row
                    if index % 2 == 0:
                        position = (TOOL_MARGIN, (position[1] + TOOL_MARGIN + TOOL_SIZE), TOOL_SIZE, TOOL_SIZE)
                    # If is odd we change the position on X, to add beside the other
                    else:
                        position = ((position[0] + TOOL_SIZE + TOOL_MARGIN), position[1], TOOL_SIZE, TOOL_SIZE)
                # Draw the tool on screen
                tool.draw(screen, position)

    def check_picked_tool(self, event):
        for tool in self._tools:
            if tool.is_over(event.pos):
                return tool

        return None
