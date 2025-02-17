import math

import pygame
from app.edible import *
from app.snake import *
from ga.genetic_algorithm import GeneticAlgorithm
from ga.population import Population


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

        self.fuel = 130
        self.points = 0
        self.time_lasted = 0

        self.edible = Edible()
        self.snake = Snake()

        self.ga = GeneticAlgorithm()
        self.population = Population(50, True)
        self.current_snake = 0
        self.current_generation = 0

    def start(self):
        self.snake.create_head()
        pygame.display.set_caption("Snake Reinforced Learning")
        return pygame.display.set_mode(self.window_size)

    def update(self, button_pressed):
        # is_pressed = False
        # if button_pressed[pygame.K_UP] and self.current_direction is not self.directions['down']:
        #     self.snake.move(self.directions['up'])
        #     self.current_direction = self.directions['up']
        #     is_pressed = True
        # if button_pressed[pygame.K_DOWN] and self.current_direction is not self.directions['up']:
        #     self.snake.move(self.directions['down'])
        #     self.current_direction = self.directions['down']
        #     is_pressed = True
        # if button_pressed[pygame.K_LEFT] and self.current_direction is not self.directions['right']:
        #     self.snake.move(self.directions['left'])
        #     self.current_direction = self.directions['left']
        #     is_pressed = True
        # if button_pressed[pygame.K_RIGHT] and self.current_direction is not self.directions['left']:
        #     self.snake.move(self.directions['right'])
        #     self.current_direction = self.directions['right']
        #     is_pressed = True
        # if not is_pressed:
        #     self.snake.move(self.current_direction)

        if button_pressed[pygame.K_UP]:
            if self.run_speed > 0:
                self.run_speed -= 5
        if button_pressed[pygame.K_DOWN]:
            if self.run_speed < 300:
                self.run_speed += 5

        self.current_direction = self.calculate_move()
        self.snake.move(self.current_direction)

        self.fuel -= 1
        self.time_lasted += 1

        self.check_eating()
        self.check_dead()

    def next_frame(self, window):
        pygame.draw.lines(window, (255, 255, 255), True, self.play_area_size, 1)
        pygame.draw.rect(window, self.edible.colour, self.edible.get_position())

        # draw the snake
        for snake_bit in self.snake.body:
            pygame.draw.rect(window, snake_bit.colour, snake_bit.get_position())

        font = pygame.font.Font('freesansbold.ttf', 15)
        text_1 = "Fitness:    " + str(self.points)
        text_surface_1 = font.render(text_1, True, (255, 255, 255))
        text_area_1 = (10, 510)
        text_2 = "Generation: " + str(self.current_generation + 1)
        text_surface_2 = font.render(text_2, True, (255, 255, 255))
        text_area_2 = (10, 540)
        text_3 = "Snake:      " + str(self.current_snake + 1)
        text_surface_3 = font.render(text_3, True, (255, 255, 255))
        text_area_3 = (10, 570)
        text_4 = "Speed:      " + str(self.run_speed)
        text_surface_4 = font.render(text_4, True, (255, 255, 255))
        text_area_4 = (250, 570)
        window.blit(text_surface_1, text_area_1)
        window.blit(text_surface_2, text_area_2)
        window.blit(text_surface_3, text_area_3)
        window.blit(text_surface_4, text_area_4)

        pygame.display.update()
        return None

    def check_eating(self):
        if self.edible.get_position() == self.snake.body[0].get_position():
            self.snake.add_piece()
            self.points += 1
            self.edible.move_edible(self.snake.body, self.points)
            self.fuel = 130

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
        self.population.individuals[self.current_snake].fitness = math.pow(self.points, 2) + self.time_lasted
        self.fuel = 130
        self.points = 0
        self.current_snake += 1
        if self.current_snake >= len(self.population.individuals):
            self.population = self.ga.evolve(self.population)
            self.current_snake = 0
            self.current_generation += 1
        self.snake.body = []
        self.snake.create_head()
        self.current_direction = self.directions['right']
        self.edible.move_edible(self.snake.body, self.points)
        # print(cause_of_death)

    def calculate_move(self):
        input_weights = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        snake_head = self.snake.body[0]

        if self.current_direction is self.directions['up']:
            #checks for walls
            for i in range(5): # left
                if snake_head.x - (i+1*10) < self.play_area_boundaries["left"]:
                    break
                input_weights[0] -= 0.2
            for i in range(5): # left-up
                if snake_head.x - (i+1*10) < self.play_area_boundaries["left"] \
                        or snake_head.y - (i+1*10) < self.play_area_boundaries["top"]:
                    break
                input_weights[1] -= 0.2
            for i in range(5): # up
                if snake_head.y - (i+1*10) < self.play_area_boundaries["top"]:
                    break
                input_weights[2] -= 0.2
            for i in range(5): # right-up
                if snake_head.x + (i+1*10) > self.play_area_boundaries["right"] \
                        or snake_head.y - (i+1*10) < self.play_area_boundaries["top"]:
                    break
                input_weights[3] -= 0.2
            for i in range(5): # right
                if snake_head.x + (i+1*10) > self.play_area_boundaries["right"]:
                    break
                input_weights[4] -= 0.2

            # checks for edible


            #checks for tail


        snake_head = self.snake.body[0]
        distance_to_edible = []
        udlr = {
            'up': [snake_head.x, snake_head.y - 10],
            'down': [snake_head.x - 10, snake_head.y],
            'left': [snake_head.x + 10, snake_head.y],
            'right': [snake_head.x, snake_head.y + 10]
        }

        if self.current_direction is self.directions['up']:
            distance_to_edible = [
                math.sqrt(math.pow((udlr['up'][0] - self.edible.x), 2) +
                          math.pow((udlr['up'][1] - self.edible.y), 2)),
                0,
                math.sqrt(math.pow((udlr['left'][0] - self.edible.x), 2) +
                          math.pow((udlr['left'][1] - self.edible.y), 2)),
                math.sqrt(math.pow((udlr['right'][0] - self.edible.x), 2) +
                          math.pow((udlr['right'][1] - self.edible.y), 2))
            ]
        if self.current_direction is self.directions['down']:
            distance_to_edible = [
                0,
                math.sqrt(math.pow((udlr['down'][0] - self.edible.x), 2) +
                          math.pow((udlr['down'][1] - self.edible.y), 2)),
                math.sqrt(math.pow((udlr['left'][0] - self.edible.x), 2) +
                          math.pow((udlr['left'][1] - self.edible.y), 2)),
                math.sqrt(math.pow((udlr['right'][0] - self.edible.x), 2) +
                          math.pow((udlr['right'][1] - self.edible.y), 2))
            ]
        if self.current_direction is self.directions['left']:
            distance_to_edible = [
                math.sqrt(math.pow((udlr['up'][0] - self.edible.x), 2) +
                          math.pow((udlr['up'][1] - self.edible.y), 2)),
                math.sqrt(math.pow((udlr['down'][0] - self.edible.x), 2) +
                          math.pow((udlr['down'][1] - self.edible.y), 2)),
                math.sqrt(math.pow((udlr['left'][0] - self.edible.x), 2) +
                          math.pow((udlr['left'][1] - self.edible.y), 2)),
                0
            ]
        if self.current_direction is self.directions['right']:
            distance_to_edible = [
                math.sqrt(math.pow((udlr['up'][0] - self.edible.x), 2) +
                          math.pow((udlr['up'][1] - self.edible.y), 2)),
                math.sqrt(math.pow((udlr['down'][0] - self.edible.x), 2) +
                          math.pow((udlr['down'][1] - self.edible.y), 2)),
                0,
                math.sqrt(math.pow((udlr['right'][0] - self.edible.x), 2) +
                          math.pow((udlr['right'][1] - self.edible.y), 2))
            ]

        move_calculations = [
            self.population.individuals[self.current_snake].genes[0] * distance_to_edible[0] +
            self.population.individuals[self.current_snake].genes[1] * (udlr['up'][1] / 15),

            self.population.individuals[self.current_snake].genes[0] * distance_to_edible[1] +
            self.population.individuals[self.current_snake].genes[1] * (udlr['down'][1] / 15),

            self.population.individuals[self.current_snake].genes[0] * distance_to_edible[2] +
            self.population.individuals[self.current_snake].genes[1] * (udlr['left'][0] / 15),

            self.population.individuals[self.current_snake].genes[0] * distance_to_edible[3] +
            self.population.individuals[self.current_snake].genes[1] * (udlr['right'][0] / 15),
        ]

        remove_zero = []
        if distance_to_edible[0] != 0:
            remove_zero.append(move_calculations[0])
        if distance_to_edible[1] != 0:
            remove_zero.append(move_calculations[1])
        if distance_to_edible[2] != 0:
            remove_zero.append(move_calculations[2])
        if distance_to_edible[3] != 0:
            remove_zero.append(move_calculations[3])

        winner = min(remove_zero)

        if winner == move_calculations[0]:
            return self.directions['up']
        if winner == move_calculations[1]:
            return self.directions['down']
        if winner == move_calculations[2]:
            return self.directions['left']
        if winner == move_calculations[3]:
            return  self.directions['right']


