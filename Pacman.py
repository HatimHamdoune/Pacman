from Characters import Character, Ghost
import pygame

class Pacman(Character):
    MODEL_WIDTH, MODEL_HEIGHT = 39 , 35
    DEAD_MODEL_WIDTH = 40
    SPRITE_LOCATION_X, SPRITE_LOCATION_X_DEAD, SPRITE_LOCATION_Y = 1140, 1220, 0
    NORMAL_SPRITE_TILT, DEAD_SPRITE_TILT = 0, 1 
    NUMBER_OF_MODELS, NUMBER_OF_MODELS_DEAD = 3, 12
    INVINCIBILITY_TIMER_OFF = 1337
    def __init__(self, filename) -> None:
        super().__init__(filename)
        self.x_matrix = 1
        self.y_matrix = 1
        self.invincible = False
        self.invincibility_duration = 4000
        self.points = 0
        self.sprites["right"] = self.spritesheet.get_sprites(Pacman.SPRITE_LOCATION_X, Pacman.SPRITE_LOCATION_Y,  Pacman.NUMBER_OF_MODELS, Pacman.MODEL_WIDTH, Pacman.MODEL_HEIGHT, Pacman.NORMAL_SPRITE_TILT)
        self.sprites["up"] = self.rotate_90_degrees(self.sprites["right"])
        self.sprites["left"] = self.rotate_90_degrees(self.sprites["up"])
        self.sprites["down"] = self.rotate_90_degrees(self.sprites["left"])
        self.sprites["dead"] = self.spritesheet.get_sprites(Pacman.SPRITE_LOCATION_X_DEAD, Pacman.SPRITE_LOCATION_Y, Pacman.NUMBER_OF_MODELS_DEAD, Pacman.DEAD_MODEL_WIDTH, Pacman.MODEL_HEIGHT, Pacman.DEAD_SPRITE_TILT)
        self.current_sprites = self.sprites["right"]
        self.current_model_index = 0
        self._model = self.current_sprites[self.current_model_index]
        self.is_eating = True
        self.chomp_sound = pygame.mixer.Sound("./audio/munch.wav")
        self.power_pellet_sound = pygame.mixer.Sound("./audio/power_pellet.wav")
        self.death_sound = pygame.mixer.Sound("./audio/death.wav")
        self.new_life_sound = pygame.mixer.Sound("./audio/extrapac.wav")
        self.dead = False
        self.just_respawned = False
        self.pellets_eaten = 0
        self.last_life_gained_at = 1
        self.got_new_life = False

    @property
    def hitbox(self):
        return self.x_coordinate, self.x_coordinate + Pacman.MODEL_WIDTH, self.y_coordinate, self.y_coordinate + Pacman.MODEL_HEIGHT
        
    @property
    def model(self):
        return self.current_sprites[self.current_model_index]

    def check_status(self, ghosts, map):
        self.eat_pellets(map, ghosts)
        self.check_for_death(ghosts)
        if not self.dead:
            self.move(map)
        self.play_sound()
    
    def check_extra_life(self):
        if self.points % 10000 == 0 and self.points != self.last_life_gained_at:
            self.last_life_gained_at = self.points
            self.got_new_life = True
            return True

    def map_cleared(self):
        return self.pellets_eaten % 244 == 0 and self.pellets_eaten != 0
    
    def clear_pellets(self):
        self.pellets_eaten = 0

    def check_for_death(self, ghosts):
        for ghost in ghosts:
            if self.touches_hitbox(ghost) and not self.invincible:
                self.dead = True
                self.current_sprites = self.sprites["dead"]

    def next_model(self):
        if self.dead:
            self.current_model_index += 1
            if self.current_model_index >= len(self.current_sprites):
                self.respawn()
        elif self.can_move:
            self.just_respawned = False
            self.current_model_index += 1
            if self.current_model_index >= len(self.current_sprites):
                self.current_model_index = 0
        else:
            self.current_model_index = 1           

    def play_sound(self):
        pygame.mixer.init()
        pygame.mixer.set_num_channels(1)
        if self.dead:
            self.power_pellet_sound.stop()
            self.death_sound.play()       
        if self.got_new_life:
            self.new_life_sound.play()
            self.got_new_life = False
        elif self.invincible:
            self.power_pellet_sound.play()
        elif not self.invincible:
            self.power_pellet_sound.stop()
        if self.is_eating:
            self.chomp_sound.play()

    def rotate_90_degrees(self, sprites):
        #used to rotate the character models after extracting them from the spritesheet, only used for pacman
        rotated_sprites = []
        rotation_angle = 90
        for sprite in sprites:
            rotated_sprites.append(pygame.transform.rotate(sprite, rotation_angle))
        return rotated_sprites

    def touches_hitbox(self, ghost):
        offset = 2
        if self.y_matrix == ghost.y_matrix:
            if self.x_coordinate - offset < ghost.x_coordinate < self.x_coordinate + Pacman.MODEL_WIDTH + offset:
                return True
            if self.x_coordinate - offset < ghost.x_coordinate + Ghost.MODEL_WIDTH < self.x_coordinate + Pacman.MODEL_WIDTH + offset:
                return True
        if self.x_matrix == ghost.x_matrix:
            if self.y_coordinate - offset < ghost.y_coordinate < self.y_coordinate + Pacman.MODEL_HEIGHT + offset:
                return True
            if self.y_coordinate - offset < ghost.y_coordinate + Ghost.MODEL_HEIGHT < self.y_coordinate + Pacman.MODEL_HEIGHT + offset:
                return True
        return False

    
    def respawn(self):
        self.dead = False
        self.just_respawned = True
        self.reset_directions()
        self.current_model_index = 0
        self.looking_right = True
        self.x_matrix = 1
        self.y_matrix = 1
        
    
    def eat_pellets(self, map, ghosts):
        #if pacman's position has a small pellet (2) give points and change it to empty tile (1)
        if self.x_matrix < 0 or self.x_matrix >= len(map.map_matrix[0]):
            pass
        elif map.map_matrix[self.y_matrix][self.x_matrix] == map.SMALL_PELLET:
            self.is_eating = True
            self.points += 10
            map.map_matrix[self.y_matrix][self.x_matrix] = map.EMPTY_WAY
            self.pellets_eaten += 1
        #if pacman's position has a large pellet (3) give points turn invincible mode on and change it to empty tile (1)
        elif map.map_matrix[self.y_matrix][self.x_matrix] == map.POWER_PELLET:
            self.is_eating = True
            pygame.time.set_timer(Pacman.INVINCIBILITY_TIMER_OFF, 5000)
            self.points += 50
            self.invincible = True
            self.pellets_eaten += 1
            for ghost in ghosts:
                ghost.flee()
            map.map_matrix[self.y_matrix][self.x_matrix] = map.EMPTY_WAY
        else:
            self.is_eating = False
    

    
        