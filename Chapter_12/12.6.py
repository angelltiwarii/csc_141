import sys
import pygame

class Ship:

    def __init__(self, screen):

        self.screen = screen

        self.image = pygame.image.load("ship.bmp")
        self.rect = self.image.get_rect()

        self.rect.midleft = (20, screen.get_rect().centery)

        self.y = float(self.rect.y)

        self.speed = 2.0

        self.moving_up = False
        self.moving_down = False

    def update(self):

        if self.moving_up and self.rect.top > 0:
            self.y -= self.speed

        if self.moving_down and self.rect.bottom < 800:
            self.y += self.speed

        self.rect.y = self.y

    def blitme(self):

        self.screen.blit(self.image, self.rect)


class Bullet:

    def __init__(self, ship):

        self.rect = pygame.Rect(
            ship.rect.right,
            ship.rect.centery - 2,
            15,
            4
        )

        self.x = float(self.rect.x)

        self.speed = 3.0

    def update(self):

        self.x += self.speed
        self.rect.x = self.x

    def draw_bullet(self, screen):

        pygame.draw.rect(screen, (60, 60, 60), self.rect)


pygame.init()

screen = pygame.display.set_mode((1200, 800))
pygame.display.set_caption("Sideways Shooter")

ship = Ship(screen)

bullets = []

while True:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.KEYDOWN:

            if event.key == pygame.K_UP:
                ship.moving_up = True

            elif event.key == pygame.K_DOWN:
                ship.moving_down = True

            elif event.key == pygame.K_SPACE:

                bullet = Bullet(ship)
                bullets.append(bullet)

        elif event.type == pygame.KEYUP:

            if event.key == pygame.K_UP:
                ship.moving_up = False

            elif event.key == pygame.K_DOWN:
                ship.moving_down = False

    screen.fill((230, 230, 230))

    ship.update()
    ship.blitme()

    for bullet in bullets[:]:

        bullet.update()
        bullet.draw_bullet(screen)

        if bullet.rect.left > 1200:
            bullets.remove(bullet)

    pygame.display.flip()