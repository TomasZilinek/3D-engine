# from ThreeD_engine_geometry import sub_points, two_points_distance, PointThreeD, add_point_and_vector, multiply_vector
from ThreeD_engine_geometry import multiply_vector
from ThreeD_engine_vector import VectorThreeD
from random import randint


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)


class Cube:
    def __init__(self, pygame, x, y, z, side_len, resolution, moving=True):
        self.pygame = pygame
        self.ThreeD_points = []
        self.pos = [x, y, z]
        self.side = side_len
        self.resolution = resolution
        self.moving = moving
        self.move_vect = VectorThreeD(randint(-10, 10) / 20, randint(-10, 10) / 20, randint(-10, 10) / 20)
        self.dist_moved = 0
        self.create_3d_points()
        # self.pygame.time.set_timer(pygame.USEREVENT + 1, 10)

    def create_3d_points(self):
        self.ThreeD_points = [
            [self.pos[0], self.pos[1] + self.side, self.pos[2] + self.side],
            [self.pos[0] + self.side, self.pos[1] + self.side, self.pos[2] + self.side],
            [self.pos[0] + self.side, self.pos[1], self.pos[2] + self.side],
            [self.pos[0], self.pos[1], self.pos[2] + self.side],
            [self.pos[0], self.pos[1] + self.side, self.pos[2]],
            [self.pos[0] + self.side, self.pos[1] + self.side, self.pos[2]],
            [self.pos[0] + self.side, self.pos[1], self.pos[2]],
            [self.pos[0], self.pos[1], self.pos[2]]
        ]

    def move(self, dt):
        if self.moving:
            vect_coords = self.move_vect.get_coords()
            for point in self.ThreeD_points:
                point[0] += vect_coords[0] * dt
                point[1] += vect_coords[1] * dt
                point[2] += vect_coords[2] * dt

            self.dist_moved += self.move_vect.get_size() * dt
            if self.dist_moved > 300:
                self.move_vect = multiply_vector(-1, self.move_vect)
                self.dist_moved = 0

    def get_rendered_points(self, camera):
        new_pts = []
        for point in self.ThreeD_points:
            rendered_point = camera.render_3d_point(point[0], point[1], point[2])
            if rendered_point:
                rendered_point = self.add_screen_params(rendered_point)
                new_pts.append([rendered_point[0], rendered_point[1]])
        return new_pts

    def add_screen_params(self, coords):
        return [coords[0] + self.resolution[0] / 2, coords[1] + self.resolution[1] / 2]

    def draw(self, screen, camera):
        new_pts = self.get_rendered_points(camera)
        try:
            # horny a dolny stvorec:
            self.pygame.draw.line(screen, BLACK, (new_pts[0][0], new_pts[0][1]), (new_pts[1][0], new_pts[1][1]), 2)
            self.pygame.draw.line(screen, BLACK, (new_pts[1][0], new_pts[1][1]), (new_pts[2][0], new_pts[2][1]), 2)
            self.pygame.draw.line(screen, BLACK, (new_pts[2][0], new_pts[2][1]), (new_pts[3][0], new_pts[3][1]), 2)
            self.pygame.draw.line(screen, BLACK, (new_pts[3][0], new_pts[3][1]), (new_pts[0][0], new_pts[0][1]), 2)

            self.pygame.draw.line(screen, GREEN, (new_pts[4][0], new_pts[4][1]), (new_pts[5][0], new_pts[5][1]), 2)
            self.pygame.draw.line(screen, GREEN, (new_pts[5][0], new_pts[5][1]), (new_pts[6][0], new_pts[6][1]), 2)
            self.pygame.draw.line(screen, GREEN, (new_pts[6][0], new_pts[6][1]), (new_pts[7][0], new_pts[7][1]), 2)
            self.pygame.draw.line(screen, GREEN, (new_pts[7][0], new_pts[7][1]), (new_pts[4][0], new_pts[4][1]), 2)

            # 4 zvisle steny
            self.pygame.draw.line(screen, RED, (new_pts[0][0], new_pts[0][1]), (new_pts[4][0], new_pts[4][1]), 2)
            self.pygame.draw.line(screen, RED, (new_pts[1][0], new_pts[1][1]), (new_pts[5][0], new_pts[5][1]), 2)
            self.pygame.draw.line(screen, RED, (new_pts[2][0], new_pts[2][1]), (new_pts[6][0], new_pts[6][1]), 2)
            self.pygame.draw.line(screen, RED, (new_pts[3][0], new_pts[3][1]), (new_pts[7][0], new_pts[7][1]), 2)
        except:
            pass


"""
class Triangle:
    def __init__(self, screen, pygame, resolution, p1, p2, p3, color):
        self.pointsThreeD = [p1, p2, p3]
        self.resolution = resolution
        self.color = color
        self.pygame = pygame
        self.screen = screen
        self.vectorsThreeD = [sub_points(p2, p1), sub_points(p3, p1)]
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

    def draw(self, camera):
        points2d = [camera.render_3d_point(p) for p in self.pointsThreeD]
        self.vectorsTwoD = [sub_points(points2d[1], points2d[0]), sub_points(points2d[2], points2d[0])]
        self.get_distances_and_draw(camera, points2d[0], points2d[1], [points2d[2]])

    def get_dist(self, camera, points2d, sc_x, sc_y):
        koefs = [0, 0]
        koefs[1] = (sc_x - points2d[0]) / \
                   ((points2d[2][0] - points2d[0][0]) *
                    (1 - points2d[1][0] * (points2d[0][1] - sc_y) - (points2d[2][1] - points2d[0][1]) *
                     (points2d[0][1] + points2d[1][0]) - points2d[0][1] * (sc_y - points2d[0][1])))
        koefs[0] = (sc_y - points2d[0][1] + koefs[1] * (points2d[2][1] - points2d[0][1])) / \
                   (points2d[1][1] - points2d[0][1])
        mi = add_point_and_vector(self.pointsThreeD[0],
                                  multiply_vector((two_points_distance(points2d[1], points2d[0]) /
                                                   koefs[0]), sub_points(self.pointsThreeD[1], self.pointsThreeD[0])))
        mi = add_point_and_vector(mi, multiply_vector((two_points_distance(points2d[2], points2d[0]) /
                                  koefs[1]), sub_points(self.pointsThreeD[2], self.pointsThreeD[0])))
        qi = camera.get_intersection_with_camera_plane(mi)
        return two_points_distance(mi, qi)


class Npolygon:
    def __init__(self, screen, pygame, camera, sides, resolution, threed_points, color):
        if len(sides) < 3:
            raise ValueError("Too few polygon sides (" + str(sides) + ")")
        self.pygame = pygame
        self.screen = screen
        self.camera = camera
        self.resolution = resolution
        self.threed_points = threed_points
        self.color = color
        self.triangles = []
        self.set_triangles()

    def set_triangles(self):
        last_point = self.threed_points[1]
        for count, point in enumerate(self.threed_points[2:]):
            self.triangles.append(Triangle(self.screen, self.pygame, self.resolution, self.threed_points[0], last_point,
                                           point, self.color))
            last_point = point

    def draw(self, camera):
        for triangle in self.triangles:
            triangle.draw(camera)
"""
