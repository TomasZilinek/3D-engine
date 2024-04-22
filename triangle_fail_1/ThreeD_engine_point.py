class PointTwoD:
    def __init__(self, x, y):
        self.coords = [x, y]
        self.dimensions = 2

    def get_coords(self):
        return [x for x in self.coords]

    def put_coords(self, *args):
        if len(args) > self.dimensions:
            raise ValueError("Dimension number difference")
        self.coords = [arg for arg in args]


class PointThreeD(PointTwoD):
    def __init__(self, x, y, z):
        PointTwoD.__init__(self, x, y)
        self.coords.append(z)
        self.dimensions = 3
