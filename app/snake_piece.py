class SnakePiece:

    def __init__(self, x, y):
        self.colour = (255, 0, 0)
        self.x, self.y = x, y
        self.size = 10

    def get_position(self):
        return self.x, self.y, self.size, self.size

    def move(self, direction):
        self.x, self.y = direction[0], direction[1]

    def change_direction(self, direction):
        self.x, self.y = self.x + direction[0], self.y + direction[1]

    def get_x_y(self):
        return [self.x, self.y]
