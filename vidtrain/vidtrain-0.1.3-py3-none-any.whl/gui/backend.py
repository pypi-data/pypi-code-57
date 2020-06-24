import bisect
import numpy as np
import matplotlib
import matplotlib.ticker
from matplotlib import pyplot as plt
from matplotlib.backend_bases import key_press_handler, button_press_handler
from .. import datahandler
from . import interface
_BACKEND = 'tkinter'
if _BACKEND == 'tkinter':
    from .tk import RootWindow, Panel, PanelKey, Filedialog, Dialogs, Button, Tabs, FigureCanvas, NetworkListPanel, ConfigEntry, ConfigScale, ConfigSpinbox, ConfigOptionSpinbox, ScaleSpinbox


class ConfigPanel(Panel, interface.ConfigPanel):
    '''create a panel element that contains a configuration GUI'''

    def __init__(self, master, config):
        Panel.__init__(self, master=master)
        if config.panel_name is not None:
            self.add_label(text=config.panel_name)
        self.item_list = []
        for item in config.values():
            self.add_item(item)

    def add_item(self, item: datahandler.interface.ConfigItem):
        if item.gui_element_type == 'entry':
            el = ConfigEntry(config_item=item, master=self)
        elif item.gui_element_type == 'slider':
            el = ConfigScale(config_item=item, master=self)
        elif item.gui_element_type == 'spinbox':
            if isinstance(item, datahandler.interface.OptionConfigItem):
                el = ConfigOptionSpinbox(config_item=item, master=self)
            else:
                el = ConfigSpinbox(config_item=item, master=self)
        else:
            raise NotImplementedError('Unrecognized gui element type: {}'.format(item.gui_element_type))
        self.item_list.append(el)
        el.show(side=interface.TOP, fill=interface.X, expand=interface.ON)


class FigurePanel(Panel, interface.FigurePanel):
    '''create a Panel that contains an interactive matplotlib.pyplot figure'''

    def __init__(self, master: Panel, fig=None, toolbar=True, width=None, height=None, aspect=None):
        Panel.__init__(self, master=master)
        self.aspect = aspect
        self.fig = fig or plt.figure()
        self._width = width or self.fig.get_size_inches()[0] * matplotlib.rcParams['figure.dpi']
        self._height = height or self.fig.get_size_inches()[1] * matplotlib.rcParams['figure.dpi']
        self.change_aspect(aspect, width is None)
        self.figure = FigureCanvas(fig, master=self)
        self.mouse = None
        self.toolbar = None
        self.figure.draw()
        if toolbar:
            self.add_toolbar()
        self.figure.show_canvas()

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, width):
        self._width = width or self.height * self.aspect
        self._update_fig_size()

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, height):
        self._height = height or self.width / self.aspect
        self._update_fig_size()

    def update(self):
        self.figure.draw()

    def add_mouse(self, index, press_callback=None, drag_callback=None, release_callback=None):
        self.mouse = FigurePanelMouse(self, press_callback=press_callback,
                                      drag_callback=drag_callback, release_callback=release_callback)

    def add_toolbar(self):
        self.toolbar = self.figure.get_toolbar(self)

    def remove_toolbar(self):
        self.toolbar.destroy()
        self.toolbar = None

    def add_save_btn(self):
        self.save_btn = self.figure.get_save_button(self)

    def remove_save_btn(self):
        self.save_btn.destroy()
        self.save_btn = None

    def destroy(self):
        plt.close(self.fig)
        super().destroy()

    def change_aspect(self, aspect, adjust_width=True):
        if aspect is not None:
            if adjust_width:
                self.width = self.height * aspect
            else:
                self.height = self.width / aspect
        self.aspect = self.width / self.height
        self._update_fig_size()

    def _update_fig_size(self):
        self.fig.set_size_inches(
            self.width / matplotlib.rcParams['figure.dpi'],
            self.height / matplotlib.rcParams['figure.dpi'])


