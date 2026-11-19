import pygame
import sys
import random

pygame.init()

# Screen settings
WIDTH = 950
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Sideways Shooter")

clock = pygame.time.Clock()

# Colors
WHITE = (245, 245, 245)
GREEN = (80, 220, 130)
RED = (235, 85, 85)
YELLOW = (250, 215, 80)
BLACK = (12, 18, 34)

font = pygame.font.SysFont(None, 32)
big_font = pygame.font.SysFont(None, 58)

# Ship
ship = pygame.Rect(
    45, HEIGHT // 2 - 22, 58, 44
)

# Play button
play_button = pygame.Rect(
    WIDTH // 2 - 85,
    HEIGHT // 2 - 25,
    170,
    55
)

# Game variables
bullets = []
enemies = []

score = 0

game_active = False

enemy_speed = 3

spawn_counter = 0


# Start game
def start_game():

    global bullets, enemies
    global score, game_active
    global enemy_speed, spawn_counter

    bullets = []
    enemies = []

    score = 0

    enemy_speed = 3

    spawn_counter = 0

    ship.centery = HEIGHT // 2

    game_active = True


# Draw ship
def draw_ship():

    points = [
        (ship.left, ship.top),
        (ship.right, ship.centery),
        (ship.left, ship.bottom)
    ]

    pygame.draw.polygon(
        screen,
        GREEN,
        points
    )


# Main game
def main():

    global game_active
    global bullets, enemies
    global score, enemy_speed
    global spawn_counter

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
                            16,
                            8
                        )

                        bullets.append(bullet)

            elif event.type == pygame.MOUSEBUTTONDOWN:

                if event.button == 1:

                    if not game_active:

                        if play_button.collidepoint(event.pos):

                            start_game()

        # Update game
        if game_active:

            keys = pygame.key.get_pressed()

            # Move ship
            if keys[pygame.K_UP]:

                ship.y -= 6

            if keys[pygame.K_DOWN]:

                ship.y += 6

            if ship.top < 0:
                ship.top = 0

            if ship.bottom > HEIGHT:
                ship.bottom = HEIGHT

            # Create enemies
            spawn_counter += 1

            if spawn_counter >= 55:

                spawn_counter = 0

                enemy_y = random.randint(
                    25,
                    HEIGHT - 55
                )

                enemy = pygame.Rect(
                    WIDTH,
                    enemy_y,
                    38,
                    38
                )

                enemies.append(enemy)

            # Move bullets
            for bullet in bullets[:]:

                bullet.x += 10

                if bullet.left > WIDTH:

                    bullets.remove(bullet)

            # Move enemies
            for enemy in enemies[:]:

                enemy.x -= int(enemy_speed)

                if enemy.right < 0:

                    enemies.remove(enemy)

                    game_active = False

                elif enemy.colliderect(ship):

                    game_active = False

            # Check bullet collisions
            for bullet in bullets[:]:

                hit_enemy = None

                for enemy in enemies:

                    if bullet.colliderect(enemy):

                        hit_enemy = enemy
                        break

                if hit_enemy:

                    bullets.remove(bullet)

                    enemies.remove(hit_enemy)

                    score += 10

                    # Increase difficulty
                    enemy_speed += 0.15

        # Draw screen
        screen.fill(BLACK)

        score_text = font.render(
            f"Score: {score}",
            True,
            WHITE
        )

        screen.blit(score_text, (20, 15))

        if game_active:

            draw_ship()

            # Draw bullets
            for bullet in bullets:

                pygame.draw.rect(
                    screen,
                    YELLOW,
                    bullet
                )

            # Draw enemies
            for enemy in enemies:

                pygame.draw.rect(
                    screen,
                    RED,
                    enemy,
                    border_radius=6
                )

        else:

            title = big_font.render(
                "SIDEWAYS SHOOTER",
                True,
                WHITE
            )

            screen.blit(
                title,
                title.get_rect(
                    center=(WIDTH // 2, 190)
                )
            )

            pygame.draw.rect(
                screen,
                GREEN,
                play_button,
                border_radius=8
            )

            label = font.render(
                "PLAY",
                True,
                BLACK
            )

            screen.blit(
                label,
                label.get_rect(
                    center=play_button.center
                )
            )

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