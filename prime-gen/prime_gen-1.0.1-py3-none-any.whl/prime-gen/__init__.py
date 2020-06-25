from math import *
p=lambda x:True if x in g(x)else False
def g(m):
    l=[]
    for i in range(2,m+1):
        q=True
        for j in l:
            if i==floor(sqrt(j)):
                break
            elif not i%j:
                q=False
                break
        l+=[i]if q else[]
    return l