class FigurePanelMouse:
    '''handles mouse events for FigurePanel'''

    def __init__(self, figure_canvas, press_callback=interface._empty_callback, drag_callback=interface._empty_callback, release_callback=interface._empty_callback, scroll_callback=interface._empty_callback):
        self.figure_canvas = figure_canvas
        self.press_callback = press_callback
        self.drag_callback = drag_callback
        self.release_callback = release_callback
        self.scroll_callback = scroll_callback
        self.scroll_id = self.figure_canvas.figure.mpl_connect('scroll_event', self.scroll_callback)
        self.mouse_press_id = self.figure_canvas.figure.mpl_connect("button_press_event", self.on_button_press)

    def on_button_press(self, event):
        if event.button == 1:
            self.mouse_drag_id = self.figure_canvas.figure.mpl_connect(
                'motion_notify_event',
                self.on_drag)
            self.mouse_release_id = self.figure_canvas.figure.mpl_connect(
                'button_release_event',
                self.on_release)
        self.press_callback(event)
        button_press_handler(event, self.figure_canvas.figure, self.figure_canvas.toolbar)

    def on_drag(self, event):
        self.drag_callback(event)

    def on_release(self, event):
        self.figure_canvas.figure.mpl_disconnect(self.mouse_drag_id)
        self.figure_canvas.figure.mpl_disconnect(self.mouse_release_id)
        self.release_callback(event)

    def destroy(self):
        self.figure_canvas.figure.mpl_disconnect(self.mouse_press_id)
        self.figure_canvas.figure.mpl_disconnect(self.scroll_id)


class FigurePanelWatcher:
    def __init__(self, figure_canvas, enter_callback=interface._empty_callback, leave_callback=interface._empty_callback):
        self.figure_canvas = figure_canvas
        self.enter_callback = enter_callback
        self.leave_callback = leave_callback
        self.enter_id = self.figure_canvas.figure.mpl_connect('figure_enter_event', self.enter_callback)
        self.leave_id = self.figure_canvas.figure.mpl_connect('figure_leave_event', self.leave_callback)

    def destroy(self):
        self.figure_canvas.figure.mpl_disconnect(self.enter_id)
        self.figure_canvas.figure.mpl_disconnect(self.leave_id)


class FigurePanelKey:
    '''handles keyboard events for FigurePanel'''

    def __init__(self, figure_canvas, callback=None):
        self.figure_canvas = figure_canvas
        self.callback = callback or interface._empty_callback
        self.key_press_id = self.figure_canvas.figure.mpl_connect("key_press_event", self.on_key_press)

    def on_key_press(self, event):
        self.callback(event.key)
        key_press_handler(event, self.figure_canvas.figure, self.figure_canvas.toolbar)

    def destroy(self):
        self.figure_canvas.figure.mpl_disconnect(self.key_press_id)


class ImagePanel(FigurePanel, interface.ImagePanel):
    '''Panel object that contains an interactive matplotlib.pyplot figure'''

    def __init__(self, master: Panel, image: np.ndarray, toolbar=True, zoom=1, cmap='grays'):
        '''initialize ImagePanel
        Arguments:
        master: Panel into which figure will be placed
        image: numpy ndarray
        toolbar: bool enable or disable the pyplot navigation toolbar (optional, default true)
        '''
        if isinstance(zoom, tuple):
            self.im = datahandler.rotatable.Image(image=image, figsize=zoom, cmap=cmap)
        else:
            self.im = datahandler.rotatable.ZoomImage(image=image, zoom=zoom, cmap=cmap)
        FigurePanel.__init__(self, master=master, fig=self.im.fig, toolbar=toolbar)

    def update(self, image=None):
        '''refresh the figure
        Arguments:
        image: np.ndarray replaces the image data (optional)
        '''
        self.im.update(image)
        self.figure.draw()

    def get_ax(self):
        return self.im.ax


