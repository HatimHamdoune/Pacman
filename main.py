import Pacman
import Blinky
import Inky
import pygame

class Game:
    #constants to represent the window size
    WINDOW_HEIGHT = 700
    WINDOW_WIDTH = 560
    #Colors
    WHITE = (255, 255, 255)
    #invincibility timer event constant, when pacman is no longer the timer triggers it so the main program catches it 
    INVINCIBLITY_TIMER_OFF = 1337
    READY_TIMER = 1000
    def __init__(self) -> None:
        pygame.init()
        self.window_size = Game.WINDOW_WIDTH, Game.WINDOW_HEIGHT
        self.window = pygame.display.set_mode(self.window_size)
        pygame.display.set_caption("Pacman")
        self.clock = pygame.time.Clock()
        pacman_icon = pygame.image.load("pacman.ico")
        pygame.display.set_icon(pacman_icon)
        self.is_new_game = True
        self.framerate = 10
        self.lives = 3
        self.level = 1

        self.map = Map("SpriteSheet.png", 0)
        self.scoreboard = Scoreboard()
        self.pacman = Pacman.Pacman("SpriteSheet.png")
        self.blinky = Blinky.Blinky("Spritesheet.png")
        self.inky = Inky.Inky("SpriteSheet.png")
        self.ghosts = [self.blinky]

        self.main_loop()

    def main_loop(self):
        while True:
            if not self.is_new_game:
                self.check_events()
            self.check_input()
            self.refresh_screen()
            if self.is_new_game:
                self.new_game()
                pygame.time.wait(self.pacman.invincibility_duration)
                self.is_new_game = False
            if self.pacman.just_respawned:
                self.display_ready()
                self.lives -= 1
                pygame.time.wait(Game.READY_TIMER)
            
    def new_game(self):
        pygame.mixer.init()
        pygame.mixer.music.load("./audio/beginning.wav")
        pygame.mixer.music.play()
    
    def check_cleared_pellets(self):
        if self.pacman.map_cleared():
            self.is_new_game = True
            self.pacman.clear_pellets()
            self.map.new_level()
            self.pacman.respawn()
            for ghost in self.ghosts:
                ghost.respawn()
            self.level += 1
        
    def check_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    exit()
            if event.type == Game.INVINCIBLITY_TIMER_OFF:
                self.pacman.invincible = False
                for ghost in self.ghosts:
                    ghost.unflee()
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
        self.pacman.check_status(self.ghosts, self.map)
        for ghost in self.ghosts:
            ghost.roam(self.map)
        if self.pacman.check_extra_life():
            self.lives += 1
        self.check_cleared_pellets()

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
    
    def display_level(self):
        level_x_matrix = 19
        level_y_matrix = 32
        level_x_window = level_x_matrix * self.map.TILE_SIZE - Scoreboard.DISTANCE_FROM_WALL 
        level_y_window = level_y_matrix * self.map.TILE_SIZE - Scoreboard.DISTANCE_FROM_WALL
        self.window.blit(self.scoreboard.levels(self.level), (level_x_window, level_y_window))

    def display_lives(self):
        life_x_matrix = 1
        life_y_matrix = 33
        for life in range(self.lives):
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
        if not self.pacman.dead:
            self.animate_blinky()
            self.animate_inky()
        self.animate_pacman()
        self.display_score()
        self.display_level()
        if self.pacman.just_respawned:
            for ghost in self.ghosts:
                ghost.respawn()
            self.display_ready()
        if self.is_new_game:
            self.display_ready()      
        self.display_lives() 
        pygame.display.flip()
        self.clock.tick(self.framerate)

    def animate_pacman(self):
        self.pacman.next_model()
        self.window.blit(self.pacman.model, (self.pacman.x_coordinate, self.pacman.y_coordinate))
    
    def animate_blinky(self):
        self.blinky.next_model()
        self.window.blit(self.blinky.model, (self.blinky.x_coordinate, self.blinky.y_coordinate))

    def animate_inky(self):
        self.inky.next_model()
        self.window.blit(self.inky.model, (self.inky.x_coordinate, self.inky.y_coordinate))

class Scoreboard:
    DISTANCE_FROM_WALL = 8
    def __init__(self) -> None:
        self.current_score = 0
        self.font = pygame.sysfont.Font("./joystix monospace.otf", 22)

    @property
    def ready(self):
        ready_message = self.font.render("Ready!", True, Game.WHITE)
        return ready_message

    def levels(self, level):
        level_display = self.font.render(f"Level: {level}", True, Game.WHITE)
        return level_display

    def score(self, current_score):
        score = self.font.render(f"{current_score} pts", True, Game.WHITE)
        return score

    def life(self, pacman):
        lives_image = pacman.sprites["right"][1]
        lives_image = pygame.transform.scale(lives_image, (Map.TILE_SIZE, Map.TILE_SIZE))
        return lives_image

