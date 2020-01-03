import pygame
from color_picker import (
    draw_color_picker,
    get_primary_color,
    get_secondary_color,
    check_picked_color,
)

pygame.init()

gameDisplay = pygame.display.set_mode((1280, 800), pygame.RESIZABLE)
pygame.display.set_caption("PINP - PINP Is Not msPaint")
gameDisplay.fill((255, 255, 255))

drawing = False
last_pos = (0, 0)

PENCIL = 0
tool = PENCIL
FILL = 1

last_color = None


def pencil_events(event):
    global drawing, last_pos, last_color

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
        pygame.draw.line(gameDisplay, last_color, last_pos, event.pos, 1)
        last_pos = event.pos


def recursive_draw(pos, original_color, color):
    x, y = pos

    theStack = [(x, y)]

    width = gameDisplay.get_width()
    height = gameDisplay.get_height()

    while len(theStack) > 0:

        x, y = theStack.pop()

        if x < 0 or y < 0:
            continue

        if x >= width or y > height:
            continue

        if gameDisplay.get_at((x, y)) != original_color:
            continue

        gameDisplay.set_at((x, y), color)

        theStack.append((x + 1, y))  # right
        theStack.append((x - 1, y))  # left
        theStack.append((x, y + 1))  # down
        theStack.append((x, y - 1))  # up


def fill_events(event):

    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
        original_color = gameDisplay.get_at(event.pos)
        recursive_draw(event.pos, original_color, get_primary_color())

    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
        original_color = gameDisplay.get_at(event.pos)
        recursive_draw(event.pos, original_color, get_secondary_color())


while True:

    for event in pygame.event.get():

        try:

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
        except AttributeError:
            pass

        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    draw_color_picker(gameDisplay)

    pygame.display.update()
