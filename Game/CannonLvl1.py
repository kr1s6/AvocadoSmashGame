from Settings import *
from CannonBaseLvl1 import CannonBaseLvl1
class CannonLvl1(pygame.sprite.Sprite):
    def __init__(self, pos, group):
        super().__init__(group)
        self.SURFACE = pygame.display.get_surface()
        # ------------------------------CANNON IMAGE----------------------------------------------#
        CannonBaseLvl1((pos[0], LEVEL_HIGH-TILE_SIZE), group)
        cannon = pygame.image.load('../Assets/cannon.png').convert_alpha()
        cannon = pygame.transform.scale_by(cannon, 3)
        cannon = pygame.transform.rotate(cannon, 90)  #od 90 (258) do 20 (172)
        # ------------------------------BASICS---------------------------------------------------#
        self.image = cannon
        self.rect = self.image.get_rect(midbottom=pos)
        # ------------------------------CUTSCENE---------------------------------------------------#
        self._stage1 = True
        self._stage2 = True
        self.stage3 = True
        self._stage4 = True
        self.JUMP_HIGH = -23

    def cannon_enter(self, dt, player):
        if player.rect.x < 250 and self._stage1:
            player.direction.x = 1 * dt * 60
            player.rect.x += player.direction.x * 5 * dt * 60
            player.animation(dt)
        elif self._stage2:
            self._stage1 = False
            player.image = player.image_list[1][0]
            player.image = player.image_list[2]
            player.direction.y = self.JUMP_HIGH * dt * 60
            self._stage2 = False
        elif self.stage3:
            #avocado standing on top of the cannon
            player.direction.x = -1 * dt * 60
            player.rect.x += player.direction.x * 3 * dt * 60
            if player.rect.midbottom[0] <= self.rect.midtop[0]:
                player.gravity_activated = False
                player.rect.midbottom = self.rect.midtop
                self.stage3 = False
        elif self._stage4:
            player.direction.y = 1 * dt * 60
            player.rect.y += player.direction.y * dt * 60
            if player.rect.top >= self.rect.top:
                pass
