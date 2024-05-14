import pyray as pr
import Maze, Pacman, Ghost

# window size
SCREEN_WIDTH = 672
SCREEN_HEIGHT = 885

# initialize raylib and create window
pr.init_window(SCREEN_WIDTH, SCREEN_HEIGHT, "CS156 - Pacman Project")
icon = pr.load_image("../assets/images/icon.png")
pr.set_window_icon(icon)
pr.set_target_fps(60)

# load maze and font resources
maze_img = pr.load_image("../assets/images/maze.png")
maze_text = pr.load_texture_from_image(maze_img)
font = pr.load_font("../assets/font/PressStart2P.ttf")

# set up drawing rectangles
maze_src_rect = pr.Rectangle(0, 0, maze_img.width, maze_img.height)
maze_dest_rect = pr.Rectangle(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)

texture_image = pr.load_image("../assets/images/sprites.png")
texture_atlas = pr.load_texture_from_image(texture_image)

grid = Maze.init_grid(SCREEN_WIDTH, SCREEN_HEIGHT)
pacman = Pacman.create_pacman(13, 23)

blinky = Ghost.create_blinky()
pinky = Ghost.create_pinky()
inky = Ghost.create_inky()
clyde = Ghost.create_clyde()

# main game loop
while not pr.window_should_close():
      
    # update
    delta_time = pr.get_frame_time()
    
    if pr.is_key_pressed(pr.KEY_UP) or pr.is_key_pressed(pr.KEY_W):
        pacman['queued_direction'] = 'UP'
    elif pr.is_key_pressed(pr.KEY_DOWN) or pr.is_key_pressed(pr.KEY_S):
        pacman['queued_direction'] = 'DOWN'
    elif pr.is_key_pressed(pr.KEY_LEFT) or pr.is_key_pressed(pr.KEY_A):
        pacman['queued_direction'] = 'LEFT'
    elif pr.is_key_pressed(pr.KEY_RIGHT) or pr.is_key_pressed(pr.KEY_D):
        pacman['queued_direction'] = 'RIGHT'

    Pacman.move_pacman(pacman, grid, Maze)
    
    blinky.update_position(pacman['grid_pos'], grid, Maze)
    pinky.update_position(pacman['grid_pos'], grid, Maze)
    inky.update_position(pacman['grid_pos'], grid, Maze)
    clyde.update_position(pacman['grid_pos'], grid, Maze)
    
    # print(f"Pacman Pos: {pacman['grid_pos']}")
    
    # draw
    pr.begin_drawing()
    pr.clear_background(pr.BLACK)
    pr.draw_texture_pro(maze_text, maze_src_rect, maze_dest_rect, pr.Vector2(0, 0), 0, pr.WHITE)
    pr.draw_text_ex(font, "HIGH SCORE", pr.Vector2(216, 10), 24, 2, pr.WHITE)
    #pr.draw_text_ex(font, "1UP", pr.Vector2(50, 10), 24, 2, pr.WHITE)
    
    score_text = f"{pacman['score']}"
    pr.draw_text_ex(font, score_text, pr.Vector2(300, 50), 24, 2, pr.WHITE)

    Maze.draw_grid(grid)
    Pacman.draw_pacman(pacman, texture_atlas)
    
    blinky.draw_ghost(texture_atlas)
    pinky.draw_ghost(texture_atlas)
    inky.draw_ghost(texture_atlas)
    clyde.draw_ghost(texture_atlas)

    pr.end_drawing()

# unload resources and close window
pr.unload_image(icon)
pr.unload_image(maze_img)
pr.unload_texture(maze_text)
pr.unload_image(texture_image)
pr.unload_texture(texture_atlas)
pr.unload_font(font)
pr.close_window()