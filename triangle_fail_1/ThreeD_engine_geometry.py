from ThreeD_engine_vector import VectorTwoD, VectorThreeD
from ThreeD_engine_point import PointTwoD, PointThreeD
from math import sqrt


def dot_product(vector_1, vector_2):  # u . v
    if vector_1.dimensions != vector_2.dimensions:
        raise ValueError("Dimensions number difference")
    return sum([x[0] * x[1] for x in list(zip(vector_1.coords, vector_2.coords))])


def cross_product(vector_1, vector_2):  # u x v
    if vector_1.dimensions != 3 or vector_2.dimensions != 3:
        raise ValueError("Dimensions number difference")
    coords_1 = vector_1.get_coords()
    coords_2 = vector_2.get_coords()
    return VectorThreeD(coords_1[1] * coords_2[2] - coords_1[2] * coords_2[1],
                        coords_1[2] * coords_2[0] - coords_1[0] * coords_2[2],
                        coords_1[0] * coords_2[1] - coords_1[1] * coords_2[0])


def sub_points(point_1, point_2):  # A - B
    if point_1.dimensions != point_2.dimensions:
        raise ValueError("Dimensions number difference")
    new_coords = list(zip(point_1.coords, point_2.coords))
    if point_1.dimensions == 2:
        return VectorTwoD(new_coords[0][0] - new_coords[0][1],
                          new_coords[1][0] - new_coords[1][1])
    elif point_1.dimensions == 3:
        return VectorThreeD(new_coords[0][0] - new_coords[0][1],
                            new_coords[1][0] - new_coords[1][1],
                            new_coords[2][0] - new_coords[2][1])


def add_sub_vectors(vector_1, vector_2, sign):  # u +- v
    if vector_1.dimensions != vector_2.dimensions:
        raise ValueError("Dimensions number difference")
    new_coords = list(zip(vector_2.coords, vector_1.coords))
    if vector_1.dimensions == 2:
        return VectorTwoD(new_coords[0][0] + (-1 if sign == "-" else 1) * new_coords[0][1],
                          new_coords[1][0] + (-1 if sign == "-" else 1) * new_coords[1][1])
    elif vector_1.dimensions == 3:
        return VectorThreeD(new_coords[0][0] + (-1 if sign == "-" else 1) * new_coords[0][1],
                            new_coords[1][0] + (-1 if sign == "-" else 1) * new_coords[1][1],
                            new_coords[2][0] + (-1 if sign == "-" else 1) * new_coords[2][1])


def two_points_distance(point_1, point_2):  # |AB|
    if point_1.dimensions != point_2.dimensions:
        raise ValueError("Dimensions number difference")
    coords_1 = point_1.get_coords()
    coords_2 = point_2.get_coords()
    inside = (coords_1[0] - coords_2[0]) ** 2 + (coords_1[1] - coords_2[1]) ** 2
    if point_1.dimensions == 3:
        inside += (coords_1[2] - coords_2[2]) ** 2
    return sqrt(inside)


def add_point_and_vector(point, vector):  # A + u
    if point.dimensions != vector.dimensions:
        raise ValueError("Dimensions number difference")
    new_coords = list(zip(point.coords, vector.coords))
    if point.dimensions == 2:
        return PointTwoD(sum(new_coords[0]), sum(new_coords[1]))
    elif point.dimensions == 3:
        return PointThreeD(sum(new_coords[0]), sum(new_coords[1]), sum(new_coords[2]))


def multiply_vector(const, vector):  # c . u
    coords = vector.get_coords()
    if vector.dimensions == 2:
        return VectorTwoD(coords[0] * const, coords[1] * const)
    elif vector.dimensions == 3:
        return VectorThreeD(coords[0] * const, coords[1] * const, coords[2] * const)


def repair_unit_vector(vector):
    return multiply_vector(1 / sqrt(sum([x ** 2 for x in vector.get_coords()])), vector)
