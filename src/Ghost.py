import pyray as pr
import random

class Ghost:
    def __init__(self, name, pos, grid_cell_size, color, base_sprite_coords, sprite_size, scale=1.0, speed=0.25):
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
        self.mode = 'chase'

    def update_position(self, pacman_pos, grid, maze_module):
        if self.mode == 'frightened':
            if not self.path:
                self.frightened(grid, maze_module)
        elif self.mode == 'scatter':
            if not self.path:
                self.scatter(grid, maze_module)
        elif self.mode == 'chase':
            if not self.path:
                self.chase(pacman_pos, grid, maze_module)
        
        max_cols = 30
        if self.path and self.move_timer >= 1:
            next_step = self.path[0]  # get next step but do not pop it yet
            if self.should_wrap(self.grid_pos, next_step, max_cols):
                self.grid_pos = next_step  # instantly update to next position
                self.path.pop(0)  # remove step from path
                self.target_pos = self.grid_pos  # reset target position
                self.move_timer = 0  # reset move timer
            else:
                self.grid_pos = self.target_pos  # update current to target if not wrapping
                self.target_pos = self.path.pop(0)  # set new target position
                self.move_timer -= 1  # reset move timer for interpolation

            if next_step[0] < self.grid_pos[0]:
                self.direction = 'UP'
            elif next_step[0] > self.grid_pos[0]:
                self.direction = 'DOWN'
            elif next_step[1] < self.grid_pos[1]:
                self.direction = 'LEFT'
            elif next_step[1] > self.grid_pos[1]:
                self.direction = 'RIGHT'
        self.move_timer += self.speed  # increment move timer by speed
        
    def frightened(self, grid, maze_module):
        non_wall_cells = [cell for row in grid for cell in row if not cell.is_wall]
        destination = random.choice(non_wall_cells)
        start = grid[self.grid_pos[0]][self.grid_pos[1]]
        maze_module.clear_path(grid)
        maze_module.dijkstra(grid, start, destination)
        self.path = [(step.row, step.col) for step in maze_module.reconstruct_path(destination)]

    def chase(self, pacman_pos, grid, maze_module):
        print(f"Chasing Pacman at position: {pacman_pos}")

        start = grid[self.grid_pos[0]][self.grid_pos[1]]
        target = grid[pacman_pos[1]][pacman_pos[0]]
    
        print(f"Start Cell: {start}")  # Debugging start cell
        print(f"Target Cell: {target}")  # Debugging target cell

        maze_module.clear_path(grid)
        maze_module.dijkstra(grid, start, target)
        self.path = [(step.row, step.col) for step in maze_module.reconstruct_path(target)]

        
    def scatter(self, grid, maze_module):
        # define scatter behavior, where ghosts move towards fixed corners
        pass
        
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
        
    def draw_ghost(self, texture, vertical_offset=87):
        frame_offset = {'UP': 0, 'DOWN': 2, 'LEFT': 4, 'RIGHT': 6}
        frame_num = frame_offset[self.direction] + self.current_frame
        sprite_x = self.base_sprite_coords[0] + frame_num * 20  # calculate x position of the frame

        center_x, center_y = self.get_center_position(vertical_offset)
        sprite_rect = pr.Rectangle(sprite_x, self.base_sprite_coords[1], self.sprite_size[0], self.sprite_size[1])
        dest_rect = pr.Rectangle(center_x, center_y, self.sprite_size[0]*self.scale, self.sprite_size[1]*self.scale)
        pr.draw_texture_pro(texture, sprite_rect, dest_rect, pr.Vector2(0, 0), 0, self.color)

        # update animation based on animation speed timer
        self.animation_timer += 1
        if self.animation_timer >= self.animation_speed:
            self.current_frame = 1 - self.current_frame  # toggle between 0 and 1
            self.animation_timer = 0  # reset animation timer

def create_blinky():
    return Ghost("Blinky", (14, 13), 24, pr.WHITE, (0, 80), (14, 14), 2.85, speed=0.1)