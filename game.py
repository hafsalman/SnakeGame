import pygame
from pygame.locals import *
import time
import random

SIZE = 40
WINDOW = 600
GRID = WINDOW // SIZE

class Food:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.image = pygame.image.load("food.jpg").convert()
        self.image = pygame.transform.scale(self.image, (SIZE, SIZE))
        self.move()

    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))

    def move(self):
        self.x = random.randint(0, GRID - 1) * SIZE
        self.y = random.randint(0, GRID - 1) * SIZE

class Snake:
    def __init__(self, parent_screen, length):
        self.length = length
        self.parent_screen = parent_screen
        self.block = pygame.image.load("block.png").convert()
        self.block = pygame.transform.scale(self.block, (SIZE, SIZE))
        self.x = [SIZE] * length
        self.y = [SIZE] * length
        self.direction = "down"

    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)

    def draw(self):
        self.parent_screen.fill((255, 255, 255))
        for i in range(self.length):
            self.parent_screen.blit(self.block, (self.x[i], self.y[i]))

    def move_left(self):
        self.direction = "left"

    def move_right(self):
        self.direction = "right"

    def move_up(self):
        self.direction = "up"

    def move_down(self):
        self.direction = "down"

    def walk(self):
        for i in range(self.length - 1, 0, -1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]

        if self.direction == "left":
            self.x[0] -= SIZE
        if self.direction == "right":
            self.x[0] += SIZE
        if self.direction == "up":
            self.y[0] -= SIZE
        if self.direction == "down":
            self.y[0] += SIZE

        self.draw()

class Game:
    def __init__(self):
        pygame.init()
        self.surface = pygame.display.set_mode((WINDOW, WINDOW))
        self.snake = Snake(self.surface, 1)
        self.food = Food(self.surface)

    def is_collision(self, x1, y1, x2, y2):
        if x1 >= x2 and x1 < x2 + SIZE:
            if y1 >= y2 and y1 < y2 + SIZE:
                return True
        return False

    def play(self):
        self.snake.walk()
        self.food.draw()

        if self.is_collision(self.snake.x[0], self.snake.y[0], self.food.x, self.food.y):
            self.food.move()
            self.snake.increase_length()

        if (self.snake.x[0] < 0 or self.snake.x[0] >= WINDOW or
            self.snake.y[0] < 0 or self.snake.y[0] >= WINDOW):
            print("Game Over!")
            pygame.quit()
            quit()

    def run(self):
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False

                    if event.key == pygame.K_UP:
                        self.snake.move_up()

                    if event.key == pygame.K_DOWN:
                        self.snake.move_down()

                    if event.key == pygame.K_LEFT:
                        self.snake.move_left()

                    if event.key == pygame.K_RIGHT:
                        self.snake.move_right()

                elif event.type == pygame.QUIT:
                    running = False

            self.play()
            pygame.display.update()
            time.sleep(0.2)

if __name__ == "__main__":
    game = Game()
    game.run()