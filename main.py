import sys
import pygame
import random
import Node
import algo
from algo import BFS, DFS, astar
# import model

'''
Authors
Alden Lu al1168
Haoran Wen hw408
'''

pygame.display.set_caption("CS440 Proj1")

WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Path Finding Algorithm")

# draw lines on pygame application
def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, Node.GREY, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, Node.GREY, (j * gap, 0), (j * gap, width))

# draw the colors on py game
def draw(win, grid, rows, width):
    win.fill(Node.OPEN)
    for row in grid:
        for cell in row:
            cell.draw(win)

    draw_grid(win, rows, width)
    pygame.display.update()

# creates a template maze with default values
def create_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            cell = Node.Cell(i, j, gap, rows)
            grid[i].append(cell)

    return grid

# creates a randomly generated blocked maze
def generate_maze(grid, dim, p, density):
    start = grid[0][0].set_start()
    origin = grid[0][0]
    end = grid[dim - 1][dim - 1]
    target = grid[dim - 1][dim - 1].set_target()

    blockedCount = 0

    cnt = 0
    while density > 0:
        x = random.randrange(dim)
        y = random.randrange(dim)
        cell = grid[x][y]
        if cnt == (dim * dim) - 2:  # if the entire maze is blocked
            break
        if cell.is_start() or cell.is_target() or cell.is_blocked():
            continue
        cell.set_blocked()
        blockedCount += 1
        # print(cell.color)
        density -= 1
        cnt += 1
        # print("#" + str(cnt) + ": (" + str(x) + "," + str(y) + ")")
    print(str(blockedCount) + " blocked cells")

# reset all nodes to original generated maze
def reset(grid):
    for row in grid:
        for cell in row:
            if cell.is_start() or cell.is_target() or cell.is_blocked():
                continue
            cell.state = Node.OPEN

#
# def apply_model(grid, dim):
#
#     for i in range(0, dim):
#         for j in range(0, dim):
#             grid[i][j].set_danger_value(model.MODEL[i][j])



def main(win, width, dimension, prob,q):
    dim = dimension
    p = prob
    density = (dim ** 2) * p
    grid = create_grid(dim, width)
    generate_maze(grid, dim, p, density)
    print("Maze is generated")

    m_rows, m_cols = (dim, dim)
    model = [[0 for i in range(m_cols)] for j in range(m_rows)]

    run = True
    while run:
        draw(win, grid, dim, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:


    pygame.quit()


def generate_data(win, width, dimension, prob):
    dim = dimension
    p = prob
    density = (dim ** 2) * p
    grid = create_grid(dim, width)

    generate_maze(grid, dim, p, density)

    print("Generating data starting...")

    # draw(win, grid, dim, width)
    for i in range(0, 10):
        BFS(lambda: draw(win, grid, dim, width), grid, grid[0][0], dim)
        generate_maze(grid, dim, p, density)
        print(str(i) + "trial done")
    # pygame.quit(
    print("Generation complete")


if __name__ == '__main__':
    dimension = int(sys.argv[1])
    prob = float(sys.argv[2])
    q = float(sys.argv[3])
    main(WIN, WIDTH, dimension, prob,q)
    print("\nData:")
    print(algo.DATA)
