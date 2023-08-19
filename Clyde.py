from Characters import Character, Ghost
        
class Clyde(Ghost):
    SPRITE_LOCATION_X, SPRITE_LOCATION_Y = 1140, 280
    SPAWN_X = 13
    SPAWN_Y = 11
    NUMBER_OF_MODELS = 8
    def __init__(self, filename) -> None:
        super().__init__(filename)
        self.x_matrix = Clyde.SPAWN_X
        self.y_matrix = Clyde.SPAWN_Y
        self.sprites["right"] = self.spritesheet.get_sprites(Clyde.SPRITE_LOCATION_X, Clyde.SPRITE_LOCATION_Y,  Clyde.NUMBER_OF_MODELS, Clyde.MODEL_WIDTH, Clyde.MODEL_HEIGHT, Clyde.MODEL_TILT)[:2]
        self.sprites["left"] = self.spritesheet.get_sprites(Clyde.SPRITE_LOCATION_X, Clyde.SPRITE_LOCATION_Y,  Clyde.NUMBER_OF_MODELS, Clyde.MODEL_WIDTH, Clyde.MODEL_HEIGHT, Clyde.MODEL_TILT)[2:4]
        self.sprites["up"] = self.spritesheet.get_sprites(Clyde.SPRITE_LOCATION_X, Clyde.SPRITE_LOCATION_Y,  Clyde.NUMBER_OF_MODELS, Clyde.MODEL_WIDTH, Clyde.MODEL_HEIGHT, Clyde.MODEL_TILT)[4:6]
        self.sprites["down"] = self.spritesheet.get_sprites(Clyde.SPRITE_LOCATION_X, Clyde.SPRITE_LOCATION_Y,  Clyde.NUMBER_OF_MODELS, Clyde.MODEL_WIDTH, Clyde.MODEL_HEIGHT, Clyde.MODEL_TILT)[6:]
        self.current_sprites = self.sprites["right"]
        self._model = self.current_sprites[self.current_model_index]

    def respawn(self):
        self.x_matrix, self.y_matrix = Clyde.SPAWN_X, Clyde.SPAWN_Y