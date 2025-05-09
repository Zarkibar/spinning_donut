import pygame
import sys
import math
import os

# Initialize Pygame
pygame.init()

# Set up display
SCREEN_HEIGHT = 600//10
SCREEN_WIDTH = 800//10
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Spinning Donut")
clock = pygame.time.Clock()

screen_center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2)

display = [[0 for x in range(SCREEN_WIDTH)] for y in range(SCREEN_HEIGHT)]
ASCII_CHARS = [" ", ".", ",", ":", "-", "=", "+", "*", "#", "%", "@"]

CAM_MOVE_SPEED = 0.2
CAM_ROT_SPEED = 0.04
DOT_COLOR = (150, 150, 150)
DOT_RADIUS = 1

camera_pos = [0,0,-3]
camera_rot = [0,0]

light_dir = [1, -2, -2]
light_mag = math.sqrt(sum(c*c for c in light_dir))
light_dir = [c / light_mag for c in light_dir]  # normalize

move_vertical = 0
move_horizontal = 0
rot_vertical = 0
rot_horizontal = 0

k1 = 100
k2 = 1

theta = math.pi / 180

def project_point(point):
    x = k1 * point[0] / (point[2] + k2) 
    y = k1 * point[1] / (point[2] + k2)
    
    screen_x = int(x + screen_center[0])
    screen_y = int(y + screen_center[1])
    return (screen_x, screen_y)

def rotate_point_y(point, angle):
    x, y, z = point
    cos_a = math.cos(angle)
    sin_a = math.sin(angle)
    return [x * cos_a - z * sin_a, y, x * sin_a + z * cos_a]

def rotate_point_x(point, angle):
    x, y, z = point
    cos_a = math.cos(angle)
    sin_a = math.sin(angle)
    return [x, y * cos_a - z * sin_a, y * sin_a + z * cos_a]

def transform_point(point, cam_pos, cam_rot):
    # Move point relative to camera
    x = point[0] - cam_pos[0]
    y = point[1] - cam_pos[1]
    z = point[2] - cam_pos[2]

    # Rotate around camera
    point = rotate_point_y([x, y, z], -cam_rot[1])  # yaw (left-right)
    point = rotate_point_x(point, -cam_rot[0])      # pitch (up-down)

    return point

def update_all_points_rotation(points, normals, t):
    for point in points:
        x = point[0]
        z = point[2]
        point[2] = z * math.cos(t) - x * math.sin(t)
        point[0] = x * math.cos(t) + z * math.sin(t)

    for normal in normals:
        x = normal[0]
        z = normal[2]
        normal[2] = z * math.cos(t) - x * math.sin(t)
        normal[0] = x * math.cos(t) + z * math.sin(t)

def set_ascii(point: tuple, brightness):
    try:
        display[point[1]][point[0]] = brightness
    except:
        pass

def show_point(point, cam_pos, cam_rot, color=DOT_COLOR, radius=DOT_RADIUS):
    transformed = transform_point(point, cam_pos, cam_rot)
    if transformed[2] > 0.01:
        pygame.draw.circle(screen, color, project_point(transformed), radius)

def show_all_points(points, normals, cam_pos, cam_rot, color=DOT_COLOR, radius=DOT_RADIUS):
    for point, normal in zip(points, normals):
        transformed = transform_point(point, cam_pos, cam_rot)
        normal_transformed = rotate_point_y(normal, -cam_rot[1])
        normal_transformed = rotate_point_x(normal_transformed, -cam_rot[0])

        if transformed[2] > 0.01:
            lum = compute_luminance(normal_transformed, light_dir)
            brightness = int(255 * lum)
            col = (brightness, brightness, brightness)
            set_ascii(project_point(transformed), brightness)
            pygame.draw.circle(screen, col, project_point(transformed), radius)

def compute_luminance(normal, light_dir):
    # Dot product between normal and light direction
    dot = sum(n * l for n, l in zip(normal, light_dir))
    return max(0, dot)


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
    normals = []

    for i in range(num_major):
        theta = (2 * math.pi * i) / num_major
        cos_theta = math.cos(theta)
        sin_theta = math.sin(theta)

        for j in range(num_minor):
            phi = (2 * math.pi * j) / num_minor
            cos_phi = math.cos(phi)
            sin_phi = math.sin(phi)

            # Point on surface
            x = (R + r * cos_phi) * cos_theta
            y = (R + r * cos_phi) * sin_theta
            z = r * sin_phi
            points.append([x, y, z])

            # Normal vector (center of tube to surface point)
            nx = cos_phi * cos_theta
            ny = cos_phi * sin_theta
            nz = sin_phi
            normals.append([nx, ny, nz])

    return points, normals

def load_vertices_from_obj(path):
    vertices = []

    with open("obj/"+path, 'r') as file:
        for line in file:
            if line.startswith('v '):
                parts = line.strip().split()
                x, y, z = map(float, parts[1:4])
                vertices.append([x, y, z])

    return vertices

# Points
points, normals = generate_torus() # load_vertices_from_obj("monkey.obj")

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))

    update_all_points_rotation(points, normals, theta)
    show_all_points(points, normals, camera_pos, camera_rot)

    
    os.system('cls')    # Windows
    im = []
    for row in display:
        # Convert each pixel in the row to ASCII character
        ascii_row = [ASCII_CHARS[p // 25] for p in row]
        # Combine the row into a string
        im.append("".join(ascii_row))
    # Combine all rows with newlines
    print("\n".join(im))
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
