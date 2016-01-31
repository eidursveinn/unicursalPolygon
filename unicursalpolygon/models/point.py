from sympy import *
#from unicursalpolygon.models.unicursalpolygon import N

class Point(object):
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
