from Characters import Character
import pygame

class Pacman(Character):
    MODEL_WIDTH, MODEL_HEIGHT = 39 , 35
    SPRITE_LOCATION_X, SPRITE_LOCATION_Y = 1140, 0
    NUMBER_OF_MODELS = 3
    INVINCIBILITY_TIMER_OFF = 1337
    def __init__(self, filename) -> None:
        super().__init__(filename)
        self.x_matrix = 1
        self.y_matrix = 1
        self.invincible = False
        self.points = 0
        self.sprites["right"] = self.spritesheet.get_sprites(Pacman.SPRITE_LOCATION_X, Pacman.SPRITE_LOCATION_Y,  Pacman.NUMBER_OF_MODELS, Pacman.MODEL_WIDTH, Pacman.MODEL_HEIGHT)
        self.sprites["up"] = self.rotate_90_degrees(self.sprites["right"])
        self.sprites["left"] = self.rotate_90_degrees(self.sprites["up"])
        self.sprites["down"] = self.rotate_90_degrees(self.sprites["left"])
        self.current_sprites = self.sprites["right"]
        self.current_model_index = 1
        self._model = self.current_sprites[self.current_model_index]
        self.is_eating = True
        self.chomp_sound = pygame.mixer.Sound("./audio/munch.wav")
        self.power_pellet_sound = pygame.mixer.Sound("./audio/power_pellet.wav")
        self.death_sound = pygame.mixer.Sound("./audio/death.wav")
        self.dead = False

    @property
    def hitbox(self):
        return self.x_coordinate, self.x_coordinate + Pacman.MODEL_WIDTH, self.y_coordinate, self.y_coordinate + Pacman.MODEL_HEIGHT

        
    @property
    def model(self):
        return self.current_sprites[self.current_model_index]

    def check_status(self, ghosts):
        self.check_for_death(ghosts)
        self.play_sound()

    def check_for_death(self, ghosts):
        for ghost in ghosts:
            if self.touches_hitbox(ghost):
                self.dead = True
                self.can_move = False

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

    def play_sound(self):
        pygame.mixer.init()
        pygame.mixer.set_num_channels(1)
        if self.is_eating:
            self.chomp_sound.play()
        if self.invincible:
            self.power_pellet_sound.play()
        if self.dead:
            self.death_sound.play()

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

    def respawn(self):
        self.x_coordinate = 1
        self.y_coordinate = 1
    
    def eat_pellets(self, map):
        #if pacman's position has a small pellet (2) give points and change it to empty tile (1)
        if self.x_matrix < 0 or self.x_matrix >= len(map.map_matrix[0]):
            pass
        elif map.map_matrix[self.y_matrix][self.x_matrix] == map.SMALL_PELLET:
            self.is_eating = True
            self.points += 10
            map.map_matrix[self.y_matrix][self.x_matrix] = map.EMPTY_WAY
        #if pacman's position has a large pellet (3) give points turn invincible mode on and change it to empty tile (1)
        elif map.map_matrix[self.y_matrix][self.x_matrix] == map.POWER_PELLET:
            self.is_eating = True
            pygame.time.set_timer(Pacman.INVINCIBILITY_TIMER_OFF, 5000)
            self.points += 50
            self.invincible = True
            map.map_matrix[self.y_matrix][self.x_matrix] = map.EMPTY_WAY
        else:
            self.is_eating = False
    

    
        