from Settings import *
from Button import Button
from Resize import Resize
from Saves import Saves

class Game(Resize):
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Avocado Smash!")
        pygame.display.set_icon(pygame.image.load("../Assets/icon.png"))
        Resize.SURFACE = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
        Resize.width, Resize.height = self.SURFACE.get_size()
        #----------------------------------------------------------------------------#
        self.saves = Saves()
        # ------------------------------MENU GRAPHICS----------------------------------------------#
        self.background_image = pygame.image.load('../Assets/Menu/background_menu.png').convert()
        self.background = pygame.transform.scale(self.background_image, self.SURFACE.get_size())
        self.background_rect = self.background.get_rect(topleft=(0, 0))
        # --------------------------------BUTTONS--------------------------------------------------#
        self.start = Button((self.width*19/48, self.height*7/25), "start_button.png")
        self.end = Button((self.width*19/48, self.height*11/20), "end_button.png")

    def run(self):
        while True:
            #----------------------------------------------------------------------------#
            self.SURFACE.blit(self.background, self.background_rect)
            self.start.draw()
            self.end.draw()

            if self.start.clicked:
                self.saves.run()
                self.resize()
                self.start.clicked = False
            for event in pygame.event.get():
                if event.type == VIDEORESIZE:
                    event_h = int(event.w)*9 / 16
                    Resize.SURFACE = pygame.display.set_mode((int(event.w), event_h), pygame.RESIZABLE)
                    Resize.width, Resize.height = self.SURFACE.get_size()
                    self.resize()
                if event.type == pygame.QUIT or self.end.clicked:
                    pygame.quit()
                    sys.exit()
            #----------------------------------------------------------------------------#
            pygame.display.update()
            CLOCK.tick(60)

    def resize(self):
        self.background = pygame.transform.scale(self.background_image, self.SURFACE.get_size())
        # ---------------BUTTONS-----------------#
        self.start.update_size((self.width * 19 / 48, self.height * 7 / 25))
        self.end.update_size((self.width * 19 / 48, self.height * 11 / 20))


if __name__ == '__main__':
    game = Game()
    game.run()
