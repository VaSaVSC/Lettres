import pygame


class DialogBox:

    def __init__(self):
        self.box = pygame.image.load("./dialogs/dialog_box.png")

    def render(self, screen):
        screen.blit(self.box, (0, 0))