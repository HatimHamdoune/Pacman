from Characters import Character, Ghost
        
class Pinky(Ghost):
    SPRITE_LOCATION_X, SPRITE_LOCATION_Y = 1140, 200
    SPAWN_X = 16
    SPAWN_Y = 14
    NUMBER_OF_MODELS = 8
    def __init__(self, filename) -> None:
        super().__init__(filename)
        self.x_matrix = Pinky.SPAWN_X
        self.y_matrix = Pinky.SPAWN_Y
        self.sprites["right"] = self.spritesheet.get_sprites(Pinky.SPRITE_LOCATION_X, Pinky.SPRITE_LOCATION_Y,  Pinky.NUMBER_OF_MODELS, Pinky.MODEL_WIDTH, Pinky.MODEL_HEIGHT, Pinky.MODEL_TILT)[:2]
        self.sprites["left"] = self.spritesheet.get_sprites(Pinky.SPRITE_LOCATION_X, Pinky.SPRITE_LOCATION_Y,  Pinky.NUMBER_OF_MODELS, Pinky.MODEL_WIDTH, Pinky.MODEL_HEIGHT, Pinky.MODEL_TILT)[2:4]
        self.sprites["up"] = self.spritesheet.get_sprites(Pinky.SPRITE_LOCATION_X, Pinky.SPRITE_LOCATION_Y,  Pinky.NUMBER_OF_MODELS, Pinky.MODEL_WIDTH, Pinky.MODEL_HEIGHT, Pinky.MODEL_TILT)[4:6]
        self.sprites["down"] = self.spritesheet.get_sprites(Pinky.SPRITE_LOCATION_X, Pinky.SPRITE_LOCATION_Y,  Pinky.NUMBER_OF_MODELS, Pinky.MODEL_WIDTH, Pinky.MODEL_HEIGHT, Pinky.MODEL_TILT)[6:]
        self.current_sprites = self.sprites["right"]
        self._model = self.current_sprites[self.current_model_index]

    def respawn(self):
        self.x_matrix, self.y_matrix = Pinky.SPAWN_X, Pinky.SPAWN_Y