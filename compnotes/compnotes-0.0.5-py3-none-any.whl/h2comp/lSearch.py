def lSearch(l, t):
    for i in range(len(l)):
        if l[i] == t:
            return i
    return -1