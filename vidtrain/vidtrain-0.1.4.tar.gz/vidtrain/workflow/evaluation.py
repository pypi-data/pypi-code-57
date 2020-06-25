import os
import numpy as np
from matplotlib import pyplot as plt
from .. import gui
from .. import datahandler
from . import interface


class JunctionEvaluation(gui.backend.Panel, interface.WorkflowStep):
    NAME = 'Evaluate'

    def __init__(self, master, workflow_data: datahandler.interface.WorkflowData):
        gui.backend.Panel.__init__(self, master=master)
        self.workflow_data = workflow_data
        self.file_versioning = datahandler.FileVersioning()
        self.current_stack = 0
        self.config = datahandler.Config(panel_name='')
        self.config.new_item(name='Result type', value=0, options=self._get_options(), on_change=self.update_everything)
        self.config_panel = gui.backend.ConfigPanel(master=self, config=self.config)
        self.config_panel.show(side=gui.interface.TOP, pady=5)
        self.single_stack_container = gui.backend.Panel(master=self)
        self.single_stack_container.add_label('Individual Stack Results')
        self.single_plots = gui.backend.ClassificationEvaluationPlots(master=self.single_stack_container)
        self.controls = gui.backend.StackControls(master=self.single_stack_container, callback=self.update)
        self.single_plots.show(side=gui.interface.TOP)
        self.controls.show(side=gui.interface.TOP, fill=gui.interface.X, expand=gui.interface.ON)
        self.single_stack_container.show(side=gui.interface.TOP, pady=5)
        self.combined_container = gui.backend.Panel(master=self)
        self.combined_container.add_label('Combined Results')
        self.combined_classes = gui.backend.ClassificationEvalPlot(
            master=self.combined_container, fig=plt.figure(), height=384, aspect=0.5)
        self.combined_classes.add_label('Combined Classes')
        self.combined_junctions = gui.backend.ClassificationEvalPlot(
            master=self.combined_container, fig=plt.figure(), height=384, plot='combined', aspect=2)
        self.combined_junctions.add_label('Total events per junction')
        self.combined_classes.show(side=gui.interface.LEFT)
        self.combined_junctions.show(side=gui.interface.LEFT)
        self.combined_container.show(side=gui.interface.TOP, pady=5)
        self.force_update = False
        self.update()
        # TODO: (prio 2) configure junction types

    @property
    def input(self):
        '''Input data to be processed'''
        return (self.workflow_data.annotation, self.workflow_data.pred_med, self.workflow_data.pred_std, self.workflow_data.pred_corr)

    @property
    def output(self):
        '''Output data after processing'''
        return None

    def update(self, _=None):
        if self.is_ready():
            self.config['Result type'].options = self._get_options()
            if self.config['Result type'].current_option == 'annotations':
                data = self.workflow_data.annotation
            elif self.config['Result type'].current_option == 'predictions':
                data = self.workflow_data.pred_med
            elif self.config['Result type'].current_option == 'corrected predictions':
                data = self.workflow_data.pred_corr
            self.controls.max_frame = len(data) - 1
            key = list(data.keys())[self.controls.frame]
            self.single_plots.update(data.image_stacks(key))
            if self.combined_classes.classification is None or self.force_update:
                self.update_combined_plots(data)

    def update_combined_plots(self, data):
        classes = datahandler.ImageStackClassification(
            data=np.concatenate(data.np_array()),
            category_names=list(data.category_names))
        self.combined_classes.update(classes)
        junctions = data.np_array()
        if len(junctions.shape) > 1:
            junctions = np.sum(junctions, axis=tuple(range(1, junctions.ndim)))[..., np.newaxis]
        else:
            js = np.zeros(junctions.shape)
            for i, j in enumerate(junctions):
                js[i] = np.sum(j)
            junctions = js[..., np.newaxis]
        self.combined_junctions.update(datahandler.ImageStackClassification(
            data=junctions, category_names=list(data.keys())))

    def update_everything(self, _=None):
        self.force_update = True
        self.update()

    def is_ready(self):
        '''Check if this step is ready to be run.'''
        return not self.workflow_data.annotation.empty()

    def is_done(self):
        '''Check if this step is done and ready for the next step.'''
        return not self.workflow_data.annotation.empty()

    def load_input(self):
        '''Ask user for data path and load input.'''
        if self.workflow_data.path is None:
            fd = gui.backend.Filedialog()
            self.workflow_data.path = fd.ask_open(filetypes=([]))
        path = self.default_in_file()
        try:
            self.workflow_data.annotation.load(self.file_versioning.get_newest_file(path[0]))
            self.workflow_data.pred_med.load(self.file_versioning.get_newest_file(path[1]))
            self.workflow_data.pred_std.load(self.file_versioning.get_newest_file(path[2]))
            self.workflow_data.pred_corr.load(self.file_versioning.get_newest_file(path[3]))
        except TypeError:
            pass
        self.update()

    def save_output(self):
        '''Ask user for data path and save output.'''
        pass

    def default_in_file(self):
        '''Calculate default input file path relative to path.
        Arguments:
        path: string path of original file
        Returns:
        string: default output file path
        '''
        paths = (os.path.join(datahandler.get_eval_dir(self.workflow_data.path), 'junction_annotations.npz'),
                 os.path.join(datahandler.get_eval_dir(self.workflow_data.path), 'junction_predicted_mean.npz'),
                 os.path.join(datahandler.get_eval_dir(self.workflow_data.path), 'junction_predicted_std.npz'),
                 os.path.join(datahandler.get_eval_dir(self.workflow_data.path), 'junction_predicted_manual_corrected.npz'))
        return paths

    def default_out_file(self):
        '''Calculate default output file path relative to path.
        Arguments:
        path: string path of original file
        Returns:
        string: default output file path
        '''
        pass

    def _get_options(self):
        options = ['annotations']
        if not self.workflow_data.pred_med.empty():
            options.append('predictions')
        if not self.workflow_data.pred_corr.empty():
            options.append('corrected predictions')
        return options
