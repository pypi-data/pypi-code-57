from numbers import Number
import abc
import warnings
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from . import interface


class RotatableMixin(interface.Rotatable):
    '''Mixin class for rotatable objects'''

    def __init__(self, rot=0, flipped=False):
        self.rot = rot
        self.flipped = flipped

    @property
    def rot(self):
        return self.__rot

    @rot.setter
    def rot(self, rot):
        self.__rot = rot % 4

    @property
    def flipped(self):
        return self.__flipped

    @flipped.setter
    def flipped(self, flipped):
        self.__flipped = flipped

    def rotate(self):
        self.rot += 1

    def flip(self):
        self.flipped = not self.flipped


class RotatableRectangle(RotatableMixin):
    def __init__(self, pos, size, image_shape, flipped=False, rot=0, edgecolor='w'):
        assert len(image_shape) == 2
        assert isinstance(flipped, bool)
        assert isinstance(rot, int)
        self.image_shape = image_shape
        self.flipped = flipped
        self.rot = rot
        self.dim = size
        self.pos = pos
        self.rect = patches.Rectangle(
            self.pos,
            self.dim[0], self.dim[1],
            linewidth=1,
            edgecolor=edgecolor,
            facecolor='none')

    @property
    def dim(self):
        if (self.rot % 2) > 0:
            return (self.__dim[1], self.__dim[0])
        else:
            return self.__dim

    @dim.setter
    def dim(self, size):
        try:
            if len(size) == 2:
                if (self.rot % 2) > 0:
                    self.__dim = (size[1], size[0])
                else:
                    self.__dim = tuple(size)
            else:
                raise ValueError('Rectangle dimensions must be one or two numbers. Got: {}'.format(size))
        except TypeError:
            self.__dim = (size, size)
        try:
            self.rect.set_width(self.dim[0])
            self.rect.set_height(self.dim[1])
        except AttributeError:
            pass

    @property
    def pos(self):
        return self._rotate_coords(self.__pos)

    @pos.setter
    def pos(self, pos):
        if isinstance(pos, str) and pos == 'center':
            pos = np.round((np.asarray(self.image_shape) - np.asarray(self.dim)) / 2)
        self.__pos = self._unrotate_coords(pos)

    @property
    def raw_pos(self):
        return self.__pos

    @raw_pos.setter
    def raw_pos(self, pos):
        self.__pos = tuple(pos)

    def update(self):
        self.rect.set_xy(self.pos)

    def update_from(self, rect):
        if isinstance(rect, RotatableRectangle):
            self.image_shape = rect.image_shape
            self.flipped = rect.flipped
            self.rot = rect.rot
            self.dim = rect.dim
            self.pos = np.copy(rect.pos)
            rect = rect.rect
        self.rect.update_from(rect)
        self.update()

    def draw(self, ax):
        ax.add_patch(self.rect)

    def remove(self):
        try:
            self.rect.remove()
        except NotImplementedError:
            pass

    def extract_image(self, rotatable_image):
        pos = list(map(int, self.pos))
        dim = list(map(int, self.dim))
        try:
            try:
                rotated = rotatable_image.rotated_image()
            except AttributeError:
                rotated = rotatable_image
                if self.rot > 0 or self.flipped:
                    warnings.warn(
                        'Could not rotate image. Use a RotatableImage object or make sure you rotated the input yourself.')
            result = np.copy(rotated[pos[1]: pos[1] + dim[1], pos[0]: pos[0] + dim[0]])
        except IndexError:
            result = np.zeros(dim)
        if np.any(np.asarray(result.shape) == 0):
            result = np.zeros(dim)
        return result

    def _rotate_coords(self, coord):
        if self.flipped:
            coord = self._flip_coords(coord)
        return self._value_rotation(coord, self.rot)

    def _unrotate_coords(self, coord):
        coord = self._value_rotation(coord, 4 - self.rot)
        if self.flipped:
            coord = self._flip_coords(coord)
        return coord

    def _flip_coords(self, coord):
        return (self.image_shape[0] - coord[0] - self.dim[0], coord[1])

    def _value_rotation(self, coord, rotation):
        if rotation == 1:
            coord = (coord[1], self.image_shape[1] - coord[0] - self.dim[1])
        elif rotation == 2:
            coord = (self.image_shape[0] - coord[0] - self.dim[0],
                     self.image_shape[1] - coord[1] - self.dim[1])
        elif rotation == 3:
            coord = (self.image_shape[0] - coord[1] - self.dim[0], coord[0])
        elif rotation > 4:
            raise ValueError('Rotation must be 4 or less. Got {}'.format(rotation))
        return tuple(coord)


