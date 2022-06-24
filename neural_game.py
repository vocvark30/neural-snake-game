import numpy as np
import keras

from game_renderer import *
from snake_game import *


class NeuralSnakeGame:
    def __init__(self, size, random_moves, k, name):
        self.random_moves = random_moves
        self.k = k
        self.size = size
        self.model = keras.models.load_model(name)

        self.game = SnakeGame(size)
        self.direction = Vector2(0, 1)
        self.new_direction = self.direction

        self.game_run = True

    def process_move(self):
        game_map = self.game.get_map()

        input_vector = np.eye(5)[game_map][np.newaxis]
        predict = self.model.predict(input_vector)

        # add random moves
        if self.random_moves and self.game.snake_safety() and random.uniform(0.0, 1.0) < self.k:
            predict[0][np.argmax(predict)] = 0.0

        self.new_direction = direction_to_vector(predict[0])

        if self.new_direction != self.direction * (-1) and self.new_direction != Vector2(0, 0):
            self.direction = self.new_direction

        self.game_run = self.game.snake_step(self.direction)


if __name__ == '__main__':
    run = True
    while run:
        neural_snake = NeuralSnakeGame(size=10, random_moves=True, k=0.05, name='model1.h5')
        renderer = GameRenderer()

        time1 = pygame.time.get_ticks() / 1000
        delay = 0.01

        while neural_snake.game_run and run:
            renderer.draw_game(neural_snake.game)
            if (pygame.time.get_ticks() / 1000) - time1 >= delay:
                neural_snake.process_move()
                time1 = pygame.time.get_ticks() / 1000

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

        pygame.quit()
