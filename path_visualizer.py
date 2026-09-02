import pygame
import heapq
import math

pygame.init()

# -----------------------------
# WINDOW SETTINGS
# -----------------------------
WIDTH = 800
ROWS = 40
CELL_SIZE = WIDTH // ROWS

WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Shortest Path Visualizer")

# -----------------------------
# COLORS
# -----------------------------
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (200, 200, 200)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
CYAN = (0, 255, 255)

# -----------------------------
# NODE CLASS
# -----------------------------
class Node:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.x = col * CELL_SIZE
        self.y = row * CELL_SIZE
        self.color = WHITE
        self.neighbors = []

    def get_pos(self):
        return self.row, self.col

    def is_closed(self):
        return self.color == RED

    def is_open(self):
        return self.color == GREEN

    def is_barrier(self):
        return self.color == BLACK

    def is_start(self):
        return self.color == ORANGE

    def is_end(self):
        return self.color == PURPLE

    def reset(self):
        self.color = WHITE

    def make_start(self):
        self.color = ORANGE

    def make_closed(self):
        self.color = RED

    def make_open(self):
        self.color = GREEN

    def make_barrier(self):
        self.color = BLACK

    def make_end(self):
        self.color = PURPLE

    def make_path(self):
        self.color = CYAN

    def draw(self, win):
        pygame.draw.rect(
            win,
            self.color,
            (self.x, self.y, CELL_SIZE, CELL_SIZE)
        )

    def update_neighbors(self, grid):
        self.neighbors = []

        # Down
        if self.row < ROWS - 1 and not grid[self.row + 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row + 1][self.col])

        # Up
        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row - 1][self.col])

        # Right
        if self.col < ROWS - 1 and not grid[self.row][self.col + 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col + 1])

        # Left
        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col - 1])

    def __lt__(self, other):
        return False


# -----------------------------
# GRID FUNCTIONS
# -----------------------------
def make_grid():
    grid = []

    for row in range(ROWS):
        grid.append([])

        for col in range(ROWS):
            node = Node(row, col)
            grid[row].append(node)

    return grid


def draw_grid_lines(win):
    for i in range(ROWS):
        pygame.draw.line(
            win,
            GREY,
            (0, i * CELL_SIZE),
            (WIDTH, i * CELL_SIZE)
        )

        pygame.draw.line(
            win,
            GREY,
            (i * CELL_SIZE, 0),
            (i * CELL_SIZE, WIDTH)
        )


def draw(win, grid):
    win.fill(WHITE)

    for row in grid:
        for node in row:
            node.draw(win)

    draw_grid_lines(win)
    pygame.display.update()


def get_clicked_pos(pos):
    x, y = pos

    row = y // CELL_SIZE
    col = x // CELL_SIZE

    return row, col


# -----------------------------
# PATH RECONSTRUCTION
# -----------------------------
def reconstruct_path(came_from, current, draw_func):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw_func()


# -----------------------------
# DIJKSTRA ALGORITHM
# -----------------------------
def dijkstra(draw_func, grid, start, end):
    count = 0

    priority_queue = [(0, count, start)]

    distance = {
        node: float("inf")
        for row in grid
        for node in row
    }

    distance[start] = 0
    came_from = {}

    queued = {start}

    while priority_queue:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False

        current = heapq.heappop(priority_queue)[2]

        if current == end:
            reconstruct_path(came_from, end, draw_func)
            end.make_end()
            start.make_start()
            return True

        queued.discard(current)

        for neighbor in current.neighbors:
            new_distance = distance[current] + 1

            if new_distance < distance[neighbor]:

                distance[neighbor] = new_distance
                came_from[neighbor] = current

                if neighbor not in queued:
                    count += 1

                    heapq.heappush(
                        priority_queue,
                        (
                            distance[neighbor],
                            count,
                            neighbor
                        )
                    )

                    queued.add(neighbor)
                    neighbor.make_open()

        draw_func()

        if current != start:
            current.make_closed()

    return False


# -----------------------------
# A* ALGORITHM
# -----------------------------
def heuristic(p1, p2):
    x1, y1 = p1
    x2, y2 = p2

    return abs(x1 - x2) + abs(y1 - y2)


def a_star(draw_func, grid, start, end):
    count = 0

    open_set = [(0, count, start)]

    g_score = {
        node: float("inf")
        for row in grid
        for node in row
    }

    g_score[start] = 0

    f_score = {
        node: float("inf")
        for row in grid
        for node in row
    }

    f_score[start] = heuristic(
        start.get_pos(),
        end.get_pos()
    )

    came_from = {}

    open_set_hash = {start}

    while open_set:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False

        current = heapq.heappop(open_set)[2]
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(
                came_from,
                end,
                draw_func
            )

            end.make_end()
            start.make_start()
            return True

        for neighbor in current.neighbors:

            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]:

                came_from[neighbor] = current

                g_score[neighbor] = temp_g_score

                f_score[neighbor] = (
                    temp_g_score
                    + heuristic(
                        neighbor.get_pos(),
                        end.get_pos()
                    )
                )

                if neighbor not in open_set_hash:

                    count += 1

                    heapq.heappush(
                        open_set,
                        (
                            f_score[neighbor],
                            count,
                            neighbor
                        )
                    )

                    open_set_hash.add(neighbor)
                    neighbor.make_open()

        draw_func()

        if current != start:
            current.make_closed()

    return False


# -----------------------------
# RESET SEARCH COLORS
# -----------------------------
def clear_search(grid, start, end):

    for row in grid:
        for node in row:

            if (
                not node.is_barrier()
                and node != start
                and node != end
            ):
                node.reset()

    start.make_start()
    end.make_end()


# -----------------------------
# MAIN PROGRAM
# -----------------------------
def main():
    grid = make_grid()

    start = None
    end = None

    running = True

    print("\nShortest Path Visualizer")
    print("------------------------")
    print("Left Click:")
    print("1st click  -> Start node")
    print("2nd click  -> End node")
    print("Next clicks -> Barriers")
    print()
    print("Right Click -> Remove node/barrier")
    print()
    print("Keyboard Controls:")
    print("D -> Run Dijkstra")
    print("A -> Run A*")
    print("R -> Clear search result")
    print("C -> Clear entire grid")
    print()

    while running:

        draw(WIN, grid)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            # LEFT CLICK
            if pygame.mouse.get_pressed()[0]:

                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos)

                node = grid[row][col]

                if not start and node != end:
                    start = node
                    start.make_start()

                elif not end and node != start:
                    end = node
                    end.make_end()

                elif (
                    node != start
                    and node != end
                ):
                    node.make_barrier()

            # RIGHT CLICK
            elif pygame.mouse.get_pressed()[2]:

                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos)

                node = grid[row][col]

                node.reset()

                if node == start:
                    start = None

                elif node == end:
                    end = None

            # KEYBOARD
            if event.type == pygame.KEYDOWN:

                # Dijkstra
                if event.key == pygame.K_d and start and end:

                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)

                    dijkstra(
                        lambda: draw(WIN, grid),
                        grid,
                        start,
                        end
                    )

                # A*
                if event.key == pygame.K_a and start and end:

                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)

                    a_star(
                        lambda: draw(WIN, grid),
                        grid,
                        start,
                        end
                    )

                # Clear search result only
                if event.key == pygame.K_r and start and end:
                    clear_search(
                        grid,
                        start,
                        end
                    )

                # Clear everything
                if event.key == pygame.K_c:

                    start = None
                    end = None
                    grid = make_grid()

    pygame.quit()


if __name__ == "__main__":
    main()
