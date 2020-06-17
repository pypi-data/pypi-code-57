import numpy as np
import colorsys
import os
import json

def cptfile2dict(filepath):
    """
    Extracts a color dictionary and list for a colormap object from a .cpt file

    Parameters
    ----------
    filepath: str
        filepath of a .cpt file including file extension

    Returns
    -------
    colormap name, list containing all colors, dictionary containing all colors
    """
    if not os.path.exists(filepath):
        raise ImportError("file ", filepath, "not found")
    file = open(filepath)
    name = os.path.splitext(os.path.basename(filepath))[0]
    lines = file.readlines()
    file.close()

    x = []
    r = []
    g = []
    b = []
    color_model = "RGB"
    for l in lines:
        ls = l.split()
        if l.strip():
            if l[0] == "#":
                if ls[-1] == "HSV":
                    color_model = "HSV"
                continue
            if ls[0] == "B" or ls[0] == "F" or ls[0] == "N":
                pass
            else:
                x.append(float(ls[0]))
                r.append(float(ls[1]))
                g.append(float(ls[2]))
                b.append(float(ls[3]))
                xtemp = float(ls[4])
                rtemp = float(ls[5])
                gtemp = float(ls[6])
                btemp = float(ls[7])
        else:
            continue

    x.append(xtemp)
    r.append(rtemp)
    g.append(gtemp)
    b.append(btemp)

    x = np.array(x, dtype=np.float64)
    r = np.array(r, dtype=np.float64)
    g = np.array(g, dtype=np.float64)
    b = np.array(b, dtype=np.float64)
    if color_model == "HSV":
        for i in range(r.shape[0]):
            rr, gg, bb = colorsys.hsv_to_rgb(r[i] / 360., g[i], b[i])
            r[i] = rr
            g[i] = gg
            b[i] = bb
    if color_model == "RGB":
        r = r/255
        g = g/255
        b = b/255
    x_norm = (x - x[0])/(x[-1] - x[0])

    col_list = [(r[i], g[i], b[i]) for i in range(len(r))]

    red = []
    green = []
    blue = []

    for i in range(len(x)):
        red.append([x_norm[i], r[i], r[i]])
        green.append([x_norm[i], g[i], g[i]])
        blue.append([x_norm[i], b[i], b[i]])

    color_dict = {"red": red, "green": green, "blue": blue}

    return name, col_list, color_dict


def ctfile2list(filepath):
    """
    Extracts a color list and dictionary for a colormap object from a .ct file

    Parameters
    ----------
    filepath: str
        filepath of a .ct file including file extension

    Returns
    -------
    colormap name, list containing all colors, dictionary containing all colors
    """

    if not os.path.exists(filepath):
        raise ImportError("file ", filepath, "not found")
    f = open(filepath)
    name = os.path.splitext(os.path.basename(filepath))[0]

    lines = f.readlines()
    f.close()
    red = []
    green = []
    blue = []

    for l in lines:
        ls = l.split()
        if l.strip():
            red.append(float(ls[0]))
            green.append(float(ls[1]))
            blue.append(float(ls[2]))

        else:
            continue

    red = np.array(red, dtype=np.float64)
    green = np.array(green, dtype=np.float64)
    blue = np.array(blue, dtype=np.float64)

    red = red/255
    green = green/255
    blue = blue/255

    col_list = [(red[i], green[i], blue[i]) for i in range(len(red))]

    return name, col_list


def json2list(filepath):
    """
    Creates a color dictionary or list for a colormap object from a .json file

    Parameters
    ----------
    filepath: str
        filepath of a .json file including file extension

    Returns
    -------
    colormap name, dictionary or list containing all colors, gradient defining colormap type
    """
    if not os.path.exists(filepath):
        raise ImportError("file ", filepath, "not found")
    with open(filepath, "r") as fidin:
        cmap_dict = json.load(fidin)
        cmap_dict = cmap_dict[0]
        if 'Type' in cmap_dict:
            name = cmap_dict['Name']
        else:
            name = os.path.splitext(os.path.basename(filepath))[0]
        gradient = False
        if 'Type' in cmap_dict:
            if cmap_dict['Type'] == 'Segmented':
                gradient = True
                colors = cmap_dict['RGBPoints'][0]
            else:
                rgb = cmap_dict['RGBPoints']
                colors = [tuple(i) for i in rgb]

        else:
            colors = [cmap_dict['RGBPoints'][x:x + 3] for x in range(0, len(cmap_dict['RGBPoints']), 4)]
        if cmap_dict.get('RGBPoints', None) is None:
            return None

        return name, colors, gradient

def add_alpha(colors):
    """
    Add the default alpha value 1 to every color in a list or dictionary of colors
    
    Parameters
    ----------
    colors: list or dictionary

    Returns
    -------
    list or dictionary of colors with alpha channel value
    """

    if colors is type(dict):
        alpha = []
        for i in range(len(colors['red'])):
            alpha.append(1)
        colors['alpha']=alpha
    if colors is type(list):
        for i in range(len(colors)):
            colors[i].append(1)
    return colors