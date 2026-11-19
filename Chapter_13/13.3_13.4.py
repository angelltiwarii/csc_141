import sys
import pygame

class Raindrop:

    def __init__(self, screen, x, y):

        self.screen = screen

        self.image = pygame.image.load("raindrop.bmp")

        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y

        self.y = float(y)

        self.speed = 2.0

    def update(self):

        self.y += self.speed

        if self.rect.top >= 800:
            self.y = -self.rect.height

        self.rect.y = self.y

    def draw(self):

        self.screen.blit(self.image, self.rect)


pygame.init()

screen = pygame.display.set_mode((1200, 800))
pygame.display.set_caption("Steady Rain")

raindrops = []

drop = Raindrop(screen, 0, 0)

drop_width = drop.rect.width
drop_height = drop.rect.height

number_columns = 1200 // (2 * drop_width)
number_rows = 800 // (2 * drop_height)

for row in range(number_rows):

    for column in range(number_columns):

        x = drop_width + 2 * drop_width * column
        y = drop_height + 2 * drop_height * row

        raindrops.append(Raindrop(screen, x, y))


while True:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill((230, 230, 230))

    for drop in raindrops:

        drop.update()
        drop.draw()

    pygame.display.flip()