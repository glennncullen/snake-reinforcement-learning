from app.snake_piece import *
from app.handler import *


class Snake:

    def __init__(self):
        self.handler = Handler.get_instance()
        self.body = [SnakePiece(50, 50, self.handler.directions['right'])]

    def add_piece(self):
        pass

    def move(self, direction):
        for piece in self.body:
            pass
        pass
