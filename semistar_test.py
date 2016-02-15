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


def star_property(k, perm, inv, neigh, n):
    i = inv[k]
    j = inv[(k+1)%n]
    val = lambda x : (x - perm[i]) % n
    q = val(max(neigh[i], key=val))
    p = val(min(neigh[j], key=val))
    r_lis = [val(r) for r in perm if p < val(r) and val(r) < n]
    s_lis = [val(s) for s in perm if 1 < val(s) and val(s) < q]
    rs_lines = []
    return "what"

def triple_intersection(n,p,q,r):
    from sympy import acos,sin,cos,pi,sqrt,simplify
    def simplify(a):
        return a
    def sub(v1,v2):
        return simplify(v1[0]-v2[0]), simplify(v1[1]-v2[1])
    def add(v1,v2):
        return simplify(v1[0]+v2[0]), simplify(v1[1]+v2[1])
    def dot(v1,v2):
        return simplify(v1[0]*v2[0] + v1[1]*v2[1])
    def scale(k,v):
        return simplify(k*v[0]), simplify(k*v[1])
    def length(v):
        return simplify(sqrt(v[0]**2 + v[1]**2))
    magnitude = simplify(sin((n-p)*pi/n) * 2 * sin(2*pi/n/2) / sin((p-q+1) * pi/n))
    unit_v = (simplify(-sin(q * pi / n)), simplify(cos(q * pi /n)))
    #print(1,unit_v)
    intersection = add((1,0),scale(magnitude,unit_v))
    #print(2,intersection[0], intersection[1])
    c0 = sub((1,0),intersection)
    #print(3,c0[0], c0[1])
    cr = sub((cos(r*2*pi/n), sin(r*2*pi/n)), intersection)
    #print(4,cr[0], cr[1])
    angle = simplify(acos(dot(c0,cr)/(length(c0)*length(cr))))
    #print(5,angle)
    return simplify(n - r + q - angle*n/pi)

def test_star_property(orig):
    n = len(orig)
    for i in range(n):
        val = lambda x : (x - i) % n
        perm = [val(x) for x in orig]
        neigh = [{perm[(i-1) % n], perm[(i+1) % n]} for i in range(n)]
        inv = inverse_0(perm)
        q = min(neigh[inv[0]])
        p = max(neigh[inv[1]])
        if not p > q:
            #print(i, "semistar")
            return False
        for r in range(p+1, n):
            sprime = float(triple_intersection(n,p,q,r))
            s_set = neigh[inv[r]]
            if not all(s >= sprime for s in s_set if s > 1):
                #print(i, "star", p,q,r,s_set,float(sprime))
                return False
    return True



if __name__ == "__main__":
    while 1:
        try:
            perm = get_csv_line()
        except:
            break
        if test_star_property(perm):
            print("yes", perm)
        else:
            print("no", perm)
