from random import *


class Edible:

    def __init__(self):
        self.colour = (0, 255, 0)
        self.x, self.y = randint(1, 49) * 10, randint(1, 49) * 10
        self.size = 10

    def get_position(self):
        return self.x, self.y, self.size, self.size

    def move_edible(self, snake):
        self.x, self.y = randint(1, 49) * 10, randint(1, 49) * 10
        for snake_bit in snake:
            if self.get_position() == snake_bit.get_position():
                self.move_edible(snake)
                break
