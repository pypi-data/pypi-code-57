def partition(A, lb, rb):
    # qs lb to rb inclusive
    # print(f"Partition({A}, {lb}, {rb}) ---->  ", end="")
    if lb >= rb:
        # print("terminate")
        return -1
    else:
        pivot = A[lb]
        while True:
            #most left outta place
            for l in range(lb+1, rb+1):
                if A[l] > pivot:
                    break
            #most right outta place
            for r in range(rb, lb-1, -1):
                if A[r] <= pivot:
                    break
            if r > l:
                A[l], A[r] = A[r], A[l]
            else: 
                # print(A, r, l)
                break
        A[lb], A[r] = A[r], A[lb]
        # print(A, l, r)
        return r #the new pivot position


def helper(A, lb, rb):
    split = partition(A, lb, rb)
    # print(lb, rb, split)
    if split != -1:
        helper(A, lb, split-1)
        helper(A, split+1, rb)

def wrapper(A):
    helper(A, 0, len(A)-1)

x = [1,2,3,4,5,6,7]
import random
for _ in range(100):
    random.shuffle(x)
    wrapper(x)
    assert x == [1,2,3,4,5,6,7]

def iter_qs(A):
    stack = []
    stack.insert(0, (0, len(A)-1))
    while len(stack) != 0:
        lb, rb = stack.pop()
        split = partition(A, lb, rb)
        if split != -1:
            stack.insert(0, (lb, split-1))
            stack.insert(0, (split+1, rb))

for _ in range(100):
    random.shuffle(x)
    iter_qs(x)
    assert x == [1,2,3,4,5,6,7]