class RotatableImagePanel(ImagePanel, interface.RotatableImagePanel):

    def __init__(self, master, image, toolbar=True, zoom=1):
        self.im = datahandler.rotatable.RotatableFigure(image, zoom=zoom)
        FigurePanel.__init__(self, master=master, fig=self.im.fig, toolbar=toolbar)

    @property
    def rot(self):
        '''integer: stores the rotation in radians'''
        return self.im.rot

    @rot.setter
    def rot(self, rot: int):
        self.im.rot = rot

    @property
    def flipped(self):
        '''boolean: stores the flipped state'''
        return self.im.flipped

    @flipped.setter
    def flipped(self, flipped: bool):
        self.im.flipped = flipped

    def add_controls(self, master=None):
        if master is None:
            master = self
        self.image_controls = Panel(master=master)
        self.rotate_button = Button(
            self.image_controls,
            text='rotate',
            on_click=self.rotate)
        self.rotate_button.show(side=interface.LEFT)
        self.flip_button = Button(
            self.image_controls,
            text='flip',
            on_click=self.flip)
        self.flip_button.show(side=interface.LEFT)
        self.image_controls.show(side=interface.BOTTOM, fill=interface.BOTH, expand=interface.ON)

    def rotate(self):
        self.im.rotate()
        self.update()
        try:
            self.rotation_callback()
        except AttributeError:
            pass

    def flip(self):
        self.im.flip()
        self.update()
        try:
            self.flip_callback()
        except AttributeError:
            pass


class LinkedImages(Panel, interface.ImagePanel):
    def __init__(self, master, image_list, toolbar=False, zoom=1):
        Panel.__init__(self, master)
        self.image_list = image_list
        self.canvas_list = []
        self.mouse_list = []
        for i, image in enumerate(self.image_list):
            self.mouse_list.append(None)
            self.canvas_list.append(RotatableImagePanel(master=self, image=np.squeeze(image),
                                                        toolbar=toolbar, zoom=zoom))
            if i > 0:
                self.canvas_list[i].rotation_callback = self.canvas_list[0].rotate
                self.canvas_list[i].flip_callback = self.canvas_list[0].flip
            self.canvas_list[i].show(side=interface.LEFT, fill=interface.X, expand=interface.ON, padx=2, pady=2)

    def update(self, image_list=None):
        if image_list is not None:
            self.image_list = image_list
        for i in range(len(self.canvas_list)):
            self.canvas_list[i].update(self.image_list[i])

    def add_mouse(self, index, press_callback=None, drag_callback=None, release_callback=None):
        '''add mouse event callback handler to the matplotlib figure
        Arguments:
        index:  int index of the image that the callbacks should be assigned to.
                If index is not an int, the callback will be assigned to all figures.
        press_callback (optional): function handle executed on mouse button press
        drag_callback (optional): function handle executed on mouse drag (with button pressed)
        release_callback (optional): function handle executed on mouse button release
        '''
        if type(index, int):
            self.mouse_list[index] = FigurePanelMouse(self.canvas_list[index],
                                                      press_callback=press_callback,
                                                      drag_callback=drag_callback,
                                                      release_callback=release_callback)
        else:
            for n, canvas in enumerate(self.canvas_list):
                self.mouse_list[n] = FigurePanelMouse(canvas,
                                                      press_callback=press_callback,
                                                      drag_callback=drag_callback,
                                                      release_callback=release_callback)

    def add_controls(self):
        self.canvas_list[0].add_controls(self)

    def get_ax(self, index):
        return self.canvas_list[index].get_ax()


class LinkedStacks(Panel, interface.StackPanel):
    def __init__(self, master, stack_list, toolbar=False, zoom=1):
        Panel.__init__(self, master)
        self.controls = StackControls(master=self, callback=self.update_frame, key_ud=False)
        self.on_frame_change = interface._empty_callback
        self._stacks = stack_list
        self.controls.max_frame = self.max_frame
        self.images = LinkedImages(self, self.image_list,
                                   toolbar=toolbar, zoom=zoom)
        self.controls.show(side=interface.BOTTOM, fill=interface.X, expand=interface.ON)
        self.images.show(side=interface.BOTTOM)

    @property
    def stack_list(self):
        return self._stacks

    @stack_list.setter
    def stack_list(self, stack_list):
        self._stacks = stack_list
        self.controls.max_frame = self.max_frame
        self.update()

    @property
    def frame(self):
        return self.controls.frame

    @frame.setter
    def frame(self, frame):
        self.controls.frame = frame
        self.update()
        self.on_frame_change(frame)

    @property
    def frames_of_interest(self):
        return self.controls.frames_of_interest

    @frames_of_interest.setter
    def frames_of_interest(self, foi: list):
        self.controls.frames_of_interest = foi

    @property
    def on_frame_change(self):
        return self._on_frame_change

    @on_frame_change.setter
    def on_frame_change(self, on_frame_change):
        self._on_frame_change = on_frame_change

    @property
    def max_frame(self):
        return min([stack.shape[0] for stack in self.stack_list]) - 1

    @property
    def image_list(self):
        return [np.squeeze(stack[self.frame]) for stack in self.stack_list]

    def add_mouse(self, *args, **kw):
        self.images.add_mouse(*args, **kw)

    def update(self):
        self.images.update(self.image_list)

    def get_ax(self, index):
        return self.images.get_ax(index)

    def update_frame(self, frame=None):
        if frame is not None:
            self.frame = frame
        else:
            self.update()
            self.on_frame_change(self.frame)


