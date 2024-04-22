import pygame
from ThreeD_engine_camera import Camera
from ThreeD_engine_shape import Npolygon
from ctypes import windll


def mouse_motion(coords):
    if sum(coords) < 1000:
        x_angle = -coords[0] / ((resolution[0] / 2) / 60)
        y_angle = coords[1] / ((resolution[1] / 2) / 30)
        camera.mouse_move(-x_angle, -y_angle)
        draw_shapes()


def add_screen_params(coords):
    return [coords[0] + resolution[0] / 2, coords[1] + resolution[1] / 2]


def draw_shapes():
    for shape in shapes:
        camera.draw_shape(shape)

    axis = [add_screen_params(camera.render_3d_point(0, 0, 0)),  # origin
            add_screen_params(camera.render_3d_point(150, 0, 0)),
            add_screen_params(camera.render_3d_point(0, 150, 0)),
            add_screen_params(camera.render_3d_point(0, 0, 150))]

    # osi x, y, z
    try:
        pygame.draw.line(screen, red, (axis[0][0], axis[0][1]), (axis[1][0], axis[1][1]))  # x axis
        pygame.draw.line(screen, blue, (axis[0][0], axis[0][1]), (axis[2][0], axis[2][1]))  # y axis
        pygame.draw.line(screen, yellow, (axis[0][0], axis[0][1]), (axis[3][0], axis[3][1]))  # z axis
    except:
        pass


white = (255, 255, 255)
black = (0, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)
red = (255, 0, 0)
yellow = (255, 255, 0)
pygame.init()

windll.user32.SetProcessDPIAware()
resolution = (windll.user32.GetSystemMetrics(0), windll.user32.GetSystemMetrics(1))
screen = pygame.display.set_mode(resolution, pygame.FULLSCREEN)
screen.fill(white)
pygame.event.set_grab(True)
pygame.mouse.set_visible(False)
pygame.mouse.set_pos(int(resolution[0]), int(resolution[1]))

camera = Camera(resolution)
side = 5

points = [
    [0, side, side], [side, side, side], [side, 0, side], [0, 0, side],
    [0, side, 0], [side, side, 0], [side, 0, 0], [0, 0, 0]
]

shapes = [Npolygon(screen, pygame, camera, resolution, [[0, 0, 0], [0, side, 0], [side, side, 0], [side, 0, 0]], red)]
"""
shapes = [Npolygon(screen, pygame, camera, resolution, [[0, 0, 0], [0, side, 0], [side, side, 0], [side, 0, 0]], red),
          Npolygon(screen, pygame, camera, resolution, [[0, 0, 0], [side, 0, 0], [side, 0, side], [0, 0, side]], yellow),
          Npolygon(screen, pygame, camera, resolution, [[0, 0, 0], [0, side, 0], [0, side, side], [0, 0, side]], blue),
          Npolygon(screen, pygame, camera, resolution, [[0, side, 0], [side, side, 0], [side, side, side], [0, side, side]], yellow),
          Npolygon(screen, pygame, camera, resolution, [[0, 0, side], [side, 0, side], [side, side, side], [side, 0, side]], red),
          Npolygon(screen, pygame, camera, resolution, [[0, 0, side], [side, side, 0], [side, side, side], [side, 0, side]], blue)]
"""

used_keys = {pygame.K_w: "forward", pygame.K_a: "left", pygame.K_s: "backward", pygame.K_d: "right",
             pygame.K_KP2: "down", pygame.K_KP4: "left", pygame.K_KP6: "right", pygame.K_KP8: "up",
             pygame.K_KP_PLUS: "sp+", pygame.K_KP_MINUS: "sp-", pygame.K_e: "rot_right", pygame.K_q: "rot_left",
             pygame.K_LSHIFT: "down", pygame.K_SPACE: "up"}

pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 30)
textsurface = myfont.render('Press Esc to quit', False, (0, 0, 0))


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                quit()
        elif event.type == pygame.MOUSEMOTION:
            mouse_motion(pygame.mouse.get_rel())
    keys_pressed = pygame.key.get_pressed()
    for k, v in used_keys.items():
        if keys_pressed[k]:
            camera.move_direction(v)

    screen.fill(white)
    draw_shapes()
    screen.blit(textsurface, (resolution[0] * 0.85, resolution[1] * 0.95))
    pygame.display.update()
