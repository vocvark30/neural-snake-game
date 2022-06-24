import numpy as np

import matplotlib.pyplot as plot
import sqlite3 as sql

with sql.connect("ai_games.sqlite3") as connection:
    cursor = connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM games WHERE ((score - 1) * 1.0 / steps) > 0.07 AND size = 10")

    for i in cursor.fetchall():
        print(i)

    cursor.execute("SELECT steps, score FROM games "
                   "WHERE size = 10 and steps > 50 ORDER BY 1.0 * (score - 1) / steps")

    steps = []
    score = []

    for i in cursor.fetchall():
        steps.append(i[0])
        score.append(i[1])

    steps = np.array(steps, dtype=float)
    score = np.array(score, dtype=float)

    print(f'size = {steps.size}')
    plot.plot((score - 1) / steps)
    plot.show()
