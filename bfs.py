from base import Node, reconstruct_path
import base
import pygame
from queue import Queue

clock = pygame.time.Clock()


class bfsNode(Node):
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


def bfs_alg(draw, start, end, fps):
    # The open list in BFS is a Queue.
    open_list = Queue()
    # Tracks the parent of each node
    came_from = {}
    # Put the start node on the open list
    open_list.put(start)
    # Mark the start node as visited
    start.visited = True
    # Tracks the distance of each node from the start
    distance = {}
    distance[start] = 0
    while not open_list.empty():
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    quit()
        # Gets node from the Queue
        node = open_list.get()
        if node != start and node != end:
            # This shows that the node is in the closed list
            node.make_closed()
        # If we reach our goal noad we construct the path and end the algorithm
        if node == end:
            reconstruct_path(came_from, end, draw, start, end)
            return True, distance[node]

        for neighbour in node.neighbours:
            # If a neighbour is not in the closed list
            if not neighbour.visited:
                # We track where each node is coming from, this helps us construct the path
                came_from[neighbour] = node
                if neighbour != start and neighbour != end:
                    # Shows that neighbour is in the open list
                    neighbour.make_open()
                # Adds neighbour to the open list
                open_list.put(neighbour)
                # We mark all nodes added to the open list as visited
                neighbour.visited = True
                distance[neighbour] = distance[node] + 1
        draw()


def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = bfsNode(i, j, gap, rows)
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
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    quit()

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
                    return bfs_alg(lambda: base.draw(window, grid,
                                              ROWS, width), start, end, fps)

                if event.key == pygame.K_r:
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)
    pygame.quit()


if __name__ == "__main__":
    WIDTH = 600
    window = pygame.display.set_mode((WIDTH, WIDTH))
    pygame.display.set_caption("Path Finder")
    main(window, WIDTH, 10000)
