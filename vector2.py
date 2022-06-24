class Vector2:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector2(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector2(self.x - other.x, self.y - other.y)

    def __mul__(self, x):
        return Vector2(self.x * x, self.y * x)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return f'(x = {self.x}, y = {self.y})'

    def __hash__(self):
        return hash((self.x, self.y))

    def copy(self):
        return Vector2(self.x, self.y)