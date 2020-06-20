#!/usr/bin/env python3

class SheetgearError(RuntimeError):
    def __init__(self, *args, **kwargs):
        super(SheetgearError, self).__init__(self,*args,**kwargs)

class InvalidGridRangeError(SheetgearError):
    def __init__(self, *args, **kwargs):
        super(InvalidGridRangeError, self).__init__(self,*args,**kwargs)

class SheetNotFoundError(SheetgearError):
    def __init__(self, *args, **kwargs):
        super(SheetNotFoundError, self).__init__(self,*args,**kwargs)
