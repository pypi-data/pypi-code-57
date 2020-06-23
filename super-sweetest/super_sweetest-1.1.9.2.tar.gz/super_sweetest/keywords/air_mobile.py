# coding=utf-8

# @Time: 2020/3/11 11:05
# @Auther: liyubin

from airtest.core.api import *
from airtest.core.api import swipe as swipe_air # 为统一config关键字，与swipe函数冲突
from super_sweetest.globals import g
from super_sweetest.log import logger
from super_sweetest.locator import locating_air_element
from super_sweetest.config import element_wait_timeout
from super_sweetest.config import rgb_flag



def get_width_height():
    width, height = g.poco.get_screen_size()
    return width, height


def swipe(step):
    """
    1、通过传入的固定坐标滑动

    2、获取设备分辨率计算合适的坐标
    :param poco: 对象
    :param num_list: (0.2, 0.2, 2, 6)
    :return:
    width 宽 w1 w2 小数   0.1-0.9
    height 高  h1 h2 正数 1-9
    """
    num_list = locating_air_element(step)
    duration = step['data'].get('持续时间', 1)


    # 固定坐标滑动
    # start_x = int(num_list[0])
    # start_y = int(num_list[1])
    #
    # end_x = int(num_list[2])
    # end_y = int(num_list[3])
    # if duration:
    #     swipe_air((start_x, start_y), (end_x, end_y), float(duration))
    # else:
    #     swipe_air((start_x, start_y), (end_x, end_y))

    # 相对坐标滑动
    w1 = float(num_list[0])
    w2 = float(num_list[1])
    h1 = float(num_list[2])
    h2 = float(num_list[3])
    width, height = get_width_height()
    start_pt = (float(width * w1), float(height // h1))
    end_pt = (float(width * w2), float(height // h2))

    if duration:
        swipe_air(start_pt, end_pt, float(duration))
    else:
        swipe_air(start_pt, end_pt)
    sleep(1)


def swipe_photo(step):
    value = locating_air_element(step)
    v1 = value[0]
    v2 = value[1]
    swipe_air(Template(filename=v1, rgb=rgb_flag), Template(filename=v2, rgb=rgb_flag))


def tap(step):
    duration = step['data'].get('持续时间', 0.01)
    photo_path, threshold_value, target_pos_value, rgb_value = locating_air_element(step)
    if duration:
        touch(Template(filename=photo_path, threshold=threshold_value, target_pos=target_pos_value, rgb=rgb_value), duration=float(duration))
    else:
        touch(Template(filename=photo_path, threshold=threshold_value, target_pos=target_pos_value, rgb=rgb_value))


def tap_point(step):
    """
    相对坐标点击 TAP_POINT
    point :相对坐标点
    times :点击次数
    :param step:
    :return:
    """
    point, times = locating_air_element(step)
    point1 = point[0]
    point2 = point[1]
    width, height = get_width_height()
    touch([point1*width, point2*height], times=times)


def input(step):
    by, value = locating_air_element(step)
    data = step['data']
    for key in data:
        if by.lower() == 'text':
            if g.platform.lower() == 'air_android':
                g.poco(text=value).set_text(data[key])
            else:
                # ios poco(value).set_text(value)
                g.poco(value).set_text(data[key])
        elif by.lower() == 'textmatches':
            g.poco(textMatches=value).set_text(data[key])
        else:
            if key.startswith('text'):
                text(data['text'], False)
            else:
                text(data[key], False)


def click(step):
    by, value = locating_air_element(step)
    if by.lower() == 'text':
        try:
            if g.platform.lower() == 'air_android':
                g.poco(text=value).click()
            else:
                # ios
                g.poco(value).click()
        except Exception as e:
            sleep(1)
            if g.platform.lower() == 'air_android':
                g.poco(text=value).click()
            else:
                # ios
                g.poco(value).click()
            logger.info('retry poco click, element: %s error msg: %s' % (value, e))
    elif by.lower() == 'textmatches':
        g.poco(textMatches=value).click()
    else:
        assert False, '请指定 element 中 value值：%s 对应的 by 类型为： text'% value


def check(step):
    photo_path, threshold_value, target_pos_value, rgb_value = locating_air_element(step)
    assert exists(Template(filename=photo_path, threshold=threshold_value, target_pos=target_pos_value, rgb=rgb_value))


def notcheck(step):
    photo_path, threshold_value, target_pos_value, rgb_value = locating_air_element(step)
    assert_not_exists(Template(filename=photo_path, threshold=threshold_value, target_pos=target_pos_value, rgb=rgb_value))


def check_text(step):
    by, value = locating_air_element(step)
    if by.lower() == 'text':
        if g.platform.lower() == 'air_android':
            assert g.poco(text=value).exists(), '检查文本 %s 失败'%value
        else:
            # ios
            assert g.poco(value).exists(), '检查文本 %s 失败' % value
    elif by.lower() == 'textmatches':
        assert g.poco(textMatches=value).exists(), '模糊检查文本 %s 失败' % value


def notcheck_text(step):
    by, value = locating_air_element(step)
    if by.lower() == 'text':
        if g.platform.lower() == 'air_android':
            if g.poco(text=value).exists(): raise '反向检查文本 %s 失败'%value
        else:
            # ios
            if g.poco(value).exists(): raise '反向检查文本 %s 失败' % value
    elif by.lower() == 'textmatches':
        if g.poco(textMatches=value).exists(): raise  '模糊反向检查文本 %s 失败' % value


def wait_(step):
    photo_path, threshold_value, target_pos_value, rgb_value = locating_air_element(step)
    wait(Template(filename=photo_path, threshold=threshold_value, target_pos=target_pos_value, rgb=rgb_value), timeout=element_wait_timeout)


def back(step):
    keycode = locating_air_element(step)
    keyevent(keycode)


def home(step):
    keycode = locating_air_element(step)
    keyevent(keycode)


def menu(step):
    keycode = locating_air_element(step)
    keyevent(keycode)


def power(step):
    keycode = locating_air_element(step)
    keyevent(keycode)


def delete():
    # 删除输入框内容
    for i in range(30):
        keyevent('KEYCODE_DEL')


def wake_(step):
    """唤醒手机"""
    wake()