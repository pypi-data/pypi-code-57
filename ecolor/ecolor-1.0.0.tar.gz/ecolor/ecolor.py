color_black = 30
color_red = 31
color_green = 32
color_yellow = 33
color_blue = 34
color_purplish_red = 35
color_cyan_blue = 36
color_white = 37

bg_black = 40
bg_red = 41
bg_green = 42
bg_yellow = 43
bg_blue = 44
bg_purplish_red = 45
bg_cyan_blue = 46
bg_white = 47

display_default = 0
display_highlighting = 1
display_underline = 4
display_twinkle = 5
display_reverse = 7
display_visible = 8


def color(content, color=color_white, background=bg_black, display=display_default):
    print(f'\033[{display};{color};{background}m{content}\033[0m')

