bucket = {}

def add(i, u):
    if i not in bucket.keys():
        bucket[i] = 0
    bucket[i] += u