from app.snake_piece import *
from app.handler import *


class Snake:

    def __init__(self):
        self.body = []

    def create_head(self):
        self.body = [SnakePiece(50, 50)]

    def add_piece(self):
        self.body.append(SnakePiece(-10, -10))

    def move(self, direction):
        for i in range(len(self.body), 0, -1):
            index = i - 1
            if index == 0:
                self.body[index].change_direction(direction)
                break
            self.body[index].move(self.body[index-1].get_x_y())
