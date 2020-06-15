import numpy as np
import pathlib

def find_index(data,base=0,kind="-2+"):
    a = np.where(data > base, 1, 0)
    if kind == "-2+":
        a1 = np.where(np.diff(a) == 1)[0]
    elif kind == "+2-":
        a1 = np.where(np.diff(a) == -1)[0]
    else:
        a2 = np.where(np.diff(a) == 1)[0]
        a3 = np.where(np.diff(a) == -1)[0]
        a1 = np.hstack([a2,a3])
        a1.sort()
    return a1

def find_vertex_index(data,kind):
    a = np.diff(data)
    a = np.where(a > 0, 1, 0)
    if kind == "downward_convex":
        a1 = np.where(np.diff(a) == 1)[0]
    elif kind == "upward_convex":
        a1 = np.where(np.diff(a) == -1)[0]
    else:
        a2 = np.where(np.diff(a) == 1)[0]
        a3 = np.where(np.diff(a) == -1)[0]
        a1 = np.hstack([a2,a3])
        a1.sort()
    return a1 + 1

def memory_usage():
    import sys
    print("{}{: >25}{}{: >10}{}".format('|','Variable Name','|','Memory','|'))
    print(" ------------------------------------ ")
    for var_name in dir():
        if not var_name.startswith("_"):
            print("{}{: >25}{}{: >10}{}".format('|',var_name,'|',sys.getsizeof(eval(var_name)),'|'))

def ggdir():
    return pathlib.Path.home() /"GoogleDrive"