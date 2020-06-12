from abc import ABC
from typing import List, Any, Union, Optional
from see137.common import InjectableObject
from see137.common import ComponentAbstract
from loguru import logger




class Pipeline(ABC, InjectableObject):
    """ 
        Use pipeline to run a large sequence of commands back to back. 
        Results from the previous result to process the next component/or pipeline.
    """
    def __init__(self, steps: List[Union['ComponentAbstract', 'Pipeline']]=[], name:Optional[str]=None, processor=None):
        self.steps:List[Union['ComponentAbstract', 'Pipeline']] = steps
        self.history = []
        self.name = name or self.__class__.__name__
        self._within_pipeline = []
        if processor is not None:
            self.processor = processor


    @property
    def within_pipeline(self):
        return self._within_pipeline
    
    @within_pipeline.setter
    def within_pipeline(self, _name):
        self._within_pipeline.append(_name)

    def verify(self):
        """Verify Steps
            Verify if the steps are all component abstracts and that it's not empty
        """
        if not bool(self.steps):
            raise AttributeError("Steps are Falsy (likely haven't added or replaced the variable). Please add a ComponentAbstract")
        for step in self.steps:
            if not isinstance(step, ComponentAbstract) and not isinstance(step, Pipeline):
                raise TypeError(
                    "One of the steps isn't an instance of ComponentAbstract or Pipeline. Only those two types."
                )

    @property
    def is_history(self):
        if len(self.history) > 0:
            return True
        return False

    @property
    def latest_history(self):
        if self.is_history:
            return self.history[-1]
        return None

    def pipe(self, component: Union[Union['ComponentAbstract', 'Pipeline'], List[Union['ComponentAbstract', 'Pipeline']]]):
        """Add component to pipeline. Use instead of the constructure.

        Arguments:
            item {Union[ComponentAbstract, Pipeline]} -- [description]
        """
        if isinstance(component, list):
            self.steps.extend(component)
            return self
        else:
            self.steps.append(component)
            return self

    @logger.catch(reraise=True)
    def step(self, item:Any, override=False, is_loud=True, **kwargs):
        """Runs through a sequence of events. Takes the previous one and passes it onto the next one. Done to monitor highly relational queries.

        Arguments:
            item {Any} -- The item we itend to process. For many components this is an addict dictionary. 
            
            NOTE: In future should have more constrains for this parameter.

        Returns:
            [Any] -- Returns the last item in pipeline. That can either be a pipeline response, or the response of a component.
        """
        self.verify()
        self.reset()
        for index, _step in enumerate(self.steps):
            step_result = None
            if is_loud:
                logger.debug(f"Running {_step.name}")
            _step.within_pipeline = self.name
            _step.processor = self.processor
            
            if index == 0:
                step_result = _step.step(item, override=override, is_loud=is_loud, **kwargs)
            if self.is_history:
                step_result = _step.step(self.latest_history, override=override, is_loud=is_loud, **kwargs)
            self.history.append(step_result)
        return self.latest_history

    def reset(self):
        self.history = []





if __name__ == "__main__":

    pipe = Pipeline([
        "find_item_metadata", "pull_data_from_outside", "store_data",
        "find_strategy", "find_send_location", "create_model", "send_model"
    ])
    pipe.step("sample_id")