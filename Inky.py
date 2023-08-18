from Characters import Character, Ghost
        
class Inky(Ghost):
    SPRITE_LOCATION_X, SPRITE_LOCATION_Y = 1140, 240
    SPAWN_X = 12
    SPAWN_Y = 14
    NUMBER_OF_MODELS = 8
    def __init__(self, filename) -> None:
        super().__init__(filename)
        self.x_matrix = Inky.SPAWN_X
        self.y_matrix = Inky.SPAWN_Y
        self.sprites["right"] = self.spritesheet.get_sprites(Inky.SPRITE_LOCATION_X, Inky.SPRITE_LOCATION_Y,  Inky.NUMBER_OF_MODELS, Inky.MODEL_WIDTH, Inky.MODEL_HEIGHT, Inky.MODEL_TILT)[:2]
        self.sprites["left"] = self.spritesheet.get_sprites(Inky.SPRITE_LOCATION_X, Inky.SPRITE_LOCATION_Y,  Inky.NUMBER_OF_MODELS, Inky.MODEL_WIDTH, Inky.MODEL_HEIGHT, Inky.MODEL_TILT)[2:4]
        self.sprites["up"] = self.spritesheet.get_sprites(Inky.SPRITE_LOCATION_X, Inky.SPRITE_LOCATION_Y,  Inky.NUMBER_OF_MODELS, Inky.MODEL_WIDTH, Inky.MODEL_HEIGHT, Inky.MODEL_TILT)[4:6]
        self.sprites["down"] = self.spritesheet.get_sprites(Inky.SPRITE_LOCATION_X, Inky.SPRITE_LOCATION_Y,  Inky.NUMBER_OF_MODELS, Inky.MODEL_WIDTH, Inky.MODEL_HEIGHT, Inky.MODEL_TILT)[6:]
        self.current_sprites = self.sprites["right"]
        self._model = self.current_sprites[self.current_model_index]

    def respawn(self):
        self.x_matrix, self.y_matrix = Inky.SPAWN_X, Inky.SPAWN_Y

