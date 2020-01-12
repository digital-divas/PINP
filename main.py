from cv2 import cv2 as cv
import pygame
from models.ColorPicker import ColorPicker
from models.Tool import Tool
from models.ToolPicker import ToolPicker
from models.Eraser import Eraser
from models.Pencil import Pencil
from models.PaintBucket import PaintBucket

from models.Menubar import MenuBar
from models.Canvas import Canvas

import subprocess

pygame.init()


def get_image(file_path=None):
    try:
        if file_path is None:
            file_path = subprocess.check_output(["zenity", "--file-selection"])
            file_path = file_path.decode("utf8").replace("\n", "")
        image = cv.imread(file_path)
        return cv.cvtColor(image, cv.COLOR_RGB2BGR)
    except subprocess.CalledProcessError:
        pass


def save_frame(frame):
    try:
        file_path = subprocess.check_output(
            ["zenity", "--file-selection", "--save", "--confirm-overwrite"]
        )
        file_path = file_path.decode("utf8").replace("\n", "")
        frame_to_be_saved = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        cv.imwrite(file_path, frame_to_be_saved)
    except subprocess.CalledProcessError:
        pass


EVENT_BUTTONS_TO_LISTEN = [1, 3]

image_rgb = get_image("test.jpg")

gameDisplay = pygame.display.set_mode((1280, 800), pygame.RESIZABLE)
pygame.display.set_caption("PINP - PINP Is Not msPaint")
tool = None
menu_bar = MenuBar()
canvas = Canvas()
color_picker = ColorPicker()
pencil = Pencil()
paint_bucket = PaintBucket()
eraser = Eraser()
tool_picker = ToolPicker([eraser, pencil, paint_bucket])

while True:

    gameDisplay.fill((128, 128, 128))
    menu_bar.draw(gameDisplay)
    color_picker.draw(gameDisplay)
    tool_picker.draw(gameDisplay)
    canvas.render(gameDisplay, image_rgb)

    for event in pygame.event.get():

        try:
            if tool and isinstance(tool, Tool):
                tool.do_functionality(event, canvas, color_picker)

            # Ctrl + O
            if event.type == pygame.KEYDOWN and event.unicode == "\x0f": 
                image_rgb = get_image()
            # Ctrl + S
            if event.type == pygame.KEYDOWN and event.unicode == "\x13":
                save_frame(image_rgb)

            if event.type == pygame.VIDEORESIZE:
                # FIXME
                print("resizing")
                # There's some code to add back window content here.
                # gameDisplay = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                old_surface_saved = gameDisplay
                gameDisplay = pygame.display.set_mode(
                    (event.w, event.h), pygame.RESIZABLE
                )
                # On the next line, if only part of the window
                # needs to be copied, there's some other options.
                gameDisplay.blit(old_surface_saved, (0, 0))
                del old_surface_saved

            if event.type == pygame.MOUSEBUTTONDOWN and event.button in EVENT_BUTTONS_TO_LISTEN:
                checked_tool = tool_picker.check_picked_tool(event)
                color_picker.check_picked_color(event)

                if checked_tool:
                    tool = checked_tool

        except AttributeError:
            pass

        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    pygame.display.update()
