from Settings import *

class CannonBaseLvl1(pygame.sprite.Sprite):
    def __init__(self, pos, group):
        super().__init__(group)
        self.SURFACE = pygame.display.get_surface()
        self.width, self.height = self.SURFACE.get_size()
        # ------------------------------WHEEL IMAGE----------------------------------------------#
        self.wheel_image = pygame.image.load('../Assets/wheel.png').convert_alpha()
        self.wheel = pygame.transform.scale(self.wheel_image, (self.width*51/640, self.height*17/120))
        # ------------------------------BASICS---------------------------------------------------#
        self.image = self.wheel
        self.rect = self.image.get_rect(midbottom=pos)