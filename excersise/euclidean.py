def euclidean(a: int, b: int):
    r = -1  # this will be the residue
    coeff = []
    while r != 0:
        # print(f"{a}={a//b}*{b}+{a%b}")
        coeff.append(a // b)
        r = a % b  # new residue is simply "a mod b"
        a = b
        b = r
    coeff = coeff[0:-1]
    return a, coeff


# inverse calculation, calculates x^-1 mod m
def extendedeuclidean(m: int, x: int) -> int:
    gcd, coeff = euclidean(m, x)
    if gcd != 1:
        print(f"{x} has no inverse mod {m}, since gcd({x},{m})={gcd}")
        return False
    c1 = 1
    last = -1
    c2 = (-1) * coeff[last]
    while True:
        prev_c1 = c1
        prev_c2 = c2
        c1 = prev_c2
        last = last - 1
        c2 = prev_c1 + prev_c2 * (-1) * coeff[last]
        # print(f"c1={c1}, c2={c2}")
        if last == len(coeff) * (-1):
            break
    return c2 % m
