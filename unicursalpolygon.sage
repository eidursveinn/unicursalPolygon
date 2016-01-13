class Line(object):
    def __init__(self, p1, p2):
        #self.intersections = []
        self.start = p1
        self.end = p2
        self.m, self.c = two_points_to_line(p1.point, p2.point) # does not work atm

    def intersects(self, other):
        #error handling
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
        intersections.sort(key=self.start.point.dist_from())
        if len(intersections) > 0:
            self.start.next_inner = intersections[0]
            self.end.prev_inner = intersections[-1]

class Point(object):
    def __init__(self, theta=None, r=None, x=None, y=None):
        if theta is not None and r is not None:
            self.theta = theta
            self.r = r
            self.x, self.y = polar_to_cartesian(theta, r)
        elif x is not None and y is not None:
            self.x = x
            self.y = y
            self.theta, self.r = cartesian_to_polar(x, y)
        else:
            print("Point arguments missing")
    def cartesian(self):
        return self.x, self.y
    def polar(self):
        return self.theta, self.r
    def dist_from(self):
        return lambda other: (self.x - other.x)**2 + (self.y - other.y)**2
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
        self.point = Point(theta=theta, r=r)
        self.next_inner = None
        self.prev_inner = None

class UnicursalPolygon(object):
    def __init__(self, perm):
        self.perm = perm
        self.n = len(perm)
        self.boundary_points = [OuterBoundaryPoint(i * 2*pi/self.n, 1) for i in xrange(self.n)]
        self.lines = [Line(self.boundary_points[perm[i]], self.boundary_points[perm[(i+1)%self.n]]) for i in xrange(self.n)]
        self.__calculate_boundary_points()
        self.star = None

    def __calculate_boundary_points(self):
        for line_i in xrange(self.n):
            lis = []
            line = self.lines[line_i]
            for line_j in xrange(self.n):
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



def polar_to_cartesian(theta,r):
    """
    Converts polar coordinates to cartesian coordinates.

    INPUT:

    - ``theta`` -- Angle in radians

    - ``r`` -- Distance from origin

    OUTPUT:

    Cartesian coordinates (x,y) equivalent to the given polar coordinates
    """
    x = N(r*cos(theta))
    y = N(r*sin(theta))
    return x,y

def cartesian_to_polar(x,y):
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
    if x == 0 and y == 0:
        return 0,0
    r = sqrt(x**2 + y**2)
    theta = 1/2*pi if x == 0 else arctan(y/x)
    if x == 0 and y < 0:
        theta += pi
    if x < 0:
        theta += pi
    elif x > 0 and y < 0:
        theta += 2*pi
    return N(theta), N(r)

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
    return [i*m % n for i in xrange(n)]
