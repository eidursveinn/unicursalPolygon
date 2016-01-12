# overloads the estimate function to symplify symbolic expressions
#def N(_): return _ if _ is None else _.simplify_full()

def generate_arm_points(n):
    """
    Return `n` polar coordinates with equal distance on the unit circle.

    INPUT:

    - ``n`` -- non-negative integer

    OUTPUT:

    A list of length n of polar-coordinates evenly spaced on the unit circle
    """
    return [(i * 2*pi/n, 1) for i in xrange(n)]

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
    r = sqrt(x**2 + y**2)
    theta = 0 if x == 0 else arctan(y/x)
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
    x1,y1 = p1
    x2,y2 = p2
    if x1 == x2:
        return None, x1
    m = (y2-y1)/(x2-x1)
    c = -m*x1+y1
    return m,c

def slope_order(origin):
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
    return lambda x: x if x < origin else x - 2*pi

def estimate_equality(a,b):
    return False

def boundary_points(perm, return_lines=False):
    """
    Given a permutation represented as a list of indicies,
    return coordinates of the boundary of a unicursal polygon.

    METHOD:

    The unicursal polygon is drawn in the following way.
    We start with n evenly spaced points on the unit circle numbered 0 to n-1
    in slope order. Then a line is drawn from the 1st to the 2nd point of the
    permutation 2nd to 3rd and so on and finally from the last point to the 1st
    the boundary of these lines form a polygon and the boundary points of that
    polygon is returned.

    INPUT:

    - ``perm`` - a list of integers of length n where each integer
      {0, 1, ...,  n-1} appears exactly once.

    OUTPUT:

    A list of cartesian points (2-tuples) that make the boundary of the polygon


    USAGE:

    The following displays a 5-armed regular star polygon {5/2}

    ::

        sage: points = boundary_points([0,2,4,1,3])
        sage: polygon(points).show(axes=False)

    TODO:

    A lot
    """
    n = len(perm)
    outer_polar = generate_arm_points(n)
    outer_cartesian = [polar_to_cartesian(a,b) for a,b in outer_polar]
    lines = [two_points_to_line(outer_cartesian[perm[i]], outer_cartesian[perm[(i+1)%n]]) for i in range(n)]
    if return_lines:
        x = var('x')
        res = []
        for m,c in lines:
            if m != None:
                res.append(m*x + c)
        return res
    inner_polar = []
    res = []
    res.extend(outer_polar)
    for line_i in range(len(lines)):
        lis = []
        m1, c1 = lines[line_i]
        for line_j in range(len(lines)):
            m2, c2 = lines[line_j]
            if line_i == line_j \
                or line_i == (line_j + 1) % n \
                or line_i == (line_j - 1) % n \
                or (m1 is not None and m2 is not None and m1 - m2 == 0):
                continue
            # calculate intersections
            if m1 == None:
                x = c1
                y = m2*x + c2
            elif m2 == None:
                x = c2
                y = m1*x + c1
            else:
                #if m1 - m2 == 0: continue
                x = (c1-c2)/(m2-m1)
                y = m1*x + c1
            lis.append((x, y))
        polar_lis = [cartesian_to_polar(*cart) for cart in lis]
        # float r is bad, and not needed
        polar_lis = [(theta, r) for theta,r in polar_lis if r < 1]
        #what if no intersection or just one
        if len(polar_lis) == 0: continue

        order = slope_order(outer_polar[perm[line_i]][0])
        polar_lis.sort(key=lambda x: order(x[0]))
        inner_polar.append(polar_lis[0])
        inner_polar.append(polar_lis[-1])
    res.extend(list(set(inner_polar)))
    res.sort()
    return [polar_to_cartesian(a,b) for a,b in res]
