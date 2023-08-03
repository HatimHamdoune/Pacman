import pygame


class Sprite:
    def __init__(self, filename, sprite_location, n_sprites, sprite_width, sprite_height) -> None:
        self.spritesheet = SpriteSheet(filename, sprite_width, sprite_height)
        self.y_coordinate = 16
        self.x_coordinate = 16
        self.temp_y = self.y_coordinate
        self.temp_x = self.x_coordinate
        self.looking_right = True
        self.looking_left = False
        self.looking_up = False
        self.looking_down = False
        self._sprites = self.spritesheet.get_sprites(sprite_location, n_sprites)
        self._width = 37
        self._height = 37
        self._current_model = 0
        self._model = self.sprite_collection[self._current_model]
        self.can_move = True

    @property
    def coordinates(self):
        return self.x_coordinate, self.y_coordinate

    @property
    def model(self):
        return self._current_model

    @property
    def sprite_collection(self):
        return self._sprites

    @property
    def hitbox(self):
        return self.temp_x, self.temp_x + self._width, self.temp_y, self.temp_y + self._height

    def touches_hitbox(self, second_object):
        left_edge_touches = self.hitbox[0] <= second_object.hitbox[1] < self.hitbox[1]
        right_edge_touches = self.hitbox[0] <= second_object.hitbox[0] < self.hitbox[1]
        top_edge_touches = self.hitbox[2] <= second_object.hitbox[3] < self.hitbox[3]
        bottom_edge_touches = self.hitbox[2] <= second_object.hitbox[2] < self.hitbox[3]
        return  (left_edge_touches or right_edge_touches) and (top_edge_touches or bottom_edge_touches)

   
    def next_model(self, desired_model):
        self._current_model = self.sprites[desired_model]

    def reset_directions(self):
        self.looking_down, self.looking_up, self.looking_left, self.looking_right = False, False, False, False

class Pacman(Sprite):
    def __init__(self, filename, sprite_location, n_sprites, sprite_width, sprite_height) -> None:
        super().__init__(filename, sprite_location, n_sprites, sprite_width, sprite_height)
        self.invincible = True
        self.points = 0
        
    
    def respawn(self):
        self.x_coordinate = 1
        self.y_coordinate = 1

    def move(self, map):
        if self.looking_down:
            self.temp_y += 1
        if self.looking_up:
            self.temp_y -= 1
        if self.looking_right:
            self.temp_x += 1
        if self.looking_left:
            self.temp_x -= 1
        self.check_wall(map)
        if self.can_move:
            self.x_coordinate = self.temp_x
            self.y_coordinate = self.temp_y
        else:
            self.temp_x = self.x_coordinate
            self.temp_y = self.y_coordinate

    
    def check_wall(self, map):
        for x in range(self.hitbox[0], self.hitbox[1]):
            if x in map.wall_coordinates:
                for y in range(self.hitbox[2], self.hitbox[3]):
                    if y in map.wall_coordinates[x]:
                        self.can_move = False
                        return
        self.can_move = True
    
class Ghost(Sprite):
    def __init__(self, filename, sprite_location, n_sprites, sprite_width, sprite_height) -> None:
        super().__init__(filename, sprite_location, n_sprites, sprite_width, sprite_height)

    def in_proximity(self, second_object):
        offset = 100
        left_edge_touches = self.hitbox[0] - offset <= second_object.hitbox[1] < self.hitbox[1] + offset
        right_edge_touches = self.hitbox[0] - offset <= second_object.hitbox[0] < self.hitbox[1] + offset
        top_edge_touches = self.hitbox[2] - offset <= second_object.hitbox[3] < self.hitbox[3] + offset
        bottom_edge_touches = self.hitbox[2] - offset <= second_object.hitbox[2] < self.hitbox[3] + offset 
        return  (left_edge_touches or right_edge_touches) and (top_edge_touches or bottom_edge_touches)


        
class Fruits(Sprite):
    def __init__(self, filename, sprite_location, n_sprites, sprite_width, sprite_height) -> None:
        super().__init__(filename, sprite_location, n_sprites, sprite_width, sprite_height)

class SpriteSheet:
    def __init__(self, filename, character_width, character_height) -> None:
        self.spritesheet = pygame.image.load(filename)
        self.character_width = character_width
        self.character_height = character_height

    def get_sprites(self, x_coordinate, n_sprites):
        sprites = []
        for i in range(n_sprites):
            sprite = self.spritesheet.subsurface(pygame.Rect(x_coordinate, i * self.character_height, self.character_width, self.character_height))
            sprites.append(sprite)
        return sprites