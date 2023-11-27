def fast_exponential(b, e, m):
    r = 1
    b = b % m
    while e:
        if e & 1:
            r = (r * b) % m
        b = (b**2) % m
        e = e >> 1
    return r
