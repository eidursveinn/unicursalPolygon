#!/usr/bin/env python3
from unicursalpolygon.utils import get_csv_line, inverse_0

def semistar_property(k, perm, inv, neigh, n):
    i = inv[k]
    j = inv[(k+1)%n]
    val = lambda x : (x - perm[i]) % n
    intersection = neigh[i].intersection(neigh[j])
    if len(intersection) == 0:
        a = val(min(neigh[i], key=val))
        b = val(max(neigh[j], key=val))
        return a < b
    elif len(intersection) == 1:
        a = val(neigh[i].difference(intersection).pop())
        b = val(neigh[j].difference(intersection).pop())
        common = val(intersection.pop())
        return not ((a > common) and (b < common))
    else:
        assert("SIZE OF INTERSECTION IS NOT 0/1" == 0)

def test_semistar_property(perm):
    n = len(perm)
    inv = inverse_0(perm)
    neigh = [{perm[(i-1) % n], perm[(i+1) % n]} for i in range(n)]
    return all(semistar_property(i, perm, inv, neigh, n) for i in range(n))

while 1:
    try:
        perm = get_csv_line()
    except:
        break
    if test_semistar_property(perm):
        print("yes", perm)
    else:
        print("no", perm)
