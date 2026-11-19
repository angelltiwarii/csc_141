import pygame
import sys
import json
import random
from pathlib import Path

pygame.init()

# Screen settings
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Alien Invasion")

clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
GREEN = (80, 220, 130)
RED = (235, 90, 90)
YELLOW = (250, 215, 80)
BLUE = (90, 160, 245)
BLACK = (15, 20, 35)

# Fonts
font = pygame.font.SysFont(None, 30)
big_font = pygame.font.SysFont(None, 58)

HIGH_SCORE_FILE = Path(__file__).with_name("alien_high_score.json")


# Settings class
class Settings:

    def __init__(self):
        self.ship_speed = 5
        self.bullet_speed = 8
        self.alien_speed = 1
        self.alien_direction = 1
        self.alien_points = 50
        self.difficulty = "Easy"

    def set_difficulty(self, level):

        self.difficulty = level

        if level == "Easy":
            self.ship_speed = 5
            self.bullet_speed = 8
            self.alien_speed = 1

        elif level == "Medium":
            self.ship_speed = 5.5
            self.bullet_speed = 9
            self.alien_speed = 1.6

        elif level == "Hard":
            self.ship_speed = 6
            self.bullet_speed = 10
            self.alien_speed = 2.3


# Button class
class Button:

    def __init__(self, x, y, width, height, text):

        self.rect = pygame.Rect(x, y, width, height)
        self.text = text

    def draw(self, selected=False):

        color = GREEN if selected else BLUE

        pygame.draw.rect(
            screen, color, self.rect, border_radius=8
        )

        label = font.render(self.text, True, BLACK)

        screen.blit(
            label,
            label.get_rect(center=self.rect.center)
        )


# Ship class
class Ship:

    def __init__(self):

        self.rect = pygame.Rect(0, 0, 64, 34)

        self.rect.midbottom = (
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT - 25
        )

        self.x = float(self.rect.x)

        self.moving_left = False
        self.moving_right = False

    def update(self, settings):

        if self.moving_left and self.rect.left > 0:
            self.x -= settings.ship_speed

        if self.moving_right and self.rect.right < SCREEN_WIDTH:
            self.x += settings.ship_speed

        self.rect.x = round(self.x)

    def draw(self):

        points = [
            (self.rect.left, self.rect.bottom),
            (self.rect.centerx, self.rect.top),
            (self.rect.right, self.rect.bottom)
        ]

        pygame.draw.polygon(screen, GREEN, points)


# Alien class
class Alien:

    def __init__(self, x, y):

        self.rect = pygame.Rect(x, y, 38, 28)

    def draw(self):

        pygame.draw.rect(
            screen, RED, self.rect, border_radius=5
        )

        pygame.draw.circle(
            screen, WHITE,
            (self.rect.x + 10, self.rect.y + 10), 3
        )

        pygame.draw.circle(
            screen, WHITE,
            (self.rect.x + 28, self.rect.y + 10), 3
        )


# Bullet class
class Bullet:

    def __init__(self, x, y, speed, color, direction=-1):

        self.rect = pygame.Rect(x - 3, y - 10, 6, 14)

        self.y = float(self.rect.y)

        self.speed = speed
        self.color = color
        self.direction = direction

    def update(self):

        self.y += self.speed * self.direction

        self.rect.y = round(self.y)

    def draw(self):

        pygame.draw.rect(screen, self.color, self.rect)


# Game statistics
class GameStats:

    def __init__(self):

        self.score = 0
        self.high_score = self.load_high_score()
        self.game_active = False

    def load_high_score(self):

        try:
            with open(HIGH_SCORE_FILE) as file_object:
                return json.load(file_object)

        except (FileNotFoundError, ValueError, TypeError):
            return 0

    def save_high_score(self):

        with open(HIGH_SCORE_FILE, 'w') as file_object:
            json.dump(self.high_score, file_object)


