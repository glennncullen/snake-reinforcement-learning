import pygame
from app.edible import *
from app.snake import *


class Handler:
    __instance = None

    @staticmethod
    def get_instance():
        if Handler.__instance is None:
            Handler()
        return Handler.__instance

    def __init__(self):
        if Handler.__instance is not None:
            raise Exception("This is a Singleton!")
        else:
            Handler.__instance = self
        self.is_running = True
        self.window_size = (510, 510)
        self.play_area_size = [(10, 10), (10, 500), (500, 500), (500, 10)]
        self.play_area_boundaries = {
            'top border': 10,
            'bottom border': 500,
            'left border': 10,
            'right border': 500
        }
        self.directions = {
            'up': [],
            'down': [],
            'left': [],
            'right': []
        }
        self.run_speed = 100

        self.edible = Edible()
        self.snake = Snake()

    def update(self, button_pressed):

        if button_pressed[pygame.K_UP]:
            self.snake.move(self.directions['up'])
        if button_pressed[pygame.K_DOWN]:
            self.snake.move(self.directions['down'])
        if button_pressed[pygame.K_LEFT]:
            self.snake.move(self.directions['left'])
        if button_pressed[pygame.K_RIGHT]:
            self.snake.move(self.directions['right'])
        return None

    def next_frame(self, window):
        pygame.draw.lines(window, (255, 255, 255), True, self.play_area_size, 1)
        pygame.draw.rect(window, self.edible.colour, self.edible.get_position())

        # draw the snake
        for snake_bit in self.snake.body:
            pass

        pygame.display.update()
        return None

    def start(self):
        pygame.display.set_caption("Snake Reinforced Learning")
        return pygame.display.set_mode(self.window_size)
