import pyray as pr
import time

DURATION_EAT_PELLET = 0.5455
DURATION_EAT_FRUIT = 1.0

last_played_times = {
    "eat_pellet": 0,
    "eat_fruit": 0
}

def can_play_sound(sound_key, duration):
    current_time = time.time()
    last_played = last_played_times[sound_key]
    return current_time - last_played > duration

def create_pacman(grid_x, grid_y, cell_size=24, scale=2.85, vertical_offset=87, horizontal_offset=0):
    scaled_size = 13 * scale
    pacman = {
        'x': horizontal_offset + grid_x * cell_size + (cell_size - scaled_size) / 2,
        'y': vertical_offset + grid_y * cell_size + (cell_size - scaled_size) / 2,
        'size': scaled_size,
        'grid_pos': (grid_x, grid_y),
        'old_x': horizontal_offset + grid_x * cell_size + (cell_size - scaled_size) / 2,  # old position for interpolation
        'old_y': vertical_offset + grid_y * cell_size + (cell_size - scaled_size) / 2,  # old position for interpolation
        'current_direction': 'STOP',
        'queued_direction': 'STOP',
        'speed': 8,
        'last_move_time': pr.get_time(),
        'current_frame': 0,
        'frame_offset': 0,
        'score': 0,
        'ghosts_eaten': 0,
        'sprite_regions': [
            pr.Rectangle(0, 0, 13, 13), pr.Rectangle(20, 0, 13, 13), pr.Rectangle(40, 0, 13, 13),
            pr.Rectangle(0, 20, 13, 13), pr.Rectangle(20, 20, 13, 13), pr.Rectangle(40, 20, 13, 13)
        ]
    }
    return pacman

def move_pacman(pacman, ghosts, eat_pellet_sound, eat_fruit_sound, grid, maze, vertical_offset=87, horizontal_offset=0):
    current_time = pr.get_time()
    grid_x, grid_y = pacman['grid_pos']
    current_dir = pacman['current_direction']
    queued_dir = pacman['queued_direction']

    if current_time - pacman['last_move_time'] > 1 / pacman['speed']:
        # save old positions for interpolation
        pacman['old_x'] = pacman['x']
        pacman['old_y'] = pacman['y']

        # handle tunnel teleporting
        if (grid_x, grid_y) == (0, 14) and current_dir == 'LEFT':
            grid_x = 26
        elif (grid_x, grid_y) == (27, 14) and current_dir == 'RIGHT':
            grid_x = 1
        else:
            effective_dir = queued_dir if not maze.is_direction_blocked(grid_x, grid_y, queued_dir) else current_dir
            if not maze.is_direction_blocked(grid_x, grid_y, effective_dir):
                if effective_dir == 'UP':
                    grid_y -= 1
                    pacman['frame_offset'] = 3  # use vertical frames
                elif effective_dir == 'DOWN':
                    grid_y += 1
                    pacman['frame_offset'] = 3  # use vertical frames
                elif effective_dir == 'LEFT':
                    grid_x -= 1
                    pacman['frame_offset'] = 0  # use horizontal frames
                elif effective_dir == 'RIGHT':
                    grid_x += 1
                    pacman['frame_offset'] = 0  # use horizontal frames

                pacman['current_direction'] = effective_dir
                pacman['last_move_time'] = current_time
                pacman['current_frame'] = (pacman['current_frame'] + 1) % 3  # cycle through 0, 1, 2

        # update pacman's grid position
        pacman['grid_pos'] = (grid_x, grid_y)

        # check cell type for pellet consumption
        current_cell = grid[grid_y][grid_x]
        if current_cell.cell_type == 0:  # Small pellet
            if can_play_sound("eat_pellet", DURATION_EAT_PELLET):
                pr.play_sound(eat_pellet_sound)
                last_played_times["eat_pellet"] = time.time()
            current_cell.cell_type = 2
            pacman['score'] += 10
        elif current_cell.cell_type == 3:  # Power pellet
            if can_play_sound("eat_pellet", DURATION_EAT_PELLET):
                pr.play_sound(eat_pellet_sound)
                last_played_times["eat_pellet"] = time.time()
            current_cell.cell_type = 2
            pacman['score'] += 50
            pacman['ghosts_eaten'] = 0
            for ghost in ghosts:
                ghost.mode = 'frightened'
                ghost.frightened_start_time = time.time()
        elif current_cell.cell_type == 4:  # Fruit
            if current_cell.fruit_type:
                pacman['score'] += current_cell.fruit_type['score']
            if can_play_sound("eat_fruit", DURATION_EAT_FRUIT):
                pr.play_sound(eat_fruit_sound)
                last_played_times["eat_fruit"] = time.time()
            current_cell.cell_type = 2

        # update actual position for rendering
        pacman['x'] = horizontal_offset + grid_x * 24 + (24 - pacman['size']) / 2
        pacman['y'] = vertical_offset + grid_y * 24 + (24 - pacman['size']) / 2
    
def draw_pacman(pacman, pacman_texture):
    current_time = pr.get_time()
    time_since_last_move = current_time - pacman['last_move_time']
    move_interval = 1 / pacman['speed']
    time_fraction = min(time_since_last_move / move_interval, 1)  # clamp to 1 to avoid overshooting

    # interpolated position
    interpolated_x = pacman['old_x'] + (pacman['x'] - pacman['old_x']) * time_fraction
    interpolated_y = pacman['old_y'] + (pacman['y'] - pacman['old_y']) * time_fraction

    frame_index = pacman['frame_offset'] + pacman['current_frame']
    frame = pacman['sprite_regions'][frame_index]
    pacman_dest_rect = pr.Rectangle(interpolated_x, interpolated_y, pacman['size'], pacman['size'])

    if pacman['current_direction'] == 'LEFT':
        frame.width = abs(frame.width)
    else:
        frame.width = -abs(frame.width)

    if pacman['current_direction'] == 'DOWN':
        frame.height = -abs(frame.height)
    else:
        frame.height = abs(frame.height)

    pr.draw_texture_pro(pacman_texture, frame, pacman_dest_rect, pr.Vector2(0, 0), 0, pr.WHITE)