from unicursalpolygon.models.unicursalpolygon import UnicursalPolygon
from unicursalpolygon.models.cyclicpartition import CyclicPartition
import remove_point

graph = {}

def add_node(perm):
    n = len(perm)
    if n < 4:
        return None
    polygon = UnicursalPolygon(perm)
    partition = CyclicPartition(polygon.skip_list)
    try:
        star = polygon.is_star()
    except:
        star = None
    if not partition in graph:
        d = {}
        for i in range(len(perm)):
            tmp = list(perm)
            x = tmp.pop(i)
            to_check = remove_point.standardize(tmp)
            child = add_node(to_check)
            if child is not None:
                d[x] = child
        graph[partition] = (star, d)
    return partition


#also this
while 1:
    try:
        perm = [int(i) for i in input().split(',')]
    except EOFError:
        break
    add_node(perm)

for key in graph:
    print(key,graph[key])
