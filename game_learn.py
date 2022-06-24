import sqlite3 as sql
from tensorflow import keras
from keras.layers import Input, Dense, Flatten, Conv2D, Dropout, MaxPooling2D

from snake_game import *
from vector2 import *


def get_game_data(size: int, database):
    game_maps_data_list = []
    directions_data_list = []

    # get data from database
    with sql.connect(database) as connection:
        cursor = connection.cursor()
        cursor.execute(f'SELECT steps, score, game_maps, directions FROM games '
                       f'WHERE ((score - 1) * 1.0 / steps) > 0.06 AND steps > 50 AND size = {size}')

        # iterate over each game
        for game in cursor.fetchall():
            game_maps_data = np.frombuffer(game[2], dtype=np.int8).reshape((game[0], size, size))
            directions_data = np.frombuffer(game[3], dtype=np.int8).reshape((game[0], 2))

            # iterate over each step except last 2 and transform to vector form
            for i in range(game[0] - 2):
                game_maps_data_list.append(
                    np.eye(5)[game_maps_data[i]])  # transform: [0 1 2] => [[1 0 0], [0 1 0], [0 0 1]]
                directions_data_list.append(vectorMap[Vector2(directions_data[i][0],
                                                              directions_data[i][1])])

        x_data = np.array(game_maps_data_list, dtype=np.int8)
        y_data = np.array(directions_data_list, dtype=np.int8)

        return x_data, y_data


if __name__ == '__main__':
    map_size = 10
    x1, y1 = get_game_data(map_size, "games.sqlite3")
    x2, y2 = get_game_data(map_size, "ai_games.sqlite3")

    x = np.concatenate((x1, x2), axis=0)
    y = np.concatenate((y1, y2), axis=0)

    model = keras.Sequential()

    # size of map, map_enum
    model.add(Input((map_size, map_size, 5)))
    model.add(Conv2D(32, (2, 2), padding='same', activation='relu'))
    model.add(MaxPooling2D((2, 2), strides=2))
    model.add(Flatten())
    model.add(Dense(64, activation='relu'))
    model.add(Dropout(0.4))
    model.add(Dense(128, activation='relu'))
    model.add(Dropout(0.2))
    model.add(Dense(4, activation='softmax'))

    model.compile(optimizer=keras.optimizers.Adam(learning_rate=0.0001), loss='categorical_crossentropy')

    print(f'model = {model.summary()}')

    model.fit(x, y, epochs=60, batch_size=64, validation_split=0.15)

    model.save('model1.h5')
