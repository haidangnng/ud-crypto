import string
from euclidean import extendedeuclidean

dict = {}
for index, value in enumerate(string.ascii_lowercase):
    dict[value] = index

dict[" "] = 26
dict["."] = 27
print(dict)


def ElGamal(text, dhinfo, encrypt):
    key = dhinfo[0]
    p = dhinfo[1]
    if encrypt:
        return (text * key) % p
    if not encrypt:
        inverse_key = extendedeuclidean(p, key)
        return (text * inverse_key) % p
