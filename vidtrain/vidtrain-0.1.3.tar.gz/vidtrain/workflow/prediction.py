import os
from .. import gui
from .. import datahandler
from . import interface


class JunctionPrediction(gui.backend.Panel, interface.WorkflowStep):
    NAME = 'Test/Predict'

    def __init__(self, master, workflow_data: datahandler.interface.WorkflowData):
        gui.backend.Panel.__init__(self, master=master)
        self.workflow_data = workflow_data
        self.network_list_panel = None
        self.display_height = 384
        self.input_panel = gui.backend.Panel(master=self)
        self.buttons = gui.backend.Panel(master=self)
        self.load_external_button = gui.backend.Button(
            master=self.buttons, text='load networks', on_click=self.load_external_networks)
        self.load_external_button.show()
        self.prediction_button = gui.backend.Button(master=self.buttons, text='start prediction')
        self.prediction_button.show(side=gui.interface.LEFT)
        self.buttons.show(side=gui.interface.BOTTOM)
        self.sequence_len = 64
        self.time_overlap = 16  # TODO: (prio 2) get this from the network panel
        self.file_versioning = datahandler.FileVersioning()
        if self.is_ready():
            self.update()

    @property
    def input(self):
        '''Input data to be processed'''
        return (self.workflow_data.networks, self.workflow_data.processed, self.workflow_data.annotation)

    @input.setter
    def input(self, inp: tuple):
        assert isinstance(inp[0], datahandler.interface.NetworkList)
        self.workflow_data.networks.update(inp[0])
        assert isinstance(inp[1], datahandler.interface.MultiImageStack)
        self.workflow_data.processed.update(inp[1])
        if len(inp) > 2:
            assert isinstance(inp[2], datahandler.interface.MultiImageStackClassification)
            self.workflow_data.annotation.update(inp[2])
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
        return (self.workflow_data.pred_med, self.workflow_data.pred_std, self.workflow_data.pred_corr)

    @output.setter
    def output(self, output_data:  tuple):
        for item in output_data:
            assert isinstance(item, datahandler.interface.MultiImageStackClassification)
        self.workflow_data.pred_med.update(output_data[0])
        if len(output_data) > 1:
            self.workflow_data.pred_std.update(output_data[1])
        if len(output_data) > 2:
            self.workflow_data.pred_corr.update(output_data[2])

    def update(self):
        if self.is_ready():
            try:
                self.data_panel.update(self.workflow_data.processed)
                self.network_list_panel.destroy()
            except AttributeError:
                self.create_gui()
            self._add_networklist_panel()
            self.sequence_len = self.workflow_data.networks.get_network(0).input_shape[0]
            self.data_panel.annotation.force = True
            self.data_panel.num_categories = self.workflow_data.networks.get_network(0).num_categories

    def create_gui(self):
        self.output = (datahandler.MultiImageStackClassification(multi_image_stack=self.workflow_data.processed),)
        self.network_list_placeholder = gui.backend.Panel(master=self.input_panel)
        self.network_list_placeholder.show(side=gui.interface.LEFT)
        self.data_panel = gui.backend.MultiStacksAnnotations(
            master=self.input_panel, multi_stack=self.workflow_data.processed)
        # TODO: show current value under mouse
        self.data_panel.show(side=gui.interface.LEFT)
        self.input_panel.show(side=gui.interface.TOP)
        self.prediction_button.on_click = self.start_prediction

    def _add_networklist_panel(self):
        self.network_list_panel = gui.backend.NetworkListPanel(
            master=self.network_list_placeholder, network_list=self.workflow_data.networks)
        self.network_list_panel.show(side=gui.interface.LEFT)

    def is_ready(self):
        '''Check if this step is ready to be run.'''
        return not self.workflow_data.processed.empty() and not self.workflow_data.networks.empty()

    def is_done(self):
        '''Check if this step is done and ready for the next step.'''
        return not self.workflow_data.pred_med.empty()

    def load_input(self):
        if self.workflow_data.path is None:
            fd = gui.backend.Filedialog()
            self.workflow_data.path = fd.ask_open(filetypes=([]))
        path = self.default_in_file()
        self.workflow_data.networks.load(path[0])
        self.update()

    def save_output(self):
        paths = self.default_out_file()
        self.workflow_data.pred_med.save(paths[0])
        self.workflow_data.pred_std.save(paths[1])
        self.data_panel.annotation.save(paths[2])

    def default_in_file(self):
        return (os.path.join(datahandler.get_eval_dir(self.workflow_data.path), 'network'), os.path.join(datahandler.get_eval_dir(self.workflow_data.path), 'junction_stacks.npz'), os.path.join(datahandler.get_eval_dir(self.workflow_data.path), 'junction_annotations.npz'))

    def default_out_file(self):
        paths = (os.path.join(datahandler.get_eval_dir(self.workflow_data.path), 'junction_predicted_mean.npz'),
                 os.path.join(datahandler.get_eval_dir(self.workflow_data.path), 'junction_predicted_std.npz'),
                 os.path.join(datahandler.get_eval_dir(self.workflow_data.path), 'junction_predicted_manual_corrected.npz'))
        return paths

    def start_prediction(self, formatter_class=datahandler.SequencePredictionFormatter):
        formatter = formatter_class(sequence_len=self.sequence_len, time_overlap=self.time_overlap)
        self.workflow_data.pred_med, self.workflow_data.pred_std = self.workflow_data.networks.predict(
            self.workflow_data.processed, formatter)
        self.workflow_data.pred_corr = self.workflow_data.pred_med.copy()
        self.data_panel.annotation = self.workflow_data.pred_corr
        self.data_panel.numpaths_update(self.workflow_data.pred_med.num_categories)

    def load_external_networks(self):
        fd = gui.backend.Filedialog()
        path = fd.ask_open(filetypes=([('taining weights', '.h5')]))
        try:
            path = self.file_versioning.get_part_before_time(path)
            if len(self.file_versioning.get_file_list(path)) > 0:
                self.workflow_data.networks.clear()
                self.workflow_data.networks.load(path)
                self.update()
        except TypeError:
            pass
