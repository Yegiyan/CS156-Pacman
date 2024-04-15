import pyray as pr

def create_pacman(grid_x, grid_y, cell_size=24, scale=2.85, vertical_offset=87, horizontal_offset=0):
    scaled_size = 13 * scale
    pacman = {
        'x': horizontal_offset + grid_x * cell_size + (cell_size - scaled_size) / 2,
        'y': vertical_offset + grid_y * cell_size + (cell_size - scaled_size) / 2,
        'size': scaled_size,
        'grid_pos': (grid_x, grid_y),
        'current_direction': 'STOP',
        'queued_direction': 'STOP',
        'speed': 5,  # pixels per second
        'last_move_time': pr.get_time(),
        'sprite_region': pr.Rectangle(0, 0, 13, 13)
    }
    return pacman

def move_pacman(pacman, maze, vertical_offset=87, horizontal_offset=0):
    current_time = pr.get_time()
    grid_x, grid_y = pacman['grid_pos']
    current_dir = pacman['current_direction']
    queued_dir = pacman['queued_direction']
    
    # decide effective direction
    if current_time - pacman['last_move_time'] > 1 / pacman['speed']:
        effective_dir = queued_dir if not maze.is_wall_in_direction(grid_x, grid_y, queued_dir) else current_dir
        if not maze.is_wall_in_direction(grid_x, grid_y, effective_dir):
            if effective_dir == 'UP':
                grid_y -= 1
            elif effective_dir == 'DOWN':
                grid_y += 1
            elif effective_dir == 'LEFT':
                grid_x -= 1
            elif effective_dir == 'RIGHT':
                grid_x += 1
                
            # update current direction to effective direction if movement happened
            pacman['current_direction'] = effective_dir
            pacman['last_move_time'] = current_time

    pacman['grid_pos'] = (grid_x, grid_y)
    pacman['x'] = horizontal_offset + grid_x * 24 + (24 - pacman['size']) / 2
    pacman['y'] = vertical_offset + grid_y * 24 + (24 - pacman['size']) / 2