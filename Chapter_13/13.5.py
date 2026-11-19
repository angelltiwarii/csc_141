import sys
import pygame
import random

pygame.init()

screen = pygame.display.set_mode((1200, 800))
pygame.display.set_caption("Sideways Shooter Part 2")

ship = pygame.Rect(20, 350, 60, 40)

bullets = []
aliens = []

for i in range(8):

    alien = pygame.Rect(
        random.randint(900, 1150),
        random.randint(50, 750),
        40,
        40
    )

    aliens.append(alien)

ship_speed = 5

while True:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.KEYDOWN:

            if event.key == pygame.K_SPACE:

                bullet = pygame.Rect(
                    ship.right,
                    ship.centery,
                    15,
                    5
                )

                bullets.append(bullet)

    keys = pygame.key.get_pressed()

    if keys[pygame.K_UP] and ship.top > 0:
        ship.y -= ship_speed

    if keys[pygame.K_DOWN] and ship.bottom < 800:
        ship.y += ship_speed

    screen.fill((230, 230, 230))

    pygame.draw.rect(screen, (0, 100, 255), ship)

    for bullet in bullets[:]:

        bullet.x += 8

        pygame.draw.rect(screen, (0, 0, 0), bullet)

        if bullet.left > 1200:
            bullets.remove(bullet)

    for alien in aliens[:]:

        alien.x -= 2

        pygame.draw.rect(screen, (0, 200, 0), alien)

        if alien.left < 0:
            aliens.remove(alien)

        for bullet in bullets[:]:

            if alien.colliderect(bullet):

                aliens.remove(alien)

                if bullet in bullets:
                    bullets.remove(bullet)

                break

    pygame.display.flip()