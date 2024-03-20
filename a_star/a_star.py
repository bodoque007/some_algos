import pygame
import numpy as np
from queue import PriorityQueue
import time

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
N = 30
M = 30
WINDOW_SIZE = [800, 800]
GRID_SIZE = min(WINDOW_SIZE) // max(N, M)

grid = [[0 for _ in range(N)] for _ in range(M)]
# Later on used to actually draw the grid onto the screen.
pixel_array = np.zeros((N, M, 3), dtype=np.uint8)


pygame.init()
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("A* Maze Runner")
clock = pygame.time.Clock()

def get_color(value):
    color_map = {
        0: WHITE,
        1: BLACK,
        2: GREEN,
        3: RED,
        4: BLUE
    }
    return color_map.get(value, BLACK)

def draw_obstacle(x, y, start, end, click=1):
    row = x // GRID_SIZE
    col = y // GRID_SIZE
    if 0 <= row < N and 0 <= col < M and (row, col) != start and (row, col) != end:
        if click == 1:
            grid[row][col] = 1
        else:
            grid[row][col] = 0

def user_draw_maze(start, end):
    drawing = False 
    running = True 
    while running:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    drawing = True
                    draw_obstacle(*event.pos, start, end)
                elif event.button == 3:
                    draw_obstacle(*event.pos, start, end, 3)
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                drawing = False
            elif event.type == pygame.MOUSEMOTION and drawing:
                draw_obstacle(*event.pos, start, end)
        draw_screen()

def draw_screen():
    for row in range(N):
        for col in range(M):
            pixel_array[row, col] = get_color(grid[row][col])

    # Create a surface from the pixel array
    surface = pygame.surfarray.make_surface(pixel_array)

    # Blit the surface onto the screen
    screen.blit(pygame.transform.scale(surface, WINDOW_SIZE), (0, 0))

    pygame.display.flip()
    time.sleep(0.05) 

def is_viable_neighbor(neighbor_row, neighbor_col):
    # Checks if neighbor is in between boundaries and not a wall.
    return 0 <= neighbor_row < N and 0 <= neighbor_col < M and grid[neighbor_row][neighbor_col] != 1
    
# Will be used as heuristic.
def manhattan_distance(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)

def a_star(start, end):
    current = start
    end = end

    g_score = {(i, j): float('inf') for i in range(N + 1) for j in range(M + 1)}
    g_score[current] = 0
    
    f_score = {(i, j): float('inf') for i in range(N + 1) for j in range(M + 1)}
    f_score[current] = manhattan_distance(current[0], current[1], end[0], end[1])


    open = PriorityQueue()
    # Open's queue structure for cell i,j is (f_score_of_ij, manhattan_distance_of_ij, (i, j))
    # The idea is that we'll always use the cell with the least f_score, and if the f_score of two different cells are equal, we'll use the one with the least manhattan_distance.
    open.put((f_score[current], manhattan_distance(current[0], current[1], end[0], end[1]), current))
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    while not open.empty():
        draw_screen()
        current = open.get()[2]

        if current == end:
            print("Found!")
            return

        grid[current[0]][current[1]] = 4  # Marks visited and paints it blue.
        for dx, dy in directions:
            neighbor_row, neighbor_col = current[0] + dx, current[1] + dy
            if is_viable_neighbor(neighbor_row, neighbor_col):
                # The following updates the score for the neighbor.
                tentative_gScore = g_score[current] + 1
                temp_f_score = tentative_gScore + manhattan_distance(neighbor_row, neighbor_col, end[0], end[1])

                if temp_f_score < f_score[(neighbor_row, neighbor_col)]:
                    g_score[(neighbor_row, neighbor_col)] = tentative_gScore
                    f_score[(neighbor_row, neighbor_col)] = temp_f_score
                    open.put((temp_f_score, manhattan_distance(neighbor_row, neighbor_col, end[0], end[1]), (neighbor_row, neighbor_col)))
    print("Not found! NOOOOOOOOOO")


def select_starting_and_ending():
    start = None
    end = None
    selecting = True

    while selecting:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x, y = event.pos
                row = x // GRID_SIZE
                col = y // GRID_SIZE
                if 0 <= row < N and 0 <= col < M:
                    if start is None:
                        start = (row, col)
                        grid[row][col] = 2
                        print("Starting point selected:", start)
                    elif end is None and (row, col) != start:
                        end = (row, col)
                        grid[row][col] = 3
                        print("Ending point selected:", end)
                        selecting = False  # Exit selection mode
        draw_screen()
    return start, end

if __name__ == "__main__":
    start, end = select_starting_and_ending()
    user_draw_maze(start, end)
    a_star(start, end)
    pygame.quit()