from Settings import *

class CannonBaseLvl1(pygame.sprite.Sprite):
    def __init__(self, pos, group):
        super().__init__(group)
        # ------------------------------WHEEL IMAGE----------------------------------------------#
        wheel = pygame.image.load('../Assets/wheel.png').convert_alpha()
        wheel = pygame.transform.scale_by(wheel, 3)
        # ------------------------------BASICS---------------------------------------------------#
        self.image = wheel
        self.rect = self.image.get_rect(midbottom=pos)