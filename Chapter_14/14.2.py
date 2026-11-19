import pygame
import sys

pygame.init()

# Screen
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Target Practice")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 100, 255)
RED = (220, 0, 0)
GREEN = (0, 200, 0)

font = pygame.font.SysFont(None, 40)

# Ship
ship = pygame.Rect(50, 270, 40, 60)
ship_speed = 5

# Target
target = pygame.Rect(720, 250, 35, 100)
target_speed = 4

# Bullets
bullets = []
bullet_speed = 8

# Game statistics
misses = 0
game_active = False

# Play button
play_button = pygame.Rect(330, 300, 140, 60)

clock = pygame.time.Clock()


def start_game():

    global misses, game_active, target_speed

    misses = 0

    ship.y = 270
    target.y = 250

    bullets.clear()

    target_speed = 4

    game_active = True


while True:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:

            if play_button.collidepoint(event.pos):

                if not game_active:
                    start_game()

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_SPACE and game_active:

                bullet = pygame.Rect(
                    ship.right,
                    ship.centery,
                    15,
                    6
                )

                bullets.append(bullet)

    if game_active:

        # Move ship
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            ship.y -= ship_speed

        if keys[pygame.K_DOWN]:
            ship.y += ship_speed

        ship.clamp_ip(screen.get_rect())

        # Move target
        target.y += target_speed

        if target.top <= 0 or target.bottom >= 600:
            target_speed *= -1

        # Move bullets
        for bullet in bullets[:]:

            bullet.x += bullet_speed

            # Count missed bullets
            if bullet.left > 800:

                bullets.remove(bullet)

                misses += 1

        # Check collisions
        for bullet in bullets[:]:

            if bullet.colliderect(target):

                bullets.remove(bullet)

                # Move target to a new position
                target.y = 250

                misses = 0

        # End game after three misses
        if misses >= 3:
            game_active = False

    # Draw screen
    screen.fill(BLACK)

    if game_active:

        pygame.draw.rect(screen, BLUE, ship)
        pygame.draw.rect(screen, RED, target)

        for bullet in bullets:
            pygame.draw.rect(screen, WHITE, bullet)

        text = font.render(
            f"Misses: {misses}/3",
            True,
            WHITE
        )

        screen.blit(text, (20, 20))

    else:

        pygame.draw.rect(screen, GREEN, play_button)

        button_text = font.render(
            "PLAY",
            True,
            BLACK
        )

        screen.blit(
            button_text,
            button_text.get_rect(center=play_button.center)
        )

        if misses >= 3:

            game_over = font.render(
                "GAME OVER",
                True,
                WHITE
            )

            screen.blit(game_over, (320, 220))

    pygame.display.flip()

    clock.tick(60)