import pygame
import time
from GridSearchAlgorithm import GridSearchAlgorithm
from utils import draw_map, test_case_generator, draw_box, SCREEN_WIDTH, SCREEN_HEIGHT, GREY1, GREY2, WHITE

algor_texts = ["Breath First Search", "A Star Search", "Best First Search"]
testcase_texts = ["Test Case : 0", "Test Case : 1", "Test Case : 2", "Test Case : 3", "Test Case : 4", "Test Case : 5"]

algor_index, testcase_index, iteration, total_cost = 0, 0, 0, 0
state_status, path_map, elapsed_time = None, None, None

rows, columns, walls, target_pos, init_pos = test_case_generator(testcase_index)

grid_search_algor = GridSearchAlgorithm(rows=rows, columns=columns, walls=walls, target_pos=target_pos, init_pos=init_pos)
table_map = grid_search_algor.get_map()

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("GridSearchAlgorithm")

running = True
start_time = time.time()
while running:
    screen.fill(WHITE)

    if (path_map is None):
        if (algor_index == 0):
            state_status, path_map,  total_cost  = grid_search_algor.breath_first_search() 
        elif (algor_index == 1):
            state_status, path_map, total_cost = grid_search_algor.a_star_search()
        elif (algor_index == 2):
            state_status, path_map,  total_cost  = grid_search_algor.best_first_search()
        iteration += 1
        elapsed_time =  time.time() - start_time
        
    draw_map(screen, rows = rows, columns = columns, table_map = table_map , status=state_status, path = path_map) 

    draw_box(screen, f'iteration : {iteration}', 1100, 125, 250, 50, GREY2)
    draw_box(screen, f'cost : {total_cost:.2f}', 1100, 175, 250, 50, GREY2)
    draw_box(screen, f'time : {elapsed_time:.2f} s', 1100, 225, 250, 50, GREY2)

    draw_box(screen, "Algorithm", 50, 75, 250, 50, GREY1)
    draw_box(screen,  algor_texts[algor_index],  50, 125, 250, 50, GREY2 )
    draw_box(screen, "Test Case", 50, 200, 250, 50, GREY1)
    draw_box(screen, testcase_texts[testcase_index],  50, 250, 250, 50, GREY2)
    draw_box(screen, "Restart", 50, 325, 250, 50, GREY2)

    draw_box(screen, "Result", 1100, 75, 250, 50, GREY1)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  
                if 50 <= event.pos[0] <= 300 and 125 <= event.pos[1] <= 175 or 250 <= event.pos[1] <= 300 or 325 <= event.pos[1] <= 375:
                    if (125 <= event.pos[1] <= 175 ):
                        algor_index = (algor_index + 1) % len(algor_texts)

                    elif 250 <= event.pos[1] <= 300:
                        testcase_index = (testcase_index + 1) % len(testcase_texts)
                        rows, columns, walls, target_pos, init_pos = test_case_generator(testcase_index)

                    path_map = None
                    iteration = 0
                    grid_search_algor.map_reset(rows, columns, walls, target_pos, init_pos)
                    table_map = grid_search_algor.get_map()
                    start_time = time.time()


    pygame.display.flip()
    pygame.time.Clock().tick(30)  

pygame.quit()