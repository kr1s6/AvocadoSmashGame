import pygame

class Button(pygame.sprite.Sprite):
    def __init__(self, pos, image):
        super().__init__()
        self.SURFACE = pygame.display.get_surface()
        self.button = pygame.image.load(f'../Assets/Menu/{image}').convert_alpha()
        self.button = pygame.transform.scale_by(self.button, 7)
        self.rect = self.button.get_rect(topleft=pos)
        # ----------------------------------------------------------------------------------------#
        self.clicked = False

    def draw(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0] is True and self.clicked is False:
                print("Clicked")
                self.clicked = True

        self.SURFACE.blit(self.button, self.rect)
