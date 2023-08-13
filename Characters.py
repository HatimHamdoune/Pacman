import pygame

class Character:
    DISTANCE_FROM_WALL = 8 
    MAP_TILE_SIZE = 20
    def __init__(self, filename) -> None:
        self.spritesheet = SpriteSheet(filename)
        self.y_matrix = 0
        self.x_matrix = 0
        self.looking_right = True
        self.looking_left = False
        self.looking_up = False
        self.looking_down = False
        self.sprites = {}
        self.can_move = True

    @property
    def coordinates(self):
        #returns the character's position in the matrix
        return self.x_matrix, self.y_matrix

    @property
    def x_coordinate(self):
        return self.x_matrix * Character.MAP_TILE_SIZE - Character.DISTANCE_FROM_WALL

    @property
    def y_coordinate(self):
        return self.y_matrix * Character.MAP_TILE_SIZE - Character.DISTANCE_FROM_WALL

    def reset_directions(self):
        self.looking_down, self.looking_up, self.looking_left, self.looking_right = False, False, False, False

    def check_for_walls(self, map):
        if self.looking_left:
            if self.left_is_free(map):
                self.can_move = True
            else:
                self.can_move = False
        if self.looking_right:
            if self.right_is_free(map):
                self.can_move = True
            else:
                self.can_move = False
        if self.looking_up:
            if self.up_is_free(map):
                 self.can_move = True
            else:
                self.can_move = False
        if self.looking_down:
            if self.down_is_free(map):
                  self.can_move = True
            else:
                self.can_move = False

    def next_model(self):
        if self.can_move:
            self.current_model_index += 1
            if self.current_model_index >= len(self.current_sprites):
                self.current_model_index = 0
        else:
            self.current_model_index = 1

    def left_is_free(self, map):
        turn_direction_x = self.x_matrix - 1
        turn_direction_y = self.y_matrix
        try:
            if map.map_matrix[turn_direction_y][turn_direction_x] > 0:
                return True
            else:
                return False
        except IndexError:
            return True

    def right_is_free(self, map):
        turn_direction_x = self.x_matrix + 1
        turn_direction_y = self.y_matrix
        try:
            if map.map_matrix[turn_direction_y][turn_direction_x] > 0:
                return True
            else:
                return False
        except IndexError:
            return True

    def up_is_free(self, map):
        turn_direction_x = self.x_matrix
        turn_direction_y = self.y_matrix - 1
        try:
            if map.map_matrix[turn_direction_y][turn_direction_x] > 0:
                return True
            else:
                return False
        except:
            return True

    def down_is_free(self, map):
        turn_direction_x = self.x_matrix
        turn_direction_y = self.y_matrix + 1
        try:
            if map.map_matrix[turn_direction_y][turn_direction_x] > 0:
                return True
            else:
                return False
        except IndexError:
            return True

    def move(self, map):
        self.check_for_walls(map)
        self.check_direction()
        if self.can_move:
            if self.looking_down:
                self.y_matrix += 1
            if self.looking_up:
                self.y_matrix -= 1
            if self.looking_right:
                self.x_matrix += 1
            if self.looking_left:
                self.x_matrix -= 1
        if self.x_matrix < 0:
            self.x_matrix = len(map.map_matrix[0])
        elif self.x_matrix >= len(map.map_matrix[0]):
            self.x_matrix = -1

    
class Ghost(Character):
    MODEL_WIDTH, MODEL_HEIGHT = 39 , 40
    MODEL_TILT = 0
    SPRITE_FLEE_LOCATION_X, SPRITE_LOCATION_X, SPRITE_LOCATION_Y = 1460, 1140, 159
    DISTANCE_FROM_WALL = 8 
    NUMBER_OF_FLEE_MODELS = 4
    def __init__(self, filename) -> None:
        super().__init__(filename)
        self.flee_sprites = self.spritesheet.get_sprites(Ghost.SPRITE_FLEE_LOCATION_X, Ghost.SPRITE_LOCATION_Y, Ghost.NUMBER_OF_FLEE_MODELS, Ghost.MODEL_WIDTH, Ghost.MODEL_HEIGHT, Ghost.MODEL_TILT)
        self.fleeing = False
        self.current_sprites = []
    
    def flee(self):
        self.fleeing = True
        self.current_sprites = self.flee_sprites

    

class SpriteSheet:
    def __init__(self, filename) -> None:
        self.spritesheet = pygame.image.load(filename)

    def get_sprites(self, x_coordinate, y_coordinate, n_sprites, character_width, character_height, tilt):
        #gets the number of sprites to be extracted (n_sprites), and extracts sprites accordingly
        sprites = []
        for i in range(n_sprites):
            sprite = self.spritesheet.subsurface(pygame.Rect(x_coordinate + character_width * i, y_coordinate, character_width, character_height + (i * tilt)))
            print(f"--{x_coordinate}, {i}")
            sprites.append(sprite)
        return sprites