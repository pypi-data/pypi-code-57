import random
colv = int()
colvmax = int()



BLACK =("\033[30m")
RED = ("\033[31m")
GREEN =("\033[32m")
YELLOW =("\033[33m")
BLUE = ("\033[34m")
VIOLET = ("\033[35m")
WHITE = ("\033[37m")

BG_BLACK =("\033[40m")
BG_RED = ("\033[41m")
BG_GREEN =("\033[42m")
BG_YELLOW =("\033[43m")
BG_BLUE = ("\033[44m")
BG_VIOLET = ("\033[45m")
BG_WHITE = ("\033[47m")

EF_FAT = ("\033[1m")
EF_FADED = ("\033[2m")
EF_CURSIVE = ("\033[3m")
EF_UNDERLINE = ("\033[4m")
EF_TINBG = ("\033[7m")



def print_n(text, colvmax):
    global colv
    run = True
    while run:
        if colv!=colvmax:
            print(text)
            colv+=(int(1))
        else:
            run = False
            colv = 0



def print_c(text_1, colortext, colorbg, colvmax):
    global colv
    run = True
    while run:
        if colv!=colvmax:
            print(colortext + colorbg + "{}\033[0m".format(text_1))
            colv+= (int(1))
        else:
            run = False
            colv = 0



def print_c_plus_1(text_1, colortext, colorbg, effect, colvmax):
    global colv
    run = True
    while run:
        if colv!=colvmax:
            print(colortext + colorbg + effect + "{}\033[0m".format(text_1))
            colv+= (int(1))
        else:
            run = False
            colv = 0


def print_c_plus_2(text_1, colortext, colorbg, effect, effect_2, colvmax):
    global colv
    run = True
    while run:
        if colv!=colvmax:
            print(colortext + colorbg + effect + effect_2 + "{}\033[0m".format(text_1))
            colv+= (int(1))
        else:
            run = False
            colv = 0

def print_c_plus_3(text_1, colortext, colorbg, effect, effect_2, effect_3, colvmax):
    global colv
    run = True
    while run:
        if colv!=colvmax:
            print(colortext + colorbg + effect + effect_2 + effect_3 + "{}\033[0m".format(text_1))
            colv+= (int(1))
        else:
            run = False
            colv = 0



def print_c_plus_4(text_1, colortext, colorbg, effect, effect_2, effect_3, effect_4, colvmax):
    global colv
    run = True
    while run:
        if colv!=colvmax:
            print(colortext + colorbg + effect + effect_2 + effect_3 + effect_4 + "{}\033[0m".format(text_1))
            colv+= (int(1))
        else:
            run = False
            colv = 0

def print_c_plus_5(text_1, colortext, colorbg, effect, effect_2, effect_3, effect_4, effect_5, colvmax):
    global colv
    run = True
    while run:
        if colv!=colvmax:
            print(colortext + colorbg + effect + effect_2 + effect_3 + effect_4 + effect_5 + "{}\033[0m".format(text_1))
            colv+= (int(1))
        else:
            run = False
            colv = 0





def print_c_2(text_1, text_2, colortext_1, colorbg_1, colortext_2, colorbg_2, colvmax):
    global colv
    run = True
    while run:
        if colv!=colvmax:
            print(colortext_1 + colorbg_1 + "{}\033[0m".format(text_1) + colortext_2 + colorbg_2 + "{}\033[0m".format(text_2))
            colv+= (int(1))
        else:
            run = False
            colv = 0



def print_c_2_plus_1(text_1, text_2, colortext_1, colorbg_1, colortext_2, colorbg_2, effect, colvmax):
    global colv
    run = True
    while run:
        if colv!=colvmax:
            print(colortext_1 + colorbg_1 + effect + "{}\033[0m".format(text_1)+colortext_2 + colorbg_2 + effect + "{}\033[0m".format(text_2))
            colv+= (int(1))
        else:
            run = False
            colv = 0


def print_c_2_plus_2(text_1, text_2, colortext_1, colorbg_1, colortext_2, colorbg_2, effect, effect_2, colvmax):
    global colv
    run = True
    while run:
        if colv!=colvmax:
            print(colortext_1 + colorbg_1 + effect + effect_2 + "{}\033[0m".format(text_1)+colortext_2 + colorbg_2 + effect + effect_2 + "{}\033[0m".format(text_2))
            colv+= (int(1))
        else:
            run = False
            colv = 0

def print_c_2_plus_3(text_1, text_2, colortext_1, colorbg_1, colortext_2, colorbg_2, effect, effect_2, effect_3, colvmax):
    global colv
    run = True
    while run:
        if colv!=colvmax:
            print(colortext_1 + colorbg_1 + effect + effect_2 + effect_3 + "{}\033[0m".format(text_1)+colortext_2 + colorbg_2 + effect + effect_2 + effect_3 + "{}\033[0m".format(text_2))
            colv+= (int(1))
        else:
            run = False
            colv = 0


def print_c_2_plus_4(text_1, text_2,  colortext_1, colorbg_1, colortext_2, colorbg_2, effect, effect_2, effect_3, effect_4, colvmax):
    global colv
    run = True
    while run:
        if colv!=colvmax:
            print(colortext_1 + colorbg_1 + effect + effect_2 + effect_3 + effect_4 + "{}\033[0m".format(text_1)+colortext_2 + colorbg_2 + effect + effect_2 + effect_3 + effect_4 + "{}\033[0m".format(text_2))
            colv+= (int(1))
        else:
            run = False
            colv = 0

