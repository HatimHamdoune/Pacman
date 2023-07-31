import Sprites
import pygame

class Game:
    WINDOW_SIZE = 600
    def __init__(self) -> None:
        self.window_size = Game.WINDOW_SIZE
        self.window = pygame.display.set_mode((self.window_size, self.window_size))
        pygame.display.set_caption("Pacman")
        self.clock = pygame.time.Clock()

        pacman_sprite_location, pacman_n_sprites, pacman_width, pacman_height = 848, 12, 51, 49
        self.pacman = Sprites.Pacman("SpriteSheet.png", pacman_sprite_location, pacman_n_sprites, pacman_width, pacman_height)
        self.ghosts = []
        fruit_sprite_location, fruit_n_sprites, fruit_width, fruit_height = 596, 7, 53, 49
        self.fruits = Sprites.Fruits("Spritesheet.png", fruit_sprite_location, fruit_n_sprites, fruit_width, fruit_height)
        self.lives = 3

        self.game_still_ongoing = True
        self.level_won = False
        self.level_lost = False

        self.main_loop()

    def initialize_ghosts(self):
        starting_ghost_position = 644
        number_of_sprites = 8
        ghost_width = 51
        ghost_height = 49
        for i in range(4):
            self.ghosts.append(Sprites.Ghost("SpriteSheet.png", starting_ghost_position + (ghost_height * i), number_of_sprites, ghost_width, ghost_height))

    
if __name__ == "__main__":
    Game()