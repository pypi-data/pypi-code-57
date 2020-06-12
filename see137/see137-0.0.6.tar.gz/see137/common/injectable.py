class InjectableObject:
    _processor = None

    @property
    def processor(self):
        if self._processor is None:
            raise AttributeError("Injected processor hasn't been set. ")
        return self._processor

    @processor.setter
    def processor(self, _processor):
        self._processor = _processor
    
    def set_processor(self, _processor):
        self._processor = _processor