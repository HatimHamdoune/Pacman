from Characters import Character, Ghost
        
class Blinky(Ghost):
    MODEL_WIDTH, MODEL_HEIGHT = 39 , 40
    NUMBER_OF_MODELS = 8
    SPRITE_LOCATION_X, SPRITE_LOCATION_Y = 1140, 159
    DISTANCE_FROM_WALL = 8 
    def __init__(self, filename) -> None:
        super().__init__(filename)
        self.x_matrix = 13
        self.y_matrix = 11
        self.sprites["right"] = self.spritesheet.get_sprites(Blinky.SPRITE_LOCATION_X, Blinky.SPRITE_LOCATION_Y,  Blinky.NUMBER_OF_MODELS, Blinky.MODEL_WIDTH, Blinky.MODEL_HEIGHT)[:2]
        self.sprites["left"] = self.spritesheet.get_sprites(Blinky.SPRITE_LOCATION_X, Blinky.SPRITE_LOCATION_Y,  Blinky.NUMBER_OF_MODELS, Blinky.MODEL_WIDTH, Blinky.MODEL_HEIGHT)[2:4]
        self.sprites["up"] = self.spritesheet.get_sprites(Blinky.SPRITE_LOCATION_X, Blinky.SPRITE_LOCATION_Y,  Blinky.NUMBER_OF_MODELS, Blinky.MODEL_WIDTH, Blinky.MODEL_HEIGHT)[4:6]
        self.sprites["down"] = self.spritesheet.get_sprites(Blinky.SPRITE_LOCATION_X, Blinky.SPRITE_LOCATION_Y,  Blinky.NUMBER_OF_MODELS, Blinky.MODEL_WIDTH, Blinky.MODEL_HEIGHT)[6:]
        self.current_sprites = self.sprites["right"]
        self.current_model_index = 1
        self._model = self.current_sprites[self.current_model_index]

    @property
    def model(self):
        return self.current_sprites[self.current_model_index]