class MultiStacks(Panel):
    def __init__(self, master, multi_stack: datahandler.interface.MultiImageStack, toolbar=False, zoom=1):
        Panel.__init__(self, master)
        self._multi_stack = None
        self.frames_of_interest = dict()
        self.controls = StackControls(master=self, callback=self.update_stack, key_lr=False)
        self.multi_stack = multi_stack
        self.stack_display = LinkedStacks(master=self,
                                          stack_list=[self.multi_stack[self.stack_names[0]]],
                                          toolbar=toolbar,
                                          zoom=zoom)
        self.stack_display.add_label(text=self.stack_names[0])
        self.controls.add_label(text='switch stack:')
        self.stack_display.show(side=interface.TOP)
        self.controls.show(side=interface.TOP, fill=interface.X, expand=interface.ON)
        self.on_frame_change = interface._empty_callback
        self.on_stack_change = interface._empty_callback

    @property
    def multi_stack(self):
        return self._multi_stack

    @multi_stack.setter
    def multi_stack(self, ms: datahandler.interface.MultiImageStack):
        self._multi_stack = ms
        self.stack_names = list(self.multi_stack.keys())
        self.controls.max_frame = len(self.stack_names) - 1

    @property
    def stack_key(self):
        return self.stack_names[self.controls.frame]

    @stack_key.setter
    def stack_key(self, key):
        self.update_stack(key=key)

    @property
    def frame(self):
        return self.stack_display.frame

    @frame.setter
    def frame(self, frame):
        self.update_frame(frame=frame)

    @property
    def on_frame_change(self):
        return self.stack_display.on_frame_change

    @on_frame_change.setter
    def on_frame_change(self, on_frame_change):
        self.stack_display.on_frame_change = on_frame_change

    def update(self, multi_stack=None):
        if isinstance(multi_stack, datahandler.interface.MultiImageStack):
            self.multi_stack = multi_stack
        self.update_stack()

    def update_stack(self, index=None, key=None):
        if index is None:
            index = self.controls.frame
        key = key or self.stack_names[index]
        self.frame = 0
        self.stack_display.label['text'] = key
        self.stack_display.stack_list = [self.multi_stack[key]]
        if len(self.frames_of_interest) == len(self.multi_stack):
            self.stack_display.frames_of_interest = self.frames_of_interest[key]
        self.on_stack_change(key)

    def update_frame(self, frame=None):
        self.stack_display.update_frame(frame=frame)

    def next_stack(self, inc=1):
        self.controls.frame += inc


