import pyray as pr
import Maze, Pacman

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

pacman_sprite = pr.load_image("../assets/images/sprites.png")
pacman_texture = pr.load_texture_from_image(pacman_sprite)

grid = Maze.init_grid(SCREEN_WIDTH, SCREEN_HEIGHT)
pacman = Pacman.create_pacman(13, 23)

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

    Pacman.move_pacman(pacman, Maze)
    
    # draw
    pr.begin_drawing()
    pr.clear_background(pr.BLACK)
    pr.draw_texture_pro(maze_text, maze_src_rect, maze_dest_rect, pr.Vector2(0, 0), 0, pr.WHITE)
    pr.draw_text_ex(font, "HIGH SCORE", pr.Vector2(216, 10), 24, 2, pr.WHITE)
    pr.draw_text_ex(font, "1UP", pr.Vector2(50, 10), 24, 2, pr.WHITE)

    #Maze.draw_grid(grid)
    Pacman.draw_pacman(pacman, pacman_texture)

    pr.end_drawing()

# unload resources and close window
pr.unload_image(icon)
pr.unload_image(maze_img)
pr.unload_texture(maze_text)
pr.unload_image(pacman_sprite)
pr.unload_texture(pacman_texture)
pr.unload_font(font)
pr.close_window()