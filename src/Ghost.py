import pyray as pr
import random
import time

class Ghost:
    def __init__(self, name, pos, spawn_pos, grid_cell_size, color, base_sprite_coords, sprite_size, scale=1.0, speed=0.35):
        self.name = name
        self.grid_pos = pos
        self.target_pos = pos
        self.spawn_pos = spawn_pos
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
        self.frightened_start_time = None
        self.mode = 'scatter'
        self.update_interval = 0.1 # interval in seconds for updating the path
        self.last_update_time = time.time()
        self.eaten_coords = (0, 200)
        self.scatter_index = 0
        self.scatter_corners = {
            "Blinky": [(1, 26), (5, 23), (3, 21)],  # top-right
            "Pinky": [(1, 1), (3, 6), (5, 2)],      # top-left
            "Inky": [(29, 26), (26, 15), (26, 21)], # bottom-right
            "Clyde": [(29, 1), (23, 9), (29, 12)]   # bottom-left
        }

    def update_position(self, pacman_pos, pacman_direction, blinky_pos, grid, maze_module):
        current_time = time.time()
        
        if self.mode == 'frightened':
            self.speed = 0.08
            if self.grid_pos[1] == pacman_pos[0] and self.grid_pos[0] == pacman_pos[1]:
                self.mode = 'eaten'
                self.path = self.return_to_spawn(grid, maze_module)  # generate path to spawn point
                return
            
        if self.mode == 'eaten':
            self.speed = 0.1425
            if self.grid_pos == self.spawn_pos:
                self.mode = random.choice(['scatter', 'chase'])  # choose mode randomly
            if not self.path:
                self.path = self.return_to_spawn(grid, maze_module)
            
        if self.mode == 'frightened' and (current_time - self.frightened_start_time) >= 8:
                    self.mode = 'scatter'

        if self.mode in ['frightened', 'scatter', 'chase']:
            if not self.path or (len(self.path) == 1 and self.move_timer >= 1):
                if self.mode == 'frightened':
                    self.path = self.frightened(grid, maze_module)
                elif self.mode == 'scatter':
                    self.scatter(grid, maze_module)
                elif self.mode == 'chase':
                    self.chase(pacman_pos, pacman_direction, blinky_pos, grid, maze_module)
                self.last_update_time = current_time

        if self.path:
            next_step = self.path[0]
            if self.grid_pos == pacman_pos:
                self.path = []
            if self.move_timer >= 1:
                if self.grid_pos != next_step: # ensure it moves to the next grid cell
                    self.grid_pos = next_step
                    self.move_timer = 0 # reset move timer after aligning with grid
                    if len(self.path) > 1:
                        self.update_direction(self.path[1]) # update direction to next after current
                    else:
                        self.update_direction(next_step)
                if self.path:
                    self.target_pos = next_step
                    self.path.pop(0)

        self.move_timer += self.speed

    def return_to_spawn(self, grid, maze_module):
        start = grid[self.grid_pos[0]][self.grid_pos[1]]
        spawn = grid[self.spawn_pos[0]][self.spawn_pos[1]]
        maze_module.clear_path(grid)
        maze_module.dijkstra(grid, start, spawn)
        path = [(step.row, step.col) for step in maze_module.reconstruct_path(spawn)]
        if path and path[0] == self.grid_pos:
            path.pop(0)
        return path

    def update_direction(self, next_step):
        if next_step[0] < self.grid_pos[0]:
            self.direction = 'UP'
        elif next_step[0] > self.grid_pos[0]:
            self.direction = 'DOWN'
        elif next_step[1] < self.grid_pos[1]:
            self.direction = 'LEFT'
        elif next_step[1] > self.grid_pos[1]:
            self.direction = 'RIGHT'

    def chase(self, pacman_pos, pacman_direction, blinky_pos, grid, maze_module):
        if self.name == "Blinky":
            # pathfind from blinky's current position to target
            start = grid[self.grid_pos[0]][self.grid_pos[1]]
            target = grid[pacman_pos[1]][pacman_pos[0]]
            maze_module.clear_path(grid)
            maze_module.dijkstra(grid, start, target)
            path = [(step.row, step.col) for step in maze_module.reconstruct_path(target)]
            if path and path[0] == self.grid_pos:
                path.pop(0)
            self.path = path
            
        elif self.name == "Pinky":
            target_y, target_x = pacman_pos

            # adjust target based on Pacman's direction
            if pacman_direction == 'UP':
                target_x -= 4
            elif pacman_direction == 'DOWN':
                target_x += 4
            elif pacman_direction == 'LEFT':
                target_y -= 4
            elif pacman_direction == 'RIGHT':
                target_y += 4

            # check if target is within the grid boundaries
            if 0 <= target_x < len(grid) and 0 <= target_y < len(grid[0]):
                if not grid[target_x][target_y].is_wall:
                    valid_target = True
                else:
                    valid_target = False
            else:
                valid_target = False

            # fallback to blinky's chase behavior if target is not valid
            if not valid_target:
                target_y, target_x = pacman_pos

            # pathfind from pinky's current position to target
            start = grid[self.grid_pos[0]][self.grid_pos[1]]
            target = grid[target_x][target_y]
            maze_module.clear_path(grid)
            maze_module.dijkstra(grid, start, target)
            path = [(step.row, step.col) for step in maze_module.reconstruct_path(target)]
            if path and path[0] == self.grid_pos:
                path.pop(0)
            self.path = path
            
        if self.name == "Inky":
            # calculate intermediate target two cells in front of pacman
            inter_target_y, inter_target_x = pacman_pos
            if pacman_direction == 'UP':
                inter_target_x -= 2
            elif pacman_direction == 'DOWN':
                inter_target_x += 2
            elif pacman_direction == 'LEFT':
                inter_target_y -= 2
            elif pacman_direction == 'RIGHT':
                inter_target_y += 2
            
            # ensure intermediate target is within grid boundaries
            inter_target_x = max(0, min(inter_target_x, len(grid) - 1))
            inter_target_y = max(0, min(inter_target_y, len(grid[0]) - 1))

            # calculate vector from blinky to intermediate target
            vector_x = inter_target_x - blinky_pos[0]
            vector_y = inter_target_y - blinky_pos[1]

            # extend vector by its own length from intermediate target
            final_target_x = inter_target_x + vector_x
            final_target_y = inter_target_y + vector_y
            
            # check if final target is within grid
            final_target_x = max(0, min(final_target_x, len(grid) - 1))
            final_target_y = max(0, min(final_target_y, len(grid[0]) - 1))

            # check if final target is not wall else  fall back to blinky's behavior
            if grid[final_target_x][final_target_y].is_wall:
                final_target_y, final_target_x = pacman_pos

            # pathfind from inky's current position to final target
            start = grid[self.grid_pos[0]][self.grid_pos[1]]
            target = grid[final_target_x][final_target_y]
            maze_module.clear_path(grid)
            maze_module.dijkstra(grid, start, target)
            path = [(step.row, step.col) for step in maze_module.reconstruct_path(target)]
            if path and path[0] == self.grid_pos:
                path.pop(0)
            self.path = path
            
        if self.name == "Clyde":
            # calculate distance between clyde and pacman, with a threshold of 8 cells
            distance = ((self.grid_pos[0] - pacman_pos[0]) ** 2 + (self.grid_pos[1] - pacman_pos[1]) ** 2) ** 0.5
            threshold = 8
            
            if distance < threshold:
                # use blinky's chase behaviour
                start = grid[self.grid_pos[0]][self.grid_pos[1]]
                target = grid[pacman_pos[1]][pacman_pos[0]]
                maze_module.clear_path(grid)
                maze_module.dijkstra(grid, start, target)
                path = [(step.row, step.col) for step in maze_module.reconstruct_path(target)]
                if path and path[0] == self.grid_pos:
                    path.pop(0)
                self.path = path
            else:
                # revert to scatter mode
                self.scatter(grid, maze_module)
        
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
        path = [(step.row, step.col) for step in maze_module.reconstruct_path(destination)]
        if path and path[0] == self.grid_pos:
            path.pop(0)
        return path
        
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

        # initial coordinates should default to normal mode coordinates
        sprite_x = self.base_sprite_coords[0] + frame_num * 20
        sprite_y = self.base_sprite_coords[1]

        if self.mode == 'frightened':
            current_time = time.time()
            time_left = self.frightened_start_time + 8 - current_time  # calculate remaining time in frightened mode
            
            if time_left <= 3:
                # alternate between textures every 0.10 seconds for visual cue
                index = int((current_time % 1) // 0.10) % 4
                sprite_x = 20 * index  # coordinates 0, 20, 40, 60 based on time fraction
                sprite_y = 160
            else:
                sprite_x = 20 * self.current_frame  # alternates between x-coord 0 and 20 normally
                sprite_y = 160

        elif self.mode == 'eaten':
            # adjust texture coordinates specifically for 'eaten' mode
            sprite_x, sprite_y = self.eaten_coords
            sprite_x += {'UP': 0, 'DOWN': 20, 'LEFT': 40, 'RIGHT': 60}[self.direction]

        center_x, center_y = self.get_center_position(vertical_offset)
        sprite_rect = pr.Rectangle(sprite_x, sprite_y, self.sprite_size[0], self.sprite_size[1])
        dest_rect = pr.Rectangle(center_x, center_y, self.sprite_size[0] * self.scale, self.sprite_size[1] * self.scale)

        # ghost wrap-around logic for moving through tunnels
        if self.should_wrap(self.grid_pos, self.target_pos, max_cols):
            if self.direction == 'LEFT':
                wrap_x = (max_cols * self.grid_cell_size) + center_x
                wrap_rect = pr.Rectangle(wrap_x, center_y, self.sprite_size[0] * self.scale, self.sprite_size[1] * self.scale)
                pr.draw_texture_pro(texture, sprite_rect, wrap_rect, pr.Vector2(0, 0), 0, self.color)
            elif self.direction == 'RIGHT':
                wrap_x = center_x - (max_cols * self.grid_cell_size)
                wrap_rect = pr.Rectangle(wrap_x, center_y, self.sprite_size[0] * self.scale, self.sprite_size[1] * self.scale)
                pr.draw_texture_pro(texture, sprite_rect, wrap_rect, pr.Vector2(0, 0), 0, self.color)
        else:
            pr.draw_texture_pro(texture, sprite_rect, dest_rect, pr.Vector2(0, 0), 0, self.color)

        # animation update logic
        self.animation_timer += 1
        if self.animation_timer >= self.animation_speed:
            self.current_frame = 1 - self.current_frame  # toggle between frame 0 and 1
            self.animation_timer = 0  # reset timer


def create_blinky():
    return Ghost("Blinky", (14, 12), (14, 12), 24, pr.WHITE, (0, 80), (14, 14), 2.85, speed=0.1425)

def create_pinky():
    return Ghost("Pinky", (14, 11), (14, 11), 24, pr.WHITE, (0, 100), (14, 14), 2.85, speed=0.1425)

def create_inky():
    return Ghost("Inky", (14, 15), (14, 15), 24, pr.WHITE, (0, 120), (14, 14), 2.85, speed=0.1425)

def create_clyde():
    return Ghost("Clyde", (14, 16), (14, 16), 24, pr.WHITE, (0, 140), (14, 14), 2.85, speed=0.1425)