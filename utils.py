import pygame
import numpy as np
np.random.seed(42)

SCREEN_WIDTH, SCREEN_HEIGHT = 1400, 1000
TILE_SIZE = 15
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREY1 = (128, 128, 128)
GREY2 = (200, 200, 200)

pygame.font.init()

font = pygame.font.Font(None, 36)

def draw_box(screen, text, x, y, width, height, color):
    pygame.draw.rect(screen, color, (x, y, width, height))
    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))
    screen.blit(text_surface, text_rect)

def draw_map(screen, rows, columns , table_map , status=None, path = None):


    map_width =  rows
    map_height = columns

    offset_x = (SCREEN_WIDTH - map_width * TILE_SIZE) // 2
    offset_y = (SCREEN_HEIGHT - map_height * TILE_SIZE) // 2

    for x, row in enumerate(table_map):
        for y, cell in enumerate(row):
            rect = pygame.Rect(offset_x + x * TILE_SIZE, offset_y + y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            pygame.draw.rect(screen, WHITE, rect)
            pygame.draw.rect(screen, BLACK, rect, 1)  # Draw border around each cell

    for pos, color in status.items():
        if color == '1':
            pygame.draw.rect(screen, RED, pygame.Rect(offset_x + pos[0] * TILE_SIZE, offset_y + pos[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE))
        elif color == '2':
            pygame.draw.rect(screen, GREY2, pygame.Rect(offset_x + pos[0] * TILE_SIZE, offset_y + pos[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE))

    if path != None:
        for sol in path:
            pygame.draw.rect(screen, BLUE, pygame.Rect(offset_x + sol[0] * TILE_SIZE, offset_y + sol[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE))


    for x, row in enumerate(table_map):
        for y, cell in enumerate(row):
            rect = pygame.Rect(offset_x + x * TILE_SIZE, offset_y + y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            rect_wall = pygame.Rect((offset_x + x * TILE_SIZE), (offset_y + y * TILE_SIZE) ,( TILE_SIZE),( TILE_SIZE))

            if cell == 'I': # I Init
                pygame.draw.rect(screen, GREEN, rect)
            elif cell == '|': # | Wall
                pygame.draw.rect(screen, BLACK, rect_wall)
            elif cell == 'T': # T Target
                pygame.draw.rect(screen, BLUE, rect)

def wall_generator(rows, num_walls, initial_pos, target_pos )->list:
    wall_coords = np.random.randint(0, rows, size=(num_walls, 2))
    walls = []
    for coord in wall_coords:
        while tuple(coord) == initial_pos or tuple(coord) == target_pos:
            coord = np.random.randint(0, rows, size=2)
        walls.append([coord[0], coord[1]])
    return walls


def test_case_generator(testcase:int):
    rows, columns = 50, 50
    walls = []
    ## Test Case 0 
    # start -> End
    if (testcase == 0):
        princess_pos = (24, 24)
        knight_pos = (0, 0)

    ## Test Case 1
    # wall_random 1
    elif (testcase == 1):
        princess_pos = (49, 49)
        knight_pos = (0, 0)    
        num_walls = 500
        walls = wall_generator(rows, num_walls, knight_pos, princess_pos)

    ## Test Case 2
    # wall_random 2
    elif (testcase == 2):
        princess_pos = (49, 49)
        knight_pos = (0, 0)
        num_walls = 1200
        walls = wall_generator(rows, num_walls, knight_pos, princess_pos)
    ## Test Case 3
    ## one side init
    elif (testcase == 3):
        princess_pos = (47, 25)
        knight_pos = (2, 25)    
        for index in range(20):
            walls.append([12,15+index])

        for index in range(7):
            walls.append([5 + index,15])

        for index in range(7):
            walls.append([5 + index,34])
    ## Test Case 4
    ## one side target 
    elif (testcase == 4):
        princess_pos = (47, 25)
        knight_pos = (2, 25)    
        for index in range(20):
            walls.append([37,15+index])

        for index in range(7):
            walls.append([38 + index,15])

        for index in range(7):
            walls.append([38 + index,34])
    ## Test Case 5
    ## two side target
    elif (testcase == 5):
        princess_pos = (47, 25)
        knight_pos = (2, 25)   

        for index in range(20):
            walls.append([12,15+index])

        for index in range(7):
            walls.append([5 + index,15])

        for index in range(7):
            walls.append([5 + index,34])

        for index in range(20):
            walls.append([37,15+index])

        for index in range(7):
            walls.append([38 + index,15])

        for index in range(7):
            walls.append([38 + index,34]) 


    return rows, columns, walls, princess_pos, knight_pos
