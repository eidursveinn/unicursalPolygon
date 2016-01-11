def generate_arm_points(n):
    return [(i * 2*pi/n, 1) for i in range(n)]

def polar_to_cartesian(theta,r):
    return (r*cos(theta), r*sin(theta))

def cartesian_to_polar(x,y):
    r = sqrt(x**2 + y**2)
    theta = 0 if x == 0 else arctan(y/x)
    if x < 0:
        theta += pi
    elif x > 0 and y < 0:
        theta += 2*pi #probably redundant
    return theta, r

# returns a tuple, first number is the slope, second is the starting point
# if slope is vertical we return None, x
def two_points_to_line(p1,p2):
    x1,y1 = p1
    x2,y2 = p2
    if x1 == x2:
        return None, x1
    m = (y2-y1)/(x2-x1)
    c = -m*x1+y1
    return m,c

# returns
def boundary_points(perm):
    n = len(perm)
    outer_polar = generate_arm_points(n)
    outer_cartesian = [polar_to_cartesian(a,b) for a,b in outer_polar]
    lines = [two_points_to_line(outer_cartesian[perm[i]], outer_cartesian[perm[(i+1)%n]]) for i in range(n)]
    inner_polar = []
    res = []
    res.extend(outer_polar)
    for l1 in lines:
        lis = []
        m1, c1 = l1
        for l2 in lines:
            m2, c2 = l2
            if l1 == l2 or m1 == m2:
                continue
            # calculate intersections
            if m1 == None:
                x = c1
                y = m2*x + c2
            elif m2 == None:
                x = c2
                y = m1*x + c1
            else:
                if m1 - m2 == 0: continue
                x = (c1-c2)/(m2-m1)
                y = m1*x + c1
            lis.append((x, y))
        polar_lis = [cartesian_to_polar(*cart) for cart in lis]
        # float r is bad, and not needed
        polar_lis = [(theta, r) for theta,r in polar_lis if r < 1]
        #what if no intersection or just one
        if len(polar_lis) == 0: continue
        polar_lis.sort()
        inner_polar.append(polar_lis[0])
        inner_polar.append(polar_lis[-1])
    res.extend(list(set(inner_polar)))
    res.sort()
    return [polar_to_cartesian(a,b) for a,b in res]

res = boundary_points([0,2,4,1,3])
res = [(float(a),float(b)) for a,b in res]
print("whoohoo", len(res), res)
p = polygon(res)
# wow what a beauty
