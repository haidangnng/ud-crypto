from exponential import fast, fast_exp
from primility import millerrabin
from euclidean import euclidean, extendedeuclidean
import random
import hashlib


def generator(a, m):
    # we want to check if "a" is a generator "mod m" ("m" is prime)
    # not optimized, but works
    # much more faster: find the divisors of (m-1) and only
    # check a^(divisors). If any of them is 1 (except for the last) then
    # "a" is not a generator
    # test = [1, 2, 41, 82, 1333985652677110515343913989, 2667971305354221030687827978, 54693411759761531129100473549]

    powers = set([])
    for i in range(0, m):
        powers.add(fast_exp(a, i, m))
    if len(powers) == m - 1:
        return True
    else:
        return False


def DH(L):  # PROBLEM: this alg. simulates both parties
    first = int("1" + "0" * (L - 1))
    last = int("9" * L)
    # print(first,last)
    while True:
        r = random.randint(first, last)
        if millerrabin(r, 10):  # we are using OUR Miller-Rabin alg.
            p = r
            break
    # print(f"prime: {p}")
    x = random.randint(1, p - 1)
    y = random.randint(1, p - 1)
    while True:
        g = random.randint(1, p - 1)
        if generator(g, p):  # we are using OUR generator alg.
            break
    # print(f"generator: {g}")
    gx = fast(g, x, p)  # we are using OUR fast exp. alg.
    gy = fast(g, y, p)
    key = fast(g, x * y, p)
    return p, g, x, y, gx, gy, key


def half_DH(L):
    first = int("1" + "0" * (L - 1))
    last = int("9" * L)
    while True:
        r = random.randint(first, last)
        if millerrabin(r, 10):
            p = r
            break
    x = random.randint(1, p - 1)
    while True:
        g = random.randint(1, p - 1)
        if generator(g, p):
            break
    gx = fast(g, x, p)
    return p, g, x, gx


def keygen_DH(p, g, gx, secret=-1):
    if secret == -1:
        y = random.randint(1, p - 1)
    else:
        y = secret
    gy = fast(g, y, p)
    gxy = fast(gx, y, p)
    return y, gy, gxy


def ElGamal(text, dhinfo, encrypt):
    # dhinfo is the key + prime
    key = dhinfo[0]
    p = dhinfo[1]
    if encrypt:
        return (text * key) % p
    if not encrypt:
        inverse_key = extendedeuclidean(p, key)
        return (text * inverse_key) % p


def RSA(L, m):
    # generate two random primes of length L
    first = int("1" + "0" * (L - 1))
    last = int("9" * L)
    p = -1
    q = -1
    while True:
        r = random.randint(first, last)
        if millerrabin(r, 10) and p == -1:
            p = r
        elif millerrabin(r, 10) and q == -1:
            q = r
            break
    # print(p,q)
    n = p * q
    lam = (p - 1) * (q - 1)
    while True:
        e = random.randint(2, lam - 1)
        gcd, _ = euclidean(lam, e)
        if gcd == 1:
            break
    # print(p,q,e)
    d = extendedeuclidean(lam, e)
    c = fast(m, e, n)
    return p, q, n, lam, e, d, c


def RSA_decrypt(c, d, n):
    return fast(c, d, n)


def signature_create(m):
    h = hashlib.sha256()
    h.update(m.encode())
    hashed_message = int(h.hexdigest(), 16)
    # print(hashed_message)
    p, q, n, lam, e, d, _ = RSA(5, 123)  # 123 is just a placeholder
    enc_hash = RSA_decrypt(hashed_message, d, n)
    # print(enc_hash)
    return m, enc_hash, n, e


def signature_verify(m, enc_hash, n, e):
    h = RSA_decrypt(enc_hash, e, n)
    mh = hashlib.sha256()
    mh.update(m.encode())
    hashed_message = int(mh.hexdigest(), 16) % n
    print(h, hashed_message)
    if h == mh:
        return True
    else:
        return False


"""
SECURE COMMUNICATION CHANNEL:
1) X generates its part of the DH key
    GETS: nothing
    KEEPS: x
    SENDS: p, g, g^x
2) Y generates its part of the DH key and the key
    GETS: p, g, g^x
    KEEPS: y, g^(xy)
    SENDS: g^y
3) X generates the key
    GETS: g^y
    KEEPS: g^(xy)
    SENDS: nothing
4) X generates the encrypted message
    GETS: nothing
    KEEPS: m
    SENDS: key*m (mod p)
5) Y decrypts the encrypted message
    GETS: encrypted message
    KEEPS: m
    SENDS: nothing, return c2%m
"""


# print(euclidean(1002,23))
# print(millerrabin(101,10))

# print(generator(2,101))
# print(DH(4))

"""
print("-----FIRST STEP (X)-----")
p,g,x,gx = half_DH(5)
print(f"Sending p, g, g^x: {p}, {g}, {gx}")
print(f"Keeping x: {x}")
 
print("-----SECOND STEP (Y)-----")
y,gy,gxy = keygen_DH(p,g,gx)
print(f"Sending gy: {gy}")
print(f"Keeping y, g^xy (key/password): {y}, {gxy}")
 
print("-----THIRD STEP (X)-----")
_,_,gxy = keygen_DH(p,g,gy,x)
print(f"Sending nothing")
print(f"Keeping g^xy (key/password): {gxy}")
 
print("-----FOURTH STEP (X)-----")
m = 1234 # plaintext, readable message, e.g. "hello"
c = ElGamal(m,[gxy,p],True)
print(f"Sending encrypted message: {c}")
print(f"Keeping original message: {m}")
 
print("-----FIFTH STEP (Y)-----")
m = ElGamal(c,[gxy,p],False)
print(f"Sending nothing")
print(f"Keeping original message: {m}")
"""
# print(RSA(5,27))
# print(RSA_decrypt(814640110,450719399,2594608853))
# m, enc_hash, n, e = signature_create("some message")
# result = signature_verify("some message", enc_hash, n, e)
#
millerrabin(561, 1)
# print(millerrabin(101,10))
