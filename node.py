import pygame

CAVE = (255, 0, 0) # Red
FOREST = (0, 0, 255) #Blue
HILL = (128,0,128) #Purple
FLAT = (255, 255, 255) # white
GREY = (128, 128, 128)


class Cell:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = col * width
        self.y = row * width
        self.state = FLAT
        self.is_closed = False
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows
        self.false_neg_prob = -1.0
        self.belief_prob = -1.0
        self.confidence_prob = -1.0

    def set_belief_prob(self, prob):
        self.belief_prob = prob
    def get_belief_prob(self):
        return self.belief_prob

    def set_confidence_prob(self, prob):
        self.confidence_prob = prob

    def get_confidence_prob(self):
        return self.confidence_prob

    def get_false_neg_prob(self):
        return self.false_neg_prob
    def set_false_neg_prob(self):
        if self.state == FLAT:
             self.false_neg_prob = 0.1
        elif self.state == HILL:
            self.false_neg_prob = 0.3

        elif self.state == FOREST:
            self.false_neg_prob = 0.7

        elif self.state == CAVE:
            self.false_neg_prob = 0.9

    def get_pos(self):
        return self.row, self.col

    def get_state(self):
        return self.state
    def set_state(self, val):
        self.state = val

    def draw(self, win):
        pygame.draw.rect(win, self.state, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        self.neighbors = []
        if self.row < self.total_rows - 1:  # DOWN
            self.neighbors.append(grid[self.row + 1][self.col])

        if self.row > 0:  # UP
            self.neighbors.append(grid[self.row - 1][self.col])

        if self.col < self.total_rows - 1:  # RIGHT
            self.neighbors.append(grid[self.row][self.col + 1])

        if self.col > 0:  # LEFT
            self.neighbors.append(grid[self.row][self.col - 1])

    def get_neighbors(self):
        return self.neighbors

    def __lt__(self, other):
        return False

