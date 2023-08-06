import pygame

class Character:
    def __init__(self, filename) -> None:
        self.spritesheet = SpriteSheet(filename)
        self.y_coordinate = 0
        self.x_coordinate = 0
        self.looking_right = True
        self.looking_left = False
        self.looking_up = False
        self.looking_down = False
        self.sprites = {}

    @property
    def coordinates(self):
        return self.x_coordinate, self.y_coordinate

    @property
    def model(self):
        return self._model

    @property
    def sprite_collection(self):
        return self._sprites

    @property
    def hitbox(self):
        hitbox_trim = 9
        return self.x_coordinate + hitbox_trim, self.x_coordinate + self._width - hitbox_trim, self.y_coordinate + hitbox_trim, self.y_coordinate + self._height - hitbox_trim

    def rotate_90_degrees(self, sprites):
        rotated_sprites = []
        for sprite in sprites:
            rotated_sprites.append(pygame.transform.rotate(sprite, 90))
        return rotated_sprites

    def touches_hitbox(self, second_object):
        left_edge_touches = self.hitbox[0] <= second_object.hitbox[1] < self.hitbox[1]
        right_edge_touches = self.hitbox[0] <= second_object.hitbox[0] < self.hitbox[1]
        top_edge_touches = self.hitbox[2] <= second_object.hitbox[3] < self.hitbox[3]
        bottom_edge_touches = self.hitbox[2] <= second_object.hitbox[2] < self.hitbox[3]
        return  (left_edge_touches or right_edge_touches) and (top_edge_touches or bottom_edge_touches)

    def reset_directions(self):
        self.looking_down, self.looking_up, self.looking_left, self.looking_right = False, False, False, False

    def move(self, map):
        self.check_walls(map)
        if self.can_move:
            if self.looking_down:
                self.y_coordinate += 1
            if self.looking_up:
                self.y_coordinate -= 1
            if self.looking_right:
                self.x_coordinate += 1
            if self.looking_left:
                self.x_coordinate -= 1
        if self.x_coordinate > map.width:
            self.x_coordinate = 0 - self._width
        if self.x_coordinate < -self._width:
            self.x_coordinate = map.width


         

class Pacman(Character):
    MODEL_WIDTH, MODEL_HEIGHT = 40 , 35
    SPRITE_LOCATION = 1140
    NUMBER_OF_MODELS = 3
    SPAWN_X, SPAWN_Y = 12, 50
    def __init__(self, filename) -> None:
        super().__init__(filename)
        self.x_coordinate = Pacman.SPAWN_X
        self.y_coordinate = Pacman.SPAWN_Y
        self.invincible = False
        self.points = 0
        self.sprites["right"] = self.spritesheet.get_sprites(Pacman.SPRITE_LOCATION, Pacman.NUMBER_OF_MODELS, Pacman.MODEL_WIDTH, Pacman.MODEL_HEIGHT)
        self.sprites["up"] = self.rotate_90_degrees(self.sprites["right"])
        self.sprites["left"] = self.rotate_90_degrees(self.sprites["up"])
        self.sprites["down"] = self.rotate_90_degrees(self.sprites["left"])
        self.current_sprites = self.sprites["right"]
        self._model = self.sprites["up"][1]

    def check_direction(self):
        if self.looking_right:
            self.current_sprites = self.sprites["right"]
        if self.looking_left:
            self.current_sprites = self.sprites["left"]
        if self.looking_down:
            self.current_sprites = self.sprites["down"]
        if self.looking_up:
            self.current_sprites = self.sprites["up"]

    
    
    def respawn(self):
        self.x_coordinate = 1
        self.y_coordinate = 1

    

    
        






    
class Ghost(Character):
    def __init__(self, filename) -> None:
        super().__init__(filename)

    def in_proximity(self, second_object):
        offset = 100
        left_edge_touches = self.hitbox[0] - offset <= second_object.hitbox[1] < self.hitbox[1] + offset
        right_edge_touches = self.hitbox[0] - offset <= second_object.hitbox[0] < self.hitbox[1] + offset
        top_edge_touches = self.hitbox[2] - offset <= second_object.hitbox[3] < self.hitbox[3] + offset
        bottom_edge_touches = self.hitbox[2] - offset <= second_object.hitbox[2] < self.hitbox[3] + offset 
        return  (left_edge_touches or right_edge_touches) and (top_edge_touches or bottom_edge_touches)


        

class SpriteSheet:
    def __init__(self, filename) -> None:
        self.spritesheet = pygame.image.load(filename)

    def get_sprites(self, x_coordinate, n_sprites, character_width, character_height):
        sprites = []
        for i in range(n_sprites):
            sprite = self.spritesheet.subsurface(pygame.Rect(x_coordinate + character_width * i, 0, character_width, character_height))
            sprites.append(sprite)
        return sprites