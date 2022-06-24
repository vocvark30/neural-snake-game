# neural-snake-game

![snake_game](https://user-images.githubusercontent.com/107685702/175537627-2105e72b-d89a-4734-8c2d-f85f6c78d988.gif)

AI for a snake game

### Project have following scripts:
- <b>main</b> - play and write to database
- <b>game_learn</b> - create convolutional neural network model from games database and ai_games database
- <b>neural_game</b> - neural network plays
- <b>test_snake</b> - neural network plays many times without rendering graphics, games are written to ai_games database
- <b>information</b>- script for visualizing data from databases


### Project uses following libraries:
- <b>numpy</b> - all game data stored in numpy arrays
- <b>pygame</b> - for rendering
- <b>sqlite3</b> - databases with stored games
- <b>tensorflow</b>, <b>keras</b> - for creating and using neural networks
- <b>matplotlib</b> - to plot data
