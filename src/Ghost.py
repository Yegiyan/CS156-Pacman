import pyray as pr
import random
import time

class Ghost:
    def __init__(self, name, pos, grid_cell_size, color, base_sprite_coords, sprite_size, scale=1.0, speed=0.35):
        self.name = name
        self.grid_pos = pos
        self.target_pos = pos
        self.grid_cell_size = grid_cell_size
        self.color = color
        self.base_sprite_coords = base_sprite_coords
        self.sprite_size = sprite_size
        self.scale = scale
        self.speed = speed
        self.path = []
        self.move_timer = 0
        self.current_frame = 0
        self.animation_timer = 0
        self.animation_speed = 20
        self.direction = 'UP'
        self.just_changed_path = False
        self.mode = 'scatter'
        self.update_interval = 0.1 # interval in seconds for updating the path
        self.last_update_time = time.time()
        self.scatter_index = 0
        self.scatter_corners = {
            "Blinky": [(1, 26), (5, 23), (3, 21)],  # top-right
            "Pinky": [(1, 1), (3, 6), (5, 2)],      # top-left
            "Inky": [(29, 26), (26, 15), (26, 21)], # bottom-right
            "Clyde": [(29, 1), (23, 9), (29, 12)]   # bottom-left
        }

    def update_position(self, pacman_pos, grid, maze_module):
        current_time = time.time()

        if self.mode == 'frightened':
            if not self.path:
                self.frightened(grid, maze_module)
        elif self.mode == 'scatter':
            if not self.path or len(self.path) == 1:  # check if it's time to update path early
                self.scatter(grid, maze_module)
        elif self.mode == 'chase':
            if not self.path or (current_time - self.last_update_time > self.update_interval):
                self.chase(pacman_pos, grid, maze_module)
                self.last_update_time = current_time

        if self.path:
            next_step = self.path[0]  # peek next step
            if self.grid_pos == pacman_pos:
                self.path = []  # clear path if reached target
            elif self.move_timer >= 1:
                self.grid_pos = self.path.pop(0)  # move to next step
                if self.path:
                    self.target_pos = self.path[0]
                self.move_timer = 0  # reset move timer

            self.update_direction(next_step)

        self.move_timer += self.speed  # increment move timer by speed

    def update_direction(self, next_step):
        if next_step[0] < self.grid_pos[0]:
            self.direction = 'UP'
        elif next_step[0] > self.grid_pos[0]:
            self.direction = 'DOWN'
        elif next_step[1] < self.grid_pos[1]:
            self.direction = 'LEFT'
        elif next_step[1] > self.grid_pos[1]:
            self.direction = 'RIGHT'

    def chase(self, pacman_pos, grid, maze_module):
        if self.name == "Blinky":
            start = grid[self.grid_pos[0]][self.grid_pos[1]]
            target = grid[pacman_pos[1]][pacman_pos[0]]
            maze_module.clear_path(grid)
            maze_module.dijkstra(grid, start, target)
            path = [(step.row, step.col) for step in maze_module.reconstruct_path(target)]
            if path and path[0] == self.grid_pos:
                path.pop(0)
            self.path = path
            
        if self.name == "Pinky":
            # specific pinky chase pathing here
            pass
            
        if self.name == "Inky":
            # specific inky chase pathing here
            pass
            
        if self.name == "Clyde":
            # specific clyde chase pathing here
            pass
        
    def scatter(self, grid, maze_module):
        corners = self.scatter_corners[self.name]
        target_corner = corners[self.scatter_index]
    
        start = grid[self.grid_pos[0]][self.grid_pos[1]]
        target = grid[target_corner[0]][target_corner[1]]
        maze_module.clear_path(grid)
        maze_module.dijkstra(grid, start, target)
        path = [(step.row, step.col) for step in maze_module.reconstruct_path(target)]
    
        if path and path[0] == self.grid_pos:
            path.pop(0)
        self.path = path

        # increment scatter index to rotate to next corner
        self.scatter_index = (self.scatter_index + 1) % len(corners)

    def frightened(self, grid, maze_module):
        non_wall_cells = [cell for row in grid for cell in row if not cell.is_wall]
        destination = random.choice(non_wall_cells)
        start = grid[self.grid_pos[0]][self.grid_pos[1]]
        maze_module.clear_path(grid)
        maze_module.dijkstra(grid, start, destination)
        self.path = [(step.row, step.col) for step in maze_module.reconstruct_path(destination)]
        
    def get_center_position(self, vertical_offset):
        # interpolate positions between current and target based on move_timer
        pixel_x = (self.grid_pos[1] * (1 - self.move_timer) + self.target_pos[1] * self.move_timer) * self.grid_cell_size
        pixel_y = (self.grid_pos[0] * (1 - self.move_timer) + self.target_pos[0] * self.move_timer) * self.grid_cell_size
        pixel_y += vertical_offset
        
        scaled_width = self.sprite_size[0] * self.scale
        scaled_height = self.sprite_size[1] * self.scale
        center_x = pixel_x + (self.grid_cell_size - scaled_width) / 2
        center_y = pixel_y + (self.grid_cell_size - scaled_height) / 2
        return center_x, center_y
        
    def should_wrap(self, current_pos, next_pos, max_cols):
        return abs(current_pos[1] - next_pos[1]) > 1 and (current_pos[1] == 0 or next_pos[1] == 0 or current_pos[1] == max_cols-1 or next_pos[1] == max_cols-1)
        
    def draw_ghost(self, texture, vertical_offset=87, max_cols=28):
        frame_offset = {'UP': 0, 'DOWN': 2, 'LEFT': 4, 'RIGHT': 6}
        frame_num = frame_offset[self.direction] + self.current_frame
        sprite_x = self.base_sprite_coords[0] + frame_num * 20  # calculate x position of the frame

        center_x, center_y = self.get_center_position(vertical_offset)
        sprite_rect = pr.Rectangle(sprite_x, self.base_sprite_coords[1], self.sprite_size[0], self.sprite_size[1])
        dest_rect = pr.Rectangle(center_x, center_y, self.sprite_size[0]*self.scale, self.sprite_size[1]*self.scale)

        # check if the ghost should wrap around the screen
        if self.should_wrap(self.grid_pos, self.target_pos, max_cols):
            if self.direction == 'LEFT': # if moving left through the tunnel, draw on the right side
                wrap_x = (max_cols * self.grid_cell_size) + center_x
                wrap_rect = pr.Rectangle(wrap_x, center_y, self.sprite_size[0]*self.scale, self.sprite_size[1]*self.scale)
                pr.draw_texture_pro(texture, sprite_rect, wrap_rect, pr.Vector2(0, 0), 0, self.color)
            elif self.direction == 'RIGHT': # if moving right through the tunnel, draw on the left side
                wrap_x = center_x - (max_cols * self.grid_cell_size)
                wrap_rect = pr.Rectangle(wrap_x, center_y, self.sprite_size[0]*self.scale, self.sprite_size[1]*self.scale)
                pr.draw_texture_pro(texture, sprite_rect, wrap_rect, pr.Vector2(0, 0), 0, self.color)
        else:
            pr.draw_texture_pro(texture, sprite_rect, dest_rect, pr.Vector2(0, 0), 0, self.color)

        # update animation based on animation speed timer
        self.animation_timer += 1
        if self.animation_timer >= self.animation_speed:
            self.current_frame = 1 - self.current_frame  # toggle between 0 and 1
            self.animation_timer = 0  # reset animation timer

def create_blinky():
    return Ghost("Blinky", (14, 12), 24, pr.WHITE, (0, 80), (14, 14), 2.85, speed=0.1425)

def create_pinky():
    return Ghost("Pinky", (14, 11), 24, pr.WHITE, (0, 100), (14, 14), 2.85, speed=0.1425)

def create_inky():
    return Ghost("Inky", (14, 14), 24, pr.WHITE, (0, 120), (14, 14), 2.85, speed=0.1425)

def create_clyde():
    return Ghost("Clyde", (14, 15), 24, pr.WHITE, (0, 140), (14, 14), 2.85, speed=0.1425)