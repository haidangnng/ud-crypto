# Fast exponentiation
def fast(b, e, m):
    e = bin(e)[2:]
    result = 1
    for i in e:
        if i == "1":
            result = (b * (result**2)) % m
        else:
            result = (result**2) % m
    return result


def fast_exp(b, e, m):
    r = 1
    b = b % m
    while e:
        if e & 1:
            r = (r * b) % m
        b = (b**2) % m
        e = e >> 1

    return r
