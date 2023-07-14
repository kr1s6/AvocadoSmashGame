from Settings import *
from CannonLvl1 import CannonLvl1
from Resize import Resize

class Level(Resize):
    def __init__(self):
        super().__init__()
        Resize.SURFACE = pygame.display.get_surface()
        Resize.width, Resize.height = Resize.SURFACE.get_size()
        Resize.tile_size = TILE_SIZE * Resize.width / WIDTH
        # ------------------------------SPRITE GROUPS----------------------------------------------#
        self.player_group = pygame.sprite.Group()
        self.all_sprites = CameraGroup()
        self.front_sprites = FrontCameraGroup()
        self.collision_sprites = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        # ---------------------------------------CANNON---------------------------------------------------#
        self.cannon_lvl1 = CannonLvl1((2*self.tile_size, LEVEL_HEIGHT-self.tile_size),
                                      [self.all_sprites, self.front_sprites])

class CameraGroup(pygame.sprite.Group, Resize):
    def __init__(self):
        super().__init__()
        self.offset = pygame.math.Vector2(0, LEVEL_HEIGHT - self.height)
        self.initial_offset_y = LEVEL_HEIGHT - self.height
        # ------------------------------LEVEL 1 GRAPHIC----------------------------------------------#
        self.background_image = pygame.image.load('../Assets/Level1/background_lvl1.png').convert()
        self.background = pygame.transform.scale(self.background_image, self.SURFACE.get_size())
        self.background_rect = self.background.get_rect(topleft=(0, 0))

    def custom_draw(self, player):
        # ------------------------------PLAYER CENTERING----------------------------------------------#
        if self.width/2 <= player.rect.centerx <= (LEVEL_WIDTH - self.width / 2):
            self.offset.x = player.rect.centerx - self.width/2
        if player.rect.centery <= (LEVEL_HEIGHT - self.height/2):
            self.offset.y = player.rect.centery - self.height/2
        #----fixed bug with wrong self.offset.y----
        if player.rect.centery >= (LEVEL_HEIGHT - self.height/2):
            self.offset.y = self.initial_offset_y
        # ------------------------------DRAWING GRAPHICS CENTERED ON PLAYER---------------------------#
        background_offset = self.background_rect.topleft
        self.SURFACE.blit(self.background, background_offset)

        for sprite in self.sprites():
            offset_rect = sprite.rect.copy()
            offset_rect.center -= self.offset
            self.SURFACE.blit(sprite.image, offset_rect)

    def update_size(self):
        self.background = pygame.transform.scale(self.background_image, self.SURFACE.get_size())
        # ------------------------------RESIZING----------------------------------#
        for sprite in self.sprites():
            sprite.update_size()

class FrontCameraGroup(pygame.sprite.Group, Resize):
    def __init__(self):
        super().__init__()
        self.offset = pygame.math.Vector2(0, 0)
        self.initial_offset_y = LEVEL_HEIGHT - self.height

    def custom_draw(self, player):
        # ------------------------------PLAYER CENTERING----------------------------------------------#
        if self.width / 2 <= player.rect.centerx <= (LEVEL_WIDTH - self.width / 2):
            self.offset.x = player.rect.centerx - self.width / 2
        if player.rect.centery <= self.height/2:
            self.offset.y = player.rect.centery - self.height/2
        # ----fixed bug with wrong self.offset.y----
        if player.rect.centery >= (LEVEL_HEIGHT - self.height / 2):
            self.offset.y = self.initial_offset_y
        # ------------------------------DRAWING GRAPHICS CENTERED ON PLAYER---------------------------#
        for sprite in self.sprites():
            offset_rect = sprite.rect.copy()
            offset_rect.center -= self.offset
            self.SURFACE.blit(sprite.image, offset_rect)

    def update_size(self):
        # ------------------------------RESIZING----------------------------------#
        for sprite in self.sprites():
            sprite.update_size()