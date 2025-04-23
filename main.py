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

# Points
points = [
    # Cube vertices (original 8)
    [-1, -1, -1],  # point1
    [-1, -1,  1],  # point2
    [-1,  1, -1],  # point3
    [-1,  1,  1],  # point4
    [ 1, -1, -1],  # point5
    [ 1, -1,  1],  # point6
    [ 1,  1, -1],  # point7
    [ 1,  1,  1],  # point8

    # Face centers (6)
    [ 0,  0, -1],  # front face
    [ 0,  0,  1],  # back face
    [ 0, -1,  0],  # bottom face
    [ 0,  1,  0],  # top face
    [-1,  0,  0],  # left face
    [ 1,  0,  0],  # right face

    # Edge midpoints (12)
    [ 0, -1, -1],  # between [-1,-1,-1] and [ 1,-1,-1]
    [-1,  0, -1],  # between [-1,-1,-1] and [-1, 1,-1]
    [-1, -1,  0],  # between [-1,-1,-1] and [-1,-1, 1]
    [ 0,  1, -1],  # between [-1, 1,-1] and [ 1, 1,-1]
    [-1,  1,  0],  # between [-1, 1,-1] and [-1, 1, 1]
    [ 0, -1,  1],  # between [-1,-1, 1] and [ 1,-1, 1]
    [ 0,  1,  1],  # between [-1, 1, 1] and [ 1, 1, 1]
    [ 1, -1,  0],  # between [ 1,-1,-1] and [ 1,-1, 1]
    [ 1,  0, -1],  # between [ 1,-1,-1] and [ 1, 1,-1]
    [ 1,  1,  0],  # between [ 1, 1,-1] and [ 1, 1, 1]
    [ 1,  0,  1],  # between [ 1,-1, 1] and [ 1, 1, 1]
    [-1,  0,  1],  # between [-1,-1, 1] and [-1, 1, 1]
]

k1 = 400
k2 = 4

theta = 0
del_theta = math.pi / 18000

DOT_COLOR = (255, 0, 0)
DOT_RADIUS = 3

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

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((30, 30, 30))

    theta += del_theta

    update_all_points_rotation(theta)
    show_all_points()
    
    pygame.display.flip()
    time.sleep(0.01)

pygame.quit()
sys.exit()