class RectangleList(RotatableMixin):
    def __init__(self):
        self.rect_list = []

    @property
    def pos(self):
        try:
            return self.rect_list[0].pos
        except IndexError:
            return None

    @pos.setter
    def pos(self, pos):
        try:
            offset = map(lambda a, b: a - b, pos, self.rect_list[0].pos)
            for rect in self.rect_list:
                rect.pos = map(lambda a, b: a + b, offset, rect.pos)
        except IndexError:
            pass

    @property
    def dim(self):
        try:
            return self.rect_list[0].dim
        except IndexError:
            return None

    @dim.setter
    def dim(self, size):
        for rect in self.rect_list:
            rect.dim = size

    @property
    def rot(self):
        try:
            return self.rect_list[0].rot
        except IndexError:
            return None

    @rot.setter
    def rot(self, rot):
        for rect in self.rect_list:
            rect.rot = rot

    @property
    def flipped(self):
        try:
            return self.rect_list[0].flipped
        except IndexError:
            return None

    @flipped.setter
    def flipped(self, flipped):
        for rect in self.rect_list:
            rect.flipped = flipped

    def flip(self):
        for rect in self.rect_list:
            rect.flip()

    def rotate(self):
        for rect in self.rect_list:
            rect.rotate()

    def update(self):
        for rect in self.rect_list:
            rect.update()

    def add_rect(self, pos, edgecolor='w', size=None, image_shape=None, rot=None, flipped=None):
        if size is None:
            try:
                size = self.rect_list[0].dim
            except IndexError:
                size = 16
        if image_shape is None:
            try:
                image_shape = self.rect_list[0].image_shape
            except IndexError:
                image_shape = (512, 512)
        if rot is None:
            try:
                rot = self.rect_list[0].rot
            except IndexError:
                rot = 0
        if flipped is None:
            try:
                flipped = self.rect_list[0].flipped
            except IndexError:
                flipped = False
        self.rect_list.append(RotatableRectangle(pos, size, image_shape, flipped, rot, edgecolor))
        # TODO (prio 5) use rect_list[-1].update_from(rect_list[0]) and possibly switch to IdenticalList

    def delete_rect(self, index=-1):
        self.rect_list.pop(index).remove()

    def remove_all(self):
        for rect in self.rect_list:
            rect.remove()

    def add_all(self, ax):
        for rect in self.rect_list:
            ax.add_patch(rect.rect)

    def refresh_ax(self, ax):
        self.remove_all()
        self.add_all(ax)


class RectangleMatrix(RectangleList):
    def __init__(self, image_shape=(512, 512), num_rows=1, num_cols=16, row_height=16, rot=0, flipped=False, size=16):
        super().__init__()
        from numbers import Number
        assert isinstance(num_rows, int)
        assert isinstance(num_cols, int)
        assert isinstance(row_height, Number)
        self.num_rows = num_rows
        self.num_cols = num_cols
        self._row_height = row_height
        left_pos = [0, image_shape[1]]
        self.add_rect(left_pos, edgecolor='r', size=size, image_shape=image_shape, rot=rot, flipped=flipped)
        self.left_rect = self.rect_list[0]
        right_pos = [image_shape[0], image_shape[1]]
        self.add_rect(right_pos, edgecolor='b', size=size, image_shape=image_shape, rot=rot, flipped=flipped)
        self.right_rect = self.rect_list[1]
        self.current_rect = self.left_rect
        self.update_rect_number()

    @property
    def row_height(self):
        return self._row_height

    @row_height.setter
    def row_height(self, height):
        self._row_height = height
        self.distribute()

    def generator(self):
        indices = list(range(len(self.rect_list)))
        indices.append(1)
        del(indices[1])  # we need to put the second element last so that the rectangles are in the order they appear on screen
        for i in indices:
            yield self.rect_list[i]

    def update_rect_number(self):
        target = self.num_rows * self.num_cols
        diff = target - len(self.rect_list)
        if diff > 0:
            for _ in range(diff):
                self.add_rect(self.left_rect.pos)
        elif diff < 0:
            for _ in range(abs(diff)):
                self.delete_rect()
        if diff != 0:
            self.distribute()

    def distribute(self):
        cur_rect = 2
        x_dist = self.right_rect.pos[0] - self.left_rect.pos[0]
        y_dist = self.right_rect.pos[1] - self.left_rect.pos[1]
        for row in range(self.num_rows):
            x_col_step = (x_dist) / (self.num_cols - 1)
            y_col_step = (y_dist) / (self.num_cols - 1)
            if abs(x_dist) < abs(y_dist):
                row_x = self.left_rect.pos[0] - row * self.row_height
                row_y = self.left_rect.pos[1]
                if y_col_step != 0:
                    row_y += row * x_col_step * self.row_height / y_col_step
            else:
                row_x = self.left_rect.pos[0]
                row_y = self.left_rect.pos[1] - row * self.row_height
                if x_col_step != 0:
                    row_x += row * y_col_step * self.row_height / x_col_step
            start = 1 if row == 0 else 0
            for col in range(start, self.num_cols - start):
                pos = [row_x + col * x_col_step, row_y + col * y_col_step]
                self.rect_list[cur_rect].pos = pos
                cur_rect += 1
        self.update()

    def store_current_pos(self, pos):
        self.current_rect.pos = pos
        self.distribute()

    def move_current_rect(self, key):
        update = False
        pos = list(self.current_rect.pos)
        if str(key).lower() in ['up', '8']:
            pos[1] -= 1
            update = True
        elif str(key).lower() in ['down', '2']:
            pos[1] += 1
            update = True
        elif str(key).lower() in ['left', '4']:
            pos[0] -= 1
            update = True
        elif str(key).lower() in ['right', '6']:
            pos[0] += 1
            update = True
        if update:
            self.current_rect.pos = pos
            self.distribute()

    def select_left(self):
        self.current_rect = self.left_rect

    def select_right(self):
        self.current_rect = self.right_rect

    def toggle_corner(self):
        if self.current_rect == self.right_rect:
            self.select_left()
        else:
            self.select_right()


