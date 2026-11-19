import pygame
import sys
import random

pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Alien Invasion - Refactoring")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
BLUE = (0, 100, 255)

font = pygame.font.SysFont(None, 40)

# Ship
ship = pygame.Rect(375, 520, 50, 50)

# Game objects
bullets = []
aliens = []

# Settings
ship_speed = 5
bullet_speed = 8
alien_speed = 2

# Statistics
score = 0
level = 1
high_score = 0

game_active = False

clock = pygame.time.Clock()


def create_fleet():

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


def prep_images():

    global score_image
    global high_score_image
    global level_image

    score_image = font.render(
        f"Score: {score}",
        True,
        WHITE
    )

    high_score_image = font.render(
        f"High Score: {high_score}",
        True,
        WHITE
    )

    level_image = font.render(
        f"Level: {level}",
        True,
        WHITE
    )


def start_game():

    global score, level, game_active

    score = 0
    level = 1

    ship.centerx = 400

    bullets.clear()

    create_fleet()

    prep_images()

    game_active = True


def start_new_level():

    global level, alien_speed

    level += 1

    # Increase alien speed
    alien_speed *= 1.2

    # Create a new fleet
    create_fleet()

    # Prepare updated images
    prep_images()


def check_collisions():

    global score, high_score

    for bullet in bullets[:]:

        for alien in aliens[:]:

            if bullet.colliderect(alien):

                bullets.remove(bullet)
                aliens.remove(alien)

                score += 10 * level

                if score > high_score:
                    high_score = score

                prep_images()

                break


def check_events():

    global game_active

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

                bullets.append(bullet)


def update_game():

    if not game_active:
        return

    # Move ship
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        ship.x -= ship_speed

    if keys[pygame.K_RIGHT]:
        ship.x += ship_speed

    ship.clamp_ip(screen.get_rect())

    # Move bullets
    for bullet in bullets[:]:

        bullet.y -= bullet_speed

        if bullet.bottom < 0:
            bullets.remove(bullet)

    # Move aliens
    for alien in aliens:
        alien.y += alien_speed

    # Check collisions
    check_collisions()

    # Start a new level when fleet is destroyed
    if len(aliens) == 0:
        start_new_level()


def draw_screen():

    screen.fill(BLACK)

    if game_active:

        pygame.draw.rect(screen, BLUE, ship)

        for bullet in bullets:
            pygame.draw.rect(screen, WHITE, bullet)

        for alien in aliens:
            pygame.draw.rect(screen, GREEN, alien)

    else:

        message = font.render(
            "Press P to Play",
            True,
            WHITE
        )

        screen.blit(message, (300, 300))

    # Update scoreboard
    prep_images()

    screen.blit(score_image, (20, 20))
    screen.blit(high_score_image, (500, 20))
    screen.blit(level_image, (20, 60))

    pygame.display.flip()


# Main game loop
while True:

    check_events()

    update_game()

    draw_screen()

    clock.tick(60)