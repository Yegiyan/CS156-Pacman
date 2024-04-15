import pyray as pr
import Grid

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

# main game loop
while not pr.window_should_close():
    pr.begin_drawing()
    pr.clear_background(pr.BLACK)
    pr.draw_texture_pro(maze_text, maze_src_rect, maze_dest_rect, pr.Vector2(0, 0), 0, pr.WHITE)
    pr.draw_text_ex(font, "HIGH SCORE", pr.Vector2(216, 10), 24, 2, pr.WHITE)
    pr.draw_text_ex(font, "1UP", pr.Vector2(50, 10), 24, 2, pr.WHITE)

    Grid.GridTest(SCREEN_WIDTH, SCREEN_HEIGHT)

    pr.end_drawing()

# unload resources and close window
pr.unload_image(icon)
pr.unload_image(maze_img)
pr.unload_texture(maze_text)
pr.unload_font(font)
pr.close_window()
