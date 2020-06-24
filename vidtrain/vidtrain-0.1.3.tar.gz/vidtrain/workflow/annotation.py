import os
import numpy as np
from .. import gui
from .. import datahandler
from . import interface
# TODO: (prio 5) enable storing and loading training data and trained networks in a central database


class JunctionAnnotation(gui.backend.Panel, interface.WorkflowStep):
    NAME = 'Annotate Junction Crossing Events'

    def __init__(self, master, workflow_data: datahandler.interface.WorkflowData):
        gui.backend.Panel.__init__(self, master=master)
        self.workflow_data = workflow_data
        self.gui = None
        self.copy_prediction_button = None
        self.prediction_threshold_config = None
        self.autosave = False
        self.file_versioning = datahandler.FileVersioning()
        if self.is_ready():
            self.update()
        # TODO: (prio 2) enable adding training data from another source

    @property
    def input(self):
        '''Input data to be annotated'''
        return self.workflow_data.processed

    @input.setter
    def input(self, inp: datahandler.interface.MultiImageStack):
        self.self.workflow_data.processed.update(inp)
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
        return self.workflow_data.annotation

    def update(self):
        if self.is_ready():
            try:
                self.gui.update(self.input)
            except AttributeError:
                self.create_gui()
            if self.autosave and self.workflow_data.path is not None:
                self.gui.on_annotation_leave = self.auto_save_output
            else:
                self.gui.on_annotation_leave = gui.interface._empty_callback
            if not self.workflow_data.pred_corr.empty():
                self.add_copy_predictions_ui()

    def create_gui(self):
        if self.is_ready():
            self.gui = gui.backend.MultiStacksAnnotations(master=self, multi_stack=self.input, annotation=self.output)
            self.gui.add_config_ui()
            self.gui.show(side=gui.interface.LEFT)
        # TODO: (prio 3) add configuration for class names (use listbox and entry widgets)

    def is_ready(self):
        '''Check if this step is ready to be run.'''
        return not self.input.empty()

    def is_done(self):
        '''Check if this step is done and ready for the next step.'''
        try:
            return self.is_ready and not self.output.empty()
        except AttributeError:
            return False

    def load_input(self):
        if self.workflow_data.path is None:
            fd = gui.backend.Filedialog()
            self.workflow_data.path = fd.ask_open(filetypes=([('numpy compressed', 'npz')]))
        if os.path.exists(self.default_in_file()):
            self.input.load(self.default_in_file())
            self.update()
        try:
            self.output.load(self.file_versioning.get_newest_file(self.default_out_file()))
        except TypeError:
            pass

    def save_output(self, unique=True):
        assert self.is_done, 'Cannot save output data without input. Please set/load input data first.'
        if self.workflow_data.path is None:
            fd = gui.backend.Filedialog()
            self.workflow_data.path = fd.ask_save(filetypes=([('numpy compressed', 'npz')]))
        out_path = self.file_versioning.get_name(base_path=self.default_out_file(), unique=unique)
        self.output.save(out_path)

    def auto_save_output(self):
        if self.gui.annotation_changed:
            self.save_output()
            self.gui.annotation_changed = False

    def default_in_file(self):
        return os.path.join(datahandler.get_eval_dir(self.workflow_data.path), 'junction_stacks.npz')

    def default_out_file(self):
        return os.path.join(datahandler.get_eval_dir(self.workflow_data.path), 'junction_annotations.npz')

    def add_copy_predictions_ui(self):
        if self.copy_prediction_button is None:
            self.copy_prediction_button = gui.backend.Button(
                self.gui.annotation_config, text='copy predictions', on_click=self.copy_predictions)
            self.copy_prediction_button.show(side=gui.interface.BOTTOM)
            self.prediction_threshold_config = datahandler.Config()
            self.prediction_threshold_config.new_item(name='Prediction trheshold', value=0.5,
                                                      from_=0.1, to=0.9, on_change=self.copy_predictions)
            self.prediction_threshold_config_panel = gui.backend.ConfigPanel(
                self.gui.annotation_config, self.prediction_threshold_config)
            self.prediction_threshold_config_panel.show(side=gui.interface.BOTTOM)

    def copy_predictions(self, _=None):
        self.workflow_data.annotation.update_from(self.workflow_data.pred_corr)
        self.workflow_data.annotation.apply_threshold(self.prediction_threshold_config['Prediction trheshold'].value)
        self.gui.update()
