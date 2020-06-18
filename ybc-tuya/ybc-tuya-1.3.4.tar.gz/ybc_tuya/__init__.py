import sys
import ybc_tuya.tuya
from ybc_tuya.drawing_board import init as _do_init_drawing_board


_all_functions_decorated = False
decorated_functions = ['black_eyes', 'bear', 'beard', 'car_wheel2', 'car_wheel1',
                       'car_head', 'car_body', 'car', 'clean', 'canvas', 'diamond',
                       'draw_rect', 'draw_circle', 'egg', 'eyes', 'huaji', 'flower',
                       'fengche', 'face', 'fill_rect', 'fill_color', 'fill_circle',
                       'hmbb', 'head', 'hide', 'jiqimao_scarf', 'jiqimao_nose',
                       'jiqimao_mouth', 'jiqimao_head', 'jiqimao_face', 'jiqimao_beard',
                       'jiqimao', 'lxzfx', 'love', 'lion', 'leaf', 'ladybug', 'logo',
                       'moveAround', 'mouth', 'mao_goto', 'my_goto', 'nose', 'pout',
                       'pikachu', 'petals', 'petal', 'programmer', 'pen_speed', 'pen_size',
                       'pen_color', 'rainbow_c1', 'rainbow', 'ruler', 'rainbow_c2',
                       'rainbow_c3', 'rainbow_c4', 'rainbow_c5', 'rainbow_c6', 'rainbow_c7',
                       'rainbow_c8', 'rectangle', 'rgb', 'robot', 'robot_body', 'robot_eyes',
                       'robot_face', 'robot_foot', 'robot_hands', 'robot_head', 'robot_mouth',
                       'scarf', 'stop', 'screw', 'setting', 'shield', 'shield_c1', 'shield_c2',
                       'shield_c3', 'shield_c4', 'shield_star', 'snow', 'stamen', 'stem',
                       'taiji', 'whitebear', 'xiaohuangren', 'xzpq_ears', 'xiongbenxiong',
                       'xzpq', 'xzpq_body', 'xzpq_cheek', 'xzpq_eyes', 'xzpq_foot', 'xzpq_hands',
                       'xzpq_head', 'xzpq_mouth', 'xzpq_nose', 'xzpq_tail', 'yqcr']


def init_drawing_board(fn):
    """
    初始化画板装饰器，装饰涂鸦的所有方法，保证在调用时画板是打开的

    :param fn:
    :return:
    """
    def wrapped(*args, **kwargs):
        _do_init_drawing_board()
        return fn(*args, **kwargs)

    return wrapped


def decorate_all_in_module(module):
    for name in dir(module):
        if name.startswith('_'):
            continue
        if name in decorated_functions:
            obj = getattr(module, name)
            setattr(module, name, init_drawing_board(obj))
    global _all_functions_decorated
    _all_functions_decorated = True


decorate_all_in_module(ybc_tuya.tuya)

if _all_functions_decorated:
    # import decorated functions
    from ybc_tuya.tuya import (
        black_eyes, bear, beard, car_wheel2, car_wheel1, car_head, car_body,
        car, clean, canvas, diamond, draw_rect, draw_circle, egg, eyes, huaji, flower,
        fengche, face, fill_rect, fill_color, fill_circle, hmbb, head, hide,
        jiqimao_scarf, jiqimao_nose, jiqimao_mouth, jiqimao_head, jiqimao_face, jiqimao_beard,
        jiqimao, lxzfx, love, lion, leaf, ladybug, logo, moveAround, mouth, mao_goto, my_goto,
        nose, pout, pikachu, petals, petal, programmer, pen_speed, pen_size, pen_color,
        rainbow_c1, rainbow, ruler, rainbow_c2, rainbow_c3, rainbow_c4, rainbow_c5, rainbow_c6,
        rainbow_c7, rainbow_c8, rectangle, rgb, robot, robot_body, robot_eyes, robot_face,
        robot_foot, robot_hands, robot_head, robot_mouth, scarf, stop, screw,
        setting, shield, shield_c1, shield_c2, shield_c3, shield_c4, shield_star, snow, stamen,
        stem, taiji, whitebear, xiaohuangren, xzpq_ears, xiongbenxiong, xzpq, xzpq_body,
        xzpq_cheek, xzpq_eyes, xzpq_foot, xzpq_hands, xzpq_head, xzpq_mouth, xzpq_nose, xzpq_tail,
        yqcr
    )

if sys.platform == 'skulpt':
    import turtle
else:
    from ybc_tuya.override_turtle import turtle

__all__ = ['black_eyes', 'bear', 'beard', 'car_wheel2', 'car_wheel1', 'car_head', 'car_body',
           'car', 'clean', 'canvas', 'diamond', 'draw_rect', 'draw_circle', 'egg', 'eyes',
           'huaji', 'flower', 'fengche', 'face', 'fill_rect', 'fill_color',
           'fill_circle', 'hmbb', 'head', 'hide', 'jiqimao_scarf', 'jiqimao_nose',
           'jiqimao_mouth', 'jiqimao_head', 'jiqimao_face', 'jiqimao_beard', 'jiqimao',
           'lxzfx', 'love', 'lion', 'leaf', 'ladybug', 'logo', 'moveAround', 'mouth',
           'mao_goto', 'my_goto', 'nose', 'pout', 'pikachu', 'petals', 'petal', 'programmer',
           'pen_speed', 'pen_size', 'pen_color', 'rainbow_c1', 'rainbow', 'ruler', 'rainbow_c2',
           'rainbow_c3', 'rainbow_c4', 'rainbow_c5', 'rainbow_c6', 'rainbow_c7', 'rainbow_c8',
           'rectangle', 'rgb', 'robot', 'robot_body', 'robot_eyes', 'robot_face', 'robot_foot',
           'robot_hands', 'robot_head', 'robot_mouth', 'scarf', 'stop', 'screw',
           'setting', 'shield', 'shield_c1', 'shield_c2', 'shield_c3', 'shield_c4',
           'shield_star', 'snow', 'stamen', 'stem', 'taiji', 'whitebear', 'xiaohuangren',
           'xzpq_ears', 'xiongbenxiong', 'xzpq', 'xzpq_body', 'xzpq_cheek', 'xzpq_eyes',
           'xzpq_foot', 'xzpq_hands', 'xzpq_head', 'xzpq_mouth', 'xzpq_nose', 'xzpq_tail',
           'yqcr', 'turtle']

__version__ = '1.3.4'
