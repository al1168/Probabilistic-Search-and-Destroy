#Agent1

import random
import numpy as np

#Return True if target is found otherwise Return False
def search(cell, target):
    FNR = cell.get_false_neg_prob() #false neg rate
    randVal = np.random.choice(np.arange(0, 2), p=[1-FNR, FNR])
    if randVal == 0: #Beats false negative rate
        if cell == target:  # cell is target
            return True  # target is here
        else:
            return False # target is not here

    elif randVal == 1: #Not able to beat FNR
        return False # Not able to find target
    else: # something went wrong
        print("ERROR: agents.py->search")
        return


#update Belief
def update_beliefs(curr, belief_dict, grid, tot):

    belief_dict[curr] = belief_dict[curr] * curr.get_false_neg_prob()

    #total_prob = 1 * sum(belief_dict.values())
    #norm = [float(i) / sum(raw) for i in raw]


    factor = 1.0 / sum(belief_dict.values())
    normalised_d = {k: v * factor for k, v in belief_dict.items()}

    belief_dict = normalised_d
    #update cell's belief prob with belief_dict
    for row in grid:
        for cell in row:
            cell.set_belief_prob(belief_dict[cell])

    return belief_dict

#manhattan distance
def man_dist(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

#agent 1
def run(start, target, grid, dim, time, distance):
    explored = [] # for printing purposes

    #initiate belief probs for each cell
    tot = dim**2
    belief_dict = dict()
    for row in grid:
        for cell in row:
            cell.set_belief_prob(1/tot)
            belief_dict[cell] = cell.get_belief_prob()

    current = start
    explored.append(current.get_pos())

    searching = True
    while searching:

        action = search(current, target)

        if action == True:
            print("\nAgent 1 Result:")
            print("Target Found")
            print("Time: "+str(time))
            print("Distance: " + str(distance))
            searching = False
        else:
            time += 1
            print("Target not found: "+str(current.get_pos())+" "+str(time))
            print("Continue Searching...\n")

            belief_dict = update_beliefs(current, belief_dict, grid, tot)

            highest_belief = max(belief_dict.values()) #get highest belief
            cell_list = [key for key in belief_dict if belief_dict[key] == highest_belief] # list of cells that share the highest belief
            #if current in cell_list:
            #    cell_list.remove(current)

            min_d = 1000000000000
            #temp_cell = grid[0][0]
            for cell in cell_list:
                temp_d = man_dist(current.get_pos(), cell.get_pos())
                if temp_d < min_d:
                    min_d = temp_d
                    current = cell

            #current = temp_cell
            explored.append(current.get_pos())
            distance += min_d

    print("\nDebugging: ")
    #print("Explored ["+str(len(explored))+"]: "+str(explored))
    print("Prob Sum: "+str(sum(belief_dict.values())))
    print("Done")

    return (time, distance)