import pygame
from app.edible import *
from app.snake import *


class Handler:
    __instance = None

    @staticmethod
    def get_instance():
        if Handler.__instance is None:
            __instance = Handler()
        return Handler.__instance

    def __init__(self):
        if Handler.__instance is not None:
            raise Exception("This is a Singleton!")
        else:
            Handler.__instance = self
        self.is_running = True
        self.window_size = (510, 600)
        self.play_area_size = [(10, 10), (10, 500), (500, 500), (500, 10)]
        self.play_area_boundaries = {
            'top border': 10,
            'bottom border': 490,
            'left border': 10,
            'right border': 490
        }
        self.directions = {
            'up': [0, -10],
            'down': [0, 10],
            'left': [-10, 0],
            'right': [10, 0]
        }
        self.current_direction = self.directions['right']

        self.run_speed = 100

        self.fuel = 2500
        self.points = 0

        self.edible = Edible()
        self.snake = Snake()


    def start(self):
        self.snake.create_head()
        pygame.display.set_caption("Snake Reinforced Learning")
        return pygame.display.set_mode(self.window_size)

    def update(self, button_pressed):
        is_pressed = False
        if button_pressed[pygame.K_UP] and self.current_direction is not self.directions['down']:
            self.snake.move(self.directions['up'])
            self.current_direction = self.directions['up']
            is_pressed = True
        if button_pressed[pygame.K_DOWN] and self.current_direction is not self.directions['up']:
            self.snake.move(self.directions['down'])
            self.current_direction = self.directions['down']
            is_pressed = True
        if button_pressed[pygame.K_LEFT] and self.current_direction is not self.directions['right']:
            self.snake.move(self.directions['left'])
            self.current_direction = self.directions['left']
            is_pressed = True
        if button_pressed[pygame.K_RIGHT] and self.current_direction is not self.directions['left']:
            self.snake.move(self.directions['right'])
            self.current_direction = self.directions['right']
            is_pressed = True
        if not is_pressed:
            self.snake.move(self.current_direction)

        self.fuel -= 1

        self.check_eating()
        self.check_dead()

    def next_frame(self, window):
        pygame.draw.lines(window, (255, 255, 255), True, self.play_area_size, 1)
        pygame.draw.rect(window, self.edible.colour, self.edible.get_position())

        # draw the snake
        for snake_bit in self.snake.body:
            pygame.draw.rect(window, snake_bit.colour, snake_bit.get_position())

        text_1 = "Fitness: " + str(self.points)
        font = pygame.font.Font('freesansbold.ttf',15)
        text_surface = font.render(text_1, True, (255, 255, 255))
        text_area = (10, 510)
        window.blit(text_surface, text_area)

        pygame.display.update()
        return None

    def check_eating(self):
        if self.edible.get_position() == self.snake.body[0].get_position():
            self.edible.move_edible(self.snake.body)
            self.snake.add_piece()
            self.points += 1
            self.fuel = 2500

    def check_dead(self):
        if self.fuel <= 0:
            self.funeral_arrangements("No fuel")
        if self.snake.body[0].x < self.play_area_boundaries['left border']:
            self.funeral_arrangements("OOB left")
        if self.snake.body[0].x > self.play_area_boundaries['right border']:
            self.funeral_arrangements("OOB right")
        if self.snake.body[0].y < self.play_area_boundaries['top border']:
            self.funeral_arrangements("OOB top")
        if self.snake.body[0].y > self.play_area_boundaries['bottom border']:
            self.funeral_arrangements("OOB bottom")
        for snake_bit in self.snake.body:
            if snake_bit is self.snake.body[0]:
                continue
            if snake_bit.get_position() == self.snake.body[0].get_position():
                self.funeral_arrangements("ate himself")

    def funeral_arrangements(self, cause_of_death):
        print(cause_of_death)
        pass
