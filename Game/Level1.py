import pygame.sprite
from pytmx.util_pygame import load_pygame
import time
import sys
from Tilemap import *
from Slime import Slime
from Level import Level
class Level1(Level):
    def __init__(self):
        super().__init__()
        self.SURFACE = pygame.display.get_surface()
        self.running = True
        # ------------------------------TILE MAP---------------------------------------------------#
        tmx = load_pygame('../Assets/Level1/tilemap.tmx')
        ground_layer = tmx.get_layer_by_name('ground')

        for x, y, surface in ground_layer.tiles():
            pos = (x * 64, y * 64)
            print(pos)
            Tile(pos, surface, [self.all_sprites, self.collision_sprites])
        # -------------------------------------SPRITES----------------------------------------------------#
        Slime((1000, LEVEL_HIGH - 70), [self.all_sprites, self.enemies], self.collision_sprites, self.player)

    # def player_killed(self):
    #     if self.player.lives <= 0:
    #         self.player.kill()
    #         self.running = False
    #     if self.player.rect.centery >= HIGH:
    #         if self.player.lives >= 3:
    #             self.player.lives = 1
    #         else:
    #             self.player.lives -= 1
    #         self.player.smaller()
    #         self.player.rect.center = self.player.pos
    #         self.all_sprites.offset = pygame.math.Vector2(0, 0)

    def run(self):
        # ---------------------------------------------------------------------------------#
        previous_time = time.time()
        while self.running:
            dt = time.time() - previous_time
            previous_time = time.time()
            # --------------------------------MAIN ACTIONS-------------------------------------#
            self.SURFACE.fill('black')
            self.all_sprites.custom_draw(self.player)
            # self.front_sprites.custom_draw(self.player)
            self.all_sprites.update(dt)
            # ----------------------------------------------------------------------------#
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
            # ----------------------------------------------------------------------------#
            pygame.display.update()
            CLOCK.tick(60)
        self.running = True