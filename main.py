import pygame
from color_picker import draw_color_picker, get_primary_color, get_secondary_color, set_primary_color

pygame.init()

gameDisplay = pygame.display.set_mode((1280, 800), pygame.RESIZABLE)
pygame.display.set_caption("PINP - PINP Is Not msPaint")
gameDisplay.fill((255, 255, 255))

drawing = False
last_pos = (0, 0)

PENCIL = 0
tool = PENCIL
FILL = 1


def pencil_events(event, color):
    global drawing, last_pos

    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
        drawing = True
        last_pos = event.pos
    if event.type == pygame.MOUSEBUTTONUP:
        drawing = False

    if drawing:
        pygame.draw.line(gameDisplay, color, last_pos, event.pos, 1)
        last_pos = event.pos


def recursive_draw(pos, original_color, color):
    x, y = pos

    if x - 1 > 0 and gameDisplay.get_at((x - 1, y)) == original_color:
        gameDisplay.set_at((x - 1, y), color)
        recursive_draw((x - 1, y), original_color)

    if x + 1 < 800 and gameDisplay.get_at((x + 1, y)) == original_color:
        gameDisplay.set_at((x + 1, y), color)
        recursive_draw((x + 1, y), original_color)

    if gameDisplay.get_at((x, y - 1)) == original_color:
        gameDisplay.set_at((x, y - 1), color)
        recursive_draw((x, y - 1), original_color)

    if gameDisplay.get_at((x, y + 1)) == original_color:
        gameDisplay.set_at((x, y + 1), color)
        recursive_draw((x, y + 1), original_color)


def draw_to_left(pos, original_color, color):

    x, y = pos

    while True:
        if x > 0 and gameDisplay.get_at((x, y)) == original_color:
            gameDisplay.set_at((x, y), color)
            draw_to_up((x, y), original_color)
            draw_to_down((x, y), original_color)
            x -= 1
        else:
            break


def draw_to_up(pos, original_color, color):

    x, y = pos

    while True:
        if y > 0 and gameDisplay.get_at((x, y - 1)) == original_color:
            gameDisplay.set_at((x, y - 1), color)
            y -= 1
        else:
            break


def draw_to_down(pos, original_color, color):
    x, y = pos

    while True:
        if y < 599 and gameDisplay.get_at((x, y + 1)) == original_color:
            gameDisplay.set_at((x, y + 1), color)
            y += 1
        else:
            break


cur_direction = (-1, 0)
backtrack = False
findloop = False
mark = None
mark2 = None
mark_direction = None
mark2_direction = None


def is_filled(pos, original_color):
    x, y = pos
    return (
        x < 0
        or x >= 800
        or y < 0
        or y >= 600
        or gameDisplay.get_at((x, y)) != original_color
    )


def is_empty(pos, original_color):
    x, y = pos
    return (
        800 > x >= 0 and 600 > y >= 0 and gameDisplay.get_at((x, y)) == original_color
    )


def is_front_filled(pos, original_color):
    global cur_direction
    x, y = pos
    return is_filled((x + cur_direction[0], y + cur_direction[1]), original_color)


def is_front_empty(pos, original_color):
    global cur_direction
    x, y = pos
    return is_empty((x + cur_direction[0], y + cur_direction[1]), original_color)


def is_back_filled(pos, original_color):
    global cur_direction
    x, y = pos
    return is_filled((x - cur_direction[0], y - cur_direction[1]), original_color)


def is_back_empty(pos, original_color):
    global cur_direction
    x, y = pos
    return is_empty((x - cur_direction[0], y - cur_direction[1]), original_color)


def is_front_left_empty(pos, original_color):
    global cur_direction
    x, y = pos
    x += cur_direction[0]
    y += cur_direction[1]
    turn_left()
    x += cur_direction[0]
    y += cur_direction[1]
    turn_right()
    return is_empty((x, y), original_color)


def move_foward(pos):
    global cur_direction
    x, y = pos
    return x + cur_direction[0], y + cur_direction[1]


def is_back_left_empty(pos, original_color):
    global cur_direction
    x, y = pos
    x -= cur_direction[0]
    y -= cur_direction[1]
    turn_left()
    x -= cur_direction[0]
    y -= cur_direction[1]
    turn_right()
    return is_empty((x, y), original_color)


def is_right_empty(pos, original_color):
    global cur_direction
    x, y = pos

    turn_right()
    x += cur_direction[0]
    y += cur_direction[1]
    turn_left()
    return is_empty((x, y), original_color)


def is_left_empty(pos, original_color):
    global cur_direction
    x, y = pos

    turn_left()
    x += cur_direction[0]
    y += cur_direction[1]
    turn_right()
    return is_empty((x, y), original_color)


