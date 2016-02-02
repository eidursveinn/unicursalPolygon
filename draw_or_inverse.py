#!/usr/bin/env python3
from unicursalpolygon.models.unicursalpolygon import UnicursalPolygon

def inverse_0(perm):
    tmp = [ (elem,i) for i,elem in enumerate(perm)]
    tmp.sort()
    return [b for a,b in tmp]

def main():
    drawing = False;
    starLis = []
    while 1:
        if drawing:
            try:
                line = input()
                lis = line.split(',')
                lis = [int(i) for i in lis]
                UnicursalPolygon(lis).draw(save=True)
            except EOFError:
                break
        else:
            try:
                line = input()
                lis = line.split(',')
                lis = [int(i) for i in lis]
                a = UnicursalPolygon(lis)
                b = UnicursalPolygon(inverse_0(lis))
                try:
                    tmp = a.is_star()
                    tmp2 = b.is_star()
                except:
                    print("b failed is_star()," + str(b.perm))
                    continue
                if tmp and tmp2:
                    print("star: {} inverses into a star {}".format(str(lis),str(b.perm)))
                    starLis.append(a)
                    starLis.append(b)
                elif tmp:
                    print("star: {} does not inverse into a star {}".format(str(lis),str(b.perm)))
                elif tmp2:
                    print("non-star: {} inverses into a star {}".format(str(lis),str(b.perm)))
                else:
                    print(str(lis) + " neither are stars: " + str(unicursalpolygon.inverse_0(lis)))
            except EOFError:
                break

    for perm in starLis:
        perm.draw()
if __name__ == "__main__":
    main()
