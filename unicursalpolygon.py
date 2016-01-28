#!/usr/bin/env python3
from generator import CyclicPermutationsHalfAvoidingNeighbours
from generator import UniqueCyclicPermutationsHalfAvoidingNeighbours
from partition_generator import PartitionsOfMultiplesOfLength
from sympy import *
import sys
import os.path

# temporary wrapper allowing for N(None) to be None instead of zero
def N(number):
    if number is None:
        return None
    return float(number)

class Line(object):
    def __init__(self, p1, p2):
        #self.intersections = []
        self.start = p1
        self.end = p2
        self.m, self.c = two_points_to_line(p1.point, p2.point)

    def intersects(self, other):
        if self.m == other.m:
            return None
        if self.m == None:
            x = self.c
            y = other.m*x + other.c
        elif other.m == None:
            x = other.c
            y = self.m*x + self.c
        else:
            x = (self.c-other.c)/(other.m-self.m)
            y = self.m*x + self.c
        return Point(x=x, y=y)

    def assign_innerpoints(self, lines):
        intersections = []
        for line in lines:
            res = self.intersects(line)
            if res is not None and res.r < 1:
                intersections.append(res)
        intersections.sort(key=self.start.point.dist_from_squared())
        if len(intersections) > 0:
            self.start.next_inner = intersections[0]
            self.end.prev_inner = intersections[-1]

class Point(object):
    '''
    wow
    '''
    def __init__(self, theta=None, r=None, x=None, y=None, accurate=False):
        # is ok.
        self.min_dist = lambda n : float(2 * sin(pi/n) * sin(pi/n) * tan(pi/(2*n)))
        if theta is not None and r is not None:
            self.theta = theta
            self.r = r
            self.x, self.y = polar_to_cartesian(theta, r, accurate=accurate)
        elif x is not None and y is not None:
            self.x = x
            self.y = y
            self.theta, self.r = cartesian_to_polar(x, y, accurate=accurate)
        # these are fucked
        elif x is not None and r is not None:
            self.x = x
            self.r = r
            self.y = sqrt(r**2 - x**2)
            self.theta,_ = cartesian_to_polar(self.x,self.y)
        elif y is not None and r is not None:
            self.y = y
            self.r = r
            self.x = sqrt(r**2 - y**2)
            self.theta,_ = cartesian_to_polar(self.x,self.y)
        # these are very fucked
        elif x is not None and theta is not None:
            raise ValueError("x,theta not ready")
            self.x = x
            self.theta = theta
            self.r = x / cos(theta) if cos(theta) != 0 else x
            self.y = sqrt(r**2 - x**2)
        elif y is not None and theta is not None:
            raise ValueError("y,theta not ready")
        else:
            raise ValueError("Point arguments missing, provide at least two")
    def cartesian(self):
        return self.x, self.y
    def polar(self):
        return self.theta, self.r
    def dist_from_squared(self):
        return lambda other: (self.x - other.x)**2 + (self.y - other.y)**2
    def equals(self, other, n=None):
        dist_from_squared = self.dist_from_squared()
        # we choose 1e-6 for the time being since it should work for at least the first few stars we get
        if n is not None:
            return dist_from_squared(other) < self.min_dist(n) ** 2
        else:
            return dist_from_squared(other) < 1e-12
    def slope_order(self):
        def fun(P):
            norm = P.theta - self.theta
            if norm < 0:
                return norm + 2*pi
            return norm
        """
        Returns a key function to sort angles.

        INPUT:

        - ``origin`` -- starting angle

        USAGE:

        Sorting a list of angles from some origin other than 0.

        EXAMPLES:

        Sorting in slope order from angle 1/4*pi.

        ::

            sage: lis = [0, 1/8*pi, 1/4*pi, 1/2*pi, pi]
            sage: lis.sort(key=slope_order(1/4*pi))
            sage: lis
            [1/4*pi, 1/2*pi, pi, 0, 1/8*pi]

        TODO:

        Currently the returned function will only work as expected if input is in
        the range [0, 2*pi[.
        """
        return lambda P: P.theta - self.theta + 2*pi if P.theta < self.theta else P.theta - self.theta

class OuterBoundaryPoint(object):
    def __init__(self, theta, r):
        self.point = Point(theta=theta, r=r, accurate=True)
        self.next_inner = None
        self.prev_inner = None

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


def mp_work(c):
    if UnicursalPolygon(c).is_star():
        return c, True
    else:
        return c, False
def generate_stars_multiprocessing(n, optimization=True, progress_bar=False):
    import multiprocessing as mp
    gen = list(CyclicPermutationsHalfAvoidingNeighbours(n, optimization=optimization))
    pool = mp.Pool()
    tmp = pool.map(mp_work, gen)
    stars = []
    other = []
    error = []
    for a,b in tmp:
        if b:
            stars.append(a)
        else:
            other.append(a)
    return stars, other, error
