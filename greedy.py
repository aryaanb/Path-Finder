from base import Node, reconstruct_path
import base
import pygame
from queue import PriorityQueue

clock = pygame.time.Clock()


class GreedyNode(Node):
    def __init__(self, row, col, width, total_rows):
        super().__init__(row, col, width, total_rows)
        self.visited = False
        self.weight = 0
        self.intensity = 255

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
    q = PriorityQueue()
    distance = {node: float("inf") for row in grid for node in row}
    distance[start] = h(start.get_pos(), end.get_pos())
    came_from = {}
    count = 0
    q.put((distance[start], count, start))
    while not q.empty():
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    quit()

        node = q.get()[2]
        node.visited = True
        if node != start and node != end:
            node.make_open()
        if node == end:
            reconstruct_path(came_from, end, draw, start, end)
            start.make_start()
            end.make_end()
            return True
        for neighbour in node.neighbours:
            if not neighbour.visited:
                neighbour.visited=True
                count += 1
                distance[neighbour] = h(neighbour.get_pos(), end.get_pos()) + neighbour.weight
                came_from[neighbour] = node
                q.put((distance[neighbour], count, neighbour))
        draw()


def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = GreedyNode(i, j, gap, rows)
            grid[i].append(node)

    return grid


def main(window, width, fps):
    ROWS = 40
    grid = make_grid(ROWS, width)
    start = None
    end = None
    run = True
    started = False
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
                    algorithm(lambda: base.draw(window, grid,
                                              ROWS, width), grid, start, end, fps)

                if event.key == pygame.K_r:
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)

    pygame.quit()


if __name__ == "__main__":
    WIDTH = 600
    window = pygame.display.set_mode((WIDTH, WIDTH))
    pygame.display.set_caption("Path Finder")
    main(window, WIDTH)
