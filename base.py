import pygame
pygame.init()
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)
clock = pygame.time.Clock()


class Node:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neighbours = []
        self.width = width
        self.total_rows = total_rows
        self.visited = False

    def get_pos(self):
        return self.row, self.col

    # To check if node is on the closed list
    def is_closed(self):
        return self.color == TURQUOISE

    # To check if node is in the open list
    def is_open(self):
        return self.color == BLUE

    # Checks if node is an obstacle
    def is_barrier(self):
        return self.color == BLACK

    def is_start(self):
        return self.color == GREEN

    def is_end(self):
        return self.color == RED

    def reset(self):
        self.color = WHITE

    def make_closed(self):
        self.color = TURQUOISE

    def make_open(self):
        self.color = BLUE

    def make_barrier(self):
        self.color = BLACK

    def make_start(self):
        self.color = GREEN

    def make_end(self):
        self.color = RED

    def make_path(self):
        self.color = PURPLE

    def draw(self, window):
        pygame.draw.rect(window, self.color,
                         (self.x, self.y, self.width, self.width))

    def update_neighbours(self, grid):
        self.neighbours = []
        # above
        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():
            self.neighbours.append(grid[self.row - 1][self.col])
        # below
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():
            self.neighbours.append(grid[self.row + 1][self.col])
        # right
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():
            self.neighbours.append(grid[self.row][self.col + 1])
        # left
        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():
            self.neighbours.append(grid[self.row][self.col - 1])

        # # top right diagonal
        # if self.row > 0 and self.col < self.total_rows - 1 and not grid[self.row - 1][self.col + 1].is_barrier():
        #     self.neighbours.append(grid[self.row - 1][self.col + 1])
        # # top left diagonal
        # if self.row > 0 and self.col > 0 and not grid[self.row - 1][self.col -1].is_barrier():
        #     self.neighbours.append(grid[self.row - 1][self.col -1])
        # # bottom right diagonal
        # if self.row < self.total_rows - 1 and self.col < self.total_rows - 1 and not grid[self.row + 1][self.col + 1].is_barrier():
        #     self.neighbours.append(grid[self.row + 1][self.col + 1])
        # # bottom left diagonal
        # if self.row < self.total_rows - 1 and self.col > 0 and not grid[self.row + 1][self.col - 1].is_barrier():
        #     self.neighbours.append(grid[self.row + 1][self.col - 1])

    def __lt__(self, other):
        return False


def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i, j, gap, rows)
            grid[i].append(node)

    return grid


def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
        pygame.draw.line(win, GREY, (i * gap, 0), (i * gap, width))


def draw(win, grid, rows, width):
    win.fill(WHITE)

    for row in grid:
        for node in row:
            node.draw(win)
    draw_grid(win, rows, width)
    pygame.display.update()


def get_clicked_pos(pos, rows, width):
    gap = width // rows
    x, y = pos
    row = x // gap
    col = y // gap
    return row, col


def reconstruct_path(came_from, current, draw, start, end):
    while current in came_from:
        current = came_from[current]
        if current != start and current != end:
            current.make_path()
        draw()
