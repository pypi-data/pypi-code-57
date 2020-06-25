import os
import numpy as np
import micdata
from .. import gui
from .. import datahandler
from . import interface


class JunctionExtraction(gui.backend.Panel, interface.WorkflowStep):
    NAME = 'Extract Junctions'

    def __init__(self, master, workflow_data: datahandler.interface.WorkflowData):
        gui.backend.Panel.__init__(self, master=master)
        self.workflow_data = workflow_data
        self.projection_config = datahandler.Config()
        self.projection_config.new_item(name='Projection method', value=0, options=['median', 'std', 'max', 'mean'])
        self.projection_chooser = gui.backend.Panel(master=self)
        self.proj_config_panel = gui.backend.ConfigPanel(master=self.projection_chooser, config=self.projection_config)
        self.proj_config_panel.show(side=gui.interface.LEFT)
        self.create_image_btn = gui.backend.Button(
            self.projection_chooser, 'apply', on_click=self.re_calculate_image)
        self.create_image_btn.show(side=gui.interface.LEFT, padx=5, pady=2)
        self.projection_chooser.show(side=gui.interface.TOP, fill=gui.interface.X, expand=gui.interface.ON)
        self.input_cache = None
        self.image = None
        self.rectangles = None
        self.main_figure = None
        self.config_panel = None
        self.config = datahandler.Config(panel_name='Rectangle config:')
        self.config.new_item(name='Rows', value=1,
                             from_=1, to=100, on_change=self._on_row_update)
        self.config.new_item(name='Columns', value=16,
                             from_=2, to=100, on_change=self._on_col_update)
        self.config.new_item(name='Rectangle size (px)', value=16,
                             from_=8, to=256, increment=8, on_change=self._on_dim_update)
        self.config.new_item(name='Row height (px)', value=16.0,
                             from_=4.0, to=64.0, increment=0.01, on_change=self._on_height_update)
        self.config.new_item(name='Move', value=0, options=[
                             'red rectangle', 'blue rectangle'], on_change=self._select_rectangle)
        self.buttons = gui.backend.Panel(master=self)
        self.done_button = gui.backend.Button(master=self.buttons, text='extract junctions')
        self.done_button.show(side=gui.interface.LEFT)
        self.buttons.show(side=gui.interface.BOTTOM)
        self.dialogs = gui.backend.Dialogs(title='Junction Extraction')
        # TODO: (prio 4) save/load rectangles and median image
        # TODO: (prio 5) add optional background subtraction

    @property
    def input(self):
        '''Input data to be processed'''
        return self.workflow_data.raw

    @input.setter
    def input(self, input_data: np.ndarray):
        self.workflow_data.raw.data = input_data
        self.update()

    @property
    def config(self):
        '''Configuration data'''
        return self._config

    @config.setter
    def config(self, conf: datahandler.interface.Config):
        self._config = conf

    @property
    def output(self):
        '''Output data after processing'''
        return self.workflow_data.processed

    @output.setter
    def output(self, output_data: datahandler.interface.MultiImageStack):
        self.workflow_data.processed.update(output_data)

    def figure_panel_label(self):
        return self.projection_config['Projection method'].current_option + ' projection:'

    def cache_data(self):
        self.input_cache = np.copy(self.input.data)

    def data_changed(self):
        return not np.array_equal(self.input_cache, self.input.data)

    def create_image(self):
        if self.data_changed():
            self.image = getattr(self.input, self.projection_config['Projection method'].current_option)()
            self.cache_data()

    def re_calculate_image(self):
        self.input_cache = None
        self.main_figure_panel.edit_label(self.figure_panel_label())
        self.update()

    def update(self):
        if self.is_ready():
            self.create_image()
            try:
                self.main_figure.update(self.image)
            except AttributeError:
                self.create_gui()

    def create_gui(self):
        self.rectangles = datahandler.rotatable.RectangleMatrix(
            image_shape=(self.input.image_shape[:2]),
            num_rows=self.config['Rows'].value,
            num_cols=self.config['Columns'].value,
            size=self.config['Rectangle size (px)'].value,
            row_height=self.config['Row height (px)'].value)
        self.fig_zoom_canvas = gui.backend.Panel(master=self)
        self.main_figure_panel = gui.backend.Panel(master=self.fig_zoom_canvas)
        self.main_figure_panel.add_label(self.figure_panel_label())
        self.main_figure = gui.backend.RotatableImagePanel(master=self.main_figure_panel, image=self.image)
        self.main_figure.add_controls()
        self.main_figure.show()
        self.main_figure_panel.show(padx=2)
        self.rectangles.add_all(self.main_figure.get_ax())
        self.main_figure_mouse = gui.backend.FigurePanelMouse(
            figure_canvas=self.main_figure,
            press_callback=self._on_mouse_button_press,
            drag_callback=self._on_mouse_drag)
        self.main_figure_key = gui.backend.FigurePanelKey(
            self.main_figure,
            callback=self._on_key_press)
        self.main_figure.rotation_callback = self._inc_rotation
        self.main_figure.flip_callback = self._toggle_flip
        self.zoom = gui.backend.Panel(self.fig_zoom_canvas)
        self.zoom.add_label(text='left')
        self.left_zoom_figure = gui.backend.RotatableImagePanel(
            master=self.zoom, image=self._extract_rect_image(self.rectangles.left_rect), toolbar=False, zoom=self.image.shape[1] / 2 / self.config['Rectangle size (px)'].value)
        self.left_zoom_figure.show(side=gui.interface.TOP)
        self.zoom.add_label(text='right')
        self.right_zoom_figure = gui.backend.RotatableImagePanel(
            master=self.zoom, image=self._extract_rect_image(self.rectangles.right_rect), toolbar=False, zoom=self.image.shape[1] / 2 / self.config['Rectangle size (px)'].value)
        self.right_zoom_figure.show(side=gui.interface.TOP)
        self.zoom.show(side=gui.interface.TOP)
        self.fig_zoom_canvas.show(side=gui.interface.TOP)
        self.config_panel = gui.backend.ConfigPanel(master=self, config=self.config)
        self.config_panel.show(side=gui.interface.BOTTOM, fill=gui.interface.X, expand=gui.interface.ON)
        self.done_button.on_click = self._save_rect_stacks

    def is_ready(self):
        '''Check if this step is ready to be run.'''
        return not self.input.empty()

    def is_done(self):
        '''Check if this step is done and the next step can be run.'''
        return isinstance(self.output, datahandler.interface.MultiImageStack)

    def load_input(self):
        self.input.load(self.default_in_file())
        self.update()
        if os.path.exists(self.default_out_file()):
            self.output.load(self.default_out_file())

    def save_output(self):
        if self.workflow_data.path is None:
            fd = gui.backend.Filedialog()
            self.workflow_data.path = fd.ask_save(filetypes=([('numpy compressed', 'npz')]))
        self.output.save(self.default_out_file())

    def default_in_file(self):
        return self.workflow_data.path

    def default_out_file(self):
        return os.path.join(datahandler.get_eval_dir(self.workflow_data.path), 'junction_stacks.npz')

    def _inc_rotation(self):
        self.rectangles.rotate()
        self._update_fig()

    def _toggle_flip(self):
        self.rectangles.flip()
        self._update_fig()

    def _on_row_update(self, rows):
        self.rectangles.num_rows = int(rows)
        self.rectangles.update_rect_number()
        self.rectangles.refresh_ax(self.main_figure.im.ax)
        self.main_figure.figure.draw()

    def _on_col_update(self, cols):
        self.rectangles.num_cols = int(cols)
        self.rectangles.update_rect_number()
        self.rectangles.refresh_ax(self.main_figure.im.ax)
        self.main_figure.figure.draw()

    def _on_dim_update(self, size):
        self.rectangles.dim = int(size)
        self._update_fig()

    def _on_height_update(self, height):
        self.rectangles.row_height = height
        self._update_fig()

    def _update_fig(self):
        self.rectangles.update()
        self.main_figure.update()
        self._update_zoom()

    def _update_zoom(self):
        self.left_zoom_figure.update(image=self._extract_rect_image(self.rectangles.left_rect))
        self.right_zoom_figure.update(image=self._extract_rect_image(self.rectangles.right_rect))

    def _on_mouse_button_press(self, event):
        if event.button == 1:
            self.rectangles.store_current_pos((event.xdata, event.ydata))
            self.main_figure.update()
            self._update_zoom()
        else:
            self.config['Move'].toggle()

    def _on_mouse_drag(self, event):
        self.rectangles.store_current_pos((event.xdata, event.ydata))
        self.main_figure.update()
        self._update_zoom()

    def _on_key_press(self, key):
        self.rectangles.move_current_rect(key)
        self.main_figure.update()
        self._update_zoom()

    def _select_rectangle(self, rect):
        if rect == 0:
            self.rectangles.select_left()
        else:
            self.rectangles.select_right()

    def _save_rect_stacks(self):
        x_diff = abs(self.rectangles.rect_list[0].raw_pos[0] - self.rectangles.rect_list[1].raw_pos[0])
        y_diff = abs(self.rectangles.rect_list[0].raw_pos[1] - self.rectangles.rect_list[1].raw_pos[1])
        self.output.clear()
        for rect in self.rectangles.generator():
            pos = list(map(int, rect.raw_pos))
            if any(p < 0 for p in pos):
                continue
            dim = rect.dim
            if x_diff > y_diff:  # make sure the dimension with larger differences is printed first
                key = 'x:{:04d};y:{:04d}'.format(pos[0], pos[1])
            else:
                key = 'y:{:04d};x:{:04d}'.format(pos[1], pos[0])
            try:
                substack = self.input.copy_tile(pos, dim)
                substack = self.main_figure.im.rotate_stack(substack)
            except IndexError:
                continue
            self.output[key] = substack
        self.dialogs.info(message='Extracted {} junction stacks.'.format(len(self.output.keys())))

    def _extract_rect_image(self, rect):
        return rect.extract_image(self.main_figure.im)