class ImageStackClassification(Panel):
    def __init__(self, master, multi_stack: datahandler.interface.MultiImageStackClassification, toolbar=False, zoomed_height=385):
        Panel.__init__(self, master)
        self.fast_seeker = FastSeeker()
        self.height = 7
        self.threshold = 0.5
        self.changed = False
        self.frames_of_interest = dict()
        self.multi_stack = multi_stack
        self.key = next(iter(multi_stack.keys()))
        self.frame = 0
        self.zoomed_height = zoomed_height
        self.toolbar = toolbar
        self.image_panel = None
        self.mouse = None
        self.watcher = None
        self.frame_indicator = None
        self.on_scroll = interface._empty_callback
        self.figure_leave_callback = interface._empty_callback
        self.over_scroll = 0
        self.under_scroll = 0
        self.over_scroll_threshold = 12
        self.on_over_scroll = interface._empty_callback
        self.create_figure()

    @property
    def multi_stack(self):
        return self._multi_stack

    @multi_stack.setter
    def multi_stack(self, ms: datahandler.interface.MultiImageStackClassification):
        self._multi_stack = ms
        self.changed = False

    @property
    def offset(self):
        return int(np.floor(self.height / 2))

    @property
    def total_frames(self):
        return self.multi_stack[self.key].shape[0]

    @property
    def max_frame(self):
        return self.total_frames - 1

    def create_figure(self):
        area = self.current_area()
        shape = area.shape
        self.image_panel = ImagePanel(self, area, cmap='magma',
                                      toolbar=self.toolbar, zoom=self.zoomed_height/self.height)
        self.image_panel.show()
        self.mouse = FigurePanelMouse(self.image_panel, press_callback=self.toggle, scroll_callback=self.scroll_frame)
        self.watcher = FigurePanelWatcher(self.image_panel, leave_callback=self.on_figure_leave)
        self.frame_indicator = datahandler.rotatable.RotatableRectangle(
            pos=(-0.5, -0.5), size=(shape[1], 1), image_shape=shape)
        self.update_indicator()
        self.frame_indicator.draw(self.image_panel.get_ax())

    def change_frame(self, frame):
        if frame < 0:
            frame = 0
            self.under_scroll += 1
        elif frame > 0:
            self.under_scroll = 0
        if frame > self.max_frame:
            frame = self.max_frame
            self.over_scroll += 1
        elif frame < self.max_frame:
            self.over_scroll = 0
        self.frame = frame
        self.update()
        if self.over_scroll > self.over_scroll_threshold:
            self.over_scroll = 0
            self.on_over_scroll(1)
        elif self.under_scroll > self.over_scroll_threshold:
            self.under_scroll = 0
            self.on_over_scroll(-1)

    def change_key(self, key):
        self.key = key
        self.update()

    def current_area(self):
        data = self.multi_stack[self.key]
        if self.frame < self.offset:
            return data[:self.height, :]
        elif self.frame < data.shape[0] - self.offset:
            return data[self.frame - self.offset:self.frame + self.offset + 1, :]
        else:
            return data[-self.height:, :]

    def re_draw(self):
        self.image_panel.destroy()
        self.create_figure()

    def update(self):
        self.update_indicator()
        self.image_panel.update(self.current_area())
        if len(self.frames_of_interest) == len(self.multi_stack):
            self.fast_seeker.frames_of_interest = self.frames_of_interest[self.key]

    def update_indicator(self):
        if self.frame < self.offset:
            self.frame_indicator.pos = (-0.5, self.frame - 0.5)
        elif self.frame < self.total_frames - self.offset:
            self.frame_indicator.pos = (-0.5, self.offset - 0.5)
        else:
            self.frame_indicator.pos = (-0.5, self.height + self.frame - self.total_frames - 0.5)
        self.frame_indicator.update()

    def toggle(self, event):
        x = int(round(event.xdata))
        y = int(round(event.ydata))
        if self.frame < self.offset:
            pass
        elif self.frame < self.total_frames - self.offset:
            y += self.frame - self.offset
        else:
            y += self.total_frames - self.height
        self.multi_stack[self.key][y, x] = float(self.multi_stack[self.key][y, x] < self.threshold)
        self.changed = True
        self.update()

    def scroll_frame(self, event):
        if event.key == 'shift':
            if event.step < 0:
                self.change_frame(self.fast_seeker.fast_forward(self.frame, self.max_frame))
            if event.step > 0:
                self.change_frame(self.fast_seeker.fast_rewind(self.frame, self.max_frame))
        elif event.key == 'control':
            self.change_frame(self.frame - 2 * event.step)
        else:
            self.change_frame(self.frame - event.step)
        self.on_scroll(self.frame)

    def add_toolbar(self):
        self.image_panel.add_toolbar()

    def on_figure_leave(self, event=None):
        self.figure_leave_callback()


