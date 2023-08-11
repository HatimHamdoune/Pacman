import Characters
import pygame

class Game:
    #constants to represent the window size
    WINDOW_HEIGHT = 700
    WINDOW_WIDTH = 560
    #Colors
    WHITE = (255, 255, 255)
    #invincibility timer
    INVINCIBLITY_TIMER_OFF = 1337
    def __init__(self) -> None:
        pygame.init()
        self.window_size = Game.WINDOW_WIDTH, Game.WINDOW_HEIGHT
        self.window = pygame.display.set_mode(self.window_size)
        pygame.display.set_caption("Pacman")
        self.clock = pygame.time.Clock()
        pacman_icon = pygame.image.load("pacman.ico")
        pygame.display.set_icon(pacman_icon)
        self.is_new_game = True
        self.framerate = 5

        self.map = Map("SpriteSheet.png", 0)
        self.scoreboard = Scoreboard()
        self.pacman = Characters.Pacman("SpriteSheet.png")
        self.blinky = Characters.Blinky("Spritesheet.png")

        self.main_loop()

        

    def main_loop(self):
        while True:
            if not self.is_new_game:
                self.check_events()
            self.check_input()
            self.refresh_screen()
            if self.is_new_game:
                self.new_game()
                pygame.time.wait(4000)
                self.is_new_game = False
            
    
    def new_game(self):
        pygame.mixer.init()
        pygame.mixer.music.load("./audio/beginning.wav")
        pygame.mixer.music.play()
        
        


    def check_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    exit()
            if event.type == Game.INVINCIBLITY_TIMER_OFF:
                self.pacman.invincible = False
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
        self.pacman.check_status()
        self.pacman.move(self.map)

    def display_ready(self):
        ready_x_matrix, ready_y_matrix = 12, 17
        ready_x_window = ready_x_matrix * self.map.TILE_SIZE - Scoreboard.DISTANCE_FROM_WALL 
        ready_y_window = ready_y_matrix * self.map.TILE_SIZE - Scoreboard.DISTANCE_FROM_WALL
        self.window.blit(self.scoreboard.ready, (ready_x_window, ready_y_window))
    
    def display_score(self):
        score_x_matrix = 1
        score_y_matrix = 32
        score_x_window = score_x_matrix * self.map.TILE_SIZE - Scoreboard.DISTANCE_FROM_WALL 
        score_y_window = score_y_matrix * self.map.TILE_SIZE - Scoreboard.DISTANCE_FROM_WALL
        self.window.blit(self.scoreboard.score(self.pacman.points), (score_x_window, score_y_window))

    def display_lives(self):
        life_x_matrix = 1
        life_y_matrix = 33
        for life in range(self.pacman.lives):
            life_x_window = life_x_matrix * self.map.TILE_SIZE - Scoreboard.DISTANCE_FROM_WALL
            life_y_window = life_y_matrix * self.map.TILE_SIZE
            self.window.blit(self.scoreboard.life(self.pacman), (life_x_window, life_y_window))
            life_x_matrix += 1
            
    def draw_map(self):
        for row in range(len(self.map.map_matrix)):
            for column in range(len(self.map.map_matrix[row])):
                if self.map.map_matrix[row][column] == self.map.EMPTY_WAY:
                    self.window.blit(self.map.empty_block, (column * self.map.tile_size, row * self.map.tile_size))
                else:
                    self.window.blit(self.map.map_tiles[row][column], (column * self.map.tile_size, row * self.map.tile_size))

    def refresh_screen(self):
        self.window.fill((0, 0, 0))
        self.draw_map()
        self.animate_blinky()
        self.animate_pacman()
        self.display_score()
        if self.is_new_game:
            self.display_ready()      
        self.display_lives() 
        pygame.display.flip()
        self.clock.tick(self.framerate)

    def animate_pacman(self):
        self.pacman.next_model()
        self.window.blit(self.pacman.model, (self.pacman.x_coordinate, self.pacman.y_coordinate))
        pygame.display.update()
    
    def animate_blinky(self):
        self.blinky.next_model()
        self.window.blit(self.blinky.model, (self.blinky.x_coordinate, self.blinky.y_coordinate))

class Scoreboard:
    DISTANCE_FROM_WALL = 8
    def __init__(self) -> None:
        self.current_score = 0
        self.font = pygame.sysfont.Font("./joystix monospace.otf", 22)

    @property
    def ready(self):
        ready_message = self.font.render("Ready!", True, Game.WHITE)
        return ready_message

    def score(self, current_score):
        score = self.font.render(f"{current_score} pts", True, Game.WHITE)
        return score

    def life(self, pacman):
        lives_image = pacman.sprites["right"][1]
        lives_image = pygame.transform.scale(lives_image, (Map.TILE_SIZE, Map.TILE_SIZE))
        return lives_image

class Map:
    #hard coded the map dimensions and tile size
    MAP_HEIGHT = 620
    MAP_WIDTH = 560
    TILE_SIZE = 20
    WALL = 0
    EMPTY_WAY = 1
    SMALL_PELLET = 2
    POWER_PELLET = 3
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