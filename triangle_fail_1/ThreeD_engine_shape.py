from ThreeD_engine_geometry import sub_points, two_points_distance, PointThreeD, add_point_and_vector, multiply_vector,\
    PointTwoD


class Triangle:
    def __init__(self, screen, pygame, resolution, p1, p2, p3, color):
        self.pointsThreeD = [PointThreeD(*p) for p in [p1, p2, p3]]
        self.resolution = resolution
        self.color = color
        self.pygame = pygame
        self.screen = screen
        self.vectorsThreeD = [sub_points(PointThreeD(*p2), PointThreeD(p1[0], p1[1], p1[2])),
                              sub_points(PointThreeD(*p3), PointThreeD(p1[0], p1[1], p1[2]))]
        self.vectorsTwoD = []

    def get_distances_and_draw(self, camera, p1, p2, p3):
        upper = [0, 0]
        lower = [0, self.resolution[1]]
        points = [p1, p2, p3]
        for p in points:
            if p[1] > upper[1]:
                upper = p
            if p[1] < lower[1]:
                lower = p
        for p in points:
            if p != upper and p[1] == upper[1] or p != lower and p[1] == lower[1]:
                base = "up" if p != upper and p[1] == upper[1] else "down"
                left = p if p[0] < (upper[0] if base == "up" else lower[0]) else (upper if base == "up" else lower)
                right = (upper if base == "up" else lower) if p[0] < (upper[0] if base == "up" else lower[0]) else p
                edge = [x for x in points if x not in [left, right]][0]
                k1 = 0 if left[0] - edge[0] == 0 else 1 / ((left[1] - edge[1]) / (left[0] - edge[0]))
                k2 = 0 if right[0] - edge[0] == 0 else 1 / ((right[1] - edge[1]) / (right[0] - edge[0]))
                left_x = left[0] if base == "up" else edge[0]
                right_x = right[0] if base == "up" else edge[0]
                y = left[1] if base == "up" else edge[1]
                limit = (left[1] if base == "down" else edge[1])
                while y >= limit:
                    x_p = left_x
                    while x_p < right_x:
                        dist = self.get_dist(camera, [p1, p2, p3], int(x_p), int(y))
                        if dist < camera.dist_list[int(y)][int(x_p)]:
                            self.screen.set_at((int(x_p), int(y)), self.color)
                            camera.dist_list[int(y)][int(x_p)] = dist
                        x_p += 1
                    y -= 1
                    left_x -= k1
                    right_x -= k2
                return
        middle = [0, 0]
        for p in points:
            if p not in [upper, lower]:
                middle = p
                break
        int_p = [upper[0] + ((lower[0] - upper[0]) * (middle[1] - upper[1])) / (lower[1] - upper[1]), middle[1]]
        self.get_distances_and_draw(camera, upper, middle, int_p)
        self.get_distances_and_draw(camera, middle, int_p, lower)

    def add_screen_params(self, coords):
        return [coords[0] + self.resolution[0] / 2, coords[1] + self.resolution[1] / 2]

    def draw(self, camera):
        points2d = [self.add_screen_params(camera.render_3d_point(*p.get_coords())) for p in self.pointsThreeD]
        self.vectorsTwoD = [sub_points(PointTwoD(points2d[1][0], points2d[1][1]), PointTwoD(points2d[0][0], points2d[0][1])),
                            sub_points(PointTwoD(points2d[2][0], points2d[2][1]), PointTwoD(points2d[0][0], points2d[0][1]))]
        self.get_distances_and_draw(camera, points2d[0], points2d[1], points2d[2])

    def get_dist(self, camera, points2d, sc_x, sc_y):
        koefs = [0, 0]
        koef_1_men = ((points2d[2][0] - points2d[0][0]) *
                      (1 - points2d[1][0] * (points2d[0][1] - sc_y) - (points2d[2][1] - points2d[0][1]) *
                      (points2d[0][1] + points2d[1][0]) - points2d[0][1] * (sc_y - points2d[0][1])))
        if koef_1_men == 0:
            koef_1_men = 0.0000000001
        koefs[1] = (sc_x - points2d[0][0]) / koef_1_men
        koefs[0] = (sc_y - points2d[0][1] + koefs[1] * (points2d[2][1] - points2d[0][1])) / \
                   (0.0000000000001 if points2d[1][1] - points2d[0][1] == 0 else points2d[1][1] - points2d[0][1])
        points2d = [PointTwoD(p[0], p[1]) for p in points2d]
        mi = add_point_and_vector(self.pointsThreeD[0],
                                  multiply_vector((two_points_distance(points2d[1], points2d[0]) /
                                                   koefs[0]), sub_points(self.pointsThreeD[1], self.pointsThreeD[0])))
        mi = add_point_and_vector(mi, multiply_vector((two_points_distance(points2d[2], points2d[0]) /
                                  koefs[1]), sub_points(self.pointsThreeD[2], self.pointsThreeD[0])))
        qi = camera.get_intersection_with_camera_plane(mi.get_coords())
        return two_points_distance(mi, qi)


class Npolygon:
    def __init__(self, screen, pygame, camera, resolution, threed_points, color):
        if len(threed_points) < 3:
            raise ValueError("Too few polygon sides (" + str(len(threed_points)) + ")")
        self.pygame = pygame
        self.screen = screen
        self.camera = camera
        self.resolution = resolution
        self.three_d_points = threed_points
        self.color = color
        self.triangles = []
        self.set_triangles()

    def set_triangles(self):
        last_point = self.three_d_points[1]
        for count, point in enumerate(self.three_d_points[2:]):
            self.triangles.append(Triangle(self.screen, self.pygame, self.resolution, self.three_d_points[0][:],
                                           last_point[:], point[:], self.color))
            last_point = point[:]

    def draw(self, camera):
        for triangle in self.triangles:
            triangle.draw(camera)