def print_c_2_plus_5(text_1, text_2,  colortext_1, colorbg_1, colortext_2, colorbg_2, effect, effect_2, effect_3, effect_4, effect_5, colvmax):
    global colv
    run = True
    while run:
        if colv!=colvmax:
            print(colortext_1 + colorbg_1 + effect + effect_2 + effect_3 + effect_4 + effect_5 + "{}\033[0m".format(text_1)+colortext_2 + colorbg_2 + effect + effect_2 + effect_3 + effect_4 + effect_5 + "{}\033[0m".format(text_2))
            colv+= (int(1))
        else:
            run = False
            colv = 0


def print_c_3(text_1, text_2, text_3, colortext_1, colorbg_1, colortext_2, colorbg_2, colortext_3, colorbg_3, colvmax):
    global colv
    run = True
    while run:
        if colv!=colvmax:
            print(colortext_1 + colorbg_1 + "{}\033[0m".format(text_1) + colortext_2 + colorbg_2 + "{}\033[0m".format(text_2) + colortext_3 + colorbg_3 + "{}\033[0m".format(text_3))
            colv+= (int(1))
        else:
            run = False
            colv = 0



def print_c_3_plus_1(text_1, text_2, text_3, colortext_1, colorbg_1, colortext_2, colorbg_2, colortext_3, colorbg_3, effect, colvmax):
    global colv
    run = True
    while run:
        if colv!=colvmax:
            print(colortext_1 + colorbg_1 + effect + "{}\033[0m".format(text_1)+colortext_2 + colorbg_2 + effect + "{}\033[0m".format(text_2)+colortext_3 + colorbg_3 + effect + "{}\033[0m".format(text_3))
            colv+= (int(1))
        else:
            run = False
            colv = 0


def print_c_3_plus_2(text_1, text_2, text_3, colortext_1, colorbg_1, colortext_2, colorbg_2, colortext_3, colorbg_3, effect, effect_2, colvmax):
    global colv
    run = True
    while run:
        if colv!=colvmax:
            print(colortext_1 + colorbg_1 + effect + effect_2 + "{}\033[0m".format(text_1)+colortext_2 + colorbg_2 + effect + effect_2 + "{}\033[0m".format(text_2)+colortext_3 + colorbg_3 + effect + effect_2 + "{}\033[0m".format(text_3))
            colv+= (int(1))
        else:
            run = False
            colv = 0

def print_c_3_plus_3(text_1, text_2, text_3, colortext_1, colorbg_1, colortext_2, colorbg_2, colortext_3, colorbg_3, effect, effect_2, effect_3, colvmax):
    global colv
    run = True
    while run:
        if colv!=colvmax:
            print(colortext_1 + colorbg_1 + effect + effect_2 + effect_3 + "{}\033[0m".format(text_1)+colortext_2 + colorbg_2 + effect + effect_2 + effect_3 + "{}\033[0m".format(text_2)+colortext_3 + colorbg_3 + effect + effect_2 + effect_3 + "{}\033[0m".format(text_3))
            colv+= (int(1))
        else:
            run = False
            colv = 0


def print_c_3_plus_4(text_1, text_2, text_3, colortext_1, colorbg_1, colortext_2, colorbg_2, colortext_3, colorbg_3, effect, effect_2, effect_3, effect_4, colvmax):
    global colv
    run = True
    while run:
        if colv!=colvmax:
            print(colortext_1 + colorbg_1 + effect + effect_2 + effect_3 + effect_4 + "{}\033[0m".format(text_1)+colortext_2 + colorbg_2 + effect + effect_2 + effect_3 + effect_4 + "{}\033[0m".format(text_2)+colortext_3 + colorbg_3 + effect + effect_2 + effect_3 + effect_4 + "{}\033[0m".format(text_3))
            colv+= (int(1))
        else:
            run = False
            colv = 0

def print_c_3_plus_5(text_1, text_2, text_3, colortext_1, colorbg_1, colortext_2, colorbg_2,  colortext_3, colorbg_3, effect, effect_2, effect_3, effect_4, effect_5, colvmax):
    global colv
    run = True
    while run:
        if colv!=colvmax:
            print(colortext_1 + colorbg_1 + effect + effect_2 + effect_3 + effect_4 + effect_5 + "{}\033[0m".format(text_1)+colortext_2 + colorbg_2 + effect + effect_2 + effect_3 + effect_4 + effect_5 + "{}\033[0m".format(text_2)+colortext_3 + colorbg_3 + effect + effect_2 + effect_3 + effect_4 + effect_5 + "{}\033[0m".format(text_3))
            colv+= (int(1))
        else:
            run = False
            colv = 0



def print_random(text_1, colortext, colvmax):
    global colv
    colorbg = random.randint(2, 7)
    if colorbg == 2:
        colorbg = BG_RED
    if colorbg == 3:
        colorbg = BG_YELLOW
    if colorbg == 4:
        colorbg = BG_BLACK
    if colorbg == 5:
        colorbg = BG_BLUE
    if colorbg == 6:
        colorbg = BG_VIOLET
    if colorbg == 7:
        colorbg = BG_GREEN
    
    run = True
    while run:
        if colv!=colvmax:
            print(colortext + colorbg + "{}\033[0m".format(text_1))
            colv+= (int(1))
        else:
            run = False
            colv = 0



















