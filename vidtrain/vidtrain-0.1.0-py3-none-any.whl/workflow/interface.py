import abc
from ..gui import interface as gui_interface
from ..datahandler import interface as data_interface


class WorkflowStep(gui_interface.Panel):
    '''Interface for the tabs of the main gui.'''
    NAME = 'Tab name'

    @abc.abstractmethod
    def __init__(self, master: gui_interface.Panel, workflow_data: data_interface.WorkflowData):
        '''Arguments:
        master: gui_interface.Panel object into which the workflowstep panel should be placed
        workflow_data: data_interface.WorkflowData object containing the data needed for the workflow
        '''

    @property
    @abc.abstractmethod
    def input(self):
        '''Input data to be processed'''

    @property
    @abc.abstractmethod
    def output(self):
        '''Output data after processing'''

    @abc.abstractmethod
    def is_ready(self):
        '''Check if this step is ready to be run.'''

    @abc.abstractmethod
    def is_done(self):
        '''Check if this step is done and ready for the next step.'''

    @abc.abstractmethod
    def load_input(self):
        '''Ask user for data path and load input.'''

    @abc.abstractmethod
    def save_output(self):
        '''Ask user for data path and save output.'''

    @abc.abstractmethod
    def default_in_file(self):
        '''Calculate default input file path relative to path.
        Arguments:
        path: string path of original file
        Returns:
        string: default output file path
        '''

    @abc.abstractmethod
    def default_out_file(self):
        '''Calculate default output file path relative to path.
        Arguments:
        path: string path of original file
        Returns:
        string: default output file path
        '''
