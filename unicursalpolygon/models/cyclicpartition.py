from unicursalpolygon.utils import minimum_isomorphic_partition

class CyclicPartition(object):
    def __init__(self, partition):
        self.partition = minimum_isomorphic_partition(partition)
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
