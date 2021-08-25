from base import Node, reconstruct_path
import base
import pygame
from queue import PriorityQueue

clock = pygame.time.Clock()


class astarNode(Node):
    def __init__(self, row, col, width, total_rows):
        super().__init__(row, col, width, total_rows)
        self.weight = 1
        self.intensity = 255
        self.visited = False

    def add_weight(self):
        if self.intensity > 100:
            self.weight += 5
            self.color = (self.intensity, 0, self.intensity)
            self.intensity -= 10


def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)


def algorithm(draw, grid, start, end, fps):
    count = 0
    # The open list is a Priority Queue for A star
    open_list = PriorityQueue()
    open_list.put((0, count, start))  # stores the f score count and node
    came_from = {}
    # The g score is the cheapest path from the start to current node,
    # We start with a default value of infinity
    g_score = {node: float("inf") for row in grid for node in row}
    g_score[start] = 0
    # For a node n, the f_score = g_score + h(n). It is our current best guess
    # for the shortest path from start to end
    f_score = {node: float("inf") for row in grid for node in row}
    f_score[start] = h(start.get_pos(), end.get_pos())
    open_set = {start}
    while not open_list.empty():
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    quit()
        # We get the node with the smallest f_score
        node = open_list.get()[2]
        open_set.remove(node)
        if node == end:
            reconstruct_path(came_from, end, draw, start, end)
            return True, f_score[node]

        for neighbour in node.neighbours:
            # temp_g_score is the distance from the start to neighbour through 
            # the current node
            temp_g_score = g_score[node] + neighbour.weight
            if temp_g_score < g_score[neighbour]:
                # This path to the neighbour is better than the previous one
                came_from[neighbour] = node
                g_score[neighbour] = temp_g_score
                f_score[neighbour] = temp_g_score + h(neighbour.get_pos(), end.get_pos())
                if neighbour not in open_set:
                    count += 1
                    open_list.put((f_score[neighbour], count, neighbour))
                    open_set.add(neighbour)
                    if neighbour != start and neighbour != end:
                        neighbour.make_open()
        draw()
        if node != start and node != end:
            node.make_closed()

    return False, "Not found"


def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = astarNode(i, j, gap, rows)
            grid[i].append(node)

    return grid


def main(window, width, fps):
    ROWS = 40
    grid = make_grid(ROWS, width)
    start = None
    end = None
    run = True
    while run:
        base.draw(window, grid, ROWS, width)
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]:  # left click
                pos = pygame.mouse.get_pos()
                row, col = base.get_clicked_pos(pos, ROWS, width)
                node = grid[row][col]
                if not start and node != end:
                    start = node
                    start.make_start()

                elif not end and node != start:
                    end = node
                    end.make_end()

                elif node != end and node != start:
                    node.make_barrier()

            elif keys[pygame.K_w]:
                pos = pygame.mouse.get_pos()
                row, col = base.get_clicked_pos(pos, ROWS, width)
                node = grid[row][col]
                if node != end and node != start and not node.is_barrier():
                    node.add_weight()

            elif pygame.mouse.get_pressed()[2]:  # right
                pos = pygame.mouse.get_pos()
                row, col = base.get_clicked_pos(pos, ROWS, width)
                node = grid[row][col]
                node.reset()
                if node == start:
                    start = None

                elif node == end:
                    end = None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for node in row:
                            node.update_neighbours(grid)
                    return algorithm(lambda: base.draw(window, grid,
                                                       ROWS, width), grid, start, end, fps)

                if event.key == pygame.K_r:
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        quit()

    pygame.quit()


if __name__ == "__main__":
    WIDTH = 600
    window = pygame.display.set_mode((WIDTH, WIDTH))
    pygame.display.set_caption("Path Finder")
    main(window, WIDTH, 120)