def start(pos, original_color, color):
    global mark, mark2, findloop, backtrack, mark_direction, mark2_direction, cur_direction

    x, y = pos

    while True:

        count_filled_adjacent = 0

        # left
        if is_filled((x - 1, y), original_color):
            count_filled_adjacent += 1

        # up
        if is_filled((x, y - 1), original_color):
            count_filled_adjacent += 1

        # right
        if is_filled((x + 1, y), original_color):
            count_filled_adjacent += 1

        # down
        if is_filled((x, y + 1), original_color):
            count_filled_adjacent += 1

        if count_filled_adjacent != 4:
            turn_right()
            while is_front_empty((x, y), original_color):
                turn_right()

            turn_left()
            while is_front_filled((x, y), original_color):
                turn_left()

        if count_filled_adjacent == 1:
            if backtrack:
                findloop = True
            elif findloop:
                if mark is None:
                    mark = (x, y)
            elif is_front_left_empty((x, y), original_color) and is_back_left_empty(
                (x, y), original_color
            ):
                mark = None
                gameDisplay.set_at((x, y), color)
                x, y = move_foward((x, y))
                continue

        elif count_filled_adjacent == 2:
            if is_back_filled((x, y), original_color):
                if is_front_left_empty((x, y), original_color):
                    mark = None
                    gameDisplay.set_at((x, y), color)
                    x, y = move_foward((x, y))
                    continue
            elif mark is None:
                mark = (x, y)
                mark_direction = cur_direction
                mark2 = None
                findloop = False
                backtrack = False
            else:
                if mark2 is None:
                    if (x, y) == mark:
                        if cur_direction == mark_direction:
                            mark = None
                            turn_left()
                            turn_left()
                            gameDisplay.set_at((x, y), color)
                            x, y = move_foward((x, y))
                            continue
                        else:
                            backtrack = True
                            findloop = False
                            cur_direction = mark_direction
                    elif findloop:
                        mark2 = x, y
                        mark2_direction = cur_direction
                else:
                    if (x, y) == mark:
                        x, y = mark2
                        cur_direction = mark2_direction
                        mark = None
                        mark2 = None
                        backtrack = False
                        turn_left()
                        turn_left()
                        gameDisplay.set_at((x, y), color)
                        x, y = move_foward((x, y))
                        continue
                    elif (x, y) == mark2:
                        mark = (x, y)
                        cur_direction = mark2_direction
                        mark_direction = mark2_direction
                        mark2 = None

        if count_filled_adjacent == 3:
            mark = None
            gameDisplay.set_at((x, y), color)
            x, y = move_foward((x, y))
            continue

        elif count_filled_adjacent == 4:
            return -1, -1

        return x, y


def turn_right():
    global cur_direction

    if cur_direction == (-1, 0):
        cur_direction = (0, -1)
    elif cur_direction == (0, -1):
        cur_direction = (1, 0)
    elif cur_direction == (1, 0):
        cur_direction = (0, 1)
    elif cur_direction == (0, 1):
        cur_direction = (-1, 0)


def turn_left():
    global cur_direction

    if cur_direction == (-1, 0):
        cur_direction = (0, 1)
    elif cur_direction == (0, 1):
        cur_direction = (1, 0)
    elif cur_direction == (1, 0):
        cur_direction = (0, -1)
    elif cur_direction == (0, -1):
        cur_direction = (-1, 0)


def fill_events(event, color):
    global backtrack, findloop

    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
        original_color = gameDisplay.get_at(event.pos)
        x, y = event.pos

        cur_direction = (-1, 0)

        while True:

            if (
                799 > (x + cur_direction[0]) >= 0
                and 599 > (y + cur_direction[1]) >= 0
                and gameDisplay.get_at((x + cur_direction[0], y + cur_direction[1]))
                == original_color
            ):
                x, y = move_foward((x, y))
            else:
                break

        x, y = start((x, y), original_color, color)

        while x >= 0 and y >= 0:
            x, y = move_foward((x, y))
            if is_right_empty((x, y), original_color):
                if (
                    backtrack is True
                    and findloop is False
                    and (
                        is_front_empty((x, y), original_color)
                        or is_left_empty((x, y), original_color)
                    )
                ):
                    findloop = True
                turn_right()
                x, y = move_foward((x, y))

            x, y = start((x, y), original_color, color)


while True:

    for event in pygame.event.get():

        try:

            if event.type == pygame.KEYDOWN and event.key == 51:
                set_primary_color((255,0,0))

            if event.type == pygame.KEYDOWN and event.key == 49:
                tool = PENCIL
            elif event.type == pygame.KEYDOWN and event.key == 50:
                tool = FILL
            elif event.type == pygame.VIDEORESIZE:
                #FIXME
                print('resizing')
                # There's some code to add back window content here.
                # gameDisplay = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                old_surface_saved = gameDisplay
                gameDisplay = pygame.display.set_mode((event.w, event.h),
                                                pygame.RESIZABLE)
                # On the next line, if only part of the window
                # needs to be copied, there's some other options.
                gameDisplay.blit(old_surface_saved, (0,0))
                del old_surface_saved

            if tool == PENCIL:
                pencil_events(event, get_primary_color())
            elif tool == FILL:
                fill_events(event, get_primary_color())
        except AttributeError:
            pass

        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    draw_color_picker(gameDisplay)

    pygame.display.update()
