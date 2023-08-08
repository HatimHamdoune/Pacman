import Characters
import pygame

class Game:
    #constants to represent the window size
    WINDOW_HEIGHT = 670
    WINDOW_WIDTH = 560
    def __init__(self) -> None:
        self.window_size = Game.WINDOW_WIDTH, Game.WINDOW_HEIGHT
        self.window = pygame.display.set_mode(self.window_size)
        pygame.display.set_caption("Pacman")
        self.clock = pygame.time.Clock()
        pacman_icon = pygame.image.load("pacman.ico")
        pygame.display.set_icon(pacman_icon)

        self.map = Map("SpriteSheet.png", 0)
        self.pacman = Characters.Pacman("SpriteSheet.png")

        self.main_loop()

        

    def main_loop(self):
        self.new_game()
        while True:
            self.check_events()
            self.check_input()
            self.refresh_screen()
    
    def new_game(self):
        pygame.mixer.init()
        pygame.mixer.music.load("./audio/beginning.wav")
        pygame.mixer.music.play()


    def check_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    self.pacman.turn("left", self.map)
                elif event.key == pygame.K_d:
                    self.pacman.turn("right", self.map)
                elif event.key == pygame.K_w:
                    self.pacman.turn("up", self.map)
                elif event.key == pygame.K_s:
                    self.pacman.turn("down", self.map)
    
    def check_events(self):
        self.pacman.move(self.map)
         
    def refresh_screen(self):
        self.window.fill((0, 0, 0))
        for row in range(len(self.map.map_matrix)):
            for column in range(len(self.map.map_matrix[row])):
                if self.map.map_matrix[row][column] == 1:
                    self.window.blit(self.map.empty_block, (column * self.map.tile_size, row * self.map.tile_size))
                else:
                    self.window.blit(self.map.map_tiles[row][column], (column * self.map.tile_size, row * self.map.tile_size))
        self.window.blit(self.pacman.model, (self.pacman.x_coordinate, self.pacman.y_coordinate))
        pygame.display.flip()
        self.clock.tick(9)
        

class Map:
    #hard coded the map dimensions and tile size
    MAP_HEIGHT = 620
    MAP_WIDTH = 560
    TILE_SIZE = 20
    def __init__(self, filename, map_start_x) -> None:
        self.spritesheet = pygame.image.load(filename)
        self.tile_size = Map.TILE_SIZE
        self.map_tiles = self.initialize_map(map_start_x)
        #a tile from the initiated map
        self.empty_block = self.map_tiles[14][0] 
        self.map_matrix = [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                           [0,2,2,2,2,2,2,2,2,2,2,2,2,0,0,2,2,2,2,2,2,2,2,2,2,2,2,0],
                           [0,2,0,0,0,0,2,0,0,0,0,0,2,0,0,2,0,0,0,0,0,2,0,0,0,0,2,0],
                           [0,3,0,0,0,0,2,0,0,0,0,0,2,0,0,2,0,0,0,0,0,2,0,0,0,0,3,0],
                           [0,2,0,0,0,0,2,0,0,0,0,0,2,0,0,2,0,0,0,0,0,2,0,0,0,0,2,0],
                           [0,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,0],
                           [0,2,0,0,0,0,2,0,0,2,0,0,0,0,0,0,0,0,2,0,0,2,0,0,0,0,2,0],
                           [0,2,0,0,0,0,2,0,0,2,0,0,0,0,0,0,0,0,2,0,0,2,0,0,0,0,2,0],
                           [0,2,2,2,2,2,2,0,0,2,2,2,2,0,0,2,2,2,2,0,0,2,2,2,2,2,2,0],
                           [0,0,0,0,0,0,2,0,0,0,0,0,1,0,0,1,0,0,0,0,0,2,0,0,0,0,0,0],
                           [0,0,0,0,0,0,2,0,0,0,0,0,1,0,0,1,0,0,0,0,0,2,0,0,0,0,0,0],
                           [0,0,0,0,0,0,2,0,0,1,1,1,1,1,1,1,1,1,1,0,0,2,0,0,0,0,0,0],
                           [0,0,0,0,0,0,2,0,0,1,0,0,0,0,0,0,0,0,1,0,0,2,0,0,0,0,0,0],
                           [0,0,0,0,0,0,2,0,0,1,0,0,0,0,0,0,0,0,1,0,0,2,0,0,0,0,0,0],
                           [1,1,1,1,1,1,2,1,1,1,0,0,0,0,0,0,0,0,1,1,1,2,1,1,1,1,1,1],
                           [0,0,0,0,0,0,2,0,0,1,0,0,0,0,0,0,0,0,1,0,0,2,0,0,0,0,0,0],
                           [0,0,0,0,0,0,2,0,0,1,0,0,0,0,0,0,0,0,1,0,0,2,0,0,0,0,0,0],
                           [0,0,0,0,0,0,2,0,0,1,1,1,1,1,1,1,1,1,1,0,0,2,0,0,0,0,0,0],
                           [0,0,0,0,0,0,2,0,0,1,0,0,0,0,0,0,0,0,1,0,0,2,0,0,0,0,0,0],
                           [0,0,0,0,0,0,2,0,0,1,0,0,0,0,0,0,0,0,1,0,0,2,0,0,0,0,0,0],
                           [0,2,2,2,2,2,2,2,2,2,2,2,2,0,0,2,2,2,2,2,2,2,2,2,2,2,2,0],
                           [0,2,0,0,0,0,2,0,0,0,0,0,2,0,0,2,0,0,0,0,0,2,0,0,0,0,2,0],
                           [0,2,0,0,0,0,2,0,0,0,0,0,2,0,0,2,0,0,0,0,0,2,0,0,0,0,2,0],
                           [0,3,2,2,0,0,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,0,0,2,2,3,0],
                           [0,0,0,2,0,0,2,0,0,2,0,0,0,0,0,0,0,0,2,0,0,2,0,0,2,0,0,0],
                           [0,0,0,2,0,0,2,0,0,2,0,0,0,0,0,0,0,0,2,0,0,2,0,0,2,0,0,0],
                           [0,2,2,2,2,2,2,0,0,2,2,2,2,0,0,2,2,2,2,0,0,2,2,2,2,2,2,0],
                           [0,2,0,0,0,0,0,0,0,0,0,0,2,0,0,2,0,0,0,0,0,0,0,0,0,0,2,0],
                           [0,2,0,0,0,0,0,0,0,0,0,0,2,0,0,2,0,0,0,0,0,0,0,0,0,0,2,0],
                           [0,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,0],
                           [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]
    def initialize_map(self, start_x):
        #the map will be a 28x31 grid
        map_tiles = []
        for y in range(31):
            row = []
            for x in range(28):
                tile = self.spritesheet.subsurface(pygame.Rect(start_x + x * self.tile_size, y * self.tile_size, self.tile_size, self.tile_size))
                row.append(tile)
            map_tiles.append(row)
        return map_tiles
    

if __name__ == "__main__":
    Game()