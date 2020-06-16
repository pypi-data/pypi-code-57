from pycrunch.insights import trace


def test_trace_dict_variable():
    a = 2
    b = 3
    x = a + b
    trace(some_dictionary=dict(a=a, b=b, sum=x))
    trace(can_trace_a_lot=True)












