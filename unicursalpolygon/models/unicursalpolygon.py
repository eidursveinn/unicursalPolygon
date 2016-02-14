#!/usr/bin/env python3
from unicursalpolygon.models.point import Point
from unicursalpolygon.models.boundarypoint import OuterBoundaryPoint
from unicursalpolygon.models.line import Line
from sympy import pi
from unicursalpolygon.utils import N

class UnicursalPolygon(object):
    def __init__(self, perm, jumps=False):
        # perm and jumps
        if jumps:
            jump_list = [0]
            for jump in perm[:-1]:
                jump_list.append((jump_list[-1] + jump) % len(perm))
            self.perm = jump_list
        else:
            self.perm = perm
        self.n = len(perm)
        self.boundary_points = [OuterBoundaryPoint(i * 2*pi/self.n, 1) for i in range(self.n)]
        self.lines = [Line(self.boundary_points[perm[i]], self.boundary_points[perm[(i+1)%self.n]]) for i in range(self.n)]
        for point in self.boundary_points:
            point.point.x = N(point.point.x)
            point.point.y = N(point.point.y)
            point.point.theta = N(point.point.theta)
            point.point.r = N(point.point.r)
        for line in self.lines:
            line.m = N(line.m)
            line.c = N(line.c)
        self.__calculate_boundary_points()
        self.star = None
        self.skip_list = [(self.perm[(i+1) % self.n]-self.perm[i]) % self.n for i in range(self.n)]

    def __calculate_boundary_points(self):
        for line_i in range(self.n):
            lis = []
            line = self.lines[line_i]
            for line_j in range(self.n):
                other = self.lines[line_j]
                if line_i == line_j \
                    or line_i == (line_j + 1) % self.n \
                    or line_i == (line_j - 1) % self.n \
                    or (line.m is not None and other.m is not None and line.m - other.m == 0):
                    continue
                lis.append(other)
            line.assign_innerpoints(lis)

    def generate_isomorphs(self):
        permSet = set()
        fun = lambda x: [(len(x)-i)%len(x) for i in x]
        for i in range(len(self.perm)):
            currPerm = self.perm[i:] + self.perm[:i]
            for j in range(len(self.perm)):
                curr = tuple([(curr+j) % len(self.perm) for curr in currPerm])
                permSet.add(curr)
                permSet.add(curr[::-1])
        for i in range(len(self.perm)):
            currPerm = fun(self.perm)[i:]+fun(self.perm)[:i]
            for j in range(len(self.perm)):
                curr = tuple([(curr+j) % len(self.perm) for curr in currPerm])
                permSet.add(curr)
                permSet.add(curr[::-1])
        return permSet

    def points(self):
        res = []
        for p in self.boundary_points:
            key = p.prev_inner.slope_order()
            if key(p.next_inner) >= pi:
                p.prev_inner, p.next_inner = p.next_inner, p.prev_inner
            if p.prev_inner is not None: res.append(p.prev_inner)
            if p.point is not None: res.append(p.point)
            if p.next_inner is not None: res.append(p.next_inner)
        return [p.cartesian() for p in res]

    def is_star(self):
        # call the function to order the points and fix next/prev
        self.points()
        #boundary_points = copy.deepcopy(self.boundary_points)
        for i in range(self.n-1):
            if not self.boundary_points[i].next_inner.equals(self.boundary_points[i+1].prev_inner, n=self.n):
                #print("error in point nr:",i, self.boundary_points[i].next_inner.cartesian(), self.boundary_points[i+1].prev_inner.cartesian())
                return False
        # special case for last and first point
        if not self.boundary_points[self.n-1].next_inner.equals(self.boundary_points[0].prev_inner, n=self.n):
            return False
        return True

    def draw(self,save=False,arrows=True):
        import matplotlib.pyplot as pl
        x = []
        y = []
        for num in self.perm:
            x1,y1 = self.boundary_points[num].point.cartesian()
            x.append(x1)
            y.append(y1)
        x.append(x[0])
        y.append(y[0])
        # different colors, maybe implement this later
        #for i in range(len(x)-1):
        #    pl.plot([x[i],x[i+1]],[y[i],y[i+1]],color=(i/len(x),0,1))
        if arrows:
            for i in range(len(x)-1):
                pl.quiver(x[i], y[i], x[i+1]-x[i], y[i+1]-y[i], scale_units='xy', angles='xy', scale=1,width=0.0012,headwidth=8,headlength=15)
        else:
            pl.plot(x,y)
        pl.axis([-1,1,-1,1])
        pl.title(str(self.perm) + '\n' + str(self.skip_list))
        if save:
            pl.savefig(str(self.perm)+".svg")
        else:
            pl.show()
        pl.close()
