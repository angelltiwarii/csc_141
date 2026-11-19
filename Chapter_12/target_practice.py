import pygame
import sys

pygame.init()

# Screen settings
WIDTH = 900
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Target Practice")

clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
GREEN = (80, 220, 130)
RED = (235, 85, 85)
YELLOW = (250, 215, 80)
BLACK = (18, 24, 40)

font = pygame.font.SysFont(None, 34)
title_font = pygame.font.SysFont(None, 58)

# Ship
ship = pygame.Rect(
    45, HEIGHT // 2 - 20, 55, 40
)

# Target
target = pygame.Rect(
    WIDTH - 85, HEIGHT // 2 - 35, 35, 70
)

# Play button
play_button = pygame.Rect(
    WIDTH // 2 - 85,
    HEIGHT // 2 - 20,
    170,
    55
)

# Game settings
ship_speed = 6
bullet_speed = 9

target_speed = 3
original_target_speed = 3

target_direction = 1

bullets = []

misses = 0
score = 0

game_active = False


# Start game
def start_game():

    global game_active
    global misses, score
    global target_speed, target_direction
    global bullets

    game_active = True

    misses = 0
    score = 0

    target_speed = original_target_speed
    target_direction = 1

    ship.y = HEIGHT // 2 - ship.height // 2

    target.y = HEIGHT // 2 - target.height // 2

    bullets = []


# Draw ship
def draw_ship():

    points = [
        (ship.left, ship.top),
        (ship.right, ship.centery),
        (ship.left, ship.bottom)
    ]

    pygame.draw.polygon(screen, GREEN, points)


# Draw play button
def draw_button():

    pygame.draw.rect(
        screen,
        GREEN,
        play_button,
        border_radius=8
    )

    label = font.render("PLAY", True, BLACK)

    screen.blit(
        label,
        label.get_rect(center=play_button.center)
    )


# Main game
def main():

    global game_active
    global misses, score
    global target_speed, target_direction
    global bullets

    running = True

    while running:

        # Check events
        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                running = False

            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_q:

                    running = False

                elif event.key == pygame.K_p:

                    if not game_active:
                        start_game()

                elif event.key == pygame.K_SPACE:

                    if game_active:

                        bullet = pygame.Rect(
                            ship.right,
                            ship.centery - 4,
                            15,
                            8
                        )

                        bullets.append(bullet)

            elif event.type == pygame.MOUSEBUTTONDOWN:

                if event.button == 1:

                    if not game_active:

                        if play_button.collidepoint(event.pos):

                            start_game()

        # Keyboard movement
        keys = pygame.key.get_pressed()

        if game_active:

            if keys[pygame.K_UP]:

                ship.y -= ship_speed

            if keys[pygame.K_DOWN]:

                ship.y += ship_speed

            # Keep ship inside screen
            if ship.top < 0:
                ship.top = 0

            if ship.bottom > HEIGHT:
                ship.bottom = HEIGHT

            # Move target
            target.y += int(
                target_speed * target_direction
            )

            if target.top <= 0:

                target.top = 0
                target_direction = 1

            elif target.bottom >= HEIGHT:

                target.bottom = HEIGHT
                target_direction = -1

            # Move bullets
            for bullet in bullets[:]:

                bullet.x += bullet_speed

                # Bullet missed target
                if bullet.left > WIDTH:

                    bullets.remove(bullet)

                    misses += 1

                # Bullet hits target
                elif bullet.colliderect(target):

                    bullets.remove(bullet)

                    score += 1

                    # Increase target speed
                    target_speed += 0.25

            # End game after three misses
            if misses >= 3:

                game_active = False

        # Draw everything
        screen.fill(BLACK)

        pygame.draw.rect(
            screen,
            WHITE,
            (0, 0, WIDTH, HEIGHT),
            2
        )

        score_text = font.render(
            f"Score: {score}     Misses: {misses}/3",
            True,
            WHITE
        )

        screen.blit(score_text, (20, 15))

        if game_active:

            draw_ship()

            pygame.draw.rect(
                screen, RED, target
            )

            for bullet in bullets:

                pygame.draw.rect(
                    screen, YELLOW, bullet
                )

        else:

            title = title_font.render(
                "TARGET PRACTICE",
                True,
                WHITE
            )

            screen.blit(
                title,
                title.get_rect(
                    center=(WIDTH // 2, 190)
                )
            )

            if misses >= 3:

                message = font.render(
                    "Game Over! You missed three times.",
                    True,
                    WHITE
                )

                screen.blit(
                    message,
                    message.get_rect(
                        center=(WIDTH // 2, 250)
                    )
                )

            draw_button()

            hint = font.render(
                "Press P or click Play",
                True,
                WHITE
            )

            screen.blit(
                hint,
                hint.get_rect(
                    center=(WIDTH // 2, 410)
                )
            )

        pygame.display.flip()

        clock.tick(60)

    pygame.quit()

    sys.exit()


if __name__ == "__main__":

    main()