class Image(interface.Image):
    '''create a matplotlib image with fixed dimensions'''

    def __init__(self, image: np.ndarray, figsize: tuple, cmap='gray'):
        self._fig = plt.figure(figsize=figsize)
        self.im_obj = plt.imshow(image, cmap=cmap, animated=True, vmin=0, vmax=1)
        self._ax = self.im_obj.axes
        self.ax.axis('off')
        self.ax.set_position([0, 0, 1, 1])

    @property
    def fig(self):
        '''matplotlib figure'''
        return self._fig

    @property
    def ax(self):
        '''matplotlib axes'''
        return self._ax

    def update(self, image: np.ndarray):
        '''update the image with new data
        Arguments:
        image: numpy ndarray
        '''
        self.image_shape = image.shape
        self.im_obj.set_array(image)
        # self.fig.set_size_inches(*self._figsize(), forward=True)

    def __del__(self):
        plt.close(self.fig)


class ZoomImage(Image):
    '''create a matplotlib image that can easily be zoomed'''

    def __init__(self, image: np.ndarray, zoom=1, cmap='gray'):
        '''Arguments:
        image: numpy ndarray
        zoom: the zoom factor (optional)
        '''
        assert isinstance(zoom, Number)
        self.image_shape = image.shape
        self.zoom = zoom
        Image.__init__(self, image=image, figsize=self._figsize(), cmap=cmap)

    def _figsize(self):
        return (self.image_shape[1] / 72 * self.zoom, self.image_shape[0] / 72 * self.zoom)


class RotatableFigure(RotatableMixin, interface.ZoomImage):
    def __init__(self, image, flipped=False, rot=0, zoom=1):
        assert isinstance(flipped, bool)
        assert isinstance(rot, int)
        self.image = np.asarray(image)
        self.flipped = flipped
        self.rot = rot
        self.zoom_fig = ZoomImage(self.rotated_image(), zoom=zoom)

    @property
    def fig(self):
        return self.zoom_fig.fig

    @property
    def ax(self):
        return self.zoom_fig.ax

    def rotated_image(self):
        rotated = np.copy(self.image)
        if self.flipped:
            rotated = np.fliplr(rotated)
        if self.rot > 0:
            rotated = np.rot90(rotated, self.rot)
        return rotated

    def rotate_stack(self, stack):
        if self.flipped:
            stack = stack[:, :, ::-1, ...]
        if self.rot > 0:
            stack = np.rot90(stack, self.rot, axes=(1, 2))
        return stack

    def update(self, image=None):
        if image is not None:
            self.image = image
        self.zoom_fig.update(self.rotated_image())

    def __del__(self):
        del(self.zoom_fig)
