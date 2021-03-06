import sys
import pygame
import random
# import numpy as np
import Node
import agent1
import agent2
import agent3
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
AGENT1_SCORE = []
AGENT2_SCORE = []
AGENT3_SCORE = []

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
    id = 0
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            cell = Node.Cell(i, j, gap, rows)
            grid[i].append(cell)
            id +=1
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
    '''
    for row in grid:
        for cell in row:
            cell.set_state(Node.CAVE)
            cell.set_false_neg_prob()
    '''


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

            print('[' + str(cell.row) + ']' + '[' + str(cell.col) + ']' + ' FNP\t' + str(cell.false_neg_prob))
    print("Total Flat: " + str(tot_flat))




#print cell info
def print_cell_info(cell):
    print('[' + str(cell.row) + ']' + '[' + str(cell.col) + ']' + 'F Neg P:' + str(cell.false_neg_prob))


#set target

def set_target(grid, dim):
    x = random.randrange(dim)
    y = random.randrange(dim)

    target = grid[x][y]
    # target.set_state(Node.Target)
    return target



# main driver

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
    # print_prob_grid(grid, dim)
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
                # generate_landscape(grid)
                # print_prob_grid(grid, dim)
                # target = set_target(grid, dim)
                # print("Target; ")
                print_cell_info(target)
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

                if event.key == ord('d'):
                    time = 0
                    distance = 0
                    ret = agent3.run(start, target, grid, dim, time, distance, lambda: draw(win, grid, dim, width))

                if event.key == ord('j'):
                    time = 0
                    distance = 0
                    ret = agent1.run_moving_target(start, target, grid, dim, time, distance)

                if event.key == ord('k'):
                    time = 0
                    distance = 0
                    ret = agent2.run_moving_target(start, target, grid, dim, time, distance)


                if event.key == ord('1'):

                    for i in range(0, 100):
                        time = 0
                        distance = 0
                        ret = agent1.run(start, target, grid, dim, time, distance)
                        AGENT1_TIME.append(ret[0])
                        AGENT1_DIST.append(ret[1])
                        AGENT1_SCORE.append(ret[2])

                        generate_landscape(grid)
                        target = set_target(grid, dim)
                        start = set_start(grid, dim)

                    print("Agent1_Time = "+str(len(AGENT1_TIME))+" "+str(AGENT1_TIME))
                    print("Agent1_Dist = " + str(len(AGENT1_DIST)) + " " + str(AGENT1_DIST))
                    print("agent1_score = "+str(AGENT1_SCORE))

                if event.key == ord('2'):

                    for i in range(0, 20):
                        time = 0
                        distance = 0
                        ret = agent2.run(start, target, grid, dim, time, distance)
                        AGENT2_TIME.append(ret[0])
                        AGENT2_DIST.append(ret[1])
                        AGENT2_SCORE.append(ret[2])

                        generate_landscape(grid)
                        target = set_target(grid, dim)
                        start = set_start(grid, dim)

                    print("Agent2_Time = "+str(len(AGENT2_TIME))+" "+str(AGENT2_TIME))
                    print("Agent2_Dist = " + str(len(AGENT2_DIST)) + " " + str(AGENT2_DIST))
                    print("agent2_score = " + str(AGENT2_SCORE))

                if event.key == ord('3'):

                    for i in range(0, 100):
                        time = 0
                        distance = 0
                        ret = agent3.run(start, target, grid, dim, time, distance, lambda: draw(win, grid, dim, width))
                        AGENT3_TIME.append(ret[0])
                        AGENT3_DIST.append(ret[1])
                        AGENT3_SCORE.append(ret[2])

                        generate_landscape(grid)
                        target = set_target(grid, dim)
                        start = set_start(grid, dim)

                    print("Agent3_Time = "+str(len(AGENT3_TIME))+" "+str(AGENT3_TIME))
                    print("Agent3_Dist = " + str(len(AGENT3_DIST)) + " " + str(AGENT3_DIST))
                    print("agent3_score = " + str(AGENT3_SCORE))

                if event.key == ord('4'):

                    for i in range(0, 10):
                        time = 0
                        distance = 0
                        ret = agent1.run_moving_target(start, target, grid, dim, time, distance)
                        AGENT2_TIME.append(ret[0])
                        AGENT2_DIST.append(ret[1])
                        AGENT2_SCORE.append(ret[2])

                        generate_landscape(grid)
                        target = set_target(grid, dim)
                        start = set_start(grid, dim)

                    print("Agent1_Moving_Time = "+str(len(AGENT2_TIME))+" "+str(AGENT2_TIME))
                    print("Agent1_Moving_Dist = " + str(len(AGENT2_DIST)) + " " + str(AGENT2_DIST))
                    print("agent1_Moving_score = " + str(AGENT2_SCORE))

                if event.key == ord('5'):

                    for i in range(0, 10):
                        time = 0
                        distance = 0
                        ret = agent2.run_moving_target(start, target, grid, dim, time, distance)
                        AGENT2_TIME.append(ret[0])
                        AGENT2_DIST.append(ret[1])
                        AGENT2_SCORE.append(ret[2])

                        generate_landscape(grid)
                        target = set_target(grid, dim)
                        start = set_start(grid, dim)

                    print("Agent2_Moving_Time = "+str(len(AGENT2_TIME))+" "+str(AGENT2_TIME))
                    print("Agent2_Moving_Dist = " + str(len(AGENT2_DIST)) + " " + str(AGENT2_DIST))
                    print("agent2_Moving_score = " + str(AGENT2_SCORE))


    pygame.quit()


if __name__ == '__main__':
    # dimension = int(sys.argv[1])
    dimension = 50
    main(WIN, WIDTH, dimension)
