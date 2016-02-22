#!/usr/bin/env python3
from unicursalpolygon.models.unicursalpolygon import UnicursalPolygon
from unicursalpolygon.models.cyclicpartition import CyclicPartition
from unicursalpolygon.utils import permutation_to_standard_0, perm_to_partition
import semistar_test

graph = {}

def add_node(perm):
    n = len(perm)
    if n < 4:
        return None
    partition = perm_to_partition(perm)
    star = semistar_test.classify_permutation(perm)
    if not partition in graph:
        # adjacent permutations
        d = {}
        for i in range(len(perm)):
            tmp = list(perm)
            x = tmp.pop(i)
            to_check = permutation_to_standard_0(tmp)
            child = add_node(to_check)
            if child is not None:
                if child not in d:
                    d[child] = []
                d[child].append(x)
        graph[partition] = (star, d)
    return partition


n = 0
#also this
while 1:
    try:
        perm = [int(i) for i in input().split(',')]
    except EOFError:
        break
    n = max(n, len(perm))
    add_node(perm)


def print_recursive(node, removed, starclass, adjacent, indent=0):
    space = " " * (indent * 4)
    print(space, starclass, node.as_cyclic_permutation(), removed)
    for key in adjacent:
        part = key
        print_recursive(part, adjacent[key], graph[part][0], graph[part][1], indent=indent+1)

for key in graph:
    if key.n == n:
        print_recursive(key, [], graph[key][0], graph[key][1])
