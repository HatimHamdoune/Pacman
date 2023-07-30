import Sprites
import pygame

class Game:
    WINDOW_SIZE = 600
    def __init__(self) -> None:
        self.__map = Map()
        self.window_size = Game.WINDOW_SIZE
        self.window = pygame.display.set_mode(self.window_size, self.window_size)
        pygame.display.set_caption("Pacman")
        self.clock = pygame.time.Clock()

        self.pacman = Sprites.Pacman()
        self.ghosts = []
        self.lives = 3

        self.game_still_ongoing = True
        self.level_won = False
        self.level_lost = False

        self.main_loop()