def generate_stars(n, optimization=1, progress_bar=False):
    stars = []
    errors = []
    polygons = []
    if optimization <= 1:
        gen = CyclicPermutationsHalfAvoidingNeighbours(n, optimization=optimization)
    else:
        gen = (p.as_cyclic_permutation() for p in set(PartitionsOfMultiplesOfLength(n)))
    if progress_bar:
        import time
        start_time = time.time()
        print("Calculating list for progress bar", end='\r')
        gen = list(gen)
        total = len(gen)
    for i,c in enumerate(gen, start=1):
        if progress_bar:
            ratio = i/total
            percent = 100.0 * ratio
            if i % 10 == 1:
                delta = time.time() - start_time
                time_left = 0 if not ratio else (1-ratio)/ratio * delta
                num = int(ratio*60)
                bar = '[' + '#'*num + ' '*(60-num) + ']'
            print("  {:04.1f}% {} {}/{} in {:0.2f}s estimated {:0.2f} left".format(percent, bar, i, total, delta, time_left), end='\r')
        try:
            if UnicursalPolygon(c).is_star():
                stars.append(c)
            else:
                polygons.append(c)
        except KeyboardInterrupt:
            raise
        except:
            print("Unexpected error:", sys.exc_info())
            errors.append(c)
    if progress_bar:
        print()
    return stars,polygons,errors
            
def draw_stars(lis):
    for star in lis:
        UnicursalPolygon(star).draw()


def polar_to_cartesian(theta,r,accurate=False):
    """
    Converts polar coordinates to cartesian coordinates.

    INPUT:

    - ``theta`` -- Angle in radians

    - ``r`` -- Distance from origin

    OUTPUT:

    Cartesian coordinates (x,y) equivalent to the given polar coordinates
    """
    if accurate:
        x = r*cos(theta)
        y = r*sin(theta)
    else:
        x = N(r*cos(theta))
        y = N(r*sin(theta))
    return x,y

def cartesian_to_polar(x,y, accurate=False):
    """
    Converts cartesian coordinates to polar coordinates.

    INPUT:

    - ``x`` -- Distance from origin on horizontal axis

    - ``y`` -- Distance from origin on vertical axis

    OUTPUT:

    Polar coordinates (angle,distance) equivalent
    to the given cartesian coordinates.

    Angle will be in radians on the range [0, 2*pi[
    and radius will be non-negative.
    Furthermore the cartesian origin (0,0) will return (0,0)
    even though (angle,0) for any angle would be equivalent.
    """
    # origin
    if x == 0 and y == 0:
        return 0,0
    r = sqrt(x**2 + y**2)
    theta = atan2(y,x)
    while theta < 0:
        theta += 2*pi
    return (theta, r) if accurate else (N(theta), N(r))

def two_points_to_line(p1,p2):
    """
    Given two  cartesian points, the function returns a tuple (m,c)
    which are the constants for the slope-intercept form y = mx + c.

    INPUT:

    - ``p1,p2`` -- 2-tuples (x,y) which is a cartesian point.

    OUTPUT:

    A 2-tuple (m,c) where m is the slope of the line through p1,p2 and c
    is the y-axis intercept.

    If the line is vertical the function will return (None, x) where x is the x-axis intercept.
    """
    if p1.x == p2.x:
        return None, p1.x
    m = (p2.y-p1.y)/(p2.x-p1.x)
    c = -m*p1.x+p1.y
    return m,c

def schlafi_symbol(n,m):
    return [i*m % n for i in range(n)]

def inverse_0(perm):
    tmp = [ (elem,i) for i,elem in enumerate(perm)]
    tmp.sort()
    return [b for a,b in tmp]


def to_file(arg,n, stdout=True):
    import csv
    filenames = ["stars","other","error"]
    for fname, perm_lis in zip(filenames, arg):
        if stdout:
            print(fname, len(perm_lis))
            f = sys.stdout
        else:
            f = open("{fname}_{num:02d}.csv".format(num=n,fname=fname), "w")
        writer = csv.writer(f)
        if len(perm_lis):
            writer.writerows(perm_lis)
        if not stdout:
            f.close()

def main():
    import argparse
    parser = argparse.ArgumentParser('')
    parser.add_argument("-o", "--output-dir", metavar='DIR', help="When provided info will be written to file instead of stdout")
    parser.add_argument("-q", "--quiet", help="Suppress all output", action="store_const", const=True)
    parser.add_argument("-v", "--verbose", help="Place holder for debugging information", action="count")
    parser.add_argument("-p", "--progress-bar", help="!", action="store_const", const=True)
    parser.add_argument("-m", "--multiprocessing", help="After a list of permutations has been generated all cores are utilized", action="store_const", const=True)
    parser.add_argument("permutation_length", help="Length of permutations to check")
    parser.add_argument("-O", "--optimization-level", metavar='N', help="Optimization level", default='2', type=int)

    args = parser.parse_args()
    exit = False

    if args.quiet:
        sys.stdout = open("/dev/null", "a")
        sys.stderr = open("/dev/null", "a")

    if args.output_dir is not None:
        if os.path.isdir(args.output_dir):
            os.chdir(args.output_dir)
            to_screen = False
        else:
            print("Directory '{}' does not exist".format(args.output_dir))
            exit = True
    else:
        to_screen = True

    if args.multiprocessing:
        star_gen = generate_stars_multiprocessing
    else:
        star_gen = generate_stars

    if not exit:
        n = int(args.permutation_length)
        results = star_gen(n, optimization=args.optimization_level, progress_bar=args.progress_bar)
        to_file(results, n, stdout=to_screen)
    else:
        parser.print_help()
        sys.exit(0)

if __name__ == "__main__":
    main()
