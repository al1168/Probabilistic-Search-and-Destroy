import pygame

CAVE = (255, 0, 0)
FOREST = (0, 255, 0)
AGENT = (255, 255, 0)
FLAT = (0, 0, 255)
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
        self.false_neg_prob = 0

    def get_false_neg_prob(self):
        return self.false_neg_prob
     def set_false_neg_prob(self, value):
         self.false_neg_prob = value

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
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_blocked():  # DOWN
            self.neighbors.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].is_blocked():  # UP
            self.neighbors.append(grid[self.row - 1][self.col])

        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_blocked():  # RIGHT
            self.neighbors.append(grid[self.row][self.col + 1])

        if self.col > 0 and not grid[self.row][self.col - 1].is_blocked():  # LEFT
            self.neighbors.append(grid[self.row][self.col - 1])

    def get_neighbors(self):
        return self.neighbors

    def __lt__(self, other):
        return False

