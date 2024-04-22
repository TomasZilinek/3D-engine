from ThreeD_engine_geometry import *
from ThreeD_engine_vector import VectorThreeD
from ThreeD_engine_point import PointThreeD
from math import acos, degrees, cos, radians, sin


class Camera:
    def __init__(self, resolution):
        self.position_point = PointThreeD(200, 30, 30)
        self.x_axis_vector = VectorThreeD(0, -1, 0)
        self.y_axis_vector = VectorThreeD(0, 0, 1)
        self.pointing_vector = cross_product(self.x_axis_vector, self.y_axis_vector)
        self.d_parameter = 0
        self.calc_d_param()
        self.intersection_point = 0
        self.speed = 1
        self.rot_angle = 0.5
        self.zoom_const = 1250
        self.dist_list = [[0 for _ in range(resolution[0])] for _ in range(resolution[1])]

    def render_3d_point(self, x, y, z):
        self.intersection_point = self.get_intersection_with_camera_plane([x, y, z])
        w_vector = sub_points(self.intersection_point, self.position_point)
        denominator = w_vector.get_size()
        if denominator == 0:
            return [0, 0]
        angle = degrees(acos(dot_product(self.x_axis_vector, w_vector) / denominator))
        check_point_coords = add_point_and_vector(self.position_point, cross_product(self.x_axis_vector, w_vector)).get_coords()
        check_koef = self.get_line_koef(check_point_coords[0], check_point_coords[1], check_point_coords[2])
        if check_koef < 0:
            angle *= -1
        denominator = two_points_distance(self.intersection_point, PointThreeD(x, y, z)) / self.zoom_const
        if denominator == 0:
            return [0, 0]
        radius = two_points_distance(self.position_point, self.intersection_point) / denominator
        return [radius * cos(radians(angle)), radius * sin(radians(angle))]

    def get_intersection_with_camera_plane(self, point):
        p_vect_coords = self.pointing_vector.get_coords()
        line_koef = self.get_line_koef(point[0], point[1], point[2])
        return PointThreeD(point[0] + line_koef * p_vect_coords[0],
                           point[1] + line_koef * p_vect_coords[1],
                           point[2] + line_koef * p_vect_coords[2])

    def get_line_koef(self, x, y, z):  # x, y, z -> coordinates of rendered point
        p_vect_coords = self.pointing_vector.get_coords()
        return -((self.d_parameter + p_vect_coords[0] * x + p_vect_coords[1] * y + p_vect_coords[2] * z) /
                 (p_vect_coords[0] ** 2 + p_vect_coords[1] ** 2 + p_vect_coords[2] ** 2))

    def calc_d_param(self):
        p_vect_coords = self.pointing_vector.get_coords()
        coords = self.position_point.get_coords()
        self.d_parameter = -(p_vect_coords[0] * coords[0] +
                             p_vect_coords[1] * coords[1] +
                             p_vect_coords[2] * coords[2])

    def move_direction(self, direction):
        if direction == "up":
            self.position_point = add_point_and_vector(self.position_point, multiply_vector(self.speed, self.y_axis_vector))
        elif direction == "down":
            self.position_point = add_point_and_vector(self.position_point, multiply_vector(-self.speed, self.y_axis_vector))
        elif direction == "right":
            self.position_point = add_point_and_vector(self.position_point, multiply_vector(self.speed, self.x_axis_vector))
        elif direction == "left":
            self.position_point = add_point_and_vector(self.position_point, multiply_vector(-self.speed, self.x_axis_vector))
        elif direction == "forward":
            self.position_point = add_point_and_vector(self.position_point, multiply_vector(self.speed, self.pointing_vector))
        elif direction == "backward":
            self.position_point = add_point_and_vector(self.position_point, multiply_vector(-self.speed, self.pointing_vector))
        elif direction == "sp+":
            self.speed *= 1.1
        elif direction == "sp-":
            self.speed *= 0.9
        elif direction in ["rot_left", "rot_right"]:
            self.rotate(direction[4:])
        self.calc_d_param()

    def rotate(self, direction):
        if direction == "left":
            buffer = add_sub_vectors(multiply_vector(cos(radians(self.rot_angle)), self.x_axis_vector),
                                     multiply_vector(sin(radians(self.rot_angle)), self.y_axis_vector), "+")
            self.y_axis_vector = add_sub_vectors(multiply_vector(cos(radians(90 + self.rot_angle)), self.x_axis_vector),
                                                 multiply_vector(sin(radians(90 + self.rot_angle)), self.y_axis_vector),
                                                 "+")
            self.x_axis_vector.put_params(buffer.get_coords()[0], buffer.get_coords()[1], buffer.get_coords()[2])
        else:
            buffer = add_sub_vectors(multiply_vector(cos(radians(self.rot_angle)), self.x_axis_vector),
                                     multiply_vector(-sin(radians(self.rot_angle)), self.y_axis_vector), "+")
            self.y_axis_vector = add_sub_vectors(multiply_vector(cos(radians(90 - self.rot_angle)), self.x_axis_vector),
                                                 multiply_vector(sin(radians(90 - self.rot_angle)), self.y_axis_vector),
                                                 "+")
            self.x_axis_vector.put_params(buffer.get_coords()[0], buffer.get_coords()[1], buffer.get_coords()[2])
        self.x_axis_vector = repair_unit_vector(self.x_axis_vector)
        self.y_axis_vector = repair_unit_vector(self.y_axis_vector)
        self.calc_d_param()

    def mouse_move(self, x_angle, y_angle):
        if x_angle:
            self.x_axis_vector = add_sub_vectors(multiply_vector(-sin(radians(x_angle)), self.pointing_vector),
                                                 multiply_vector(cos(radians(x_angle)), self.x_axis_vector), "+")
        if y_angle:
            self.y_axis_vector = add_sub_vectors(multiply_vector(-sin(radians(y_angle)), self.pointing_vector),
                                                 multiply_vector(cos(radians(y_angle)), self.y_axis_vector), "+")
        self.pointing_vector = cross_product(self.x_axis_vector, self.y_axis_vector)
        self.calc_d_param()

    def draw_shape(self, shape):
        shape.draw(self)

    def get_dist_from_2d_screen_point(self, x, y):
        pass

    def get_real_intersection_point(self):
        return self.intersection_point
