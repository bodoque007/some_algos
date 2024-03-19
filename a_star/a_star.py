import pygame
import numpy as np
from queue import PriorityQueue
import time
import random

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
N = 30
M = 30
WIDTH = 20
HEIGHT = 20
MARGIN = 5

grid = [[0 for _ in range(N)] for _ in range(M)]

def initialize_maze(start_row=0, start_col=0, end_row=N - 5, end_col=M - 5):
    for row in range(N):
        for col in range(M):
            if row == start_row and col == start_col:
                grid[row][col] = 2  # Start cell
            elif row == end_row and col == end_col:
                grid[row][col] = 3  # End cell
            elif row % 2 != 0 and col % 2 != 0:
                grid[row][col] = 1  # Wall cell
            else:
                grid[row][col] = 0  # Path cell

    num_obstacles = random.randint(40, 50)
    for _ in range(num_obstacles):
        row = random.randint(0, N - 1)
        col = random.randint(1, M - 1)
        if grid[row][col] == 0:
            grid[row][col] = 1

pygame.init()
WINDOW_SIZE = [800, 800]
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

def draw_screen():
    pixel_array = np.zeros((N, M, 3), dtype=np.uint8)

    for row in range(N):
        for col in range(M):
            pixel_array[row, col] = get_color(grid[row][col])

    # Create a surface from the pixel array
    surface = pygame.surfarray.make_surface(pixel_array.swapaxes(0, 1))

    # Blit the surface onto the screen
    screen.blit(pygame.transform.scale(surface, WINDOW_SIZE), (0, 0))

    pygame.display.flip()
    time.sleep(0.05) 

def is_viable_neighbor(neighbor_row, neighbor_col):
    # Checks if neighbor is in between boundaries and not a wall.
    return 0 <= neighbor_row < N and 0 <= neighbor_col < M and grid[neighbor_row][neighbor_col] != 1
    
def manhattan_distance(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)

def a_star():
    current = (0, 0)
    end = (N-5, M-5)

    g_score = {(i, j): float('inf') for i in range(N + 1) for j in range(M + 1)}
    g_score[current] = 0
    
    f_score = {(i, j): float('inf') for i in range(N + 1) for j in range(M + 1)}
    f_score[current] = manhattan_distance(current[0], current[1], end[0], end[1])


    open = PriorityQueue()
    # Open's structure for cell i,j = (f_score_of_ij, manhattan_distance_of_ij, (i, j))
    # The idea is that we'll always use the cell with the least f_score, and if the f_score of two different cells match, use the one with the least manhattan_distance.
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


'''
BFS Implementation to warm-up.
def bfs():
    current = (0, 0)
    end = (N-5, M-5)
    queue = deque([current])
    visited = set()
    visited.add(current)

    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    while queue:
        current = queue.popleft()
        if current == end:
            break 
        visited.add(current)

        grid[current[0]][current[1]] = 4  # Marks visited and paint it blue.
        for dx, dy in directions:
            neighbor_row, neighbor_col = current[0] + dx, current[1] + dy
            if is_viable_neighbor(neighbor_row, neighbor_col, visited):
                queue.append((neighbor_row, neighbor_col))
'''


if __name__ == "__main__":
    initialize_maze()
    a_star()
    pygame.quit()
    