#!/usr/bin/env python3
import itertools
class bivincular_pattern(object):
    def __init__(self,perm, adj_val, adj_perm):
        self.perm = tuple(perm)
        self.adj_val = adj_val
        self.adj_perm = adj_perm
        self.n = len(perm)
    def latex(self):
        res = "\\begin{matrix}"
        for a,b in self.adj_val:
            res += "\\cmidrule[.5pt](rl){{{}-{}}}".format(a,b)
        res += "&".join((str(i) for i in range(1,self.n+1)))
        res += "\\\\"
        res += "&".join((str(i) for i in self.perm))
        res += "\\\\[-3pt]"
        for a,b in self.adj_perm:
            res += "\\cmidrule[.5pt](rl){{{}-{}}}".format(a,b)
        res += "\\end{matrix}"
        return res
        
def neighbour_avoidance():
    res = [
        bivincular_pattern((1,2),[(1,2)],[(1,2)]),
        bivincular_pattern((2,1),[(1,2)],[(1,2)]),
    ]
    return res


def no_intersection_in_circle():
    # (a 1 a'==b' 2 b)
    # (a 1 a' ... b 2 b')
    # where min(a,a') >= max(b, b')
    res = []
    for p in itertools.permutations(range(3,6)):
        if p[0] > p[2]:
            patt = (p[0], 1, p[1], 2, p[2])
            adj_val = [(1,2)]
            adj_perm = [(1,5)]
            res.append(bivincular_pattern(patt, adj_val, adj_perm))
    for p in itertools.permutations(range(3,7)):
        if min(p[0:2]) >= max(p[2:4]):
            patt = (p[0], 1, p[1], p[2], 2, p[3])
            adj_val = [(1,2)]
            adj_perm = [(1,3),(4,6)]
            res.append(bivincular_pattern(patt, adj_val, adj_perm))
    #rotations?
    return res

def nova_property_break():
    # (a 1 a' ... b 2 b' ... c d)
    # where a < a'
    #       b > b'
    #       a < b
    #       2 < c < a
    #       b < d 
    res = []
    for p in itertools.permutations(range(3,9)):
        a = min(p[0:2])
        b = max(p[2:4])
        c = p[4]
        d = p[5]
        if a < b and c < a and b < d:
            patt = (p[0], 1, p[1], p[2], 2, p[3], p[4], p[5])
            adj_val = [(1,2)]
            adj_perm = [(1,3), (4,6), (7,9)]
            tmp = bivincular_pattern(patt, adj_val, adj_perm)
            res.append(tmp)
    return res
    

if __name__ == '__main__':
    for f in neighbour_avoidance, no_intersection_in_circle, nova_property_break:
        for patt in f():
            print(patt.latex())