# Main game class
class AlienInvasion:

    def __init__(self):

        self.settings = Settings()
        self.stats = GameStats()

        self.ship = Ship()

        self.bullets = []
        self.alien_bullets = []
        self.aliens = []

        self.play_button = Button(
            420, 280, 160, 55, "Play (P)"
        )

        self.level_buttons = [
            Button(300, 365, 120, 42, "Easy"),
            Button(440, 365, 120, 42, "Medium"),
            Button(580, 365, 120, 42, "Hard")
        ]

        self.create_fleet()

    # Create aliens
    def create_fleet(self):

        self.aliens = []

        for row in range(4):

            for col in range(10):

                alien = Alien(
                    70 + col * 82,
                    65 + row * 55
                )

                self.aliens.append(alien)

    # Start or restart game
    def start_game(self):

        self.stats.score = 0
        self.stats.game_active = True

        self.bullets.clear()
        self.alien_bullets.clear()

        self.ship.rect.midbottom = (
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT - 25
        )

        self.ship.x = float(self.ship.rect.x)

        self.create_fleet()

    # Check keyboard and mouse events
    def check_events(self):

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                self.stats.save_high_score()

                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:

                self.check_keydown_events(event)

            elif event.type == pygame.KEYUP:

                if event.key == pygame.K_LEFT:
                    self.ship.moving_left = False

                elif event.key == pygame.K_RIGHT:
                    self.ship.moving_right = False

            elif event.type == pygame.MOUSEBUTTONDOWN:

                if event.button == 1:
                    self.check_buttons(event.pos)

    # Check keyboard input
    def check_keydown_events(self, event):

        if event.key == pygame.K_q:

            self.stats.save_high_score()

            pygame.quit()
            sys.exit()

        elif event.key == pygame.K_p:

            if not self.stats.game_active:
                self.start_game()

        elif event.key == pygame.K_LEFT:

            self.ship.moving_left = True

        elif event.key == pygame.K_RIGHT:

            self.ship.moving_right = True

        elif event.key == pygame.K_SPACE:

            if self.stats.game_active and len(self.bullets) < 5:

                bullet = Bullet(
                    self.ship.rect.centerx,
                    self.ship.rect.top,
                    self.settings.bullet_speed,
                    YELLOW
                )

                self.bullets.append(bullet)

    # Check button clicks
    def check_buttons(self, pos):

        if self.stats.game_active:
            return

        for button in self.level_buttons:

            if button.rect.collidepoint(pos):

                self.settings.set_difficulty(button.text)
                return

        if self.play_button.rect.collidepoint(pos):

            self.start_game()

    # Update bullets
    def update_bullets(self):

        for bullet in self.bullets[:]:

            bullet.update()

            if bullet.rect.bottom < 0:

                self.bullets.remove(bullet)

    # Update aliens
    def update_aliens(self):

        hit_edge = any(
            alien.rect.right >= SCREEN_WIDTH
            or alien.rect.left <= 0
            for alien in self.aliens
        )

        if hit_edge:

            self.settings.alien_direction *= -1

            for alien in self.aliens:
                alien.rect.y += 22

        for alien in self.aliens:

            alien.rect.x += round(
                self.settings.alien_speed
                * self.settings.alien_direction
            )

            # Aliens occasionally shoot bullets
            if random.randrange(900) == 0:

                bullet = Bullet(
                    alien.rect.centerx,
                    alien.rect.bottom,
                    4,
                    RED,
                    direction=1
                )

                self.alien_bullets.append(bullet)

            if alien.rect.bottom >= self.ship.rect.top:

                self.end_game()

    # Check collisions between bullets and aliens
    def check_bullet_alien_collisions(self):

        for bullet in self.bullets[:]:

            hit_alien = None

            for alien in self.aliens:

                if bullet.rect.colliderect(alien.rect):

                    hit_alien = alien
                    break

            if hit_alien:

                self.aliens.remove(hit_alien)
                self.bullets.remove(bullet)

                self.stats.score += self.settings.alien_points

                if self.stats.score > self.stats.high_score:

                    self.stats.high_score = self.stats.score

        if not self.aliens and self.stats.game_active:

            self.start_new_level()

    # Start a new level
    def start_new_level(self):

        self.settings.alien_speed += 0.25

        self.bullets.clear()

        self.create_fleet()

    # Check alien bullets
    def check_ship_collisions(self):

        for bullet in self.alien_bullets[:]:

            bullet.update()

            if bullet.rect.top > SCREEN_HEIGHT:

                self.alien_bullets.remove(bullet)

            elif bullet.rect.colliderect(self.ship.rect):

                self.alien_bullets.remove(bullet)

                self.end_game()

    # End game
    def end_game(self):

        self.stats.game_active = False

        self.stats.save_high_score()

    # Display score
    def draw_hud(self):

        score_text = font.render(
            f"Score: {self.stats.score}",
            True, WHITE
        )

        high_score_text = font.render(
            f"High Score: {self.stats.high_score}",
            True, WHITE
        )

        level_text = font.render(
            f"Difficulty: {self.settings.difficulty}",
            True, WHITE
        )

        screen.blit(score_text, (20, 15))
        screen.blit(high_score_text, (200, 15))
        screen.blit(level_text, (450, 15))

    # Display start screen
    def draw_start_screen(self):

        title = big_font.render(
            "ALIEN INVASION", True, WHITE
        )

        screen.blit(
            title,
            title.get_rect(
                center=(SCREEN_WIDTH // 2, 190)
            )
        )

        self.play_button.draw()

        label = font.render(
            "Choose difficulty:", True, WHITE
        )

        screen.blit(
            label,
            label.get_rect(
                center=(SCREEN_WIDTH // 2, 340)
            )
        )

        for button in self.level_buttons:

            button.draw(
                selected=(
                    button.text == self.settings.difficulty
                )
            )

    # Update screen
    def update_screen(self):

        screen.fill(BLACK)

        self.draw_hud()

        if self.stats.game_active:

            self.ship.draw()

            for alien in self.aliens:
                alien.draw()

            for bullet in self.bullets:
                bullet.draw()

            for bullet in self.alien_bullets:
                bullet.draw()

        else:

            self.draw_start_screen()

        pygame.display.flip()

    # Main game loop
    def run_game(self):

        while True:

            self.check_events()

            if self.stats.game_active:

                self.ship.update(self.settings)

                self.update_bullets()

                self.update_aliens()

                self.check_bullet_alien_collisions()

                self.check_ship_collisions()

            self.update_screen()

            clock.tick(60)


if __name__ == "__main__":

    game = AlienInvasion()

    game.run_game()