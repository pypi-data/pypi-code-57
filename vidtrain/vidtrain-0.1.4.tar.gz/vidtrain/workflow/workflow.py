import collections
from .. import gui
from .. import datahandler
from . import preparation
from . import annotation
from . import training
from . import prediction
from . import interface
from . import evaluation


class JunctionAnalysis():
    def __init__(self, path=None):
        self.root = gui.backend.RootWindow()
        self.root.wm_title('Junction Analysis')
        self.tabs = gui.backend.Tabs(master=self.root)
        self.filedialog = gui.backend.Filedialog()
        self.path = path or self.filedialog.ask_open([])
        self.workflow_data = datahandler.JunctionAnalysisData(path=self.path)
        self.prepare = preparation.JunctionExtraction(self.root, workflow_data=self.workflow_data)
        self.annotate = annotation.JunctionAnnotation(self.root, workflow_data=self.workflow_data)
        self.annotate.autosave = True
        self.train = training.JunctionNetworkTraining(self.root, workflow_data=self.workflow_data)
        self.predict = prediction.JunctionPrediction(self.root, workflow_data=self.workflow_data)
        self.evaluate = evaluation.JunctionEvaluation(self.root, workflow_data=self.workflow_data)
        self.workflow = WorkflowList([self.prepare, self.annotate, self.train, self.predict, self.evaluate])
        self.tabs.extend(self.workflow)
        self.tabs.show(side=gui.interface.TOP, fill=gui.interface.BOTH,
                       expand=gui.interface.ON)
        self.workflow.add_controls(self.root)
        self.workflow.on_step_change = self.tabs.select
        self.tabs.on_tab_select = self.workflow.select_step
        # TODO: (prio 4) check workflowStep.is_done() before activating the next button
        # TODO: (prio 1): add "loading data..." progress bar to the root window while data is being loaded

    def run(self):
        self.root.run()


class WorkflowList(collections.abc.MutableSequence):
    '''A list of workflow steps where the output of one step is passed to the next step as input
    each item is a tab in a ttk.Notebook
    below the tabs is a list of buttons that handles navigation between steps as well as loading input data and saving output data
    '''

    def __init__(self, initlist=None, on_step_change=gui.interface._empty_callback):
        self._cur = 0
        self.on_step_change = on_step_change
        self.data = []
        if initlist is not None:
            self.extend(initlist)

    @property
    def current_step(self):
        return self._cur

    @current_step.setter
    def current_step(self, tab_no):
        self._change_step(tab_no)
        self._cur = tab_no

    def add_controls(self, master):
        self.buttons = gui.backend.Panel(master=master)
        self.button_back = gui.backend.Button(master=self.buttons, text='<< back', on_click=self.back)
        self.button_back.show()
        self.button_load = gui.backend.Button(master=self.buttons, text='load', on_click=self.load)
        self.button_load.show()
        self.button_save = gui.backend.Button(master=self.buttons, text='save', on_click=self.save)
        self.button_save.show()
        self.button_next = gui.backend.Button(master=self.buttons, text='next >>', on_click=self.next)
        self.button_next.show()
        self.buttons.show(side=gui.interface.BOTTOM)

    def __getitem__(self, i): return self.data[i]

    def __delitem__(self, i): del self.data[i]

    def __len__(self): return len(self.data)

    def __setitem__(self, i, v):
        self.check(v)
        self.data[i] = v

    def insert(self, i, v):
        self.check(v)
        self.data.insert(i, v)

    def check(self, v):
        assert isinstance(v, interface.WorkflowStep)
        v.load_input()

    def next(self):
        if self.current_step < len(self) - 1:
            self.current_step += 1

    def back(self):
        if self.current_step > 0:
            self.current_step -= 1

    def load(self):
        self.data[self.current_step].load_input()

    def save(self):
        self.data[self.current_step].save_output()

    def select_step(self, step_no):
        self.current_step = step_no

    def _change_step(self, new_step):
        if new_step != self.current_step:
            self.data[new_step].update()
            self.on_step_change(new_step)
