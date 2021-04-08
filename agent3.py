import time
from queue import PriorityQueue
import Node
import numpy as np


# manhattan distance
def man_dist(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)


# update Belief
def update_beliefs(curr, belief_dict, grid, tot):
    belief_dict[curr] = belief_dict[curr] * curr.get_false_neg_prob()

    factor = 1.0 / sum(belief_dict.values())
    normalised_d = {k: v * factor for k, v in belief_dict.items()}

    belief_dict = normalised_d
    # update cell's belief prob with belief_dict
    for row in grid:
        for cell in row:
            cell.set_belief_prob(belief_dict[cell])

    return belief_dict


# update confidence probability
def update_confidence(curr, confidence_dict, belief_dict, grid):
    for k, v in confidence_dict.items():
        confidence_dict[k] = belief_dict[k] * (1 - k.get_false_neg_prob())

    # confidence_dict[curr] = belief_dict[curr] * (1-curr.get_false_neg_prob())

    factor = 1.0 / sum(confidence_dict.values())
    normalised_d = {k: v * factor for k, v in confidence_dict.items()}

    confidence_dict = normalised_d
    # update cell's confidence prob with belief_dict
    for row in grid:
        for cell in row:
            cell.set_confidence_prob(confidence_dict[cell])

    return confidence_dict


def search(cell, target):
    FNR = cell.get_false_neg_prob()  # false neg rate
    randVal = np.random.choice(np.arange(0, 2), p=[1 - FNR, FNR])
    if randVal == 0:  # Beats false negative rate
        if cell == target:  # cell is target
            return True  # target is here
        else:
            return False  # target is not here

    elif randVal == 1:  # Not able to beat FNR
        return False  # Not able to find target
    else:  # something went wrong
        print("ERROR: agents.py->search")
        return


# def generate_islands(grid):
#     # assume 50*50 grid
#     # creates regions of 25 squares
#     # island.append(grid[k+i][l+j])
#     dict = {}
#     id = 0
#     for j in range(0, 50, 5):
#         for i in range(0, 50, 5):
#             cells = []
#             it = 0
#             for k in range(0, 5):
#                 for l in range(0, 5):
#                     cells.append(grid[k + i][l + it])
#             it += 2
#             # print(len(cells))
#             temp = Island(cells, id)
#             dict[id] = temp
#             id += 1
#     return dict

def generate_islands(grid):
    # assume 50*50 grid
    # creates regions of 25 squares
    # island.append(grid[k+i][l+j])
    dict = {}
    id = 0
    for i in range(0,10):
        for j in range(0,10):
            cells = []
            for k in range(0,5):
                for l in range(0,5):
                    cells.append(grid[k+5*i][l+5*j])
            temp = Island(cells, id)
            dict[id] = temp
            id += 1
    return dict

# def compute_island_prob(islands):
#     prob_lst = []
#     for values in islands.values():
#         total_prob = 0
#         for cell in values.getIsland():
#             total_prob += cell.get_confidence_prob()
#         prob_lst.append((values.getId(),total_prob))
#     return prob_lst


# def compute_island_prob(islands, visited):
#     prob_lst = PriorityQueue()
#     d = 0
#     for values in islands.values():
#         total_prob = 0
#         for cell in values.getIsland():
#             total_prob += cell.get_confidence_prob()
#         count = visited[d]
#         temptuple = (-1*total_prob, count, values.getId())
#         prob_lst.put(temptuple)
#         d += 1
#     # print(prob_lst.qsize())
#     return prob_lst

def compute_island_prob(islands, visited):
    prob_lst = PriorityQueue()
    d = 0
    for values in islands.values():
        total_prob = 0
        for cell in values.getIsland():
            total_prob += cell.get_confidence_prob()
        count = visited[d]
        temptuple = (-1*total_prob, count, values.getId())
        prob_lst.put(temptuple)
        d += 1
    # print(prob_lst.qsize())
    return prob_lst
# def compute_island_prob(islands, visited):
#     prob_lst = []
#     d = 0
#     for values in islands.values():
#         total_prob = 0
#         for cell in values.getIsland():
#             total_prob += cell.get_confidence_prob()
#         count = visited[d]
#         temptuple = (-1*total_prob, count, values.getId())
#         prob_lst.append(temptuple)
#         d += 1
#     # print(prob_lst.qsize())
#     prob_lst.sort()
#     return prob_lst

def run(start, target, grid, dim, timed, distance, draw):
    explored = []  # for printing purposes
    previous_cell =start
    # initiate belief probs for each cell
    tot = dim ** 2
    belief_dict = dict()
    confidence_dict = dict()
    b = 0
    for row in grid:
        for cell in row:
            cell.set_belief_prob(1 / tot)
            belief_dict[cell] = cell.get_belief_prob()
            b += cell.get_belief_prob()
            cell.set_confidence_prob(1 - cell.get_false_neg_prob())
            confidence_dict[cell] = cell.get_confidence_prob()
    print("TRUE B" + str(b))
    current = start
    explored.append(current.get_pos())

    # create islands.regions in to a dictionary
    islands = generate_islands(grid)
    print(islands)
    visited = {}
    for i in range(0, 100):
        visited[i] = 0
    prob_lst = compute_island_prob(islands, visited)
    searching = True
    first_it = 0

    while searching:
        # first iteration of searching, just search cell and update belief/confidence
        if first_it == 0:
            action = search(current, target)
            # time.sleep(1)
            draw()
            timed += 1
            if action == True:
                print("\nAgent3 Result")
                print("Target Found")
                print("Time: " + str(timed))
                print("Distance: " + str(distance))
                searching = False
            else:
                print("Target not found: " + str(current.get_pos()) + " " + str(timed))
                print("Continue Searching...\n")
                belief_dict = update_beliefs(current, belief_dict, grid, tot)
                confidence_dict = update_confidence(current, confidence_dict, belief_dict, grid)
            first_it += 1
            continue

        # Give us highest probability island
        picked_island = prob_lst.get()
        print(picked_island)
        Highest_island_prob = picked_island[2]
        # print(Highest_island_prob)
        # list of all the cell we need to visit on this island
        current_list = islands[Highest_island_prob].getIsland()

        # Dictionary to store number of time visited this island
        visited[Highest_island_prob] += 1

        # list to store for printing purpose
        list = []
        for cell in current_list:
            list.append(cell.get_pos())
            current = cell
            current.set_state(Node.Agent)
            # time.sleep(1)

            action = search(current, target)
            timed += 1
            if action == True:
                print("\nAgent3 Result")
                print("Target Found")
                print("Time: " + str(timed))
                print("Distance: " + str(distance))
                searching = False
            else:
                belief_dict = update_beliefs(current, belief_dict, grid, tot)
                confidence_dict = update_confidence(current, confidence_dict, belief_dict, grid)
            # calc distance
            temp_d = man_dist(current.get_pos(), previous_cell.get_pos())
            distance += temp_d
            previous_cell = current
        print("")
        # print(list)
        # print(prob_lst.queue)
        list = []
        #
        draw()
        prob_lst = compute_island_prob(islands, visited)
        # print(visited)
        # print(prob_lst.queue)

    return


class Island:
    def __init__(self, list, id):
        self.id = id
        self.islands = list
        self.total_prob = 0

    def getId(self):
        return self.id

    def getIsland(self):
        return self.islands
