from collections import OrderedDict


class A(OrderedDict):

    def __init__(self, t1, t2):
        self.t1 = t1
        self.t2 = t2
        self['blah'] = 10
        self['blah2'] = 2

    def copy(self):
        result = OrderedDict()
        for k, v in self.items():
            result[k] = v
        return result


class B(dict):

    def __init__(self, t1, t2):
        self.t1 = t1
        self.t2 = t2
        self['blah'] = 10
        self['blah2'] = 2


aa = A(1, 2)
bb = B(1, 2)
import ipdb; ipdb.set_trace()
print(aa)
print(bb)
aa2 = aa.copy()
