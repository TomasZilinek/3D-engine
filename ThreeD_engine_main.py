import pygame
from ctypes import windll
from ThreeD_engine_camera import Camera
from ThreeD_engine_shape import Cube


def mouse_motion(coords):
    if sum(coords) < 1000:
        screen.fill(WHITE)
        x_angle = -coords[0] / ((resolution[0] / 2) / 60)
        y_angle = coords[1] / ((resolution[1] / 2) / 30)
        camera.mouse_move(-x_angle, -y_angle)
        draw_axis(0, 0, 0, 100)


def add_screen_params(coords):
    return [coords[0] + resolution[0] / 2, coords[1] + resolution[1] / 2]


def draw_axis(x, y, z, size):
    axis = [add_screen_params(camera.render_3d_point(x, y, z)),  # origin
            add_screen_params(camera.render_3d_point(x + size, y, z)),
            add_screen_params(camera.render_3d_point(x, y + size, z)),
            add_screen_params(camera.render_3d_point(x, y, z + size))]

    try:
        pygame.draw.line(screen, RED, (axis[0][0], axis[0][1]), (axis[1][0], axis[1][1]), 2)  # x axis
        pygame.draw.line(screen, BLUE, (axis[0][0], axis[0][1]), (axis[2][0], axis[2][1]), 2)  # y axis
        pygame.draw.line(screen, YELLOW, (axis[0][0], axis[0][1]), (axis[3][0], axis[3][1]), 2)  # z axis
    except:
        pass


def update(delta_time):
    screen.fill(WHITE)
    draw_axis(0, 0, 0, 500)
    for c in cubes:
        camera.draw_shape(c, screen)
    screen.blit(textsurface1, (resolution[0] * 0.85, resolution[1] * 0.95))
    screen.blit(textsurface2, (resolution[0] * 0.01, resolution[1] * 0.02))
    pygame.display.update()


# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

pygame.init()
windll.user32.SetProcessDPIAware()
resolution = (windll.user32.GetSystemMetrics(0), windll.user32.GetSystemMetrics(1))
screen = pygame.display.set_mode(resolution, pygame.FULLSCREEN)
screen.fill(WHITE)
pygame.event.set_grab(True)
pygame.mouse.set_visible(False)
pygame.mouse.set_pos(int(resolution[0]), int(resolution[1]))

camera = Camera(resolution, 1000, 0, 200)
used_keys = {pygame.K_w: "forward", pygame.K_a: "left", pygame.K_s: "backward", pygame.K_d: "right",
             pygame.K_KP2: "down", pygame.K_KP4: "left", pygame.K_KP6: "right", pygame.K_KP8: "up",
             pygame.K_KP_PLUS: "sp+", pygame.K_KP_MINUS: "sp-", pygame.K_e: "rot_right", pygame.K_q: "rot_left",
             pygame.K_LSHIFT: "down", pygame.K_SPACE: "up"}

pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 30)
textsurface1 = myfont.render('Press Esc to quit', False, (0, 0, 0))
textsurface2 = myfont.render('Controls: W, A, S, D, Shift, Space, Q, E, +, -, Esc, Mouse', False, (0, 0, 0))

cubes = list()
cubes.append(Cube(pygame, 20, 20, 20, 150, resolution))
# cubes.append(Cube(pygame, -20, -80, -70, 50, resolution))
clock = pygame.time.Clock()

while True:
    dt = clock.tick(60)
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
        elif event.type == pygame.USEREVENT + 1:
            for cube in cubes:
                cube.move(dt)
    keys_pressed = pygame.key.get_pressed()
    for k, v in used_keys.items():
        if keys_pressed[k]:
            camera.move_direction(v)

    update(dt)
