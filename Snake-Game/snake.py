# snake.py - Classic Snake game using pygame
# Run with:  python3 snake.py

import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Screen settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRID_SIZE = 20

# Colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)

FPS = 10  # game speed

class Snake:
    def __init__(self):
        # Start in center
        self.body = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = (GRID_SIZE, 0)  # moving right
        self.grow_pending = False

    def move(self):
        """Move snake one step. Return False if it dies."""
        head_x, head_y = self.body[0]
        dx, dy = self.direction
        new_head = (head_x + dx, head_y + dy)

        # Wall collision
        if (
            new_head[0] < 0 or new_head[0] >= SCREEN_WIDTH or
            new_head[1] < 0 or new_head[1] >= SCREEN_HEIGHT
        ):
            return False

        # Self collision
        if new_head in self.body:
            return False

        # Add new head
        self.body.insert(0, new_head)

        # Remove tail unless we just ate food
        if not self.grow_pending:
            self.body.pop()
        else:
            self.grow_pending = False

        return True

    def grow(self):
        self.grow_pending = True

    def set_direction(self, direction):
        """Change direction (no 180° turns)."""
        if (direction[0] * -1, direction[1] * -1) != self.direction:
            self.direction = direction

    def draw(self, screen):
        for segment in self.body:
            rect = pygame.Rect(segment[0], segment[1], GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(screen, GREEN, rect)
            pygame.draw.rect(screen, WHITE, rect, 1)


class Food:
    def __init__(self):
        self.position = self.random_position()

    def random_position(self):
        x = random.randint(0, (SCREEN_WIDTH - GRID_SIZE) // GRID_SIZE) * GRID_SIZE
        y = random.randint(0, (SCREEN_HEIGHT - GRID_SIZE) // GRID_SIZE) * GRID_SIZE
        return (x, y)

    def draw(self, screen):
        rect = pygame.Rect(self.position[0], self.position[1], GRID_SIZE, GRID_SIZE)
        pygame.draw.rect(screen, RED, rect)


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Snake Game - Samarth")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)

        self.snake = Snake()
        self.food = Food()
        self.score = 0
        self.game_over = False

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.snake.set_direction((0, -GRID_SIZE))
                elif event.key == pygame.K_DOWN:
                    self.snake.set_direction((0, GRID_SIZE))
                elif event.key == pygame.K_LEFT:
                    self.snake.set_direction((-GRID_SIZE, 0))
                elif event.key == pygame.K_RIGHT:
                    self.snake.set_direction((GRID_SIZE, 0))

        return True

    def update(self):
        if not self.snake.move():
            self.game_over = True
            return

        # Check if snake ate food
        if self.snake.body[0] == self.food.position:
            self.snake.grow()
            self.food.position = self.food.random_position()
            self.score += 10

    def draw(self):
        self.screen.fill(BLACK)

        self.snake.draw(self.screen)
        self.food.draw(self.screen)

        # Draw score
        score_text = self.font.render(f"Score: {self.score}", True, YELLOW)
        self.screen.blit(score_text, (10, 10))

        if self.game_over:
            over_text = self.font.render("GAME OVER! Press Q to quit.", True, RED)
            rect = over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            self.screen.blit(over_text, rect)

        pygame.display.flip()

    def run(self):
        running = True
        while running:
            running = self.handle_input()

            if not self.game_over:
                self.update()
            else:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                        running = False

            self.draw()
            self.clock.tick(FPS)

        print(f"Final score: {self.score}")
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = Game()
    game.run()

