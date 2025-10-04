import math

import pgzrun
import pygame

""" CONFIGURATION """

WIDTH = 1600
HEIGHT = 800

WALL_THICKNESS = 20
WALL_COLOR = (0, 0, 255)
FLOOR_COLOR = (0, 255, 0)

RAY_ANGLE = 30
RAY_COUNT = 80
RAY_PRECISION = 2
RAY_LENGTH = 200

""" VARIABLES """

walls_list = [
    Rect((0, 0), (WIDTH / 2, WALL_THICKNESS)),  # top wall
    Rect((0, 0), (WALL_THICKNESS, HEIGHT)),  # left wall
    Rect((0, HEIGHT - WALL_THICKNESS),
         (WIDTH / 2, WALL_THICKNESS)),  # bottom wall
    Rect((WIDTH / 2 - WALL_THICKNESS, 0),
         (WALL_THICKNESS, HEIGHT)),  # right wall
    Rect((80, 120), (200, WALL_THICKNESS)),
    Rect((250, 420), (WALL_THICKNESS, 320)),
    Rect((620, 150), (WALL_THICKNESS, 280)),
]

ball = {
    "x": WIDTH // 4,
    "y": HEIGHT // 2,
    "radius": 20,
    "color": (255, 0, 0),
    "angle": 0,
}

line_points = []


""" DRAW """


def draw():
    screen.fill("white")
    draw_2d()
    draw_3d()


def draw_3d():
    """Draws 3D representation of the game field
    """
    rect_width = (WIDTH / 2) / RAY_COUNT
    max_dist = WIDTH / 2
    for ray_number in range(RAY_COUNT):
        px, py, angle, wall = line_points[ray_number]
        distance = dist(ball["x"], ball["y"], px, py)
        distance = distance * math.cos(math.radians(angle - ball["angle"]))
        rect_height = (1 - (distance / max_dist)) * HEIGHT

        if wall is not None:
            draw_3d_wall(ray_number, rect_width, rect_height)

        draw_3d_floor(ray_number, rect_width, rect_height)


def draw_3d_wall(ray_number, width, height):
    """Draws 3D wall

    Args:
        ray_number (int): number of the ray
        width (int): width of one wall rectangle
        height (int): height of one wall rectangle
    """
    wall = Actor("wall1", anchor=("left", "top"))
    wall.x = width * ray_number + WIDTH / 2
    wall.y = (HEIGHT - height) / 2
    wall._surf = pygame.transform.scale(
        wall._surf, (width + 5, height + 5))
    wall._update_pos()
    wall.draw()


def draw_3d_floor(ray_number, width, height):
    """Draws 3D floor

    Args:
        ray_number (int): number of the ray
        width (int): width of one floor rectangle
        height (int): height of one floor rectangle
    """
    floor = Actor("floor", anchor=("left", "top"))
    floor.x = width * ray_number + WIDTH / 2
    floor.y = max((HEIGHT - height) / 2 + height, HEIGHT / 2)
    floor._surf = pygame.transform.scale(
        floor._surf, (width, height))
    floor._update_pos()
    floor.draw()


def draw_2d():
    """Draws 2D representation of the game field
    """
    draw_2d_walls()
    draw_2d_ball()
    draw_2d_rays()


def draw_2d_rays():
    """Draws 2d rays
    """
    for point in line_points:
        px, py, angle, wall = point
        screen.draw.line((ball["x"], ball["y"]), (px, py), "yellow")


def draw_2d_walls():
    """Draws 2d walls
    """
    for wall in walls_list:
        screen.draw.filled_rect(wall, WALL_COLOR)


def draw_2d_ball():
    """Draws 2d ball
    """
    screen.draw.filled_circle(
        (ball["x"], ball["y"]), ball["radius"], ball["color"])


""" UPDATE """


def update():
    update_ball()
    update_rays()


def update_ball():
    """Updates ball movement based on the pressed keys
    """
    if keyboard.q:
        ball["angle"] -= 1

    if keyboard.e:
        ball["angle"] += 1

    if keyboard.w:
        ball["x"] += math.cos(math.radians(ball["angle"]))
        ball["y"] += math.sin(math.radians(ball["angle"]))

    if keyboard.s:
        ball["x"] -= math.cos(math.radians(ball["angle"]))
        ball["y"] -= math.sin(math.radians(ball["angle"]))


def update_rays():
    """Generates new rays based on the ball position
    """
    line_points.clear()
    angle = ball["angle"] - RAY_ANGLE
    while angle < ball["angle"] + RAY_ANGLE:
        x = ball["x"]
        y = ball["y"]

        counter = 0
        while not check_collision(x, y) and counter < RAY_LENGTH:
            x += math.cos(math.radians(angle)) * RAY_PRECISION
            y += math.sin(math.radians(angle)) * RAY_PRECISION
            counter += 1

        wall = check_collision(x, y)
        line_points.append((x, y, angle, wall))

        angle += (RAY_ANGLE * 2) / RAY_COUNT


""" HELPERS """


def check_collision(x, y):
    """Checks if given 2D point is in collision with any of the walls

    Args:
        x (float): x coordinate of the point
        y (float): y coordinate of the point

    Returns:
        Actor: wall with which the point collides, or None otherwise
    """
    for wall in walls_list:
        if wall.collidepoint((x, y)):
            return wall

    return None


def dist(x1, y1, x2, y2):
    """Computes distance between two 2D points

    Args:
        x1 (float): x coordinate of the first point
        y1 (float): y coordinate of the first point
        x2 (float): x coordinate of the second point
        y2 (float): y coordinate of the second point

    Returns:
        float: Distance between points (x1, y1) and (x2, y2)
    """
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


""" INIT """

pgzrun.go()
