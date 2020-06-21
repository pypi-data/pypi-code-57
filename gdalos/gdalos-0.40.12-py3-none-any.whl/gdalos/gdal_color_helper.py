import re
import gdal


def pal_color_to_rgb(cc, rgb_colors):
    # r g b a -> argb
    # todo: support color names or just find the gdal implementation of this function...
    # cc = color components
    cc = re.findall(r'\d+', cc)
    try:
        if not rgb_colors:
            return (*(int(c) for c in cc),)
        if len(cc) == 1:
            return int(cc[0])
        elif len(cc) == 3:
            return (int(cc[0]) * 255 + int(cc[1])) * 255 + int(cc[2])
        elif len(cc) == 4:
            return ((int(cc[3]) * 255 + int(cc[0])) * 255 + int(cc[1])) * 255 + int(cc[2])
        else:
            return 0
    except:
        return 0


def to_number(s):
    try:
        return int(s)
    except ValueError:
        return float(s)


def color_palette_stats(color_filename, min_val=0, max_val=256, process_palette=..., rgb_colors=True):
    values = []
    colors = []
    if process_palette:
        process_colors = process_palette is ...
        try:
            with open(color_filename) as fp:
                for line in fp:
                    split_line = line.strip().split(' ', maxsplit=1)
                    num_str = split_line[0].strip()
                    if process_colors:
                        color = pal_color_to_rgb(split_line[1], rgb_colors)
                    is_percent = num_str.endswith('%')
                    if is_percent:
                        num_str = num_str.rstrip('%')
                    try:
                        num = to_number(num_str)
                        if is_percent:
                            num = (max_val-min_val)*num*0.01+min_val
                        values.append(num)
                        if process_colors:
                            colors.append(color)
                    except ValueError:
                        pass
        except IOError:
            values = None
    return values, colors


def make_color_table(color_filename):
    values, colors = color_palette_stats(color_filename, rgb_colors=False)

    # create color table
    color_table = gdal.ColorTable()
    min_val = values[0]
    min_col = colors[0]
    max_val = values[0]
    max_col = colors[0]
    for val, col in zip(values, colors):
        # set color for each value
        color_table.SetColorEntry(val, col)
        if val < min_val:
            min_val = val
            min_col = col
        if val > min_val:
            max_val = val
            max_col = col

    # fill palette below min and above max
    for i in range(0, min_val):
        color_table.SetColorEntry(i, min_col)
    for i in range(max_val, 256):
        color_table.SetColorEntry(i, max_col)
    return color_table
