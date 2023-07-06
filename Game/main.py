import pygame

from Settings import *
from Button import Button
from Saves import Saves
import sys

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Avocado Smash!")
        pygame.display.set_icon(pygame.image.load("../Assets/icon.png"))
        self.SCREEN = pygame.display.set_mode((WIDTH, HIGH), pygame.RESIZABLE)
        #----------------------------------------------------------------------------#
        self.saves = Saves()
        # ------------------------------MENU GRAPHICS----------------------------------------------#
        self.background = pygame.image.load('../Assets/Menu/background_menu.png').convert()
        self.background = pygame.transform.scale_by(self.background, 8)
        self.background_rect = self.background.get_rect(topleft=(0, 0))
        # --------------------------------BUTTONS--------------------------------------------------#
        self.start = Button((WIDTH / 2 - 100, 150), "start_button.png")
        self.end = Button((WIDTH / 2 - 100, 350), "end_button.png")

    def run(self):
        while True:
            #----------------------------------------------------------------------------#
            self.SCREEN.blit(self.background, self.background_rect)
            self.start.draw()
            self.end.draw()

            if self.start.clicked:
                self.saves.run()
                self.start.clicked = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT or self.end.clicked:
                    pygame.quit()
                    sys.exit()
            #----------------------------------------------------------------------------#
            pygame.display.update()
            CLOCK.tick(60)


if __name__ == '__main__':
    game = Game()
    game.run()
