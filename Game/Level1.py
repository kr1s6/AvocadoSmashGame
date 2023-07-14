import pygame.sprite
from pytmx.util_pygame import load_pygame
import time
from Tilemap import *
from Slime import Slime
from Level import Level, Resize
from Player import Player
class Level1(Level):
    def __init__(self):
        super().__init__()
        self.running = True
        # -------------------------------------TILE MAP---------------------------------------------------#
        tmx = load_pygame('../Assets/Level1/tilemap.tmx')
        ground_layer = tmx.get_layer_by_name('ground')
        back_ground_layer = tmx.get_layer_by_name('back_ground')
        self.tile_width, self.tile_height = (tmx.tilewidth, tmx.tileheight)

        for x, y, surface in ground_layer.tiles():
            pos = (x * self.tile_width, y * self.tile_height)
            Tile(pos, surface, [self.all_sprites, self.collision_sprites])
        for x, y, surface in back_ground_layer.tiles():
            pos = (x * self.tile_width, y * self.tile_height)
            Tile(pos, surface, self.all_sprites)
        # -------------------------------------PLAYER----------------------------------------------------#
        self.player = Player((0, LEVEL_HEIGHT-TILE_SIZE), [self.all_sprites, self.player_group], self.collision_sprites,
                             self.enemies)
        # -------------------------------------SPRITES----------------------------------------------------#
        Slime((1000, LEVEL_HEIGHT - TILE_SIZE), [self.all_sprites, self.enemies], self.collision_sprites, self.player)

    def run(self):
        # ---------------------------------------------------------------------------------#
        previous_time = time.time()
        while self.running:
            dt = time.time() - previous_time
            previous_time = time.time()
            # --------------------------------MAIN ACTIONS-------------------------------------#
            self.SURFACE.fill('black')
            self.all_sprites.custom_draw(self.player)
            self.front_sprites.custom_draw(self.player)
            self.all_sprites.update(dt)
            self.cannon_lvl1.cannon_enter_cutscene(dt, self.player)
            # ----------------------------------------------------------------------------#
            for event in pygame.event.get():
                if event.type == VIDEORESIZE:
                    event_h = int(event.w) * 9 / 16
                    Resize.SURFACE = pygame.display.set_mode((int(event.w), event_h), pygame.RESIZABLE)
                    Resize.width, Resize.height = self.SURFACE.get_size()
                    self.all_sprites.update_size()
                    self.front_sprites.update_size()
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