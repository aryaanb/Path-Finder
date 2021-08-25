from base import Node, reconstruct_path
import base
import pygame
from queue import PriorityQueue
import random

clock = pygame.time.Clock()


class dijNode(Node):
    def __init__(self, row, col, width, total_rows):
        super().__init__(row, col, width, total_rows)
        self.weight = 1
        self.intensity = 255

    def add_weight(self):
        if self.intensity > 100:
            self.weight += 5
            self.color = (self.intensity, 0, self.intensity)
            self.intensity -= 10


def algorithm(draw, grid, start, end, fps):
    q = PriorityQueue()
    count = 0
    came_from = {}
    q.put((0, count, start))
    distance = {node: float("inf") for row in grid for node in row}
    distance[start] = 0
    q_hash = {start}
    while not q.empty():
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    quit()

        current = q.get()[2]
        q_hash.remove(current)
        if current == end:
            reconstruct_path(came_from, end, draw, start, end)
            end.make_end()
            start.make_start()
            print(distance[current])
            return True
        if current != start:
            current.make_closed()

        for neighbour in current.neighbours:
            dist = distance[current] + neighbour.weight
            if dist < distance[neighbour]:
                distance[neighbour] = dist
                came_from[neighbour] = current
                if neighbour not in q_hash:
                    count += 1
                    q.put((distance[neighbour], count, neighbour))
                    q_hash.add(neighbour)
                    neighbour.make_open()
        draw()

    return False


def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = dijNode(i, j, gap, rows)
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

                elif node.weight == 5:
                    node.weight = 1

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for node in row:
                            node.update_neighbours(grid)
                    algorithm(lambda: base.draw(window, grid, ROWS, width), grid, start, end, fps)


                if event.key == pygame.K_r:
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        quit()


if __name__ == "__main__":
    WIDTH = 600
    window = pygame.display.set_mode((WIDTH, WIDTH))
    pygame.display.set_caption("Path Finder")
    main(window, WIDTH)
