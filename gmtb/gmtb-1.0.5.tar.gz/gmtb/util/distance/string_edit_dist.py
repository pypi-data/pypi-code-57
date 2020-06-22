import numpy as np
import editdistance


# compute table and pointer matrix
def string_edit_table(s1, s2):
    m = len(s1) + 1
    n = len(s2) + 1

    # init
    tbl = np.zeros((m, n))
    for i in range(m): tbl[i, 0] = i
    for j in range(n): tbl[0, j] = j

    # fill table
    for i in range(1, m):
        for j in range(1, n):
            cost = 0 if s1[i - 1] == s2[j - 1] else 1
            tbl[i, j] = min(tbl[i    , j - 1] + 1,
                            tbl[i - 1, j    ] + 1,
                            tbl[i - 1, j - 1] + cost)

    return tbl


# computes the partition distance between two clusterings
def string_edit_dist(s1, s2):
    return editdistance.eval(s1,s2)
    #return string_edit_table(s1, s2)[len(s1), len(s2)]


# computes the weighted mean between two strings
def string_edit_wm(s1, s2, alpha):
    tbl = string_edit_table(s1, s2)

    # go backwards for pointers
    step_list = []

    i = len(s1)
    j = len(s2)

    distance = tbl[i, j]

    while i > 0 and j > 0:
        if tbl[i, j] == tbl[i, j - 1] + 1:  # ins
            step_list.append("ins")
            j = j - 1
        elif tbl[i, j] == tbl[i - 1, j] + 1:  # del
            step_list.append("del")
            i = i - 1
        else:   # sub
            step_list.append("sub")
            j = j - 1
            i = i - 1

    while i > 0:
        step_list.append("del")
        i = i - 1

    while j > 0:
        step_list.append("ins")
        j = j - 1

    # go through list for actions
    num_steps = round(alpha*distance)
    wm_string = ""
    s = 0
    i = 0
    j = 0
    while s < num_steps:
        step = step_list.pop()

        if step == "ins":        # ins
            wm_string = wm_string + s2[j]
            j = j + 1
            s = s + 1
        elif step == "del":      #
            i = i + 1
            s = s + 1
        else:                    # sub
            wm_string = wm_string + s2[j]
            if s1[i] != s2[j]:
                s = s + 1
            i = i + 1
            j = j + 1

    if i < len(s1):
        wm_string = wm_string + s1[i:len(s1)]

    return wm_string



# test for sting wm
if __name__ == '__main__':
    print(string_edit_wm("BBAABB", "AA", 1))