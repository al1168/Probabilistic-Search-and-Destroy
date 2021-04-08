import sys
import pygame
import random
import numpy as np
import Node
import agent1
import agent2

'''
Authors
Alden Lu al1168
Haoran Wen hw408
'''

pygame.display.set_caption("CS440 Project 3")

WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Prob Search")

#Global Variable
AGENT1_TIME = []
AGENT1_DIST = []
AGENT2_TIME = []
AGENT2_DIST = []
AGENT3_TIME = []
AGENT3_DIST = []


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

            print_cell_info(cell)
    print("Total Flat: "+str(tot_flat))
    print("Total Hill: " + str(tot_hill))
    print("Total Forest: " + str(tot_forest))
    print("Total Cave: " + str(tot_cave))

#print cell info
def print_cell_info(cell):
    print('[' + str(cell.row) + ']' + '[' + str(cell.col) + ']' + 'F Neg P:' + str(cell.false_neg_prob))


#set target
def set_target(grid, dim):
    x = random.randrange(dim)
    y = random.randrange(dim)

    target = grid[x][y]
    return target

#set start location
def set_start(grid, dim):
    x = random.randrange(dim)
    y = random.randrange(dim)

    start = grid[x][y]
    return start

#main driver
def main(win, width, dimension):
    dim = dimension
    grid = create_grid(dim, width)

    generate_landscape(grid)
    print_prob_grid(grid, dim)
    target = set_target(grid, dim)
    print("Target; ")
    print_cell_info(target)

    start = set_start(grid, dim)
    print("Start: ")
    print_cell_info(start)

    run = True
    while run:
        draw(win, grid, dim, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    generate_landscape(grid)
                    print_prob_grid(grid, dim)
                    target = set_target(grid, dim)
                    print("Target; ")
                    print_cell_info(target)

                    start = set_start(grid, dim)
                    print("Start: ")
                    print_cell_info(start)

                if event.key == ord('a'):
                    time = 0
                    distance = 0
                    ret = agent1.run(start, target, grid, dim, time, distance)


                if event.key == ord('s'):
                    time = 0
                    distance = 0
                    ret = agent2.run(start, target, grid, dim, time, distance)

                if event.key == ord('1'):

                    for i in range(0, 50):
                        time = 0
                        distance = 0
                        ret = agent1.run(start, target, grid, dim, time, distance)
                        AGENT1_TIME.append(ret[0])
                        AGENT1_DIST.append(ret[1])

                        generate_landscape(grid)
                        target = set_target(grid, dim)
                        start = set_start(grid, dim)

                    print("Agent1_Time = "+str(len(AGENT1_TIME))+" "+str(AGENT1_TIME))
                    print("Agent1_Dist = " + str(len(AGENT1_DIST)) + " " + str(AGENT1_DIST))

                if event.key == ord('2'):

                    for i in range(0, 50):
                        time = 0
                        distance = 0
                        ret = agent2.run(start, target, grid, dim, time, distance)
                        AGENT2_TIME.append(ret[0])
                        AGENT2_DIST.append(ret[1])

                        generate_landscape(grid)
                        target = set_target(grid, dim)
                        start = set_start(grid, dim)

                    print("Agent2_Time = "+str(len(AGENT2_TIME))+" "+str(AGENT2_TIME))
                    print("Agent2_Dist = " + str(len(AGENT2_DIST)) + " " + str(AGENT2_DIST))


    pygame.quit()



if __name__ == '__main__':
    dimension = int(sys.argv[1])
    main(WIN, WIDTH, dimension)
