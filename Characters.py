import pygame

class Character:
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
    def model(self):
        return self._model

    @property
    def sprite_collection(self):
        return self._sprites

    def rotate_90_degrees(self, sprites):
        #used to rotate the character models after extracting them from the spritesheet, only used for pacman
        rotated_sprites = []
        rotation_angle = 90
        for sprite in sprites:
            rotated_sprites.append(pygame.transform.rotate(sprite, rotation_angle))
        return rotated_sprites

    def touches_hitbox(self, second_object):
        if self.coordinates == second_object.coordinates:
            return True
        return False

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
        if map.map_matrix[turn_direction_y][turn_direction_x] > 0:
            return True
        else:
            return False

    def down_is_free(self, map):
        turn_direction_x = self.x_matrix
        turn_direction_y = self.y_matrix + 1
        if map.map_matrix[turn_direction_y][turn_direction_x] > 0:
            return True
        else:
            return False

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
        self.eat_pellets(map)

    def turn(self, direction, map):
        #used the reset directions function as a switch so only the triggered direction is set to True
        if direction == "left":
            if self.left_is_free(map):
                self.reset_directions()
                self.looking_left = True
        if direction == "right":
            if self.right_is_free(map):
                self.reset_directions()
                self.looking_right = True
        if direction == "up":
            if self.up_is_free(map):
                self.reset_directions()
                self.looking_up = True
        if direction == "down":
            if self.down_is_free(map):
                self.reset_directions()
                self.looking_down = True
        





         

class Pacman(Character):
    MODEL_WIDTH, MODEL_HEIGHT = 39 , 35
    SPRITE_LOCATION = 1140
    NUMBER_OF_MODELS = 3
    DISTANCE_FROM_WALL = 8 
    MAP_TILE_SIZE = 20
    INVINCIBILITY_TIMER_OFF = 1337
    def __init__(self, filename) -> None:
        super().__init__(filename)
        self.x_matrix = 1
        self.y_matrix = 1
        self.invincible = False
        self.points = 0
        self.sprites["right"] = self.spritesheet.get_sprites(Pacman.SPRITE_LOCATION, Pacman.NUMBER_OF_MODELS, Pacman.MODEL_WIDTH, Pacman.MODEL_HEIGHT)
        self.sprites["up"] = self.rotate_90_degrees(self.sprites["right"])
        self.sprites["left"] = self.rotate_90_degrees(self.sprites["up"])
        self.sprites["down"] = self.rotate_90_degrees(self.sprites["left"])
        self.current_sprites = self.sprites["right"]
        self._model = self.current_sprites[1]

    @property
    def hitbox(self):
        return self.x_coordinate, self.x_coordinate + Pacman.MODEL_WIDTH, self.y_coordinate, self.y_coordinate + Pacman.MODEL_HEIGHT

    @property
    def x_coordinate(self):
        return self.x_matrix * Pacman.MAP_TILE_SIZE - Pacman.DISTANCE_FROM_WALL

    @property
    def y_coordinate(self):
        return self.y_matrix * Pacman.MAP_TILE_SIZE - Pacman.DISTANCE_FROM_WALL

    def check_status(self):
        if self.invincible:
            print("is invincible")
        else:
            print("not invincible anymore")

    def check_direction(self):
        if self.looking_right:
            self.current_sprites = self.sprites["right"]
            self._model = self.current_sprites[2]
        if self.looking_left:
            self.current_sprites = self.sprites["left"]
            self._model = self.current_sprites[2]
        if self.looking_down:
            self.current_sprites = self.sprites["down"]
            self._model = self.current_sprites[2]
        if self.looking_up:
            self.current_sprites = self.sprites["up"]
            self._model = self.current_sprites[2]


    def respawn(self):
        self.x_coordinate = 1
        self.y_coordinate = 1
    
    def eat_pellets(self, map):
        #if pacman's position has a small pellet (2) give points and change it to empty tile (1)
        if self.x_matrix < 0 or self.x_matrix >= len(map.map_matrix[0]):
            pass
        elif map.map_matrix[self.y_matrix][self.x_matrix] == 2:
            self.points += 10
            map.map_matrix[self.y_matrix][self.x_matrix] = 1
        #if pacman's position has a large pellet (3) give points turn invincible mode on and change it to empty tile (1)
        elif map.map_matrix[self.y_matrix][self.x_matrix] == 3:
            pygame.time.set_timer(Pacman.INVINCIBILITY_TIMER_OFF, 5000)
            self.points += 50
            self.invincible = True
            map.map_matrix[self.y_matrix][self.x_matrix] = 1
    

    
        






    
class Ghost(Character):
    def __init__(self, filename) -> None:
        super().__init__(filename)
        

class Inky(Ghost):
    def __init__(self, filename) -> None:
        super().__init__(filename)
    
    def respawn(self):
        return super().respawn()
    

        

class SpriteSheet:
    def __init__(self, filename) -> None:
        self.spritesheet = pygame.image.load(filename)

    def get_sprites(self, x_coordinate, n_sprites, character_width, character_height):
        #gets the number of sprites to be extracted (n_sprites), and extracts sprites accordingly
        sprites = []
        for i in range(n_sprites):
            sprite = self.spritesheet.subsurface(pygame.Rect(x_coordinate + character_width * i, 0, character_width, character_height))
            sprites.append(sprite)
        return sprites