import pygame
import sys
import random

pygame.init()

# Screen settings
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Sideways Shooter - Final Version")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
BLUE = (0, 100, 255)
RED = (220, 0, 0)

# Font
font = pygame.font.SysFont(None, 40)

# Ship settings
ship = pygame.Rect(30, 270, 50, 60)
ship_speed = 5

# Bullet settings
bullets = []
bullet_speed = 8

# Alien settings
aliens = []
alien_speed = 2

# Game statistics
score = 0
high_score = 0
level = 1
ship_hits = 0

game_active = False

# Play button
play_button = pygame.Rect(320, 300, 160, 60)

clock = pygame.time.Clock()


def create_fleet():

    aliens.clear()

    for row in range(5):

        for column in range(4):

            alien = pygame.Rect(
                600 + column * 45,
                40 + row * 100,
                30,
                30
            )

            aliens.append(alien)


def start_game():

    global score, level, ship_hits
    global alien_speed, game_active

    score = 0
    level = 1
    ship_hits = 0

    alien_speed = 2

    ship.y = 270

    bullets.clear()

    create_fleet()

    game_active = True


def start_new_level():

    global level, alien_speed

    level += 1

    # Increase difficulty
    alien_speed += 1

    # Create a new fleet
    create_fleet()


def draw_text(message, y):

    text = font.render(message, True, WHITE)

    screen.blit(
        text,
        text.get_rect(center=(400, y))
    )


def update_bullets():

    global score, high_score

    for bullet in bullets[:]:

        bullet.x += bullet_speed

        if bullet.left > 800:

            bullets.remove(bullet)

    # Check bullet collisions
    for bullet in bullets[:]:

        for alien in aliens[:]:

            if bullet.colliderect(alien):

                if bullet in bullets:
                    bullets.remove(bullet)

                if alien in aliens:
                    aliens.remove(alien)

                score += 10 * level

                if score > high_score:
                    high_score = score

                break


def update_aliens():

    global ship_hits, game_active

    for alien in aliens[:]:

        alien.x -= alien_speed

        # Check if alien reaches ship
        if alien.colliderect(ship):

            aliens.remove(alien)

            ship_hits += 1

        elif alien.right < 0:

            aliens.remove(alien)

            ship_hits += 1

    # End game if ship is hit three times
    if ship_hits >= 3:
        game_active = False


def check_events():

    global game_active

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
                    ship.centery - 3,
                    15,
                    6
                )

                bullets.append(bullet)


def update_ship():

    keys = pygame.key.get_pressed()

    if keys[pygame.K_UP]:
        ship.y -= ship_speed

    if keys[pygame.K_DOWN]:
        ship.y += ship_speed

    ship.clamp_ip(screen.get_rect())


def draw_game():

    screen.fill(BLACK)

    if game_active:

        pygame.draw.rect(screen, BLUE, ship)

        for bullet in bullets:
            pygame.draw.rect(screen, WHITE, bullet)

        for alien in aliens:
            pygame.draw.rect(screen, GREEN, alien)

        # Display score
        score_text = font.render(
            f"Score: {score}",
            True,
            WHITE
        )

        screen.blit(score_text, (20, 20))

        # Display high score
        high_score_text = font.render(
            f"High Score: {high_score}",
            True,
            WHITE
        )

        screen.blit(high_score_text, (550, 20))

        # Display level
        level_text = font.render(
            f"Level: {level}",
            True,
            WHITE
        )

        screen.blit(level_text, (20, 60))

        # Display remaining lives
        lives_text = font.render(
            f"Hits: {ship_hits}/3",
            True,
            WHITE
        )

        screen.blit(lives_text, (20, 100))

    else:

        draw_text("SIDEWAYS SHOOTER", 200)

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

        if score > 0:
            draw_text(f"Final Score: {score}", 400)

    pygame.display.flip()


# Main game loop
while True:

    check_events()

    if game_active:

        update_ship()

        update_bullets()

        update_aliens()

        # Start next level
        if len(aliens) == 0:
            start_new_level()

    draw_game()

    clock.tick(60)