class MultiStacksAnnotations(Panel):
    def __init__(self,
                 master,
                 multi_stack: datahandler.interface.MultiImageStack,
                 annotation=datahandler.MultiImageStackClassification(),
                 toolbar=False,
                 display_height=384,
                 copy_predictions=interface._empty_callback):
        Panel.__init__(self, master)
        self.frames_of_interest = None
        self.foi_config = datahandler.Config(panel_name=' ')
        self.foi_config.new_item(name='Frame of interest threshold', value=40, from_=0.5,
                                 to=100, increment=0.5, on_change=self._calc_foi)
        self.stacks = multi_stack
        self.display_height = display_height
        height = next(self.stacks.image_stacks()).height
        self.stack_gui = MultiStacks(master=self, multi_stack=self.stacks, zoom=self.display_height/height)
        self.stack_gui.show(side=interface.LEFT)
        self.annotation = annotation
        self.annotation.create_from_multi_image_stack(self.stacks)
        self.annotation_panel = Panel(master=self)
        self.annotation_panel_heading = Panel(master=self.annotation_panel)
        self.annotation_panel_labels = []
        self.refresh_annotation_labels()
        self.annotation_panel_heading.show(side=interface.TOP, fill=interface.X)
        self.annotation_gui = ImageStackClassification(
            master=self.annotation_panel, multi_stack=self.annotation, zoomed_height=self.display_height)
        self.stack_gui.on_stack_change = self.annotation_gui.change_key
        self.stack_gui.on_frame_change = self.annotation_gui.change_frame
        self.annotation_gui.on_scroll = self.stack_gui.update_frame
        self.annotation_gui.on_over_scroll = self.stack_gui.next_stack
        self.annotation_gui.show(side=interface.TOP, padx=2, pady=2)
        self.annotation_config = Panel(self.annotation_panel)
        self.annotation_config.show(side=interface.LEFT)
        self.annotation_panel.show(side=interface.LEFT, fill=interface.Y, expand=interface.ON)
        self.dialogs = Dialogs(title='Annotation')
        self.output_config = datahandler.Config(panel_name='Output configuration:')
        self.output_config.new_item(name='Number of Paths', gui_element_type='spinbox', value=6,
                                    from_=2, to=10, on_change=self.numpaths_update)
        self.copy_predictions = copy_predictions
        self.foi_config_panel = ConfigPanel(master=self.annotation_config, config=self.foi_config)
        self.foi_config_panel.show(side=interface.BOTTOM)
        self._calc_foi()

    @property
    def stacks(self):
        return self._stacks

    @stacks.setter
    def stacks(self, ms: datahandler.interface.MultiImageStack):
        self._stacks = ms
        self._calc_foi()

    @property
    def num_categories(self):
        return self.output_config['Number of Paths'].value

    @num_categories.setter
    def num_categories(self, cat):
        self.output_config['Number of Paths'].value = cat

    @property
    def on_annotation_leave(self):
        return self.annotation_gui.figure_leave_callback

    @on_annotation_leave.setter
    def on_annotation_leave(self, callback):
        self.annotation_gui.figure_leave_callback = callback

    @property
    def annotation_changed(self):
        return self.annotation_gui.changed

    @annotation_changed.setter
    def annotation_changed(self, val: bool):
        self.annotation_gui.changed = val

    def add_config_ui(self):
        self.output_config_panel = ConfigPanel(self.annotation_config, self.output_config)
        self.output_config_panel.show(side=interface.TOP)

    def update(self, multi_stack=None):
        if isinstance(multi_stack, datahandler.interface.MultiImageStack):
            self.stacks = multi_stack
            self.annotation.update_multi_stack(self.stacks)
            self.annotation_gui.change_key(next(iter(self.stacks.keys())))
            self.stack_gui.update(self.stacks)
        else:
            self.stack_gui.update()
        self.annotation_gui.update()

    def refresh_annotation_labels(self):
        for i, name in enumerate(self.annotation.category_names):
            try:
                self.annotation_panel_labels[i].edit_label(text=name)
            except IndexError:
                self.annotation_panel_labels.append(Panel(master=self.annotation_panel_heading))
                self.annotation_panel_labels[-1].add_label(text=name)
            self.annotation_panel_labels[i].show(side=interface.LEFT, fill=interface.X, expand=interface.ON)
        for n in range(i + 1, len(self.annotation_panel_labels)):
            self.annotation_panel_labels[n].hide()

    def numpaths_update(self, num_paths):
        '''Make sure the number of columns of output matches num_paths'''
        try:
            self.annotation.num_categories = num_paths
        except datahandler.interface.VidtrainDataLossException:
            if self.dialogs.yes_no('Reducing the number of categories will cause data loss. Are you sure?'):
                self.annotation.force = True
                self.annotation.num_categories = num_paths
            else:
                self.output_config['Number of Paths'].value = self.annotation.num_categories
        except AttributeError:
            pass
        try:
            self.annotation_gui.multi_stack = self.annotation
            self.refresh_annotation_labels()
            self.annotation_gui.re_draw()
        except AttributeError:
            pass

    def clear_annotations(self):
        self.annotation.create_from_multi_image_stack(self.stacks)
        self.annotation_gui.update()

    def add_toolbar(self):
        self.annotation_gui.add_toolbar()

    def _calc_foi(self, _=None):
        self.frames_of_interest = dict()
        for key, stack in self.stacks.items():
            iqr = np.percentile(stack, 0.75) - np.percentile(stack, 0.25)
            med = np.percentile(stack, 0.5)
            threshold = med + iqr * self.foi_config['Frame of interest threshold'].value
            self.frames_of_interest[key] = np.where(np.any(stack > threshold, axis=(1, 2, 3)))[0]
        try:
            self.stack_gui.frames_of_interest = self.frames_of_interest
            self.stack_gui.update()
            self.annotation_gui.frames_of_interest = self.frames_of_interest
            self.annotation_gui.update()
        except AttributeError:
            pass


