import pygame
import sys
import random

pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Alien Invasion - Difficulty Levels")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
BLUE = (0, 100, 255)
RED = (220, 0, 0)
GRAY = (120, 120, 120)

font = pygame.font.SysFont(None, 40)

# Difficulty buttons
easy_button = pygame.Rect(100, 300, 150, 60)
medium_button = pygame.Rect(325, 300, 150, 60)
hard_button = pygame.Rect(550, 300, 150, 60)

# Ship
ship = pygame.Rect(375, 520, 50, 50)

# Game variables
bullets = []
aliens = []

ship_speed = 5
bullet_speed = 8
alien_speed = 2

game_active = False
difficulty_selected = False

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


def start_game(difficulty):

    global ship_speed, bullet_speed, alien_speed
    global game_active, difficulty_selected, score

    # Set difficulty values
    if difficulty == "Easy":

        ship_speed = 6
        bullet_speed = 10
        alien_speed = 1

    elif difficulty == "Medium":

        ship_speed = 5
        bullet_speed = 8
        alien_speed = 2

    elif difficulty == "Hard":

        ship_speed = 4
        bullet_speed = 7
        alien_speed = 4

    ship.centerx = 400

    bullets.clear()

    score = 0

    create_aliens()

    game_active = True
    difficulty_selected = True


def draw_button(button, label):

    pygame.draw.rect(screen, GREEN, button)

    text = font.render(label, True, BLACK)

    screen.blit(
        text,
        text.get_rect(center=button.center)
    )


while True:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:

            if not game_active:

                if easy_button.collidepoint(event.pos):
                    start_game("Easy")

                elif medium_button.collidepoint(event.pos):
                    start_game("Medium")

                elif hard_button.collidepoint(event.pos):
                    start_game("Hard")

        if event.type == pygame.KEYDOWN:

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

        # Reset aliens if they reach bottom
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

        if len(aliens) == 0:
            game_active = False

    screen.fill(BLACK)

    if game_active:

        pygame.draw.rect(screen, BLUE, ship)

        for bullet in bullets:
            pygame.draw.rect(screen, WHITE, bullet)

        for alien in aliens:
            pygame.draw.rect(screen, GREEN, alien)

        score_text = font.render(
            f"Score: {score}",
            True,
            WHITE
        )

        screen.blit(score_text, (20, 20))

    else:

        title = font.render(
            "CHOOSE DIFFICULTY",
            True,
            WHITE
        )

        screen.blit(title, (260, 200))

        draw_button(easy_button, "EASY")
        draw_button(medium_button, "MEDIUM")
        draw_button(hard_button, "HARD")

        if difficulty_selected:

            message = font.render(
                "Game Over - Select Again",
                True,
                WHITE
            )

            screen.blit(message, (250, 400))

    pygame.display.flip()

    clock.tick(60)