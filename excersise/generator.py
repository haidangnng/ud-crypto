from exponential import fast_exponential


def generator(a, m):
    powers = set([])
    for i in range(0, m):
        powers.add(fast_exponential(a, i, m))
    if len(powers) == m - 1:
        return True
    else:
        return False
