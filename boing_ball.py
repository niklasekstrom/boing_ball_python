import math
import pygame

BLACK = (0, 0, 0)
GRAY = (102, 102, 102)
LIGHTGRAY = (170, 170, 170)
WHITE = (255, 255, 255)
RED = (255, 26, 1)
PURPLE = (183, 45, 168)

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

def draw_shadow(screen, points):
    ps = []
    for i in range(9):
        x, y = points[0][i]
        ps.append((x + 50, y))
    for i in range(8):
        x, y = points[9][7-i]
        ps.append((x + 50, y))
    pygame.draw.polygon(screen, GRAY, ps)

def draw_wireframe(screen):
    for i in range(13):
        p1 = (50, i*36)
        p2 = (590, i*36)
        pygame.draw.line(screen, PURPLE, p1, p2, 2)

    for i in range(16):
        p1 = (50 + i*36, 0)
        p2 = (50 + i*36, 432)
        pygame.draw.line(screen, PURPLE, p1, p2, 2)

    for i in range(16):
        p1 = (50 + i*36, 432)
        p2 = (i*42.666, 480)
        pygame.draw.line(screen, PURPLE, p1, p2, 2)

    ys = [442, 454, 468]
    for i in range(3):
        y = ys[i]
        x1 = 50 - 50.0*(y-432)/(480.0-432.0)
        p1 = (x1, y)
        p2 = (640-x1, y)
        pygame.draw.line(screen, PURPLE, p1, p2, 2)
        
def calc_and_draw(screen, phase, scale, x, y):
    points = calc_points(phase % 22.5)
    transform(points, scale, x, y)
    draw_shadow(screen, points)
    draw_wireframe(screen)
    fill_tiles(screen, points, phase >= 22.5)
    #draw_meridians(screen, points)
    #draw_parabels(screen, points)

def init_and_run_loop():
    pygame.init()

    size = (640, 512)
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("Boing Ball")

    done = False
    clock = pygame.time.Clock()

    phase = 0.0
    dp = 2.5
    x = 320
    dx = 2.1
    right = True
    y_ang = 0.0

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        phase = (phase + ((45.0 - dp) if right else dp)) % 45.0
        x += dx if right else -dx
        if x >= 505:
            right = False
        elif x <= 135:
            right = True
        y_ang = (y_ang + 1.5) % 360.0
        y = 350.0 - 200.0 * math.fabs(math.cos(y_ang * math.pi / 180.0))

        screen.fill(LIGHTGRAY)
        calc_and_draw(screen, phase, 120.0, x, y)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == '__main__':
    init_and_run_loop()
