# temporary wrapper allowing for N(None) to be None instead of zero
def N(number):
    if number is None:
        return None
    return float(number)

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

def minimum_isomorphic_partition(part):
    n = len(part)
    def complement(lis):
        return [n - i for i in lis]
    res = []
    to_check = [
            part * 2,
            complement(part) * 2,
            part[::-1] * 2,
            complement(part[::-1]) * 2
        ]
    for p in to_check:
        res.extend([p[i:i+n] for i in range(n)])
    return min(res)

def perm_to_partition(perm):
    from unicursalpolygon.models.cyclicpartition import CyclicPartition
    n = len(perm)
    return CyclicPartition([(perm[(i+1) % n]-perm[i]) % n for i in range(n)])


def get_csv_line(delim=','):
    return [int(i) for i in input().split(delim)]

def inverse_0(perm):
    tmp = [ (elem,i) for i,elem in enumerate(perm)]
    tmp.sort()
    return [b for a,b in tmp]

def schlafi_symbol(n,m):
    """
    Given the schlafi symbol for regular polygon {n/m} returns the permutation representing that polygon.

    INPUT:

    - ``n`` -- length of resulting permutation
    - ``m`` -- 

    OUTPUT:

    A list of length n where element i is i*m (mod n)
    """
    assert(gcd(n,m) == 1 and 2*m < n)
    return [i*m % n for i in range(n)]

def permutation_to_standard_0(lis):
    tmp = [(val,i) for i,val in enumerate(lis)]
    tmp = [(b[1],i) for i,b in enumerate(sorted(tmp))]
    tmp.sort()
    res = [val for _,val in tmp]
    return res

def permutation_to_oneline(x):
    return [x[(x.index(i) + 1) % len(x)] for i in range(len(x))]
