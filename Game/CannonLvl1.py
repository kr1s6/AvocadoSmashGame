from Settings import *
from Resize import Resize
from CannonBaseLvl1 import CannonBaseLvl1

class CannonLvl1(pygame.sprite.Sprite, Resize):
    def __init__(self, pos, group):
        super().__init__(group[0])
        self.all_sprites = group[0]
        self.front_sprites = group[1]
        # ------------------------------CANNON IMAGE----------------------------------------------#
        self._base = CannonBaseLvl1(pos, self.all_sprites)
        self.cannon_image = pygame.image.load('../Assets/cannon.png').convert_alpha()
        self.cannon = pygame.transform.scale(self.cannon_image, (self.width*1.29/6.4, self.height/8))
        # ------------------------------BASICS---------------------------------------------------#
        self.angle = 0
        self.pivot = self._base.rect.center  # core around which cannon will be rotating
        offset = pygame.math.Vector2(self.cannon.get_width()/8, -self.cannon.get_height()/4)
        self.pos = self.pivot + offset
        self.image = self.cannon
        self.oryginal_image = self.image
        self.rect = self.image.get_rect(center=self.pos)
        # ------------------------------CUTSCENE---------------------------------------------------#
        self._stage1_walk = True
        self._stage2_jump = True
        self._stage3_rotation = True
        self._stage4_in_cannon = True
        self._stage5 = True
        self._JUMP_HIGH = -5
        self._timer = 0

    def rotate_on_pivot(self, angle):
        if 0 <= self.angle <= 45:
            self.angle += angle
            self.image = pygame.transform.rotate(self.oryginal_image, self.angle)
            offset = self.pivot + (self.pos - self.pivot).rotate(-self.angle)
            self.rect = self.image.get_rect(center=offset)

    @staticmethod
    def rotate_player(player, oryginal_image):
        if player.direction.x == 0 and player.direction.y >= 0:
            player.angle = 180
        elif player.direction.x == 0 and player.direction.y == 0:
            player.angle = 0
        else:
            player.angle = (math.degrees(math.atan(-player.direction.y/player.direction.x))) + 90
        # print(f"angle: {player.angle} player.dir.y: {player.direction.y}, player.dir.x: {player.direction.x}")
        player.image = pygame.transform.rotate(oryginal_image, player.angle)

    @staticmethod
    def rotate_player_to_cannon(player, oryginal_image):
        if player.angle >= 90:
            player.angle = 90
        else:
            player.angle = (math.degrees(math.atan(-player.direction.y / player.direction.x))) + 90
        player.image = pygame.transform.rotate(oryginal_image, player.angle)

    def cannon_enter_cutscene(self, dt, player):
        if player.rect.x < 330 and self._stage1_walk:
            player.direction.x = 4
            player.rect.x += player.direction.x * dt * 60
            player.animation(dt)

        elif self._stage2_jump:  # avocado jump to the cannon
            self._stage1_walk = False
            player.image = player.image_list[1][0]
            self._timer += 1 * dt * 60
            if self._timer >= 20:
                player.image = player.image_list[2]
                player.direction.y = self._JUMP_HIGH
                player.direction.x = -10
                self._stage2_jump = False

        elif self._stage3_rotation:
            self.all_sprites.remove(self, self._base)
            self.front_sprites.add(self, self._base)
            self.rotate_player_to_cannon(player, player.image_list[2])
            player.rect.x += player.direction.x * dt * 60
            if player.angle == 90:
                player.gravity_activated = False
                self._stage3_rotation = False

        elif self._stage4_in_cannon:  # avocado go into cannon
            player.direction.x = -1
            player.rect.x += player.direction.x * dt * 60
            if player.rect.midright[0] <= self.rect.midright[0]-20:
                player.image = player.image_list[4]
                self._stage4_in_cannon = False
                player.gravity_activated = True
                # player.image = player.image_list[0][0]
                offset = pygame.math.Vector2(self.rect.bottomleft) + (15, 0)
                player.rect.bottomleft = offset

        elif self._stage5:
            self.rotate_on_pivot(1)

    def update_size(self):
        self.cannon = pygame.transform.scale(self.cannon_image, (self.width*1.29/6.4, self.height/8))
        self.oryginal_image = self.cannon
        self.pivot = self._base.rect.center
        offset = pygame.math.Vector2(self.cannon.get_width() / 8, -self.cannon.get_height() / 4)
        self.pos = self.pivot + offset
        self.image = self.cannon
        self.rect = self.image.get_rect(center=self.pos)

        self.image = pygame.transform.rotate(self.oryginal_image, self.angle)
        offset = self.pivot + (self.pos - self.pivot).rotate(-self.angle)
        self.rect = self.image.get_rect(center=offset)