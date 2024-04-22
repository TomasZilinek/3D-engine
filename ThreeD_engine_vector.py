

class VectorTwoD:
    def __init__(self, x, y):
        self.dimensions = 2
        self.coords = [x, y]
        self.size = 0
        self.calculate_size()
        self.size_calculated = False

    def get_coords(self):
        return [x for x in self.coords]

    def calculate_size(self):
        self.size = (sum([x ** 2 for x in self.coords])) ** (1 / 2)
        self.size_calculated = True

    def get_size(self):
        if not self.size_calculated:
            self.calculate_size()
        return self.size

    def set_coords(self, *args):
        if len(args) != self.dimensions:
            raise ValueError("New coordinates number does not match the vector's dimensions")
        self.coords = [arg for arg in args]
        self.size_calculated = False

    def make_unit_vector(self):
        k = 1 / abs(sum([c ** 2 for c in self.coords]))
        self.coords = [k * c for c in self.coords]
        self.size = 1
        self.size_calculated = True


class VectorThreeD(VectorTwoD):
    def __init__(self, x, y, z):
        VectorTwoD.__init__(self, x, y)
        self.coords.append(z)
        self.dimensions = 3
