import pygame
import numpy as np

# Initialize Pygame
pygame.init()

# Set up the drawing window
screen = pygame.display.set_mode([800, 600])

# Run until the user asks to quit
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the background with white
    screen.fill((255, 255, 255))

    # Data
    x = np.linspace(0, 10, 800)
    y = np.sin(x) * 100 + 300

    # Draw a smooth sine wave
    points = [(i, y[i]) for i in range(len(x))]
    pygame.draw.lines(screen, (0, 0, 0), False, points, 2)

    # Flip the display
    pygame.display.flip()

# Done! Time to quit.
pygame.quit()