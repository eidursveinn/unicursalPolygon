#!/usr/bin/env python3
import unicursalpolygon
def main():
    while 1:
        try:
            line = input()
            lis = line.split(',')
            lis = [int(i) for i in lis]
            unicursalpolygon.UnicursalPolygon(lis).draw(save=True)
        except EOFError:
            pass

if __name__ == "__main__":
    main()
