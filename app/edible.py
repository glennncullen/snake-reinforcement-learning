from random import *


class Edible:

    def __init__(self):
        self.colour = (0, 255, 0)
        self.x, self.y = randint(1, 49) * 10, randint(1, 49) * 10
        self.size = 10

    def get_position(self):
        return self.x, self.y, self.size, self.size

    def move_edible(self):
        self.x, self.y = randint(1, 49) * 10, randint(1, 49) * 10
