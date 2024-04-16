import pyray as pr
import heapq

# 0 = pellet
# 1 = wall
# 2 = empty space
# 3 = large pellet
# 4 = fruit
# 5 = ghost wall

maze_layout = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1],
    [1, 3, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 3, 1],
    [1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1],
    [1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 0, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 0, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 0, 1, 1, 2, 1, 1, 1, 5, 5, 1, 1, 1, 2, 1, 1, 0, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 0, 1, 1, 2, 1, 1, 1, 0, 0, 1, 1, 1, 2, 1, 1, 0, 1, 1, 1, 1, 1, 1],
    [2, 2, 2, 2, 2, 2, 0, 0, 0, 2, 1, 0, 0, 0, 0, 0, 0, 1, 2, 0, 0, 0, 2, 2, 2, 2, 2, 2],
    [1, 1, 1, 1, 1, 1, 0, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 0, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 0, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 0, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 0, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 0, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 0, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 0, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 0, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 0, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1],
    [1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1],
    [1, 3, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 3, 1],
    [1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1],
    [1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],]

class Cell:
    def __init__(self, row, col, size=24, is_wall=False): # initialize new Cell instance with top left corner set as (row, col) > (0, 0)
        self.col = col  # x position in grid
        self.row = row  # y position in grid
        self.x = col * size  # x-coordinate in pixels
        self.y = row * size  # y-coordinate in pixels
        self.size = size
        self.is_wall = is_wall
        self.cost = float('inf')  # cost of getting to cell
        self.previous = None  # store the path
        self.visited = False
        self.in_path = False # indicate if cell is part of the path

    def __lt__(self, other):
        return self.cost < other.cost

    def __eq__(self, other):
        return (self.row == other.row) and (self.col == other.col)

    def __str__(self):
        wall_status = 'Wall' if self.is_wall else 'Open'
        return f"Cell({self.col}, {self.row}, {self.size}, {wall_status})"
    
    def __repr__(self):
        return f"Cell(row={self.row}, col={self.col}, size={self.size}, is_wall={self.is_wall})"

def init_grid(screen_width, screen_height):
    cell_size = 24
    grid_width = len(maze_layout[0])
    grid_height = len(maze_layout)
    vertical_offset = 87  # center grid vertically
    
    # initialize grid
    grid = [[Cell(row, col, cell_size, is_wall=(maze_layout[row][col] == 1))
             for col in range(grid_width)] for row in range(grid_height)]
    
    return grid

def dijkstra(grid, start, end):
    start.cost = 0
    pq = []
    heapq.heappush(pq, (start.cost, start.row, start.col))  # Use row and column as identifiers

    while pq:
        current_cost, row, col = heapq.heappop(pq)
        current = grid[row][col]
        if current.visited:
            continue
        current.visited = True

        if current == end:
            break

        for neighbor in get_neighbors(grid, current):
            if neighbor.visited:
                continue
            new_cost = current_cost + 1  # Assuming each step cost is 1
            if new_cost < neighbor.cost:
                neighbor.cost = new_cost
                neighbor.previous = current
                heapq.heappush(pq, (new_cost, neighbor.row, neighbor.col))

def reconstruct_path(end):
    path = []
    step = end
    while step.previous:
        step.in_path = True
        path.append(step)
        step = step.previous
    step.in_path = True  # mark the start cell
    path.append(step)
    path.reverse()
    return path

def get_neighbors(grid, cell):
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Down, Right, Up, Left
    neighbors = []
    for dx, dy in directions:
        nx, ny = cell.col + dx, cell.row + dy
        if 0 <= nx < len(grid[0]) and 0 <= ny < len(grid):
            if not grid[ny][nx].is_wall:
                neighbors.append(grid[ny][nx])
    return neighbors

def is_wall(x, y):
    return maze_layout[x][y] == 1

def is_direction_blocked(x, y, direction):
    if direction == 'UP':
        return maze_layout[y-1][x] == 1 or maze_layout[y-1][x] == 5
    elif direction == 'DOWN':
        return maze_layout[y+1][x] == 1 or maze_layout[y+1][x] == 5
    elif direction == 'LEFT':
        return maze_layout[y][x-1] == 1 or maze_layout[y][x-1] == 5
    elif direction == 'RIGHT':
        return maze_layout[y][x+1] == 1 or maze_layout[y][x+1] == 5
    return False

def draw_grid(grid):
    vertical_offset = 87
    for row in grid:
        for cell in row:
            if cell.is_wall:
                color = (0, 0, 0, 0)
            elif cell.in_path:
                color = pr.PURPLE  # path color
            else:
                color = pr.DARKPURPLE if cell.visited else pr.DARKBROWN
            pr.draw_rectangle_lines(cell.x, cell.y + vertical_offset, cell.size, cell.size, color)