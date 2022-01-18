import pygame


class DialogBox:

    def __init__(self):
        self.box = pygame.image.load("./dialogs/dialog_box.png")
        self.box = pygame.transform.scale(self.box, (700, 100))

    def render(self, screen):
        screen.blit(self.box, (60, 680))