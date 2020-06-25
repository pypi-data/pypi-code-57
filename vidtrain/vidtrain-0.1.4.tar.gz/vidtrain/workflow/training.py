import os
from .. import gui
from .. import datahandler
from . import interface


class JunctionNetworkTraining(gui.backend.Panel, interface.WorkflowStep):
    NAME = 'Train Network'

    def __init__(self, master, workflow_data: datahandler.interface.WorkflowData):
        gui.backend.Panel.__init__(self, master=master)
        self.workflow_data = workflow_data
        self.fig_panel = None
        self.file_versioning = datahandler.FileVersioning()
        self.input_config = datahandler.Config(panel_name='Input configuration:')
        self.input_config.new_item(name='Slice length', value=64, from_=16, to=128, increment=16)
        self.input_config.new_item(name='Slice padding', value=16, from_=4, to=24, increment=4)
        self.input_config.new_item(name='Scale image to (px)', value=16, from_=16,
                                   to=128, increment=16, on_change=self._enable_scaling)
        self.input_config_panel = gui.backend.ConfigPanel(master=self, config=self.input_config)
        self.input_config_panel.show(side=gui.interface.TOP, fill=gui.interface.X, expand=gui.interface.ON)
        self.training_config = datahandler.Config(panel_name='Training configuration:')
        self.training_config.new_item(name='Percent of data for validation', value=40,
                                      from_=10, to=50, increment=5)
        self.training_config.new_item(name='Batch size', value=8, from_=1, to=64)
        self.training_config.new_item(name='Epochs', value=75, from_=25, to=1000, increment=25)
        self.training_config.new_item(name='Number of networks to train', value=1, from_=1, to=50)
        # self.training_config.new_item(name='Keep best networks', value=3, from_=1, to=50)
        self.training_config_panel = gui.backend.ConfigPanel(master=self, config=self.training_config)
        self.training_config_panel.show(side=gui.interface.TOP, fill=gui.interface.X, expand=gui.interface.ON)
        self.network_config = datahandler.Config(panel_name='Network configuration:')
        self.network_config.new_item(name='Kernels', value=32, from_=4, to=128, increment=4)
        self.network_config.new_item(name='Conv3d layers', value=1, from_=1, to=5)
        self.network_config.new_item(name='ConvLSTM2D layers', value=4, from_=0, to=4)
        self.network_config.new_item(name='Reduction layers', value=3, from_=1, to=4)
        self.network_config_panel = gui.backend.ConfigPanel(master=self, config=self.network_config)
        self.network_config_panel.show(side=gui.interface.TOP, fill=gui.interface.X, expand=gui.interface.ON)
        self.figure_panel = gui.backend.Panel(master=self)
        self.model_factory = datahandler.models.SequenceClassificationModel(config=self.network_config)
        self.network_trainer = datahandler.models.NetworkTrainer(model_factory=self.model_factory)
        self.network_list_panel = gui.backend.NetworkListPanel(
            master=self.figure_panel, network_list=self.workflow_data.networks)
        self.network_list_panel.show(side=gui.interface.LEFT)
        self.figure_panel.show(side=gui.interface.TOP)
        self.buttons = gui.backend.Panel(master=self)
        self.done_button = gui.backend.Button(master=self.buttons, text='start training')
        self.done_button.show(side=gui.interface.LEFT)
        self.buttons.show(side=gui.interface.BOTTOM)
        self.manual_scale = False
        self.update()
        # TODO: (prio 3) reserve part of the training data for testing in the prediction tab
        # TODO: (prio 1) add option to filter out empty training stacks

    @property
    def input(self):
        '''Input data to be processed'''
        return (self.workflow_data.processed, self.workflow_data.annotation)

    @input.setter
    def input(self, inp: tuple):
        self.workflow_data.processed.update(inp[0])
        self.workflow_data.annotation.update(inp[1])

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
        return self.workflow_data.networks

    def is_ready(self):
        '''Check if this step is ready to be run.'''
        return not self.workflow_data.processed.empty() and not self.workflow_data.annotation.empty()

    def is_done(self):
        '''Check if this step is done and ready for the next step.'''
        return self.is_ready() and not self.output.empty()

    def update(self):
        if self.is_ready():
            self.done_button.on_click = self.start_training
            if not self.manual_scale:
                self.input_config['Scale image to (px)'].value = next(
                    self.workflow_data.processed.image_stacks()).height

    def load_input(self):
        if self.workflow_data.path is None:
            fd = gui.backend.Filedialog()
            self.workflow_data.path = fd.ask_open(filetypes=([('numpy compressed', 'npz')]))
        (x_path, y_path) = self.default_in_file()
        y_path = self.file_versioning.get_newest_file(y_path)
        if os.path.exists(x_path) and y_path is not None:
            self.input[0].load(x_path)
            self.input[1].load(y_path)
        self.load_networks()
        # TODO: (prio 2) load/save config

    def save_output(self):
        self.output.save(self.default_out_file())

    def default_in_file(self):
        return (os.path.join(datahandler.get_eval_dir(self.workflow_data.path), 'junction_stacks.npz'), os.path.join(datahandler.get_eval_dir(self.workflow_data.path), 'junction_annotations.npz'))

    def default_out_file(self):
        return os.path.join(datahandler.get_eval_dir(self.workflow_data.path), 'network')

    def load_networks(self):
        if self.workflow_data.path is None:
            fd = gui.backend.Filedialog()
            self.workflow_data.path = fd.ask_save(filetypes=([]))
        self.workflow_data.networks.load(self.default_out_file())
        self.network_list_panel.update()

    def start_training(self):
        if self.manual_scale:
            dim = self.input_config['Scale image to (px)'].value
        else:
            dim = None
        self.slicer = datahandler.data.FormatTrainingData(
            slice_len=self.input_config['Slice length'].value,
            slice_padding=self.input_config['Slice padding'].value,
            target_dim=dim
        )
        self.data_generator = datahandler.models.TrainingDataGenerator(
            batch_size=self.training_config['Batch size'].value,
            len_sequences=self.input_config['Slice length'].value,
            test_size=self.training_config['Percent of data for validation'].value / 100)
        self.data_generator.set_data(*self.slicer.apply(*self.input))
        while self.data_generator.validation_steps() == 0 and self.training_config['Batch size'].value > 0:
            self.training_config['Batch size'].value -= 1
            self.data_generator.batch_size = self.training_config['Batch size'].value
        self.network_trainer.epochs = self.training_config['Epochs'].value
        self.network_trainer.training_data = self.data_generator
        self.network_trainer.num_categories = self.input[1].num_categories
        if self.fig_panel is None:
            self.fig_panel = gui.backend.FigurePanel(master=self.figure_panel, fig=self.network_trainer.get_fig())
            self.fig_panel.show(side=gui.interface.LEFT)
        self.network_trainer.set_canvas(self.fig_panel)
        if len(self.workflow_data.networks) == 0:
            self.load_networks()
        for _ in range(self.training_config['Number of networks to train'].value):
            trainer = self.network_trainer.copy()
            trainer.compile_model()
            trainer.train()
            unique_path = trainer.save(self.default_out_file())
            self.workflow_data.networks.append(trainer, unique_path)
            self.network_list_panel.update()

    def _enable_scaling(self, _=None):
        self.manual_scale = True
