#!/usr/bin/env python3
import sys

class CyclicPermutationsHalfAvoidingNeighbours(object):
    def __init__(self, n):
        assert(0 <= n)
        self.n = n
    def __repr__(self):
        return "Instance of {} of length {}".format(self.__class__.__name__, self.n)
    def __str__(self):
        return self.__repr__()
    def __iter__(self):
        if self.n < 5:
            return
        def calculate_iter(ind, perm):
            res = list(range(0,self.n))
            for i,val in zip(range(0,ind),perm):
                res.remove(val)
            try:
                res.remove((perm[ind-1]-1) % self.n)
            except:
                pass
            try:
                res.remove((perm[ind-1]+1) % self.n)
            except: 
                pass
            return iter(res)
        perm = [0] * self.n
        iter_lis = [None] * self.n
        iter_lis[0] = iter([0])
        iter_lis[1] = iter(list(range(2, self.n//2 +1)))
        ind = 1
        while ind != 0:
            if iter_lis[ind] is None:
                iter_lis[ind] = calculate_iter(ind, perm)
            else:
                try:
                    tmp = iter_lis[ind].__next__()
                    perm[ind] = tmp
                    ind += 1
                    if ind == self.n:
                        yield perm
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
