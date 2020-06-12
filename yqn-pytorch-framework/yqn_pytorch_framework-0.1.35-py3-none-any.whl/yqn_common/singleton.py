class Singleton(object):
    def __init__(self, cls):
        self._cls = cls
        self._instance = {}

    def __call__(self, **kwargs):
        if self._cls not in self._instance:
            self._instance[self._cls] = self._cls(**kwargs)
        return self._instance[self._cls]
