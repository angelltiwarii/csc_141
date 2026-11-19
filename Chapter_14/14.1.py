import pygame
import sys
import random

pygame.init()

# Screen settings
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Alien Invasion")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
BLUE = (0, 100, 255)
RED = (220, 0, 0)

# Font
font = pygame.font.SysFont(None, 48)

# Ship settings
ship = pygame.Rect(375, 520, 50, 50)
ship_speed = 5

# Bullets
bullets = []
bullet_speed = 8

# Aliens
aliens = []
alien_speed = 2

# Game settings
game_active = False
score = 0
clock = pygame.time.Clock()


# Function to create aliens
def create_aliens():

    aliens.clear()

    for row in range(3):

        for column in range(8):

            alien = pygame.Rect(
                50 + column * 85,
                50 + row * 65,
                40,
                35
            )

            aliens.append(alien)


# Function to start game
def start_game():

    global game_active, score

    ship.centerx = 400
    bullets.clear()

    score = 0

    create_aliens()

    game_active = True


# Function to display text
def draw_text(message, y):

    text = font.render(message, True, WHITE)

    screen.blit(
        text,
        text.get_rect(center=(400, y))
    )


# Main game loop
while True:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Check keyboard events
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_p and not game_active:
                start_game()

            if event.key == pygame.K_SPACE and game_active:

                bullet = pygame.Rect(
                    ship.centerx - 3,
                    ship.top,
                    6,
                    15
                )

                bullets.append(bullet)

    if game_active:

        # Move ship
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            ship.x -= ship_speed

        if keys[pygame.K_RIGHT]:
            ship.x += ship_speed

        if keys[pygame.K_UP]:
            ship.y -= ship_speed

        if keys[pygame.K_DOWN]:
            ship.y += ship_speed

        # Keep ship inside screen
        ship.clamp_ip(screen.get_rect())

        # Move bullets
        for bullet in bullets[:]:

            bullet.y -= bullet_speed

            if bullet.bottom < 0:
                bullets.remove(bullet)

        # Move aliens
        for alien in aliens:
            alien.y += alien_speed

        # Reset alien positions when they reach bottom
        if any(alien.bottom >= 600 for alien in aliens):

            for alien in aliens:
                alien.y = random.randint(30, 150)

        # Check collisions
        for bullet in bullets[:]:

            for alien in aliens[:]:

                if bullet.colliderect(alien):

                    bullets.remove(bullet)
                    aliens.remove(alien)

                    score += 10

                    break

        # Check if all aliens are destroyed
        if len(aliens) == 0:
            game_active = False

    # Draw screen
    screen.fill(BLACK)

    if game_active:

        # Draw ship
        pygame.draw.rect(screen, BLUE, ship)

        # Draw bullets
        for bullet in bullets:
            pygame.draw.rect(screen, WHITE, bullet)

        # Draw aliens
        for alien in aliens:
            pygame.draw.rect(screen, GREEN, alien)

        # Display score
        score_text = font.render(
            f"Score: {score}",
            True,
            WHITE
        )

        screen.blit(score_text, (20, 20))

    else:

        draw_text("ALIEN INVASION", 200)
        draw_text("Press P to Play", 300)

        if score > 0:
            draw_text(f"Final Score: {score}", 380)

    pygame.display.flip()

    clock.tick(60)