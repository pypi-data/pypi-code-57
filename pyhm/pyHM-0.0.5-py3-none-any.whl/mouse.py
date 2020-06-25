"""
Mouse()
---
.move(x, y, multiplier) moves wherever the mouse is to destination x, y.
Can be instant by setting the multiplier to 0.
Can also be slowed down by increasing the multiplier.
Default multiplier is 1 if no multiplier is parsed.
"""


class Mouse(object):

    def __init__(self, dependencies):
        self.interpolate = dependencies['interpolate']
        self.pyautogui = dependencies['pyautogui']
        self.numpy = dependencies['numpy']
        self.random = dependencies['random']
        self.scipy = dependencies['scipy']

    def move(self, dest_x, dest_y, multiplier=1):
        cp = self.get_control_points()
        xs, ys = self.gain_xs_and_ys(cp, dest_x, dest_y)
        points = self.gain_points(cp, xs, ys)
        duration = self.gain_duration(xs, ys, multiplier)
        self.execute(points, duration)

    def get_control_points(self):
        cp_1 = self.get_cp_1()
        cp_2 = self.get_cp_2()
        return self.random.randint(cp_1, cp_2)

    def get_cp_1(self):
        return self.random.randint(2, 7)

    def get_cp_2(self):
        return self.random.randint(10, 15)

    def gain_xs_and_ys(self, cp, dest_x, dest_y):
        current_x, current_y = self.get_current_position()
        dist_x, dist_y = self.distribute_control_points(cp, current_x, current_y, dest_x, dest_y)
        randomness = self.random.randint(7, 12)
        return self.randomise_inner_points(randomness, cp, dist_x, dist_y)

    def get_current_position(self):
        return self.pyautogui.position()

    def distribute_control_points(self, cp, x1, y1, x2, y2):
        x = self.get_x(x1, x2, cp)
        y = self.get_y(y1, y2, cp)
        return x, y

    def get_x(self, x1, x2, cp):
        return self.numpy.linspace(x1, x2, num=cp, dtype='int')

    def get_y(self, y1, y2, cp):
        return self.numpy.linspace(y1, y2, num=cp, dtype='int')

    def randomise_inner_points(self, randomness, cp, dist_x, dist_y):
        rand_x = self.scipy.random.randint(-randomness, randomness, size=cp)
        rand_y = self.scipy.random.randint(-randomness, randomness, size=cp)
        rand_x[0] = rand_y[0] = rand_x[-1] = rand_y[-1] = 0
        x = dist_x + rand_x
        y = dist_y + rand_y
        return x, y

    def gain_points(self, cp, x, y):
        degree = 3 if cp > 3 else cp - 1
        tck, u = self.interpolate.splprep([x, y], k=degree)
        u = self.numpy.linspace(0, 1, num=max(self.pyautogui.size()))
        return self.interpolate.splev(u, tck)

    def gain_duration(self, xs, ys, multiplier):
        x_diff = ((xs[0]-xs[-1])**2)**0.5
        y_diff = ((ys[0]-ys[-1])**2)**0.5
        power_of = self.gain_power_of()
        correction = self.gain_correction()
        ret_val = (((x_diff+y_diff)**power_of)/correction)*multiplier
        return int(ret_val)

    def gain_power_of(self):
        return self.random.randint(130000, 150000)/100000

    def gain_correction(self):
        return self.random.randint(13500, 16500)/10000

    def execute(self, points, duration):
        for point in self.get_formatted_points(points):
            temp_x = int(point[0])
            temp_y = int(point[1])
            self.pyautogui.platformModule._moveTo(temp_x, temp_y)
            self.wait(duration)

    @staticmethod
    def get_formatted_points(points):
        return zip(*(i.astype(int) for i in points))

    @staticmethod
    def wait(duration):
        for i in range(duration):
            pass

    def click(self, x='NotSet', y='NotSet'):
        self.setup_mouse_for_click(x, y)
        self.pyautogui.click()

    def setup_mouse_for_click(self, x, y):
        cur_x, cur_y = self.get_current_position()
        if x == 'NotSet' and y == 'NotSet':
            self.move(cur_x, cur_y)
        elif x == 'NotSet':
            self.move(cur_x, y)
        elif y == 'NotSet':
            self.move(x, cur_y)
        else:
            self.move(x, y)

    def double_click(self, x='NotSet', y='NotSet'):
        self.setup_mouse_for_click(x, y)
        interval = self.random.randint(1, 499)/1000
        self.pyautogui.click(clicks=2, interval=interval)

    def right_click(self, x='NotSet', y='NotSet'):
        self.setup_mouse_for_click(x, y)
        self.pyautogui.click(button='right')

    def down(self, button='left'):
        self.pyautogui.mouseDown(button=button)

    def up(self, button='left'):
        self.pyautogui.mouseUp(button=button)


# That's all folks...
