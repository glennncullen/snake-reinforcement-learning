class SnakePiece:

    def __init__(self, x, y, direction):
        self.colour = (255, 0, 0)
        self.x, self.y = x, y
        self.size = 10
        self.direction = direction

    def get_position(self):
        return self.x, self.y, self.size, self.size

    def move(self):
        pass

    def change_direction(self, direction):
        self.direction = direction
