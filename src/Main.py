import pyray as pr
import Maze, Pacman, Ghost
import time

# window size
SCREEN_WIDTH = 672
SCREEN_HEIGHT = 885

# initialize raylib and create window
pr.init_window(SCREEN_WIDTH, SCREEN_HEIGHT, "CS156 - Pacman Project")
icon = pr.load_image("../assets/images/icon.png")
pr.set_window_icon(icon)
pr.init_audio_device()
pr.set_target_fps(60)

# load maze and font resources
maze_img = pr.load_image("../assets/images/maze.png")
maze_text = pr.load_texture_from_image(maze_img)
font = pr.load_font("../assets/font/PressStart2P.ttf")

# set up drawing rectangles
maze_src_rect = pr.Rectangle(0, 0, maze_img.width, maze_img.height)
maze_dest_rect = pr.Rectangle(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)

# load audio
beginning_sound = pr.load_sound("../assets/audio/beginning.wav")
hasPlayedIntro = False

menu_options = ["Play", "Exit"]
current_option = 0  # start with 'Play' selected

texture_image = pr.load_image("../assets/images/sprites.png")
texture_atlas = pr.load_texture_from_image(texture_image)

grid = Maze.init_grid(SCREEN_WIDTH, SCREEN_HEIGHT)
pacman = Pacman.create_pacman(13, 23)

blinky = Ghost.create_blinky()
pinky = Ghost.create_pinky()
inky = Ghost.create_inky()
clyde = Ghost.create_clyde()

ghosts = [blinky, pinky, inky, clyde]
spawn_times = [time.time() + 5*i for i in range(len(ghosts))] # exit spawn pen every 1 second

# extra functions
def draw_menu():
    pr.begin_drawing()
    pr.clear_background(pr.BLACK)
    title_text = "PACMAN"
    pr.draw_text_ex(font, title_text, pr.Vector2(220, 150), 40, 2, pr.YELLOW)
    for i, option in enumerate(menu_options):
        color = pr.RED if i == current_option else pr.WHITE
        x = 275
        y = 300 + 50 * i
        pr.draw_text_ex(font, option, pr.Vector2(x, y), 30, 2, color)
    pr.end_drawing()

def draw_victory_screen():
    pr.begin_drawing()
    pr.clear_background(pr.BLACK)
    victory_text = "VICTORY! YOU WON!"
    pr.draw_text_ex(font, victory_text, pr.Vector2(70, 300), 30, 2, pr.YELLOW)

    exit_button_text = "EXIT GAME"
    exit_button_x = 210
    exit_button_y = 400
    pr.draw_text_ex(font, exit_button_text, pr.Vector2(exit_button_x, exit_button_y), 24, 2, pr.RED)
    pr.end_drawing()

    # check if the exit button is pressed
    if pr.is_key_pressed(pr.KEY_ENTER) or pr.is_key_pressed(pr.KEY_SPACE):
        pr.close_window()
            
def check_all_pellets_eaten(grid):
    for row in grid:
        for cell in row:
            if cell.cell_type == 0 or cell.cell_type == 3:
                return False
    return True

# main menu loop
while not pr.window_should_close():
    if pr.is_key_pressed(pr.KEY_DOWN) or pr.is_key_pressed(pr.KEY_S):
        current_option = (current_option + 1) % len(menu_options)
    elif pr.is_key_pressed(pr.KEY_UP) or pr.is_key_pressed(pr.KEY_W):
        current_option = (current_option - 1) % len(menu_options)
    elif pr.is_key_pressed(pr.KEY_ENTER) or pr.is_key_pressed(pr.KEY_SPACE):
        if current_option == 0: # play selected
            pr.play_sound(beginning_sound)
            break
        elif current_option == 1: # exit selected
            pr.close_window()
            exit()
    draw_menu()

# main game loop
while not pr.window_should_close():
      
    # update
    current_time = time.time()
    delta_time = pr.get_frame_time()
    
    if check_all_pellets_eaten(grid):
        draw_victory_screen()
        continue
    
    if pr.is_key_pressed(pr.KEY_UP) or pr.is_key_pressed(pr.KEY_W):
        pacman['queued_direction'] = 'UP'
    elif pr.is_key_pressed(pr.KEY_DOWN) or pr.is_key_pressed(pr.KEY_S):
        pacman['queued_direction'] = 'DOWN'
    elif pr.is_key_pressed(pr.KEY_LEFT) or pr.is_key_pressed(pr.KEY_A):
        pacman['queued_direction'] = 'LEFT'
    elif pr.is_key_pressed(pr.KEY_RIGHT) or pr.is_key_pressed(pr.KEY_D):
        pacman['queued_direction'] = 'RIGHT'

    Pacman.move_pacman(pacman, ghosts, grid, Maze)
    
    # update ghosts
    for i, ghost in enumerate(ghosts):
        if current_time >= spawn_times[i]:
            ghost.update_position(pacman, pacman['grid_pos'], pacman['current_direction'], blinky.grid_pos, grid, Maze)
    
    # blinky.update_position(pacman, pacman['grid_pos'], pacman['current_direction'], blinky.grid_pos, grid, Maze)
    # print(f"Pacman Pos: {pacman['grid_pos']}")
    
    # draw
    pr.begin_drawing()
    pr.clear_background(pr.BLACK)
    pr.draw_texture_pro(maze_text, maze_src_rect, maze_dest_rect, pr.Vector2(0, 0), 0, pr.WHITE)
    pr.draw_text_ex(font, "HIGH SCORE", pr.Vector2(216, 10), 24, 2, pr.WHITE)
    #pr.draw_text_ex(font, "1UP", pr.Vector2(50, 10), 24, 2, pr.WHITE)
    
    score_text = f"{pacman['score']}"
    pr.draw_text_ex(font, score_text, pr.Vector2(300, 50), 24, 2, pr.WHITE)

    Maze.draw_grid(grid, texture_atlas)
    Pacman.draw_pacman(pacman, texture_atlas)
    
    blinky.draw_ghost(texture_atlas)
    pinky.draw_ghost(texture_atlas)
    inky.draw_ghost(texture_atlas)
    clyde.draw_ghost(texture_atlas)

    pr.end_drawing()
    
    if hasPlayedIntro == False:
        time.sleep(4)
        hasPlayedIntro = True

# unload resources and close window
pr.unload_image(icon)
pr.unload_image(maze_img)
pr.unload_texture(maze_text)
pr.unload_image(texture_image)
pr.unload_texture(texture_atlas)
pr.unload_font(font)
pr.close_window()