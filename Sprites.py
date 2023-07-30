import pygame


class Sprite:
    def __init__(self, filename) -> None:
        self._model = pygame.image.load(filename + ".png")
        self._width = self._model.get_width()
        self._height = self._model.get_height()
        self.y_coordinate = 0
        self.x_coordinate = 0
        
    @property
    def model(self):
        return self._model
    
    @property
    def coordinates(self):
        return self.x_coordinate, self.y_coordinate
        
    @property
    def hitbox(self):
        return self.x_coordinate, self.x_coordinate + self._width, self.y_coordinate, self.y_coordinate + self._height

    def touches_hitbox(self, second_object):
        left_edge_contact = self.hitbox[0] <= second_object.hitbox[1] < self.hitbox[1]
        right_edge_contact = self.hitbox[0] <= second_object.hitbox[0] < self.hitbox[1]
        top_edge_contact = self.hitbox[2] <= second_object.hitbox[3] < self.hitbox[3]
        bottom_edge_contact = self.hitbox[2] <= second_object.hitbox[2] < self.hitbox[3]
        return  (left_edge_contact or right_edge_contact) and (top_edge_contact or bottom_edge_contact)


class Pacman(Sprite):
    def __init__(self, filename) -> None:
        super().__init__(filename) 
        self.looking_right = True
        self.looking_left = False
        self.looking_up = False
        self.looking_down = False
        self.invincible = True
        self.points = 0
    
    def respawn(self):
        self.x_coordinate = 1
        self.y_coordinate = 1

    def change_model(self, filename):
        self._model = pygame.image.load(filename + ".png")

    def touches_hitbox(self, second_object):
        left_edge_touches = self.hitbox[0] <= second_object.hitbox[1] < self.hitbox[1]
        right_edge_touches = self.hitbox[0] <= second_object.hitbox[0] < self.hitbox[1]
        top_edge_touches = self.hitbox[2] <= second_object.hitbox[3] < self.hitbox[3]
        bottom_edge_touches = self.hitbox[2] <= second_object.hitbox[2] < self.hitbox[3]
        return  (left_edge_touches or right_edge_touches) and (top_edge_touches or bottom_edge_touches)



    
class Ghost(Sprite):
    def __init__(self, filename) -> None:
        super().__init__(filename)