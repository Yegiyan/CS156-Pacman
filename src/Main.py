import pyray as pr

# Original Raylib Docs: https://www.raylib.com/cheatsheet/cheatsheet.html
# Python Binding of Raylib Docs: https://electronstudio.github.io/raylib-python-cffi/

# Window size
width = 800
height = 600

# Raylib initialization
pr.init_window(width, height, "CS156 - Pacman Project")
icon = pr.load_image("../assets/icon.png")
pr.set_window_icon(icon)
pr.set_target_fps(60)

# Game Loop
while not pr.window_should_close():
    pr.begin_drawing()
    pr.clear_background(pr.BLACK)
    pr.draw_text("PACMAN PROJECT", 305, 100, 20, pr.DARKBLUE)
    pr.end_drawing()

# Unload Resources
pr.unload_image(icon)
pr.close_window()