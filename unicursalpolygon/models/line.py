from unicursalpolygon.models.point import Point
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
