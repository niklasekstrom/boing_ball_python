import math
import pygame

BLACK = (0, 0, 0)
LIGHTGRAY = (192, 192, 192)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

def get_lat(phase, i):
    if i == 0:
        return -90.0
    elif i == 9:
        return 90.0
    else:
        return -90.0 + phase + (i-1) * 22.5

def calc_points(phase):
    points = {}
    sin_lat = {}
    for i in range(10):
        points[i] = {}
        lat = get_lat(phase, i)
        sin_lat[i] = math.sin(lat * math.pi / 180.0)

    for j in range(9):
        lon = -90.0 + j * 22.5
        y = math.sin(lon * math.pi / 180.0)
        l = math.cos(lon * math.pi / 180.0)
        for i in range(10):
            x = sin_lat[i] * l
            points[i][j] = (x, y)

    return points

def tilt_sphere(points, ang):
    st = math.sin(ang * math.pi / 180.0)
    ct = math.cos(ang * math.pi / 180.0)
    for i in points:
        for j in points[i]:
            x, y = points[i][j]
            x, y = x * ct - y * st, x * st + y * ct
            points[i][j] = x, y

def scale_and_translate(points, s, tx, ty):
    for i in points:
        for j in points[i]:
            x, y = points[i][j]
            x, y = x * s + tx, y * s + ty
            points[i][j] = x, y

def transform(points, s, tx, ty):
    tilt_sphere(points, 17.0)
    scale_and_translate(points, s, tx, ty)

def draw_meridians(screen, points):
    for i in range(10):
        for j in range(8):
            p1 = points[i][j]
            p2 = points[i][j+1]
            pygame.draw.line(screen, BLACK, p1, p2)

def draw_parabels(screen, points):
    for i in range(7):
        p1 = points[0][i+1]
        p2 = points[9][i+1]
        pygame.draw.line(screen, BLACK, p1, p2)

def fill_tiles(screen, points, alter):
    for j in range(8):
        for i in range(9):
            p1 = points[i][j]
            p2 = points[i+1][j]
            p3 = points[i+1][j+1]
            p4 = points[i][j+1]
            pygame.draw.polygon(screen, RED if alter else WHITE, (p1, p2, p3, p4))
            alter = not alter

def calc_and_draw(screen, phase, scale, x, y):
    points = calc_points(phase % 22.5)
    transform(points, scale, x, y)
    fill_tiles(screen, points, phase >= 22.5)
    draw_meridians(screen, points)
    draw_parabels(screen, points)

def init_and_run_loop():
    pygame.init()

    size = (800, 500)
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("Boing Ball")

    done = False
    clock = pygame.time.Clock()

    phase = 0.0
    x = 400
    right = True
    y_ang = 0.0

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        phase = (phase + (43.5 if right else 1.5)) % 45.0
        x += 1.8 if right else -1.8
        if x >= 680:
            right = False
        elif x <= 120:
            right = True
        y_ang = (y_ang + 2.5) % 360.0
        y = 380.0 - 150.0 * math.fabs(math.cos(y_ang * math.pi / 180.0))

        screen.fill(LIGHTGRAY)
        calc_and_draw(screen, phase, 120.0, x, y)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == '__main__':
    init_and_run_loop()
