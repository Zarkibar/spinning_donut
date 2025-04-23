import pygame
import sys
import math
import time

# Initialize Pygame
pygame.init()

# Set up display
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Spinning Donut")

screen_center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2)


DOT_COLOR = (150, 150, 150)
DOT_RADIUS = 1

k1 = 400
k2 = 4

theta = math.pi / 180

def project_point(point):
    x = k1 * point[0] / (point[2] + k2) 
    y = k1 * point[1] / (point[2] + k2)
    
    screen_x = int(x + screen_center[0])
    screen_y = int(y + screen_center[1])
    return (screen_x, screen_y)

def update_point_rotation(point, theta):
    x = point[0]
    z = point[2]
    point[2] = z * math.cos(theta) - x * math.sin(theta)
    point[0] = x * math.cos(theta) + z * math.sin(theta)

def update_all_points_rotation(t):
    for point in points:
        update_point_rotation(point, t)

def show_point(point, color=DOT_COLOR, radius=DOT_RADIUS):
    pygame.draw.circle(screen, color, project_point(point), radius)

def show_all_points(color=DOT_COLOR, radius=DOT_RADIUS):
    for point in points:
        show_point(point, color=color, radius=radius)


def generate_cube(step=0.33):
    coords = []
    val = -1
    while val <= 1:
        coords.append(round(val, 2))
        val += step
    coords[-1] = 1.0  # ensure exact endpoint

    points = []
    for x in coords:
        for y in coords:
            for z in coords:
                # Only add if point is on the surface (at least one coordinate at boundary)
                if abs(x) == 1 or abs(y) == 1 or abs(z) == 1:
                    points.append([x, y, z])
    return points

def generate_torus(R=1.0, r=0.4, num_major=30, num_minor=15):
    points = []

    for i in range(num_major):
        theta = (2 * math.pi * i) / num_major
        cos_theta = math.cos(theta)
        sin_theta = math.sin(theta)

        for j in range(num_minor):
            phi = (2 * math.pi * j) / num_minor
            cos_phi = math.cos(phi)
            sin_phi = math.sin(phi)

            x = (R + r * cos_phi) * cos_theta
            y = (R + r * cos_phi) * sin_theta
            z = r * sin_phi

            points.append([round(x, 4), round(y, 4), round(z, 4)])

    return points

# Points
points = generate_cube()

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((30, 30, 30))

    update_all_points_rotation(theta)
    show_all_points()
    
    pygame.display.flip()
    time.sleep(0.01)

pygame.quit()
sys.exit()
