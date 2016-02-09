#!/usr/bin/env python3
from unicursalpolygon.models.unicursalpolygon import UnicursalPolygon
from unicursalpolygon.utils import permutation_to_standard_0

if __name__ == "__main__":
    while 1:
        try:
            lis = [int(i) for i in input().split(',')]
            res = {True:[],False:[],None:[]}
            for i in range(len(lis)):
                tmp = list(lis)
                x = tmp.pop(i)
                to_check = permutation_to_standard_0(tmp)
                tmp = UnicursalPolygon(to_check)
                try:
                    res[tmp.is_star()].append(x)
                except:
                    res[None].append(x)
            print(lis,res[False],res[True])
        except EOFError:
            break