class Map:
    #hard coded the map dimensions and tile size
    ROWS = 31
    COLUMNS = 28
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
                           [0,0,0,0,0,0,2,0,0,1,0,1,1,1,1,1,1,0,1,0,0,2,0,0,0,0,0,0],
                           [1,1,1,1,1,1,2,1,1,1,0,1,1,1,1,1,1,0,1,1,1,2,1,1,1,1,1,1],
                           [0,0,0,0,0,0,2,0,0,1,0,1,1,1,1,1,1,0,1,0,0,2,0,0,0,0,0,0],
                           [0,0,0,0,0,0,2,0,0,1,0,0,0,0,0,0,0,0,1,0,0,2,0,0,0,0,0,0],
                           [0,0,0,0,0,0,2,0,0,1,1,1,1,1,1,1,1,1,1,0,0,2,0,0,0,0,0,0],
                           [0,0,0,0,0,0,2,0,0,1,0,0,0,0,0,0,0,0,1,0,0,2,0,0,0,0,0,0],
                           [0,0,0,0,0,0,2,0,0,1,0,0,0,0,0,0,0,0,1,0,0,2,0,0,0,0,0,0],
                           [0,2,2,2,2,2,2,2,2,2,2,2,2,0,0,2,2,2,2,2,2,2,2,2,2,2,2,0],
                           [0,2,0,0,0,0,2,0,0,0,0,0,2,0,0,2,0,0,0,0,0,2,0,0,0,0,2,0],
                           [0,2,0,0,0,0,2,0,0,0,0,0,2,0,0,2,0,0,0,0,0,2,0,0,0,0,2,0],
                           [0,3,2,2,0,0,2,2,2,2,2,2,2,1,1,2,2,2,2,2,2,2,0,0,2,2,3,0],
                           [0,0,0,2,0,0,2,0,0,2,0,0,0,0,0,0,0,0,2,0,0,2,0,0,2,0,0,0],
                           [0,0,0,2,0,0,2,0,0,2,0,0,0,0,0,0,0,0,2,0,0,2,0,0,2,0,0,0],
                           [0,2,2,2,2,2,2,0,0,2,2,2,2,0,0,2,2,2,2,0,0,2,2,2,2,2,2,0],
                           [0,2,0,0,0,0,0,0,0,0,0,0,2,0,0,2,0,0,0,0,0,0,0,0,0,0,2,0],
                           [0,2,0,0,0,0,0,0,0,0,0,0,2,0,0,2,0,0,0,0,0,0,0,0,0,0,2,0],
                           [0,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,0],
                           [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]
        self.default_state = [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
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
                           [0,0,0,0,0,0,2,0,0,1,0,1,1,1,1,1,1,0,1,0,0,2,0,0,0,0,0,0],
                           [1,1,1,1,1,1,2,1,1,1,0,1,1,1,1,1,1,0,1,1,1,2,1,1,1,1,1,1],
                           [0,0,0,0,0,0,2,0,0,1,0,1,1,1,1,1,1,0,1,0,0,2,0,0,0,0,0,0],
                           [0,0,0,0,0,0,2,0,0,1,0,0,0,0,0,0,0,0,1,0,0,2,0,0,0,0,0,0],
                           [0,0,0,0,0,0,2,0,0,1,1,1,1,1,1,1,1,1,1,0,0,2,0,0,0,0,0,0],
                           [0,0,0,0,0,0,2,0,0,1,0,0,0,0,0,0,0,0,1,0,0,2,0,0,0,0,0,0],
                           [0,0,0,0,0,0,2,0,0,1,0,0,0,0,0,0,0,0,1,0,0,2,0,0,0,0,0,0],
                           [0,2,2,2,2,2,2,2,2,2,2,2,2,0,0,2,2,2,2,2,2,2,2,2,2,2,2,0],
                           [0,2,0,0,0,0,2,0,0,0,0,0,2,0,0,2,0,0,0,0,0,2,0,0,0,0,2,0],
                           [0,2,0,0,0,0,2,0,0,0,0,0,2,0,0,2,0,0,0,0,0,2,0,0,0,0,2,0],
                           [0,3,2,2,0,0,2,2,2,2,2,2,2,1,1,2,2,2,2,2,2,2,0,0,2,2,3,0],
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
        for y in range(Map.ROWS):
            row = []
            for x in range(Map.COLUMNS):
                tile = self.spritesheet.subsurface(pygame.Rect(start_x + x * self.tile_size, y * self.tile_size, self.tile_size, self.tile_size))
                row.append(tile)
            map_tiles.append(row)
        return map_tiles
    
    def new_level(self):
        for row in range(Map.ROWS):
            for column in range(Map.COLUMNS):
                self.map_matrix[row][column] = self.default_state[row][column]
                

if __name__ == "__main__":
    Game()