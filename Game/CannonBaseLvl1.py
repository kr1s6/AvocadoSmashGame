from Settings import *
from Resize import Resize

class CannonBaseLvl1(pygame.sprite.Sprite, Resize):
    def __init__(self, pos, group):
        super().__init__(group)
        self.pos = pos
        # ------------------------------WHEEL IMAGE----------------------------------------------#
        self.wheel_image = pygame.image.load('../Assets/wheel.png').convert_alpha()
        self.wheel = pygame.transform.scale(self.wheel_image, (self.width*51/640, self.height*17/120))
        # ------------------------------BASICS---------------------------------------------------#
        self.image = self.wheel
        self.rect = self.image.get_rect(midbottom=pos)

    def update_size(self):
        self.wheel = pygame.transform.scale(self.wheel_image, (self.width * 51 / 640, self.height * 17 / 120))
        self.image = self.wheel
        self.pos = (2*self.tile_size, LEVEL_HEIGHT-self.tile_size)
        self.rect = self.image.get_rect(midbottom=self.pos)