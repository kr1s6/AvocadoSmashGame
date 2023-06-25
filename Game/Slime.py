import pygame.image
from Settings import *

class Slime(pygame.sprite.Sprite):
    def __init__(self, pos, group, collision_sprites, player):
        super().__init__(group)
        # ------------------------------SLIME IMAGES----------------------------------------------#
        slime_left = pygame.image.load('../Assets/Slime/slime-left.png').convert_alpha()
        slime_left = pygame.transform.scale_by(slime_left, 4)
        slime_dead = pygame.image.load('../Assets/Slime/slime-dead.png').convert_alpha()
        slime_dead = pygame.transform.scale_by(slime_dead, 4)

        self.enemy_images = [slime_left, slime_dead]
        self.enemy_images_index = 0
        self.animation_frame = 0
        # ------------------------------SOUNDS----------------------------------------------#

        # ------------------------------BASICS---------------------------------------------------#
        self.image = self.enemy_images[self.enemy_images_index]
        self.rect = self.image.get_rect(center=pos)

        self.GRAVITY = 0.8
        self.JUMP_HIGH = -10
        self.SPEED = 5
        self.JUMP_DELAY = 100
        self.pos = pos
        self.in_air = False
        self.y_velocity = self.JUMP_HIGH
        self.jump_timer = 0
        self.direction = pygame.math.Vector2(-1, 0)
        self.alive = True
        # ------------------------------COLLISION---------------------------------------------------#
        self.collision_sprites = collision_sprites
        self.player = player

    def gravity(self, dt):
        self.direction.y += self.GRAVITY * dt * 60
        self.rect.y += self.direction.y * dt * 60

    def animation(self):
        if self.direction.x < 0:
            self.image = self.enemy_images[0]

    def slime_jump(self):
        if self.jump_timer == self.JUMP_DELAY:
            self.in_air = True
            self.direction.y = self.JUMP_HIGH
            self.jump_timer = 0
        else:
            self.jump_timer += 1

    def check_collision_objects(self):
        hits = []
        for sprite in self.collision_sprites:
            if self.rect.colliderect(sprite):
                hits.append(sprite)
        return hits

    def horizontal_collision(self, dt):
        if self.in_air:
            self.rect.x += self.direction.x * self.SPEED * dt * 60

        collisions = self.check_collision_objects()
        for tile in collisions:
            self.rect.left = tile.rect.right + 10 * dt * 60

    def vertical_collision(self, dt):
        self.gravity(dt)
        collisions = self.check_collision_objects()
        for tile in collisions:
            if self.direction.y > 0:
                self.rect.bottom = tile.rect.top
                self.direction.y = 0
                self.in_air = False
            elif self.direction.y < 0:
                self.rect.top = tile.rect.bottom
                self.direction.y = 0

    def update(self, dt):
        if self.alive:
            self.slime_jump()
            self.animation()
        else:
            self.image = self.enemy_images[1]
            self.rect.size = self.image.get_size()
        self.horizontal_collision(dt)
        self.vertical_collision(dt)

        if self.rect.x <= -60 or self.rect.y >= LEVEL_HIGH:
            self.kill()