import sys
import pygame

# Initialize pygame
pygame.init()

# Create the game screen
screen = pygame.display.set_mode((1200, 800))
pygame.display.set_caption("Blue Sky")

# Set background color
bg_color = (0, 0, 255)

# Main game loop
while True:

    # Watch for keyboard and mouse events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Fill screen with blue
    screen.fill(bg_color)

    # Make the most recently drawn screen visible
    pygame.display.flip()