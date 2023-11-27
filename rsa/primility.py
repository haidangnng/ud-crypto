import random
from exponential import fast


def millerrabin(n, it):
    # calculating k and d
    d = n - 1
    k = 0
    while d % 2 != 1:
        d //= 2
        k += 1

    print(f"k: {k}")
    print(f"d:{d}")

    # doing "it" number of iterations (choosing these many random bases)
    for _ in range(0, it):
        x = random.randint(1, n - 1)
        # print(x)
        if (
            fast(x, n - 1, n) != 1
        ):  # calculating x^(n-1) mod n -> if it is not 1, n is not a prime
            return False
        # print(
        #     f"{n} PASSED the Fermat test with {x} :(, so we start with the Miller-Rabin part."
        # )
        x = fast(x, d, n)  # calculating x^d mod n
        print(f"x:{x}")
        for _ in range(1, k):  # repeatedly squaring k-1 times
            newx = fast(x, 2, n)  # squaring the number
            print(f"newx: {newx}, x: {x}, n: {n}")
            if newx == 1 and (  # newx = x^2
                x != 1 and x != n - 1
            ):  # if this new squared number is 1, but the old one is not 1 or -1 then n is not a prime
                # print(f"{n} is NOT a prime, since {x}^2 is 1, but {x} is not 1 or -1")
                return False
            x = newx  # otherwise we redefine x to be this new, squared number
        # print(f"{n} passed the Miller-Rabin test with {x}.")
    # print(f"{n} is {(1-0.25**it)*100} percent a prime")
    return True
