from cv2 import cv2 as cv
import pygame
from ToolPicker import ToolPicker
from Eraser import Eraser
from color_picker import (
    draw_color_picker,
    get_primary_color,
    get_secondary_color,
    check_picked_color,
)

import subprocess


def cvimage_to_pygame(image):
    """Convert cvimage into a pygame image"""

    return pygame.image.frombuffer(image_rgb.tostring(), image_rgb.shape[1::-1], "RGB")


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


image_rgb = get_image("test.jpg")

gameDisplay = pygame.display.set_mode((1280, 800), pygame.RESIZABLE)
pygame.display.set_caption("PINP - PINP Is Not msPaint")

drawing = False
last_pos = (0, 0)

PENCIL = 0
tool = PENCIL
FILL = 1

last_color = None


def pencil_events(event):
    global drawing, last_pos, last_color, image_rgb

    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
        drawing = True
        last_pos = event.pos
        last_color = get_primary_color()
    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
        drawing = True
        last_pos = event.pos
        last_color = get_secondary_color()
    if event.type == pygame.MOUSEBUTTONUP:
        drawing = False

    if drawing:
        last_x, last_y = last_pos
        x, y = event.pos

        # TODO: replace these number with canvas margin
        last_x -= 83
        last_y -= 3
        x -= 83
        y -= 3
        cv.line(image_rgb, (last_x, last_y), (x, y), last_color, 1)
        last_pos = event.pos


def recursive_draw(pos, color):
    global image_rgb
    x, y = pos
    # TODO: replace these number with canvas margin
    x -= 83
    y -= 3

    theStack = [(x, y)]

    height, width, _ = image_rgb.shape

    try:
        original_color = [image_rgb[y][x][0], image_rgb[y][x][1], image_rgb[y][x][2]]
    except IndexError:
        return

    color = [color[0], color[1], color[2]]

    while len(theStack) > 0:

        x, y = theStack.pop()

        if x < 0 or y < 0:
            continue

        if x >= width or y >= height:
            continue

        if not all(image_rgb[y][x] == original_color):
            continue

        image_rgb[y][x] = color

        theStack.append((x + 1, y))  # right
        theStack.append((x - 1, y))  # left
        theStack.append((x, y + 1))  # down
        theStack.append((x, y - 1))  # up


def fill_events(event):

    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
        recursive_draw(event.pos, get_primary_color())

    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
        recursive_draw(event.pos, get_secondary_color())


while True:

    gameDisplay.fill((128, 128, 128))

    draw_color_picker(gameDisplay)
    eraser = Eraser(gameDisplay)
    tool_picker = ToolPicker(gameDisplay, [eraser])

    for event in pygame.event.get():

        try:

            # Ctrl + O
            if event.type == pygame.KEYDOWN and event.unicode == "\x0f": 
                image_rgb = get_image()
            # Ctrl + S
            if event.type == pygame.KEYDOWN and event.unicode == "\x13":
                save_frame(image_rgb)

            if event.type == pygame.KEYDOWN and event.key == 49:
                tool = PENCIL
            elif event.type == pygame.KEYDOWN and event.key == 50:
                tool = FILL
            elif event.type == pygame.VIDEORESIZE:
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

            if tool == PENCIL:
                pencil_events(event)
            elif tool == FILL:
                fill_events(event)

            check_picked_color(event)

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # TODO Assign according the functionality to the cursor
                # according to the tool selected
                tool_picker.check_picked_tool(event)

        except AttributeError:
            pass

        if event.type == pygame.QUIT:
            pygame.quit()
            quit()


    # TODO: this need to be dynamic
    left_margin = 83

    gameDisplay.blit(cvimage_to_pygame(image_rgb), (left_margin, 3))

    height, width, _ = image_rgb.shape

    pygame.draw.rect(gameDisplay, (28, 36, 56), (left_margin - 3, 0, 3, 3), 0)
    pygame.draw.rect(gameDisplay, (255, 255, 255), (left_margin - 2, 1, 2, 2), 0)

    pygame.draw.rect(gameDisplay, (28, 36, 56), (width + left_margin, 0, 3, 3), 0)
    pygame.draw.rect(
        gameDisplay, (255, 255, 255), (width + left_margin + 1, 1, 2, 2), 0
    )

    pygame.draw.rect(gameDisplay, (28, 36, 56), (left_margin - 3, height + 3, 3, 3), 0)
    pygame.draw.rect(
        gameDisplay, (255, 255, 255), (left_margin - 2, height + 3 + 1, 2, 2), 0
    )

    pygame.draw.rect(gameDisplay, (28, 36, 56), (width // 2 + left_margin, 0, 3, 3), 0)
    pygame.draw.rect(
        gameDisplay, (255, 255, 255), (width // 2 + left_margin + 1, 1, 2, 2), 0
    )

    pygame.draw.rect(
        gameDisplay, (28, 36, 56), (left_margin - 3, height // 2 + 3, 3, 3), 0
    )
    pygame.draw.rect(
        gameDisplay, (255, 255, 255), (left_margin - 2, height // 2 + 3 + 1, 2, 2), 0
    )

    pygame.draw.rect(
        gameDisplay, (28, 36, 56), (width + left_margin, height + 3, 3, 3), 0
    )
    pygame.draw.rect(
        gameDisplay, (28, 36, 56), (width + left_margin, height // 2 + 3, 3, 3), 0
    )
    pygame.draw.rect(
        gameDisplay, (28, 36, 56), (width // 2 + left_margin, height + 3, 3, 3), 0
    )

    draw_color_picker(gameDisplay)

    pygame.display.update()
