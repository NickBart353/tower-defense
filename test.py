import pygame
import math

# Initialize Pygame
pygame.init()
clock = pygame.time.Clock()
dt = 0

# Screen and color settings (same as before)
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
white = (255, 255, 255)
red = (255, 0, 0)
blue = (0, 0, 255)


center_a_x = screen_width // 2
center_a_y = screen_height // 2
radius_a = 20
orbit_radius = 100

orbiting_circles = []

for i in range(8):
    start_angle = i * (math.pi / 4)
    orbiting_circles.append({'angle': start_angle, 'color': blue})


rotation_speed = 2

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(white)

    pygame.draw.circle(screen, red, (center_a_x, center_a_y), radius_a)


    for circle in orbiting_circles:
        circle['angle'] += dt * rotation_speed

        x_b = center_a_x + orbit_radius * math.cos(circle['angle'])
        y_b = center_a_y + orbit_radius * math.sin(circle['angle'])

        pygame.draw.circle(screen, circle['color'], (int(x_b), int(y_b)), 10)

    pygame.display.flip()
    dt = clock.tick(60) / 1000

# Quit Pygame
pygame.quit()