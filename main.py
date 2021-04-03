import sys
import pygame
import random
import numpy as np
import Node

'''
Authors
Alden Lu al1168
Haoran Wen hw408
'''

pygame.display.set_caption("CS440 Project 3")

WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Prob Search")

# draw lines on pygame application
def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, Node.GREY, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, Node.GREY, (j * gap, 0), (j * gap, width))

# draw the colors on py game
def draw(win, grid, rows, width):
    win.fill(Node.FLAT)
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
def generate_landscape(grid):
    lst = ["flat", "hill", "forest", "cave"]
    for row in grid:
        for cell in row:
            cell.update_neighbors(grid)
            t = random.choice(lst)
            if t == "flat":
                cell.set_state(Node.FLAT)
                cell.set_false_neg_prob()
            elif t == "hill":
                cell.set_state(Node.HILL)
                cell.set_false_neg_prob()
            elif t == "forest":
                cell.set_state(Node.FOREST)
                cell.set_false_neg_prob()
            elif t == "cave":
                cell.set_state(Node.CAVE)
                cell.set_false_neg_prob()

def print_prob_grid(grid, rows):
    tot_hill = 0
    tot_flat = 0
    tot_cave = 0
    tot_forest = 0

    for i in range(rows):
        for j in range(rows):
            cell = grid[i][j]
            if grid[i][j].get_state() == Node.FOREST:
                tot_forest += 1
            elif grid[i][j].get_state() == Node.FLAT:
                tot_flat += 1
            elif grid[i][j].get_state() == Node.HILL:
                tot_hill += 1
            elif grid[i][j].get_state() == Node.CAVE:
                tot_cave += 1

            print('[' + str(cell.row) + ']' + ' [' + str(cell.col) + ']' + 'PROB\t' + str(cell.false_neg_prob))
    print("Total Flat: "+str(tot_flat))
    print("Total Hill: " + str(tot_hill))
    print("Total Forest: " + str(tot_forest))
    print("Total Cave: " + str(tot_cave))

def set_target(grid, dim):
    x = random.randrange(dim)
    y = random.randrange(dim)

    target = grid[x][y]
    print('Target: [' + str(target.row) + ']' + ' [' + str(target.col) + ']' + 'PROB\t' + str(target.false_neg_prob))
    return target
#main driver
def main(win, width, dimension):
    dim = dimension
    grid = create_grid(dim, width)

    generate_landscape(grid)
    print_prob_grid(grid, dim)
    target = set_target(grid, dim)

    run = True
    while run:
        draw(win, grid, dim, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                generate_landscape(grid)
                print_prob_grid(grid, dim)
                target = set_target(grid, dim)


    pygame.quit()



if __name__ == '__main__':
    dimension = int(sys.argv[1])
    main(WIN, WIDTH, dimension)
