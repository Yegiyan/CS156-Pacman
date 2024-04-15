import pyray as pr

class Cell:
    def __init__(self, x, y, size, is_wall=False):
        self.x = x * size
        self.y = y * size
        self.size = size
        self.is_wall = is_wall

    def __str__(self):
        return f"Cell({self.x}, {self.y}, {self.size}, {'Wall' if self.is_wall else 'Open'})"

    def __repr__(self):
        return f"Cell(x={self.x}, y={self.y}, size={self.size}, is_wall={self.is_wall})"

def GridTest(screen_width, screen_height):
    cell_size = 24
    grid_width = screen_width // cell_size
    grid_height = 31
    
    vertical_offset = 87  # center grid vertically
    
    for x in range(grid_width):
        for y in range(grid_height):
            cell = Cell(x, y, cell_size, False)
            pr.draw_rectangle_lines(cell.x, cell.y + vertical_offset, cell.size, cell.size, pr.DARKBROWN if not cell.is_wall else pr.DARKPURPLE)
