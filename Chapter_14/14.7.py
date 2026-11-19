import pygame
import sys
import random

pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Alien Invasion - Alien Attacks")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
BLUE = (0, 100, 255)
RED = (220, 0, 0)

font = pygame.font.SysFont(None, 45)

# Ship
ship = pygame.Rect(375, 520, 50, 50)
ship_speed = 5

# Bullets
player_bullets = []
alien_bullets = []

player_bullet_speed = 8
alien_bullet_speed = 5

# Aliens
aliens = []

alien_speed = 1

# Game state
game_active = False
score = 0

clock = pygame.time.Clock()


def create_aliens():

    aliens.clear()

    for row in range(3):

        for column in range(8):

            alien = pygame.Rect(
                40 + column * 90,
                50 + row * 60,
                40,
                35
            )

            aliens.append(alien)


def start_game():

    global game_active, score

    score = 0

    ship.centerx = 400

    player_bullets.clear()
    alien_bullets.clear()

    create_aliens()

    game_active = True


def draw_text(message, y):

    text = font.render(message, True, WHITE)

    screen.blit(
        text,
        text.get_rect(center=(400, y))
    )


while True:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

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

                player_bullets.append(bullet)

    if game_active:

        # Move ship
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            ship.x -= ship_speed

        if keys[pygame.K_RIGHT]:
            ship.x += ship_speed

        ship.clamp_ip(screen.get_rect())

        # Move player bullets
        for bullet in player_bullets[:]:

            bullet.y -= player_bullet_speed

            if bullet.bottom < 0:
                player_bullets.remove(bullet)

        # Move aliens
        for alien in aliens:
            alien.y += alien_speed

        # Aliens randomly fire bullets
        if aliens and random.randint(1, 35) == 1:

            shooter = random.choice(aliens)

            alien_bullet = pygame.Rect(
                shooter.centerx - 3,
                shooter.bottom,
                6,
                15
            )

            alien_bullets.append(alien_bullet)

        # Move alien bullets
        for bullet in alien_bullets[:]:

            bullet.y += alien_bullet_speed

            if bullet.top > 600:
                alien_bullets.remove(bullet)

            elif bullet.colliderect(ship):
                game_active = False

        # Check player bullet collisions
        for bullet in player_bullets[:]:

            for alien in aliens[:]:

                if bullet.colliderect(alien):

                    player_bullets.remove(bullet)
                    aliens.remove(alien)

                    score += 10

                    break

        # Game ends if aliens reach ship
        if any(alien.bottom >= ship.top for alien in aliens):
            game_active = False

        # Create new fleet
        if len(aliens) == 0:
            create_aliens()

    # Draw screen
    screen.fill(BLACK)

    if game_active:

        pygame.draw.rect(screen, BLUE, ship)

        for bullet in player_bullets:
            pygame.draw.rect(screen, WHITE, bullet)

        for bullet in alien_bullets:
            pygame.draw.rect(screen, RED, bullet)

        for alien in aliens:
            pygame.draw.rect(screen, GREEN, alien)

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