def __to_standard__(part):
    n = len(part)
    def complement(lis):
        return [n - i for i in lis]
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
    def __str__(self):
        return str(self.partition)
    def __repr__(self):
        return "Instance of {} of length {}: {}".format(self.__class__.__name__, self.n, self)
    def __hash__(self):
        res = 0
        for i,val in enumerate(reversed(self.partition)):
            res += val*self.n**i
        return res
    def __eq__(self,other):
        return self.partition == other.partition
    def __lt__(self, other):
        return self.__hash__() < other.__hash__()
    def __ge__(self, other):
        return not self < other
    def as_cyclic_permutation(self):
        lis = [0] * self.n
        tmp = 0
        for i,val in enumerate(self.partition[:-1], start=1):
            tmp = (tmp+val) % self.n
            lis[i] = tmp
        return tuple(lis)
