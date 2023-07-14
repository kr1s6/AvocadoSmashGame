import pygame.mixer
from Settings import *
from Resize import Resize
class Player(pygame.sprite.Sprite, Resize):
    def __init__(self, pos, group, collision_sprites, enemies):
        super().__init__(group)
        self.collision_sprites = collision_sprites
        self.enemies = enemies
        # ------------------------------PLAYER IMAGES----------------------------------------------#
        player_left = pygame.image.load('../Assets/Player/avocado-left.png').convert_alpha()
        player_left2 = pygame.image.load('../Assets/Player/avocado-left2.png').convert_alpha()
        player_right = pygame.image.load('../Assets/Player/avocado-right.png').convert_alpha()
        player_right2 = pygame.image.load('../Assets/Player/avocado-right2.png').convert_alpha()
        player_jump_right = pygame.image.load('../Assets/Player/avocado-jump_right.png').convert_alpha()
        player_jump_left = pygame.image.load('../Assets/Player/avocado-jump_left.png').convert_alpha()
        player_hide = pygame.image.load('../Assets/Player/avocado-hide.png').convert_alpha()

        self.image_list = [[player_right, player_right2], [player_left, player_left2], player_jump_left,
                           player_jump_right, player_hide]
        self.images_index = 0
        self.animation_frame = 0

        self.size = (self.width*9/160, self.height*31/240)
        for i in range(len(self.image_list)):
            if hasattr(self.image_list[i], '__iter__'):
                for j in range(len(self.image_list[i])):
                    self.image_list[i][j] = pygame.transform.scale(self.image_list[i][j], self.size)
            else:
                self.image_list[i] = pygame.transform.scale(self.image_list[i], self.size)

        # ------------------------------PLAYER SOUNDS----------------------------------------------#

        # ------------------------------BASICS---------------------------------------------------#
        self.image = self.image_list[0][0]
        self.rect = self.image.get_rect(midbottom=pos)

        self.GRAVITY = 0.8
        self.AIR_RES = 0.01
        self.POWER_Y = 8
        self.POWER_X = 25
        self.gravity_velocity = self.GRAVITY
        self.air_res_velocity = self.AIR_RES
        self.y_velocity = self.POWER_Y
        self.x_velocity = self.POWER_X

        self.space_pressed = False
        self.is_launched = False
        self.in_air = False
        self.gravity_activated = True

        self.direction = pygame.math.Vector2(0, 0)
        # ------------------------------ROTATION VARIABLES--------------------------------------#
        self.angle = 0
        self.able_rotation = False
        # ------------------------------TIMER---------------------------------------------------#
        self.previous_time = 0

    def update_size(self):
        self.size = (self.width * 9 / 160, self.height * 31 / 240)
        for i in range(len(self.image_list)):
            if hasattr(self.image_list[i], '__iter__'):
                for j in range(len(self.image_list[i])):
                    self.image_list[i][j] = pygame.transform.scale(self.image_list[i][j], self.size)
            else:
                self.image_list[i] = pygame.transform.scale(self.image_list[i], self.size)
    def rotate_player(self, dt):
        if self.able_rotation:
            if self.direction.x == 0 and self.direction.y >= 0:
                self.angle = 180
            elif self.direction.x == 0 and self.direction.y == 0:
                self.angle = 0
            else:
                self.angle = (math.degrees(math.atan(-self.direction.y / self.direction.x))) + 90
            # print(f"angle: {self.angle} self.dir.y: {self.direction.y}, self.dir.x: {self.direction.x}")
            self.image = pygame.transform.rotate(self.oryginal_image, self.angle)

    def get_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and not self.space_pressed:
            self.images_index = 3
            self.space_pressed = True
            self.able_rotation = True
            self.is_launched = True
            self.in_air = True

    def animation(self, dt):
        self.animation_frame += 0.1 * dt * 60
        if self.animation_frame >= len(self.image_list[self.images_index]):
            self.animation_frame = 0
        self.image = self.image_list[self.images_index][int(self.animation_frame)]

    def gravity(self, dt):
        time = int(pygame.time.get_ticks() / 1000)
        one_sec = time > self.previous_time
        self.previous_time = time

        if self.direction.y < 0:
            self.in_air = True

        if self.in_air and self.gravity_activated:
            self.rect.y += self.direction.y * dt * 60
            reached_max_height = (self.direction.y >= 0)
            if one_sec and reached_max_height:
                self.gravity_velocity += self.GRAVITY
            self.direction.y += self.gravity_velocity

    def air_resistance(self):
        self.air_res_velocity = self.AIR_RES * self.direction.x
        if self.direction.x > 0 or self.direction.x < 0:
            self.direction.x -= self.air_res_velocity

    def avocado_launch(self, dt):
        if self.is_launched:
            self.direction.y -= self.y_velocity * dt * 60
            self.y_velocity -= self.gravity_velocity * dt * 60
            self.rect.y += self.direction.y * dt * 60
            if self.y_velocity <= 0:
                self.is_launched = False
                self.y_velocity = self.POWER_Y

        # if self.in_air:
        #     self.direction.x = self.x_velocity
        #     self.rect.x += self.direction.x * dt * 60

    def check_collision_objects(self):
        hits = []
        for sprite in self.collision_sprites:
            if self.rect.colliderect(sprite):
                hits.append(sprite)
        for enemy in self.enemies:
            if self.rect.colliderect(enemy):
                hits.append(enemy)
                if self.direction.y > 0:
                    enemy.alive = False
        return hits

    def horizontal_collision(self):
        collisions = self.check_collision_objects()
        for tile in collisions:
            if self.direction.x > 0:
                self.rect.right = tile.rect.left
                self.direction.x = 0
            elif self.direction.x < 0:
                self.rect.left = tile.rect.right
                self.direction.x = 0

    def vertical_collision(self):
        collisions = self.check_collision_objects()
        for tile in collisions:
            if self.direction.y > 0:
                self.rect.bottom = tile.rect.top
                self.in_air = False
                self.gravity_velocity = self.GRAVITY
                self.direction.y = 0
                self.direction.x = 0
            elif self.direction.y < 0:
                self.rect.top = tile.rect.bottom
        # ----fixed bug with falling through ground tiles----
        if self.rect.bottom >= LEVEL_HEIGHT:
            self.rect.bottom = LEVEL_HEIGHT - TILE_SIZE
            self.in_air = False
            self.gravity_velocity = self.GRAVITY
            self.direction.y = 0

    def update(self, dt):
        self.get_input()
        self.avocado_launch(dt)
        self.gravity(dt)
        self.air_resistance()
        # self.rotate_player(dt)
        self.vertical_collision()
        self.horizontal_collision()