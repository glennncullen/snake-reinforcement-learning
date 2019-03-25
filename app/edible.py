from random import *


class Edible:

    def __init__(self):
        self. learning_positions = [[300, 200], [350, 70], [40, 80]]
        self.colour = (0, 255, 0)
        # self.x, self.y = randint(1, 49) * 10, randint(1, 49) * 10
        self.x, self.y = 300, 200
        self.size = 10

    def get_position(self):
        return self.x, self.y, self.size, self.size

    def move_edible(self, snake, fitness):
        if fitness > 2:
            self.x, self.y = randint(1, 49) * 10, randint(1, 49) * 10
        else:
            self.x, self.y = self.learning_positions[fitness][0], self.learning_positions[fitness][1]
        for snake_bit in snake:
            if self.get_position() == snake_bit.get_position():
                self.move_edible(snake, fitness)
                break
