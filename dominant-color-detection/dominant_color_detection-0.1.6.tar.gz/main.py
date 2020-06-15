# -*- encoding: utf-8 -*-
# ! python3

from dominant_color_detection import detect_colors

if __name__ == "__main__":
    img_path = '/home/hynek/Downloads/1591173924.014700-resized.png'
    img_path = '/home/hynek/Stažené/large.jpg'
    print(detect_colors(img_path, -1))
