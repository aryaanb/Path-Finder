from base import Node, reconstruct_path
import base
import pygame
import sys

clock = pygame.time.Clock()
sys.setrecursionlimit(10**6)

class dfsNode(Node):
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


def dfs_alg(draw, start, node, end, fps, came_from, dist):
    draw()
    clock.tick(fps)
    # If we have reached the end node we return true
    if node == end:
        reconstruct_path(came_from, end, draw, start, end)
        start.make_start()
        return True, dist
    # Mark the current node as visited
    node.visited = True
    if node != start and node != end:
        node.make_closed()
    for neighbour in node.neighbours:
        # For every neighbour that has not been visited we recursively call the DFS algorithm
        if not neighbour.visited:
            if neighbour != start and neighbour != end:
                neighbour.make_open()
            came_from[neighbour] = node
            found, result = dfs_alg(
                draw, start, neighbour, end, fps, came_from, dist + 1)
            if found:
                return True, result
    return False, "Not found"


def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = dfsNode(i, j, gap, rows)
            grid[i].append(node)

    return grid


def main(window, width, fps):
    ROWS = 40
    grid = make_grid(ROWS, width)
    start = None
    end = None
    run = True
    grid[0][0].reset()
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
                    return dfs_alg(lambda: base.draw(window, grid,
                                              ROWS, width), start, start, end, fps, {}, 0)

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
    main(window, WIDTH, 200)
