import pygame
import sys
import random

pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Alien Invasion - High Score")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
BLUE = (0, 100, 255)

font = pygame.font.SysFont(None, 40)

# Ship
ship = pygame.Rect(375, 520, 50, 50)
ship_speed = 5

# Bullets
bullets = []
bullet_speed = 8

# Aliens
aliens = []
alien_speed = 2

# Game statistics
score = 0
high_score = 0
game_active = False

clock = pygame.time.Clock()


# Load high score from file
try:

    with open("high_score.txt", "r") as file:
        high_score = int(file.read())

except (FileNotFoundError, ValueError):

    high_score = 0


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

    global score, game_active

    score = 0

    ship.centerx = 400

    bullets.clear()

    create_aliens()

    game_active = True


def save_high_score():

    global high_score

    if score > high_score:

        high_score = score

        with open("high_score.txt", "w") as file:

            file.write(str(high_score))


while True:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            save_high_score()

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

    if game_active:

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

                    # Update high score
                    if score > high_score:
                        high_score = score

                    break

        if len(aliens) == 0:
            game_active = False

    screen.fill(BLACK)

    if game_active:

        pygame.draw.rect(screen, BLUE, ship)

        for bullet in bullets:
            pygame.draw.rect(screen, WHITE, bullet)

        for alien in aliens:
            pygame.draw.rect(screen, GREEN, alien)

    else:

        text = font.render(
            "Press P to Play",
            True,
            WHITE
        )

        screen.blit(text, (300, 300))

    # Display score
    score_text = font.render(
        f"Score: {score}",
        True,
        WHITE
    )

    screen.blit(score_text, (20, 20))

    # Display high score
    high_text = font.render(
        f"High Score: {high_score}",
        True,
        WHITE
    )

    screen.blit(high_text, (500, 20))

    pygame.display.flip()

    clock.tick(60)