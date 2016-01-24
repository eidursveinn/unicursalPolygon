#!/usr/bin/env python3
import sys
def arst(perm,i):
    offset = perm[i]
    n = len(perm)
    res = [(perm[(i+j) % n] - offset) % n  for j in range(n)]
    if res[1] > n//2:
        res = [-i % n for i in res]
    return res
class UniqueCyclicPermutation(object):
    def __init__(self, p):
        self.perm = p
        self.n = len(p)
        self.alike = [ arst(self.perm,i) for i in range(self.n) ]
        self.alike2 = [ arst(self.perm[::-1],i) for i in range(self.n) ]
    def equals(self,p):
        return p in self.alike or p in self.alike2

class UniqueCyclicPermutationsHalfAvoidingNeighbours(object):
    def __init__(self, n):
        assert(0 <= n)
        self.n = n
        self.gen = CyclicPermutationsHalfAvoidingNeighbours(self.n)
    def __iter__(self):
        results = []
        for perm in self.gen:
            for r in results:
                if r.equals(perm):
                    break
            else:
                results.append(UniqueCyclicPermutation(perm))
        for r in results:
            yield list(r.perm)
        return


class CyclicPermutationsHalfAvoidingNeighbours(object):
    def __init__(self, n, optimization=True):
        assert(0 <= n)
        self.n = n
        self.optimization = optimization
    def __repr__(self):
        return "Instance of {} of length {}".format(self.__class__.__name__, self.n)
    def __str__(self):
        return self.__repr__()
    def __iter__(self):
        if self.n < 5:
            return
        def safe_remove(lis,val):
            try:
                lis.remove(val)
            except ValueError:
                pass

        def calculate_iter(ind, perm):
            res = list(range(1,self.n))
            for val in perm[1:ind]:
                res.remove(val)
            safe_remove(res,(perm[ind-1]-1)%self.n)
            safe_remove(res,(perm[ind-1]+1)%self.n)
            if ind + 1 == self.n:
                safe_remove(res, (perm[0] + 1) % self.n)
                safe_remove(res, (perm[0] - 1) % self.n)

            return iter(res)
        perm = [0] * self.n
        iter_lis = [None] * self.n
        iter_lis[0] = iter([0])
        if self.optimization:
            iter_lis[1] = iter(list(range(2, self.n//2 +1)))

        ind = 1
        while ind != 0:
            if iter_lis[ind] is None:
                iter_lis[ind] = calculate_iter(ind, perm)
            else:
                try:
                    tmp = iter_lis[ind].__next__() # python3
                    #tmp = iter_lis[ind].next() # python2/sage
                    perm[ind] = tmp
                    ind += 1
                    if ind == self.n:
                        yield list(perm)
                        ind -= 1
                except StopIteration:
                    iter_lis[ind] = None
                    ind -= 1
def main(n):
    for p in CyclicPermutationsHalfAvoidingNeighbours(n):
        print(p)

if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print("Provide one number as argument")
    else:
        main(int(sys.argv[1]))
