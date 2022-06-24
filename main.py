from game_renderer import *
from snake_game import *

import sqlite3 as sql
import numpy as np
import pygame

if __name__ == '__main__':

    with sql.connect("games.sqlite3") as connection:
        cursor = connection.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS games "
                       "(size INTEGER, steps INTEGER, score INTEGER, game_maps BLOB, directions BLOB)")

        run = True
        while run:
            size = 10

            renderer = GameRenderer()

            game = SnakeGame(size)

            direction = Vector2(0, 1)
            new_direction = direction

            time1 = pygame.time.get_ticks() / 1000
            delay = 0.2  # between 2 steps
            pause_step = True
            move = False

            game_maps = []
            directions = []

            steps = 0

            game_run = True
            while game_run and run:
                renderer.draw_game(game)

                if (pause_step and move) or (not pause_step and (pygame.time.get_ticks() / 1000) - time1 >= delay):
                    time1 = (pygame.time.get_ticks() / 1000)

                    # check direction
                    if new_direction != direction * (-1) and new_direction != Vector2(0, 0):
                        direction = new_direction

                    # write current state to lists
                    game_maps.append(game.get_map())
                    directions.append(direction.copy())

                    # take step
                    game_run = game.snake_step(direction)
                    move = False
                    steps += 1

                # process input
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                    if event.type == pygame.KEYDOWN:
                        new_direction = Vector2(0, 0)
                        if event.key == pygame.K_LEFT:
                            new_direction = Vector2(-1, 0)
                            move = True
                        elif event.key == pygame.K_RIGHT:
                            new_direction = Vector2(1, 0)
                            move = True
                        elif event.key == pygame.K_DOWN:
                            new_direction = Vector2(0, -1)
                            move = True
                        elif event.key == pygame.K_UP:
                            new_direction = Vector2(0, 1)
                            move = True

            pygame.quit()

            if len(game.snake) > 2:
                # convert lists to numpy arrays to write them to database
                game_maps_array = np.array(game_maps, dtype=np.int8)
                directions_array = np.array([(direction.x, direction.y) for direction in directions],
                                            dtype=np.int8)

                cursor.execute("INSERT INTO games VALUES (?, ?, ?, ?, ?)",
                               (size, steps, len(game.snake), game_maps_array.tobytes(), directions_array.tobytes()))
                print(f'score / steps = {(len(game.snake) - 1) / steps}')
