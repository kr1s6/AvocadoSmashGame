from Settings import *
from CannonBaseLvl1 import CannonBaseLvl1
class CannonLvl1(pygame.sprite.Sprite):
    def __init__(self, pos, group):
        super().__init__(group)
        # ------------------------------CANNON IMAGE----------------------------------------------#
        CannonBaseLvl1((pos[0], LEVEL_HIGH-TILE_SIZE), group)
        cannon = pygame.image.load('../Assets/cannon.png').convert_alpha()
        cannon = pygame.transform.scale_by(cannon, 3)
        cannon = pygame.transform.rotate(cannon, 40)
        # ------------------------------BASICS---------------------------------------------------#
        self.image = cannon
        self.rect = self.image.get_rect(midbottom=pos)