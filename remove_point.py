#!/usr/bin/env python3
from unicursalpolygon.models.unicursalpolygon import UnicursalPolygon

def standardize(lis):
    tmp = [(val,i) for i,val in enumerate(lis)]
    tmp = [(b[1],i) for i,b in enumerate(sorted(tmp))]
    tmp.sort()
    res = [val for _,val in tmp]
    return res

if __name__ == "__main__":
    while 1:
        try:
            lis = [int(i) for i in input().split(',')]
            res = {True:[],False:[],None:[]}
            for i in range(len(lis)):
                tmp = list(lis)
                x = tmp.pop(i)
                to_check = standardize(tmp)
                tmp = UnicursalPolygon(to_check)
                try:
                    res[tmp.is_star()].append(x)
                except:
                    res[None].append(x)
            print(lis,res[True])
        except EOFError:
            break

