from Characters import Character, Ghost
        
class Blinky(Ghost):
    SPAWN_X = 13
    SPAWN_Y = 11
    NUMBER_OF_MODELS = 8
    def __init__(self, filename) -> None:
        super().__init__(filename)
        self.x_matrix = 13
        self.y_matrix = 11
        self.sprites["right"] = self.spritesheet.get_sprites(Blinky.SPRITE_LOCATION_X, Blinky.SPRITE_LOCATION_Y,  Blinky.NUMBER_OF_MODELS, Blinky.MODEL_WIDTH, Blinky.MODEL_HEIGHT, Blinky.MODEL_TILT)[:2]
        self.sprites["left"] = self.spritesheet.get_sprites(Blinky.SPRITE_LOCATION_X, Blinky.SPRITE_LOCATION_Y,  Blinky.NUMBER_OF_MODELS, Blinky.MODEL_WIDTH, Blinky.MODEL_HEIGHT, Blinky.MODEL_TILT)[2:4]
        self.sprites["up"] = self.spritesheet.get_sprites(Blinky.SPRITE_LOCATION_X, Blinky.SPRITE_LOCATION_Y,  Blinky.NUMBER_OF_MODELS, Blinky.MODEL_WIDTH, Blinky.MODEL_HEIGHT, Blinky.MODEL_TILT)[4:6]
        self.sprites["down"] = self.spritesheet.get_sprites(Blinky.SPRITE_LOCATION_X, Blinky.SPRITE_LOCATION_Y,  Blinky.NUMBER_OF_MODELS, Blinky.MODEL_WIDTH, Blinky.MODEL_HEIGHT, Blinky.MODEL_TILT)[6:]
        self.current_sprites = self.sprites["right"]
        self._model = self.current_sprites[self.current_model_index]

    def respawn(self):
        self.x_matrix, self.y_matrix = Blinky.SPAWN_X, Blinky.SPAWN_Y


