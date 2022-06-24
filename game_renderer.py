import pygame


class GameRenderer:
    def __init__(self):
        pygame.init()

        self.screen_size = (640, 480)
        self.block_size = self.screen_size[1] // 16

        # empty, wall, food, snake, snake_first
        self.colors = ((150, 150, 150), (10, 10, 10), (255, 0, 0), (20, 200, 20), (10, 250, 10))

        self.screen_color = (255, 255, 255)
        self.screen = pygame.display.set_mode(self.screen_size)

    def draw_game(self, game):
        self.screen.fill(self.screen_color)
        game_map = game.get_map()

        for x in range(game.size):
            for y in range(game.size):
                pygame.draw.rect(self.screen, self.colors[game_map[x, y]],
                                 (self.block_size * x, self.block_size * (game.size - y - 1),
                                  self.block_size, self.block_size))

        pygame.display.flip()
