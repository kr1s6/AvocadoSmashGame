from Settings import *
from Player import Player
from CannonLvl1 import CannonLvl1
class Level:
    def __init__(self):
        # ------------------------------SPRITE GROUPS----------------------------------------------#
        self.player_group = pygame.sprite.Group()
        self.all_sprites = CameraGroup()
        self.front_sprites = FrontCameraGroup()
        self.collision_sprites = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        # ---------------------------------------CANNON---------------------------------------------------#
        self.cannon_lvl1 = CannonLvl1((150, LEVEL_HIGH - 50), [self.all_sprites, self.front_sprites])
        # -------------------------------------PLAYER----------------------------------------------------#
        self.player = Player((0, LEVEL_HIGH - TILE_SIZE), [self.all_sprites, self.player_group], self.collision_sprites,
                             self.enemies)

class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.SURFACE = pygame.display.get_surface()
        self.offset = pygame.math.Vector2(0, LEVEL_HIGH - HIGH)
        self.initial_offset_y = LEVEL_HIGH - HIGH
        # ------------------------------LEVEL 1 GRAPHIC----------------------------------------------#
        self.background = pygame.image.load('../Assets/Level1/background_lvl1.png').convert()
        self.background = pygame.transform.scale_by(self.background, 8)
        self.background_rect = self.background.get_rect(topleft=(0, 0))

    def custom_draw(self, player):
        # ------------------------------PLAYER CENTERING----------------------------------------------#
        if WIDTH/2 <= player.rect.centerx <= (LEVEL_WIDTH - WIDTH / 2):
            self.offset.x = player.rect.centerx - WIDTH/2
        if player.rect.centery <= (LEVEL_HIGH - HIGH/2):
            self.offset.y = player.rect.centery - HIGH/2
        #----fixed bug with wrong self.offset.y----
        if player.rect.centery >= (LEVEL_HIGH - HIGH/2):
            self.offset.y = self.initial_offset_y
        # ------------------------------DRAWING GRAPHICS CENTERED ON PLAYER---------------------------#
        background_offset = self.background_rect.topleft
        self.SURFACE.blit(self.background, background_offset)

        for sprite in self.sprites():
            offset_rect = sprite.rect.copy()
            offset_rect.center -= self.offset
            self.SURFACE.blit(sprite.image, offset_rect)

class FrontCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.SURFACE = pygame.display.get_surface()
        self.offset = pygame.math.Vector2(0, 0)
        self.initial_offset_y = LEVEL_HIGH - HIGH

    def custom_draw(self, player):
        # ------------------------------PLAYER CENTERING----------------------------------------------#
        if WIDTH / 2 <= player.rect.centerx <= (LEVEL_WIDTH - WIDTH / 2):
            self.offset.x = player.rect.centerx - WIDTH / 2
        if player.rect.centery <= HIGH/2:
            self.offset.y = player.rect.centery - HIGH/2
        # ----fixed bug with wrong self.offset.y----
        if player.rect.centery >= (LEVEL_HIGH - HIGH / 2):
            self.offset.y = self.initial_offset_y
        # ------------------------------DRAWING GRAPHICS CENTERED ON PLAYER---------------------------#
        for sprite in self.sprites():
            offset_rect = sprite.rect.copy()
            offset_rect.center -= self.offset
            self.SURFACE.blit(sprite.image, offset_rect)