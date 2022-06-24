from neural_game import *

import sqlite3 as sql
import numpy as np

if __name__ == '__main__':
    games_count = 10
    max_steps = 250

    total_steps = 0
    total_score = 0

    with sql.connect("ai_games.sqlite3") as connection:
        cursor = connection.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS games "
                       "(size INTEGER, steps INTEGER, score INTEGER, game_maps BLOB, directions BLOB)")

        model = keras.models.load_model('model1.h5')

        for i in range(games_count):
            neural_snake = NeuralSnakeGame(size=10, random_moves=True, k=0.1, name='model1.h5')

            game_maps_list = []
            directions_list = []

            steps = 0

            while neural_snake.game_run and steps < max_steps:
                game_maps_list.append(neural_snake.game.get_map())

                neural_snake.process_move()

                directions_list.append(neural_snake.direction.copy())
                steps += 1

            if len(neural_snake.game.snake) > 3:
                game_maps_array = np.array(game_maps_list, dtype=np.int8)
                directions_array = np.array(
                    [(direction.x, direction.y) for direction in directions_list], dtype=np.int8)

                cursor.execute("insert into games values (?, ?, ?, ?, ?)",
                               (neural_snake.size, steps, len(neural_snake.game.snake), game_maps_array.tobytes(),
                                directions_array.tobytes()))

            total_steps += steps
            total_score += len(neural_snake.game.snake) - 1
            print(f'Game {i} score = {len(neural_snake.game.snake)}, steps = {steps}')

    print(
        f'Total steps = {total_steps}, total score = {total_score}, value = {np.around(total_score / total_steps, 3)}')