class ClassificationEvalPlot(FigurePanel):
    def __init__(self, master, isc=None, plot='classes', **kw):
        FigurePanel.__init__(self, master, **kw)
        self.classification = isc
        self.axes = self.fig.add_subplot(1, 1, 1)
        self.plot = plot
        self.title = ''

    def update(self, isc: datahandler.interface.ImageStackClassification):
        self.classification = isc
        self.axes.clear()
        self.num_cat = self.classification.data.shape[1]
        self.bar_x = list(self.classification.category_names)[:self.num_cat]
        if self.plot == 'classes':
            self.plot_classes()
        elif self.plot == 'combined':
            self.plot_combined()
        else:
            self.plot_frames()
        self.axes.set_title(self.title)
        self.fig.tight_layout()
        super().update()

    def plot_classes(self):
        self.axes.bar(self.bar_x, np.sum(self.classification.data, axis=0))
        self.axes.set_xlabel('class')
        self.axes.set_ylabel('events')
        self.axes.yaxis.set_major_locator(matplotlib.ticker.MaxNLocator(integer=True, min_n_ticks=1))
        self.axes.tick_params(axis='x', labelrotation=90)

    def plot_frames(self):
        frames = np.array(range(self.classification.data.shape[0]))
        for cat in range(self.num_cat):
            self.axes.plot(frames, self.classification.data[:, cat], label=self.bar_x[cat])
        self.axes.set_xlabel('frame')
        self.axes.set_ylabel('probability')
        self.axes.legend()
        self.axes.yaxis.set_major_formatter(matplotlib.ticker.FormatStrFormatter('%.1f'))
        self.axes.xaxis.set_major_locator(matplotlib.ticker.MaxNLocator(integer=True, prune='both'))
        self.axes.set_ylim(0, 1)

    def plot_combined(self):
        junction_names = self.classification._category_names
        self.axes.bar(junction_names, self.classification.data[:, 0])
        self.axes.set_xlabel('junction_coordinates')
        self.axes.set_ylabel('events')
        self.axes.yaxis.set_major_locator(matplotlib.ticker.MaxNLocator(integer=True, prune='both'))
        self.axes.tick_params(axis='x', labelrotation=90)


class ClassificationEvaluationPlots(Panel):
    def __init__(self, master, isc=None, height=384):
        Panel.__init__(self, master)
        self.per_class = ClassificationEvalPlot(self, fig=plt.figure(), isc=isc, height=height, aspect=0.5)
        self.per_time = ClassificationEvalPlot(self, fig=plt.figure(), isc=isc,
                                               plot='frames', height=height, aspect=2)
        self.per_class.show()
        self.per_time.show()

    def update(self, isc: datahandler.interface.ImageStackClassification):
        self.per_class.update(isc)
        self.per_time.update(isc)


