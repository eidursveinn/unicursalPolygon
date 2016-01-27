#!/usr/bin/env python3
import sys

def __to_standard__(part):
    n = len(part)
    def complement(lis):
        return [n - i for i in part]
    res = []
    to_check = [
            part * 2,
            complement(part) * 2,
            part[::-1] * 2,
            complement(part[::-1]) * 2
        ]
    for p in to_check:
        res.extend([p[i:i+n] for i in range(n)])
    return min(res)

def perm_to_partition(perm):
    n = len(perm)
    return CyclicPartition([(perm[(i+1) % n]-perm[i]) % n for i in range(n)])


class CyclicPartition(object):
    def __init__(self, partition):
        self.partition = __to_standard__(partition)
        self.n = len(partition)
    def __eq__(self,other):
        return self.partition == other.partition
    def __str__(self):
        return str(self.partition)
    def __repr__(self):
        return "Instance of {} of length {}: {}".format(self.__class__.__name__, self.n, self)
    def __hash__(self):
        res = 0
        for i,val in enumerate(reversed(self.partition)):
            res += val*self.n**i
        return res
    def as_cyclic_permutation(self):
        lis = [0] * self.n
        tmp = 0
        for i,val in enumerate(self.partition[:-1], start=1):
            tmp = (tmp+val) % self.n
            lis[i] = tmp
        return tuple(lis)

class PartitionsOfMultiplesOfLength(object):
    def __init__(self, n):
        assert(0 <= n)
        self.n = n
    def __repr__(self):
        return "Instance of {} of length {}".format(self.__class__.__name__, self.n)
    def __str__(self):
        return self.__repr__()

    def __iter__(self):
        def calc_iter(jumps, ind, sums):
            min_jump = jumps[0]
            if ind + 1 == self.n:
                tmp = self.n - (sums[0] % self.n)
                if tmp == self.n - 1 or tmp < min_jump:
                    return iter([])
                return iter([tmp])
            return iter([i for i in range(min_jump, self.n-1)
                    if all([(i+cur) % self.n for cur in sums[:ind+1]])
                ])
        if self.n < 1:
            return
        jumps = [0] * self.n
        iter_lis = [None] * self.n
        iter_lis[0] = iter(list(range(2,self.n//2 + 1)))
        ind = 0
        sums = [0] * self.n
        while ind != -1:
            if iter_lis[ind] is None:
                iter_lis[ind] = calc_iter(jumps, ind, sums)
            else:
                try:
                    tmp = next(iter_lis[ind])
                    for i in range(0,ind+1):
                        sums[i] -= jumps[ind]
                    jumps[ind] = tmp
                    for i in range(0,ind+1):
                        sums[i] += jumps[ind]
                    ind += 1
                    if ind == self.n:
                        #yield list(jumps), list(sums)
                        yield CyclicPartition(jumps)
                        ind -= 1
                except StopIteration:
                    iter_lis[ind] = None
                    for i in range(0,ind+1):
                        sums[i] -= jumps[ind]
                    jumps[ind] = 0
                    ind -= 1


def main(n):
    return list(PartitionsOfMultiplesOfLength(n))
    for i,lis in enumerate(PartitionsOfMultiplesOfLength(n)):
        print(i, lis)
        #print(lis, [(sum(lis[i:]) , s)  for i,s in enumerate(sums)])
def main2(n):
    return set(PartitionsOfMultiplesOfLength(n))
    for i,p in enumerate(set(PartitionsOfMultiplesOfLength(n))):
        print(i,p)

if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print("Provide one number as argument")
    else:
        main2(int(sys.argv[1]))
