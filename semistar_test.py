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

def triple_intersection(n,p,q,r):
    #assert(n > r)
    #assert(r > p)
    #assert(p > q)
    from sympy import acos,sin,cos,pi,sqrt,simplify,trigsimp,cancel
    # simplify is slow
    def simplify(a):
        return a
        return cancel(trigsimp(a))
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
    # 0q and 1p will intersect in c
    # length of 0c
    magnitude = simplify(sin((n-p)*pi/n) * 2 * sin(2*pi/n/2) / sin((p-q+1) * pi/n))
    # angle of oc of length 1
    unit_v = (simplify(-sin(q * pi / n)), simplify(cos(q * pi /n)))
    # the point/vector c is [1,0] + magnitude*unit_v
    intersection = add((1,0),scale(magnitude,unit_v))
    # then we can find c0 vector
    c0 = sub((1,0),intersection)
    # and cr vector
    cr = sub((cos(r*2*pi/n), sin(r*2*pi/n)), intersection)
    # the angle between c0 and cr
    theta = simplify(acos(dot(c0,cr)/(length(c0)*length(cr))))
    # Now the arc r0 and s'q create a interior angle theta
    # satisfying (r0 + s'q)/2 = theta
    # or (n-r+q-s') * pi /n = theta
    # so s' = -theta * n/pi + n -r + q
    # this s' can be compared to s, if s is less than s' then rs intersects 0c1
    return n - r + q - theta*n/pi

def test_star_property(orig):
    from sympy import S
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
            sprime = triple_intersection(n,p,q,r)
            #print(sprime)
            s_set = neigh[inv[r]]
            if any(0 < sprime - S(s) and s > 1 for s in s_set):
                #print(i, "star", p,q,r,s_set,float(sprime))
                return False
    return True


def embeddingless_star(orig):
    res = 1
    reslis = []
    n = len(orig)
    for i in range(n):
        val = lambda x : (x - i) % n
        invval = lambda x : (x + i) % n
        perm = [val(x) for x in orig]
        neigh = [{perm[(i-1) % n], perm[(i+1) % n]} for i in range(n)]
        inv = inverse_0(perm)
        q = min(neigh[inv[0]])
        p = max(neigh[inv[1]])
        if not p > q:
            #print(i, "semistar")
            return False
        if n-p-1 > 0 and q-2 > 0:
            reslis.append(i)
            res = 2
        for r in range(p+1, n):
            lis = [s for s in neigh[inv[r]] if 1 < s and s < q]
            if len(lis):
                #print("O:{} I:{} p:{} q:{} r:{} s:{}".format(i, i+1, invval(p), invval(q), invval(r), [invval(_) for _ in lis]))
                return False
    return res

from enum import IntEnum
class Star(IntEnum):
    nothing = 0
    neighbour_avoidance = 1
    semistar = 2
    star = 3
    nova = 4

def avoid_neigh(perm):
    n = len(perm)
    return all((perm[i] + 1) % n != perm[(i+1) % n] and (perm[i] - 1) % n != perm[(i+1)%n] for i in range(n))

def classify_permutation(perm):
    from unicursalpolygon.models.unicursalpolygon import UnicursalPolygon
    if not avoid_neigh(perm):
        return Star.nothing
    elif not test_semistar_property(perm):
        return Star.neighbour_avoidance
    elif embeddingless_star(perm):
        return Star.nova
    elif UnicursalPolygon(perm).is_star():
        return Star.star
    else:
        return Star.semistar

if __name__ == "__main__":
    while 1:
        try:
            perm = get_csv_line()
        except:
            break
        starclass = classify_permutation(perm)
        s = ",".join(str(p) for p in perm)
        print(starclass, s)
