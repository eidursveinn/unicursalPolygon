from unicursalpolygon.models.point import Point
class OuterBoundaryPoint(object):
    def __init__(self, theta, r):
        self.point = Point(theta=theta, r=r, accurate=True)
        self.next_inner = None
        self.prev_inner = None
