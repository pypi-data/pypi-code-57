def bubbleSort(L):
    res = L[:]
    for i in range(len(L)-1):
        swap = False
        for j in range(len(L)-i-1):
            if res[j] > res[j+1]:
                res[j], res[j+1] = res[j+1], res[j]
                swap = True
        if not swap:
            break
    return res

def insertionSort(L):
    res = L[:]
    for i in range(1, len(L)):
        j = i
        while j >= 1 and res[j] < res[j-1]:
            res[j], res[j-1] = res[j-1], res[j]
            j -= 1
    return res

def quickSort(L):
    return quickSort([i for i in L[1:] if i < L[0]] + [L[0]]) + quickSort([i for i in L[1:] if i >= L[0]]) if len(L) >= 2 else L

def merge2(a,b):
    ret = []
    while len(a) and len(b):
        if a[0] < b[0]:
            ret.append(a[0])
            a.pop(0)
        else:
            ret.append(b[0])
            b.pop(0)
    # if len(a) == 0:
    #     ret += b
    # else:
    #     ret += a
    # return ret
    return ret + a + b

def mergeSort(l):
    return merge2(mergeSort(l[:len(l)//2]),mergeSort(l[len(l)//2:])) if len(l) >= 2 else l

print(bubbleSort([5,4,3,2,1]))
print(insertionSort([5,4,3,2,1]))
print(quickSort([5,4,3,2,1]))