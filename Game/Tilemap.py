from Settings import *
from Resize import Resize
class Tile(pygame.sprite.Sprite, Resize):
    def __init__(self, pos, surface, group):
        super().__init__(group)
        self.oryginal_image = surface
        self.image = surface
        self.image = pygame.transform.scale(self.oryginal_image, (self.tile_size, self.tile_size))
        # self.pos = (x * self.tile_width, y * self.tile_height)
        self.rect = self.image.get_rect(topleft=pos)

    def update_size(self):
        Resize.tile_size = TILE_SIZE * self.width / WIDTH
        self.image = pygame.transform.scale(self.oryginal_image, (self.tile_size, self.tile_size))

# class BrickTile(pygame.sprite.Sprite):
#     def __init__(self, pos, surface, group, player_group):
#         super().__init__(group)
#         self.image = surface
#         self.rect = self.image.get_rect(topleft=pos)
#         # ------------------------------VARIABLES----------------------------------------------#
#         self.min_rect = self.rect.bottom - 20
#         self.oryginal_rect = self.rect.bottom
#         self.player_group = player_group
#         self.pushed = False
#
#     def collision_check_with_player(self):
#         for player in self.player_group:
#             if player.rect.collidepoint(self.rect.midbottom):
#                 if player.direction.y < 0 and self.rect.bottom > self.min_rect:
#                     self.destroy(player)
#                     self.rect.bottom = player.rect.top
#                     self.pushed = True
#             return player
#
#     def return_to_normal(self, player):
#         if self.pushed is True and self.rect.bottom < self.oryginal_rect and player.direction.y > 0:
#             self.rect.bottom = player.rect.top
#             if self.rect.bottom > self.oryginal_rect:
#                 self.rect.bottom = self.oryginal_rect
#
#     def destroy(self, player):
#         if player.lives >= 2:
#             self.kill()
#
#     def update(self, dt):
#         player = self.collision_check_with_player()
#         self.return_to_normal(player)
#
# class SpecialTile(pygame.sprite.Sprite):
#     def __init__(self, pos, surface, group, player_group, hearts_group):
#         super().__init__(group)
#         self.SURFACE = pygame.display.get_surface()
#         self.image = surface
#         self.rect = self.image.get_rect(topleft=pos)
#         # ------------------------------VARIABLES----------------------------------------------#
#         self.min_rect = self.rect.bottom - 20
#         self.oryginal_rect = self.rect.bottom
#         self.player_group = player_group
#         self.pushed = False
#         self.not_empty = True
#         # ------------------------------EMPTY IMAGE----------------------------------------------#
#         self.empty = pygame.image.load('../Assets/empty_special.png').convert_alpha()
#         # --------------------------------POTION-------------------------------------------------#
#         self.potion = Potion(self.rect.topleft, group[0], group[1], player_group, self.rect.top, hearts_group)
#
#     def collision_check_with_player(self):
#         for player in self.player_group:
#             if self.rect.collidepoint(player.rect.midtop):
#                 if player.direction.y < 0 and self.rect.bottom > self.min_rect:
#                     self.rect.bottom = player.rect.top
#                     self.pushed = True
#             return player
#
#     def return_to_normal(self, player):
#         if self.pushed is True and self.rect.bottom < self.oryginal_rect and player.direction.y > 0:
#             self.rect.bottom = player.rect.top
#             if self.rect.bottom > self.oryginal_rect:
#                 self.rect.bottom = self.oryginal_rect
#             if self.rect.bottom == self.oryginal_rect:
#                 self.image = self.empty
#                 self.not_empty = False
#                 self.potion.start = True
#
#     def update(self, dt):
#         if self.not_empty:
#             player = self.collision_check_with_player()
#             self.return_to_normal(player)