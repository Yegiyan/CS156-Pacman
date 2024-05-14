import pyray as pr
import heapq, random

# 0 = pellet
# 1 = wall
# 2 = empty space
# 3 = large pellet
# 4 = fruit
# 5 = ghost wall

# ghost starting positions (in box)
#
#      blinky
# inky pinky clyde

# top right:  (26, 1)
# top  left:   (1, 1)
# bot right: (26, 29)
# bot  left:  (1, 29)

# blinky spawn: (13, 11)
# pacman spawn: (13, 23)

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
    [1, 1, 1, 1, 1, 1, 0, 1, 1, 2, 1, 1, 1, 2, 2, 1, 1, 1, 2, 1, 1, 0, 1, 1, 1, 1, 1, 1],
    [2, 2, 2, 2, 2, 2, 0, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 0, 2, 2, 2, 2, 2, 2],
    [1, 1, 1, 1, 1, 1, 0, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 0, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 0, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 0, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 0, 1, 1, 2, 2, 2, 2, 4, 4, 2, 2, 2, 2, 1, 1, 0, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 0, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 0, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 0, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 0, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1],
    [1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1],
    [1, 3, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 3, 1],
    [1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1],
    [1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],]

class Cell:
    def __init__(self, row, col, size=24, cell_type=0):
        self.col = col
        self.row = row
        self.x = col * size
        self.y = row * size
        self.size = size
        self.is_wall = cell_type == 1
        self.cell_type = cell_type # indicate if cell is part of the path
        self.fruit_type = None if cell_type != 4 else get_fruit_texture()

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
    
    grid = [[Cell(row, col, cell_size, maze_layout[row][col])
             for col in range(grid_width)] for row in range(grid_height)]
    
    return grid


def dijkstra(grid, start, end):
    start.cost = 0
    pq = []
    heapq.heappush(pq, (start.cost, start.row, start.col))  # use row and column as identifiers

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
            new_cost = current_cost + 1  # each step cost is 1
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

def clear_path(grid):
    for row in grid:
        for cell in row:
            cell.in_path = False
            cell.visited = False
            cell.cost = float('inf')  # reset cost to infinity (ensures next run starts with a clean slate)
            cell.previous = None      # clear path that was previously computed

def get_neighbors(grid, cell):
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # down, right, up, left
    neighbors = []
    max_row, max_col = len(grid), len(grid[0])
    for dx, dy in directions:
        nx, ny = cell.col + dx, cell.row + dy
        
        # wrap around logic for tunnels
        nx = nx % max_col

        if 0 <= nx < max_col and 0 <= ny < max_row and not grid[ny][nx].is_wall:
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

def get_fruit_texture():
    # fruit textures in atlas
    fruits = {
        "cherry": {"x": 169, "y": 161, "width": 12, "height": 12, "score": 100},
        "strawberry": {"x": 170, "y": 181, "width": 11, "height": 13, "score": 300},
        "orange": {"x": 170, "y": 201, "width": 11, "height": 12, "score": 500},
        "apple": {"x": 169, "y": 221, "width": 12, "height": 12, "score": 700}
    }
    
    # randomly select a fruit
    fruit_name = random.choice(list(fruits.keys()))
    fruit_data = fruits[fruit_name]

    return fruit_data 

def draw_grid(grid, texture_atlas, vertical_offset=87):
    for row in grid:
        for cell in row:
            if cell.is_wall:
                color = pr.DARKGRAY  # make walls visible for debugging
            elif cell.cell_type == 0:  # pellet
                pr.draw_circle(cell.x + cell.size // 2, cell.y + cell.size // 2 + vertical_offset, 3, pr.YELLOW)
            elif cell.cell_type == 3:  # large pellet
                pr.draw_circle(cell.x + cell.size // 2, cell.y + cell.size // 2 + vertical_offset, 6, pr.YELLOW)
            elif cell.cell_type == 4: # fruit
                source_rect = pr.Rectangle(cell.fruit_type['x'], cell.fruit_type['y'], cell.fruit_type['width'], cell.fruit_type['height'])
                dest_rect = pr.Rectangle(cell.x, cell.y + vertical_offset, cell.size, cell.size)
                pr.draw_texture_pro(texture_atlas, source_rect, dest_rect, pr.Vector2(0, 0), 0, pr.WHITE)
            elif cell.cell_type == 2 or cell.cell_type == 5:  # empty space or ghost wall
                continue
            else:
                pr.draw_rectangle_lines(cell.x, cell.y + vertical_offset, cell.size, cell.size, pr.GRAY)  # non-path color