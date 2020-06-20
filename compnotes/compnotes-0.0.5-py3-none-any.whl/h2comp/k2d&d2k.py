def k2d(s, k):
    mapping = "0123456789ABCDEF"
    res = 0
    for i in range(len(s)):
        res += mapping.index(s[i]) * k ** (len(s)-1-i)
    return res

def d2k(d, k):
    mapping = "0123456789ABCDEF"
    res = ""
    while d != 0:
        res = mapping[d%k] + res
        d //= k
    return res

    
