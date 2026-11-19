import sys
import pygame
from random import randint

pygame.init()

screen = pygame.display.set_mode((1200, 800))
pygame.display.set_caption("Better Stars")

star_image = pygame.image.load("star.bmp")

star_rect = star_image.get_rect()

stars = []

star_width = star_rect.width
star_height = star_rect.height

for row in range(8):

    for column in range(12):

        x = column * 90 + randint(-10, 10)
        y = row * 90 + randint(-10, 10)

        rect = star_rect.copy()

        rect.x = x
        rect.y = y

        stars.append(rect)


while True:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill((0, 0, 0))

    for rect in stars:
        screen.blit(star_image, rect)

    pygame.display.flip()