import sys
import pygame

class GameCharacter:

    def __init__(self, screen):
        """Initialize the character and set its starting position."""

        self.screen = screen

        # Load character image
        self.image = pygame.image.load("character.bmp")

        # Get the rectangle of the image
        self.rect = self.image.get_rect()

        # Get screen rectangle
        self.screen_rect = screen.get_rect()

        # Center character on screen
        self.rect.center = self.screen_rect.center

    def blitme(self):
        """Draw character at its current position."""

        self.screen.blit(self.image, self.rect)


pygame.init()

screen = pygame.display.set_mode((1200, 800))
pygame.display.set_caption("Game Character")

bg_color = (230, 230, 230)

character = GameCharacter(screen)

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill(bg_color)

    character.blitme()

    pygame.display.flip()