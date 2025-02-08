""""
This is a simple game in python 
that is similar to the popular game 'flappy bird'
"""

import pygame
import random
import os

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

# Game settings
GRAVITY = 0.5
FLAP_STRENGTH = -10
PIPE_WIDTH = 70
PIPE_HEIGHT = 500
PIPE_GAP = 150
PIPE_SPEED = 3

# Load images
BIRD_IMAGES = [pygame.image.load(f"bird_frame_{i}.png") for i in range(3)]
PIPE_IMAGE = pygame.image.load("pipe_detailed.png")
BACKGROUND_IMAGE = pygame.image.load("background_detailed.png")

# Load sounds
FLAP_SOUND = pygame.mixer.Sound("flap.wav")
SCORE_SOUND = pygame.mixer.Sound("score.wav")
HIT_SOUND = pygame.mixer.Sound("hit.wav")

# Bird class
class Bird:
    def __init__(self):
        self.images = BIRD_IMAGES
        self.image_index = 0
        self.image = self.images[self.image_index]
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2)
        self.velocity = 0
        self.animation_counter = 0

    def update(self):
        self.velocity += GRAVITY
        self.rect.y += self.velocity
        self.animation_counter += 1
        if self.animation_counter % 5 == 0:
            self.image_index = (self.image_index + 1) % len(self.images)
            self.image = self.images[self.image_index]

    def flap(self):
        self.velocity = FLAP_STRENGTH
        FLAP_SOUND.play()

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def get_rect(self):
        return self.rect

# Pipe class
class Pipe:
    def __init__(self, x):
        self.image = PIPE_IMAGE
        self.rect_top = self.image.get_rect()
        self.rect_bottom = self.image.get_rect()
        self.rect_top.x = x
        self.rect_bottom.x = x
        self.rect_top.y = random.randint(-PIPE_HEIGHT + PIPE_GAP, 0)
        self.rect_bottom.y = self.rect_top.y + PIPE_HEIGHT + PIPE_GAP

    def update(self):
        self.rect_top.x -= PIPE_SPEED
        self.rect_bottom.x -= PIPE_SPEED

    def draw(self, screen):
        screen.blit(self.image, self.rect_top)
        screen.blit(self.image, self.rect_bottom)

    def get_rects(self):
        return self.rect_top, self.rect_bottom

# Function to display the start menu
def display_start_menu(screen, font):
    screen.fill(WHITE)
    title_text = font.render("Flappy Bird", True, BLACK)
    start_text = font.render("Press SPACE to Start", True, BLACK)
    screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, SCREEN_HEIGHT // 3))
    screen.blit(start_text, (SCREEN_WIDTH // 2 - start_text.get_width() // 2, SCREEN_HEIGHT // 2))
    pygame.display.flip()

# Function to display the scoreboard
def display_scoreboard(screen, font, score):
    screen.fill(WHITE)
    score_text = font.render(f'Your Score: {score}', True, BLACK)
    restart_text = font.render("Press SPACE to Restart", True, BLACK)
    screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 3))
    screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2))
    pygame.display.flip()

# Main game function
def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Flappy Bird")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 36)

    # Display start menu
    display_start_menu(screen, font)
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False

    bird = Bird()
    pipes = [Pipe(SCREEN_WIDTH + i * (PIPE_WIDTH + 200)) for i in range(3)]
    score = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.flap()

        bird.update()
        for pipe in pipes:
            pipe.update()
            if pipe.rect_top.right < 0:
                pipes.remove(pipe)
                pipes.append(Pipe(SCREEN_WIDTH + PIPE_WIDTH))
                score += 1
                SCORE_SOUND.play()

        # Check for collisions
        for pipe in pipes:
            if bird.get_rect().colliderect(pipe.get_rects()[0]) or bird.get_rect().colliderect(pipe.get_rects()[1]):
                HIT_SOUND.play()
                running = False

        screen.blit(BACKGROUND_IMAGE, (0, 0))
        bird.draw(screen)
        for pipe in pipes:
            pipe.draw(screen)

        # Draw score
        score_text = font.render(f'Score: {score}', True, BLACK)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(30)

    # Display scoreboard
    display_scoreboard(screen, font, score)
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    main()
                    return

    pygame.quit()

if __name__ == "__main__":
    main()
