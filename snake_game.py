import numpy as np
import random

from vector2 import *


def direction_to_vector(direction_arg):
    arg = np.argmax(direction_arg)
    if arg == 0:
        return Vector2(1, 0)
    elif arg == 1:
        return Vector2(0, 1)
    elif arg == 2:
        return Vector2(-1, 0)
    elif arg == 3:
        return Vector2(0, -1)


# dictionary for vector encoding
vectorMap = {
    Vector2(1, 0): [1, 0, 0, 0],
    Vector2(0, 1): [0, 1, 0, 0],
    Vector2(-1, 0): [0, 0, 1, 0],
    Vector2(0, -1): [0, 0, 0, 1]
}


# Map enum
class Map:
    EMPTY = 0
    WALL = 1
    FOOD = 2
    SNAKE = 3
    SNAKE_FIRST = 4


class SnakeGame:
    """
    Main class for game processing
    """

    def __init__(self, size):
        """
        :param size: size of square map
        """

        self.size = size
        self.game_map = np.zeros((size, size), np.int8)

        self.create_walls()
        self.create_food()

        self.snake = [Vector2(size // 2, size // 2)]  # initial position
        self.direction = Vector2(0, 1)  # initial direction

    def create_walls(self):
        for i in range(self.size):
            self.game_map[0, i] = Map.WALL
            self.game_map[self.size - 1, i] = Map.WALL
            self.game_map[i, 0] = Map.WALL
            self.game_map[i, self.size - 1] = Map.WALL

    def create_food(self):
        x = random.randint(1, self.size - 2)
        y = random.randint(1, self.size - 2)

        self.game_map[x, y] = Map.FOOD

    def snake_step(self, direction : Vector2):
        self.direction = direction

        new_position = self.snake[0] + direction

        if new_position.x < 0 or new_position.x >= self.size or \
                new_position.y < 0 or new_position.y >= self.size:
            return False

        if self.game_map[new_position.x, new_position.y] == Map.WALL:
            return False

        for i in self.snake:
            if new_position.x == i.x and new_position.y == i.y:
                return False

        if self.game_map[new_position.x, new_position.y] == Map.FOOD:
            self.game_map[new_position.x, new_position.y] = Map.EMPTY
            self.create_food()
        else:
            self.snake.pop()

        self.snake.insert(0, new_position)
        return True

    def get_map(self):
        new_game_map = self.game_map.copy()
        for i in self.snake:
            new_game_map[i.x, i.y] = Map.SNAKE

        new_game_map[self.snake[0].x, self.snake[0].y] = Map.SNAKE_FIRST
        return new_game_map

    def snake_safety(self):
        new_positions = [
            Vector2(self.snake[0].x + 1, self.snake[0].y),
            Vector2(self.snake[0].x - 1, self.snake[0].y),
            Vector2(self.snake[0].x, self.snake[0].y + 1),
            Vector2(self.snake[0].x, self.snake[0].y - 1)
        ]

        snake_map = self.get_map()

        for position in new_positions:
            if (position != self.snake[0] - self.direction) and \
                    (snake_map[position.x, position.y] == Map.WALL or snake_map[position.x, position.y] == Map.SNAKE):
                return False

        return True