class StackControls(Panel):
    def __init__(self, master, callback, key_lr=True, key_ud=True):
        Panel.__init__(self, master)
        self.fast_seeker = FastSeeker()
        self.callback = callback
        self.frame_slider = ScaleSpinbox(master=self, to=0, on_change=self.on_change)
        self.controls = Panel(master=self)
        self.skip_start_btn = Button(master=self.controls, text='|<', on_click=self.skip_start)
        self.ffwd_btn = Button(master=self.controls, text='>>', on_click=self.fast_forward)
        # TODO: (prio 4) add play-forward, stop, play-backward, buttons
        self.frwd_btn = Button(master=self.controls, text='<<', on_click=self.fast_rewind)
        self.skip_end_btn = Button(master=self.controls, text='>|', on_click=self.skip_end)
        self.skip_start_btn.pack(side=interface.LEFT)
        self.frwd_btn.pack(side=interface.LEFT)
        self.ffwd_btn.pack(side=interface.LEFT)
        self.skip_end_btn.pack(side=interface.LEFT)
        self.controls.pack(side=interface.BOTTOM)
        self.frame_slider.pack(side=interface.BOTTOM, fill=interface.BOTH, expand=1)
        self.key_lr = key_lr
        self.key_ud = key_ud
        if key_lr or key_ud:
            self.panel_key = PanelKey(master=master.winfo_toplevel(), callback=self.on_key_pressed)

    @property
    def frame(self):
        return self.frame_slider.value

    @frame.setter
    def frame(self, val):
        if val > self.max_frame:
            val = self.max_frame
        if val < 0:
            val = 0
        if self.frame_slider.value != int(val):
            self.frame_slider.value = int(val)
            self.on_change()

    @property
    def max_frame(self):
        return self.frame_slider.to

    @max_frame.setter
    def max_frame(self, limit):
        self.frame_slider.to = limit

    @property
    def frames_of_interest(self):
        return self.fast_seeker.frames_of_interest

    @frames_of_interest.setter
    def frames_of_interest(self, foi: list):
        self.fast_seeker.frames_of_interest = foi

    def skip_start(self):
        self.frame = 0

    def skip_end(self):
        self.frame = self.max_frame

    def fast_forward(self):
        self.frame = self.fast_seeker.fast_forward(self.frame, self.max_frame)

    def fast_rewind(self):
        self.frame = self.fast_seeker.fast_rewind(self.frame, self.max_frame)

    def on_change(self, frame=None):
        self.callback(self.frame)

    def on_key_pressed(self, key):
        if (key.lower() == 'right' and self.key_lr) or (key.lower() == 'up' and self.key_ud):
            self.frame += 1
        elif (key.lower() == 'left' and self.key_lr) or (key.lower() == 'down' and self.key_ud):
            self.frame -= 1
        elif (key.lower() == 'shift+right' and self.key_lr) or (key.lower() == 'shift+up' and self.key_ud):
            self.fast_forward()
        elif (key.lower() == 'shift+left' and self.key_lr) or (key.lower() == 'shift+down' and self.key_ud):
            self.fast_rewind()
        elif (key.lower() == 'control+right' and self.key_lr) or (key.lower() == 'control+up' and self.key_ud):
            self.frame += 2
        elif (key.lower() == 'control+left' and self.key_lr) or (key.lower() == 'control+down' and self.key_ud):
            self.frame -= 2


class FastSeeker:
    def __init__(self, frames_of_interest=[]):
        self.frames_of_interest = frames_of_interest

    def fast_forward(self, frame, max_frame):
        if len(self.frames_of_interest) > 0:
            try:
                frame = self.frames_of_interest[bisect.bisect_right(self.frames_of_interest, frame)]
            except IndexError:
                frame = self.frames_of_interest[-1]
        else:
            frame += round(max_frame / 10) + 1
        return frame

    def fast_rewind(self, frame, max_frame):
        if len(self.frames_of_interest) > 0:
            index = bisect.bisect_left(self.frames_of_interest, frame)
            if frame in self.frames_of_interest and index > 0:
                index -= 1
            try:
                frame = self.frames_of_interest[index]
            except IndexError:
                frame = self.frames_of_interest[-1]
        else:
            frame -= round(max_frame / 10) + 1
        return frame
