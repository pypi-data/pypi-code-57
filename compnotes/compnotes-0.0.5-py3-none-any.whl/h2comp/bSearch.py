def bSearch(l, t):
    """ l must be sorted """
    s = 0
    e = len(l) - 1
    while s <= e:
        m = (s+e)//2
        if l[m] == t:
            return m
        elif l[m] > t:
            e = m-1
        else:
            s = s+1
    return -1

def bs_dupl(L, t):
    start, end = 0, len(L)-1
    while start <= end:
        mid = (start+end)//2
        if L[mid] >= t:
            end = mid-1
        else:
            start = mid+1
    lb = start
    #to find the right bound, if <=, ans can be to the right.
    start, end = 0, len(L)-1
    while start <= end:
        mid = (start+end)//2
        if L[mid] <= t:
            start = mid+1
        else:
            end = mid-1
    rb = end
    return lb, rb


for i in range(1,7):
    print(bs_dupl([1,1,1,2,2,3,3,4,4,4,4,5,5,6], i))