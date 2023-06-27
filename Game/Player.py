import pygame.mixer
from Settings import *
class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group, collision_sprites, enemies):
        super().__init__(group)
        self.collision_sprites = collision_sprites
        self.enemies = enemies
        # ------------------------------PLAYER IMAGES----------------------------------------------#
        player_right = pygame.image.load('../Assets/Player/avocado-right.png').convert_alpha()
        player_right = pygame.transform.scale_by(player_right, 1.5)
        player_jump_right = pygame.image.load('../Assets/Player/avocado-jump_right.png').convert_alpha()
        player_jump_right = pygame.transform.scale_by(player_jump_right, 1.5)

        self.image_list = [player_right, player_jump_right]
        self.player_images_index = 0
        # self.animation_frame = 0
        # ------------------------------PLAYER SOUNDS----------------------------------------------#

        # ------------------------------BASICS---------------------------------------------------#
        self.image = self.image_list[0]
        self.rect = self.image.get_rect(center=pos)

        self.GRAVITY = 0.8
        self.LAUNCH_POWER = 10

        self.JUMP_HIGH = -10
        self.SPEED = 10
        self.start_pos = pos
        self.is_launched = False
        self.in_air = False
        self.direction = pygame.math.Vector2(0, 0)

        self.VELOCITY_X = 10
        self.VELOCITY_Y = 10
        self.gravity_velocity = self.GRAVITY
        self.launch_velocity = self.LAUNCH_POWER

    def get_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.in_air = True
            self.image = self.image_list[1]
            self.direction.y = self.JUMP_HIGH
        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
            if self.in_air is not True:
                self.image = self.image_list[0]
        else:
            self.direction.x = 0
        if keys[pygame.K_SPACE]:
            self.is_launched = True
            self.in_air = True


    # def animation(self, dt):
    #     self.animation_frame += 0.1 * dt * 60
    #     if self.animation_frame >= len(self.image_list[self.player_images_index]):
    #         self.animation_frame = 0
    #     self.image = self.image_list[self.player_images_index][int(self.animation_frame)]

    def gravity(self, dt):
        # velocity of gravity = gravity * time
        # velocity of gravity increases after player reach max height and start falling down
        time = int(pygame.time.get_ticks() / 1000)
        previous_time = time

        one_sec = time > previous_time
        reached_max_height = self.direction.y > 0
        if one_sec and self.in_air and reached_max_height:
            self.gravity_velocity += self.GRAVITY * dt * 60

        if not self.is_launched:
            self.direction.y += self.gravity_velocity * dt * 60
            self.rect.y += self.direction.y * dt * 60

    def avocado_launch(self, dt):
        if self.is_launched:
            self.direction.y -= self.launch_velocity * dt * 60
            self.launch_velocity -= self.gravity_velocity * dt * 60
            self.rect.y += self.direction.y * dt * 60
            if self.launch_velocity <= 0:
                self.is_launched = False
                self.launch_velocity = self.LAUNCH_POWER

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

    def horizontal_collision(self, dt):
        collisions = self.check_collision_objects()
        for tile in collisions:
            if self.direction.x > 0:
                self.rect.right = tile.rect.left
                self.direction.x = 0
            elif self.direction.x < 0:
                self.rect.left = tile.rect.right
                self.direction.x = 0

    def vertical_collision(self, dt):
        collisions = self.check_collision_objects()
        for tile in collisions:
            if self.direction.y > 0:
                self.rect.bottom = tile.rect.top
                self.in_air = False
                self.gravity_velocity = self.GRAVITY
                self.direction.y = 0
            elif self.direction.y < 0:
                self.rect.top = tile.rect.bottom

    def update(self, dt):
        self.get_input()
        self.avocado_launch(dt)
        self.gravity(dt)
        self.vertical_collision(dt)
        self.horizontal_collision(dt)