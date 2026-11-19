import sys
import pygame
import random

pygame.init()

screen = pygame.display.set_mode((1200, 800))
pygame.display.set_caption("Game Over")

ship = pygame.Rect(20, 350, 60, 40)

bullets = []
aliens = []

for i in range(5):

    alien = pygame.Rect(
        random.randint(800, 1150),
        random.randint(50, 750),
        40,
        40
    )

    aliens.append(alien)

ship_hits = 0
alien_hits = 0

game_active = True

while True:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.KEYDOWN and game_active:

            if event.key == pygame.K_SPACE:

                bullet = pygame.Rect(
                    ship.right,
                    ship.centery,
                    15,
                    5
                )

                bullets.append(bullet)

    if game_active:

        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP] and ship.top > 0:
            ship.y -= 5

        if keys[pygame.K_DOWN] and ship.bottom < 800:
            ship.y += 5

        for alien in aliens[:]:

            alien.x -= 2

            if alien.left <= ship.right and alien.colliderect(ship):

                ship_hits += 1
                aliens.remove(alien)

                if ship_hits >= 3:
                    game_active = False

        for bullet in bullets[:]:

            bullet.x += 8

            for alien in aliens[:]:

                if bullet.colliderect(alien):

                    aliens.remove(alien)
                    bullets.remove(bullet)

                    alien_hits += 1

                    break

        for bullet in bullets[:]:

            if bullet.left > 1200:
                bullets.remove(bullet)

    screen.fill((230, 230, 230))

    if game_active:

        pygame.draw.rect(screen, (0, 100, 255), ship)

        for alien in aliens:
            pygame.draw.rect(screen, (0, 200, 0), alien)

        for bullet in bullets:
            pygame.draw.rect(screen, (0, 0, 0), bullet)

    else:

        font = pygame.font.SysFont(None, 72)

        text = font.render("GAME OVER", True, (255, 0, 0))

        screen.blit(text, (450, 350))

    font = pygame.font.SysFont(None, 32)

    hits_text = font.render(
        f"Ship Hits: {ship_hits}  Alien Hits: {alien_hits}",
        True,
        (0, 0, 0)
    )

    screen.blit(hits_text, (20, 20))

    pygame.display.flip()