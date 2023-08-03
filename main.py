import Sprites
import pygame

class Game:
    WINDOW_HEIGHT = 680
    WINDOW_WIDTH = 578
    def __init__(self) -> None:
        self.window_size = Game.WINDOW_WIDTH, Game.WINDOW_HEIGHT
        self.window = pygame.display.set_mode(self.window_size)
        pygame.display.set_caption("Pacman")
        self.clock = pygame.time.Clock()

        self.map = Map()
        pacman_sprite_location, pacman_n_sprites, pacman_width, pacman_height = 848, 12, 51, 49
        self.pacman = Sprites.Pacman("SpriteSheet.png", pacman_sprite_location, pacman_n_sprites, pacman_width, pacman_height)
        self.ghosts = []
        fruit_sprite_location, fruit_n_sprites, fruit_width, fruit_height = 596, 7, 53, 49
        self.fruits = Sprites.Fruits("Spritesheet.png", fruit_sprite_location, fruit_n_sprites, fruit_width, fruit_height)
        self.lives = 3

        self.game_still_ongoing = True
        self.level_won = False
        self.level_lost = False

        # self.initialize_ghosts()
        self.main_loop()

        

    def initialize_ghosts(self):
        starting_ghost_position = 644
        number_of_sprites = 8
        ghost_width = 51
        ghost_height = 49
        for i in range(4):
            self.ghosts.append(Sprites.Ghost("SpriteSheet.png", starting_ghost_position + (ghost_height * i), number_of_sprites, ghost_width, ghost_height))

    def main_loop(self):
        while True:
            self.check_events()
            self.check_input()
            self.refresh_screen()
    
    def check_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    self.pacman.reset_directions()
                    self.pacman.looking_left = True
                elif event.key == pygame.K_d:
                    self.pacman.reset_directions()
                    self.pacman.looking_right = True
                elif event.key == pygame.K_w:
                    self.pacman.reset_directions()
                    self.pacman.looking_up = True
                elif event.key == pygame.K_s:
                    self.pacman.reset_directions()
                    self.pacman.looking_down = True
    
    def check_events(self):
        self.pacman.move(self.map)
         
    def refresh_screen(self):
        self.window.fill((0, 0, 0))
        self.window.blit(self.pacman.sprite_collection[self.pacman._current_model], (self.pacman.x_coordinate, self.pacman.y_coordinate))
        self.window.blit(self.map.map_image, (0, 0)) 
        for ghost in self.ghosts:
            self.window.blit(ghost.sprite_collection[ghost._current_model], (ghost.x_coordinate, ghost.y_coordinate))
        pygame.display.flip()
        self.clock.tick(60)
        

class Map:
    def __init__(self) -> None:
        self.map_image = pygame.image.load("maze.png")
        self.wall_coordinates = {}
        self.height = self.map_image.get_height()
        self.width = self.map_image.get_width()
        self.initialize_map()

    
    def initialize_map(self):
        for i in range(self.width):
            for j in range(self.height):
                current_pixel = self.map_image.get_at((i, j))
                if current_pixel.a != 0:
                    if i not in self.wall_coordinates:
                        self.wall_coordinates[i] = [j]
                    else:
                        self.wall_coordinates[i].append(j)
    
if __name__ == "__main__":
    Game()