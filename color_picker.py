import pygame

# Constraints
COLOR_PICKER_HEIGHT = 55

default_colors = [
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

color_positions = []

size_block = 20

primary_color = (0,0,0)
secondary_color = (255,255,255)

get_primary_color = lambda: primary_color
get_secondary_color = lambda: secondary_color

def set_primary_color(color):
    global primary_color
    primary_color = color

def set_secondary_color(color):
    global secondary_color
    secondary_color = color


def draw_color_picker(screen):
    global color_positions

    screen_height = screen.get_height()
    screen_width = screen.get_width()

    left_margin = 85

    # print(screen_height, screen_width)

    pygame.draw.rect(screen,(212,208,200),(0,screen_height-COLOR_PICKER_HEIGHT,screen_width,COLOR_PICKER_HEIGHT),0)
    pygame.draw.rect(screen,(255,255,255),(left_margin-3,screen_height-52,352,49),0)

    for index, default_color in enumerate(default_colors):
        if index % 2 == 0:
            
            start_point = (left_margin + (index/2 * 5) + (index/2 * size_block) , screen_height - 5  - size_block - size_block - 5)

            pygame.draw.rect(
                screen,
                default_color,
                (start_point[0], start_point[1], size_block, size_block),
                0,
            )

        else:

            start_point = (left_margin + ((index-1)/2 * 5) + ((index-1)/2 * size_block) , screen_height - 5  - size_block)

            pygame.draw.rect(
                screen,
                default_color,
                (start_point[0], start_point[1], size_block, size_block),
                0,
            )

        color_positions.append((start_point[0], start_point[1], start_point[0] + size_block, start_point[1] + size_block))

        
        pygame.draw.line(screen, (0,0,0), start_point, (start_point[0], start_point[1] + size_block))
        pygame.draw.line(screen, (0,0,0), start_point, (start_point[0]+ size_block, start_point[1] ))

        pygame.draw.line(screen, (212,208,200), (start_point[0] + size_block, start_point[1] + size_block), (start_point[0], start_point[1] + size_block))
        pygame.draw.line(screen, (212,208,200), (start_point[0] + size_block, start_point[1] + size_block), (start_point[0] + size_block, start_point[1] ))
    
    pygame.draw.rect(screen,get_secondary_color(),(25+(size_block//2),screen_height-45 + (size_block//2),size_block,size_block),0)
    pygame.draw.rect(screen,get_primary_color(),(25,screen_height-45,size_block,size_block),0)

def check_positions(pos, color_func):
    for index, color_position in enumerate(color_positions):
        if color_position[0] < pos[0] < color_position[2] and color_position[1] < pos[1] < color_position[3]:
            color_func(default_colors[index])
            break

def check_picked_color(event):
    global color_positions

    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
        check_positions(event.pos, set_primary_color)

    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
        check_positions(event.pos, set_secondary_color)