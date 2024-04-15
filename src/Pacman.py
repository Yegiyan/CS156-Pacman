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
        'speed': 8,
        'last_move_time': pr.get_time(),
        'current_frame': 0,
        'frame_offset': 0,
        'sprite_regions': [pr.Rectangle(0, 0, 13, 13), pr.Rectangle(20, 0, 13, 13), pr.Rectangle(40, 0, 13, 13),
                           pr.Rectangle(0, 20, 13, 13), pr.Rectangle(20, 20, 13, 13), pr.Rectangle(40, 20, 13, 13)]
    }
    return pacman

def move_pacman(pacman, maze, vertical_offset=87, horizontal_offset=0):
    current_time = pr.get_time()
    grid_x, grid_y = pacman['grid_pos']
    current_dir = pacman['current_direction']
    queued_dir = pacman['queued_direction']

    if current_time - pacman['last_move_time'] > 1 / pacman['speed']:
        # handle tunnel teleporting
        if (grid_y, grid_x) == (14, 0) and current_dir == 'LEFT':
            grid_x = 26
        elif (grid_y, grid_x) == (14, 27) and current_dir == 'RIGHT':
            grid_x = 1
        else:
            effective_dir = queued_dir if not maze.is_direction_blocked(grid_x, grid_y, queued_dir) else current_dir
            if not maze.is_direction_blocked(grid_x, grid_y, effective_dir):
                if effective_dir in ['UP', 'DOWN']:
                    grid_y += 1 if effective_dir == 'DOWN' else -1
                    pacman['frame_offset'] = 3  # use vertical frames
                elif effective_dir in ['LEFT', 'RIGHT']:
                    grid_x += 1 if effective_dir == 'RIGHT' else -1
                    pacman['frame_offset'] = 0  # use horizontal frames

                pacman['current_direction'] = effective_dir
                pacman['last_move_time'] = current_time
                pacman['current_frame'] = (pacman['current_frame'] + 1) % 3  # cycle through 0, 1, 2

    pacman['grid_pos'] = (grid_x, grid_y)
    pacman['x'] = horizontal_offset + grid_x * 24 + (24 - pacman['size']) / 2
    pacman['y'] = vertical_offset + grid_y * 24 + (24 - pacman['size']) / 2

    
def draw_pacman(pacman, pacman_texture):
    frame_index = pacman['frame_offset'] + pacman['current_frame']
    frame = pacman['sprite_regions'][frame_index]
    pacman_dest_rect = pr.Rectangle(pacman['x'], pacman['y'], pacman['size'], pacman['size'])

    if pacman['current_direction'] == 'LEFT':
        frame.width = abs(frame.width)
    else:
        frame.width = -abs(frame.width)

    if pacman['current_direction'] == 'DOWN':
        frame.height = -abs(frame.height)
    else:
        frame.height = abs(frame.height)

    pr.draw_texture_pro(pacman_texture, frame, pacman_dest_rect, pr.Vector2(0, 0), 0, pr.WHITE)