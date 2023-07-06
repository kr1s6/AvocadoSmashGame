from Settings import *
from CannonBaseLvl1 import CannonBaseLvl1
class CannonLvl1(pygame.sprite.Sprite):
    def __init__(self, pos, group):
        super().__init__(group)
        self.SURFACE = pygame.display.get_surface()
        # ------------------------------CANNON IMAGE----------------------------------------------#
        base = CannonBaseLvl1(pos, group)
        cannon = pygame.image.load('../Assets/cannon.png').convert_alpha()
        cannon = pygame.transform.scale_by(cannon, 3)
        # ------------------------------BASICS---------------------------------------------------#
        self.angle = 0
        self.pivot = base.rect.center  # core around which cannon will be rotating
        offset = pygame.math.Vector2(cannon.get_width()/8, -cannon.get_height()/4)
        self.pos = self.pivot + offset
        self.image = cannon
        self.oryginal_image = self.image
        self.rect = self.image.get_rect(center=self.pos)
        # ------------------------------CUTSCENE---------------------------------------------------#
        self._stage1 = True
        self._stage2 = True
        self.stage3 = True
        self._stage4 = True
        self._stage5 = True
        self.JUMP_HIGH = -25

    def rotate_on_pivot(self, dt, angle):
        if 0 <= self.angle <= 45:
            self.angle += angle * dt * 60
            self.image = pygame.transform.rotate(self.oryginal_image, self.angle)
            offset = self.pivot + (self.pos - self.pivot).rotate(-self.angle)
            self.rect = self.image.get_rect(center=offset)

    def cannon_enter_cutscene(self, dt, player):
        if player.rect.x < 250 and self._stage1:
            player.direction.x = 1 * dt * 60
            player.rect.x += player.direction.x * 5 * dt * 60
            player.animation(dt)
        elif self._stage2:  # avocado jump on top of the cannon
            self._stage1 = False
            player.image = player.image_list[1][0]
            player.image = player.image_list[2]
            player.direction.y = self.JUMP_HIGH * dt * 60
            self._stage2 = False
        elif self.stage3:  # avocado standing on top of the cannon
            player.direction.x = -1 * dt * 60
            player.rect.x += player.direction.x * 3 * dt * 60
            if player.rect.midbottom[0] <= self.rect.midtop[0]:
                player.gravity_activated = False
                player.rect.midbottom = self.rect.midtop
                self.stage3 = False
        elif self._stage4:  # avocado go into cannon
            player.direction.y = 1 * dt * 60
            player.rect.y += player.direction.y * dt * 60
            if player.rect.top >= self.rect.top:
                player.image = player.image_list[4]
                self._stage4 = False
        elif self._stage5:
            self.rotate_on_pivot(dt, 1)