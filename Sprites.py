import pygame


class Sprite:
    def __init__(self, filename, sprite_location, n_sprites, sprite_width, sprite_height) -> None:
        self.spritesheet = SpriteSheet(filename, sprite_width, sprite_height)
        self.y_coordinate = 14
        self.x_coordinate = 14
        self.temp_y = self.y_coordinate
        self.temp_x = self.x_coordinate
        self.looking_right = True
        self.looking_left = False
        self.looking_up = False
        self.looking_down = False
        self.wants_to_go_right = False
        self.wants_to_go_left = False
        self.wants_to_go_up = False
        self.wants_to_go_down = False
        self._sprites = self.spritesheet.get_sprites(sprite_location, n_sprites)
        self._width = self.sprite_collection[0].get_width()
        self._height = self.sprite_collection[0].get_height()
        self.offset = 12
        self._current_model = 1
        self._model = self.sprite_collection[self._current_model]
        self.can_move = True
        self.wiggle_room = 5

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
        return self.x_coordinate + self.wiggle_room, self.x_coordinate + self._width - self.offset, self.y_coordinate + self.wiggle_room, self.y_coordinate + self._height - self.offset

    def touches_hitbox(self, second_object):
        left_edge_touches = self.hitbox[0] <= second_object.hitbox[1] < self.hitbox[1]
        right_edge_touches = self.hitbox[0] <= second_object.hitbox[0] < self.hitbox[1]
        top_edge_touches = self.hitbox[2] <= second_object.hitbox[3] < self.hitbox[3]
        bottom_edge_touches = self.hitbox[2] <= second_object.hitbox[2] < self.hitbox[3]
        return  (left_edge_touches or right_edge_touches) and (top_edge_touches or bottom_edge_touches)

    def turn(self, direction, map):
        if direction == "left":
            if self.left_is_free(map):
                print("doesnt touch edge")
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
    
    def left_is_free(self, map):

        for i in range(self.hitbox[0] - self.wiggle_room, self.hitbox[0]):
            if i in map.wall_coordinates:
                for j in range(self.hitbox[2], self.hitbox[3]):
                    print(j)
                    if j in map.wall_coordinates[i]:
                        print("touches edge")
                        return False
        return True         

    def right_is_free(self, map):
        for i in range(self.hitbox[1], self.hitbox[1] + self.wiggle_room):
            if i in map.wall_coordinates:
                for j in range(self.hitbox[2], self.hitbox[3]+1):
                    if j in map.wall_coordinates[i]:
                        return False
        return True

    def up_is_free(self, map):
        for i in range(self.hitbox[0], self.hitbox[1] + self.wiggle_room):
            if i in map.wall_coordinates:
                for j in range(self.hitbox[2], self.hitbox[2] - self.wiggle_room, -1):
                    if j in map.wall_coordinates[i]:
                        return False
        return True

    def down_is_free(self, map):
        for i in range(self.hitbox[0], self.hitbox[1] + self.wiggle_room):
            if i in map.wall_coordinates:
                for j in range(self.hitbox[3], self.hitbox[3] + self.wiggle_room, -1):
                    if j in map.wall_coordinates[i]:
                        return False
        return True
   
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
        self.check_wall(map)
        if self.can_move:
            if self.looking_down:
                self.y_coordinate += 1
            if self.looking_up:
                self.y_coordinate -= 1
            if self.looking_right:
                self.x_coordinate += 1
            if self.looking_left:
                self.x_coordinate -= 1

    def wall_to_the_left(self, map):
        x = self.hitbox[0] + self.wiggle_room
        if x in map.wall_coordinates:
            for y in range(self.hitbox[2], self.hitbox[3]):
                if y in map.wall_coordinates[x]:
                    return True
        return False 

    def wall_to_the_right(self, map):
        x = self.hitbox[1] + self.wiggle_room
        if x in map.wall_coordinates:
            for y in range(self.hitbox[2], self.hitbox[3]):
                if y in map.wall_coordinates[x]:
                    return True
        return False
    
    def wall_on_top(self, map):
        y = self.hitbox[2] - self.wiggle_room
        for x in range(self.hitbox[0], self.hitbox[1] + self.wiggle_room):
            if x in map.wall_coordinates:
                if y in map.wall_coordinates[x]:
                    return True
        return False

    def wall_on_bot(self, map):
        y = self.hitbox[3] + self.wiggle_room
        for x in range(self.hitbox[0], self.hitbox[1] + self.wiggle_room):
            if x in map.wall_coordinates:
                if y in map.wall_coordinates[x]:
                    return True
        return False

    def check_wall(self, map):
        if self.looking_left:
            if self.wall_to_the_left(map):
                self.can_move = False
        if self.looking_right:
            if self.wall_to_the_right(map):
                self.can_move = False
        if self.looking_up:
            if self.wall_on_top(map):
                self.can_move = False
        if self.looking_down:
            if self.wall_on_bot(map):
                self.can_move = False
        



    
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