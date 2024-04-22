from math import sqrt


class VectorTwoD:
    def __init__(self, x, y):
        self.dimensions = 2
        self.coords = [x, y]
        self.size = 0
        self.calculate_size()

    def get_coords(self):
        return [x for x in self.coords]

    def calculate_size(self):
        self.size = sqrt(sum([x ** 2 for x in self.coords]))

    def get_size(self):
        self.calculate_size()
        return self.size

    def put_params(self, *args):
        if len(args) != self.dimensions:
            raise ValueError("Dimensions number difference")
        self.coords = [arg for arg in args]
        self.calculate_size()


class VectorThreeD(VectorTwoD):
    def __init__(self, x, y, z):
        VectorTwoD.__init__(self, x, y)
        self.coords.append(z)
        self.dimensions = 3
