import pygame


class DialogBox:

    X_POS = 40
    Y_POS = 680

    def __init__(self):
        self.box = pygame.image.load("./dialogs/dialog_box.png")
        self.box = pygame.transform.scale(self.box, (750, 100))
        self.texts = []
        self.text_index = 0
        self.letter_index = 0
        self.font = pygame.font.Font("./dialogs/dialog_font.ttf", 18)
        self.reading = False
        self.name = ""

    def execute(self, name, dialog=[]):
        if self.reading:
            self.next_text()
        else:
            self.reading = True
            self.text_index = 0
            self.texts = dialog
            self.name = name

    def render(self, screen):
        if self.reading:
            self.letter_index += 1
            if self.letter_index >= len(self.texts[self.text_index]):
                self.letter_index = self.letter_index

            screen.blit(self.box, (self.X_POS, self.Y_POS))
            text = self.font.render(self.texts[self.text_index][0:self.letter_index], False, (0, 0, 0))
            screen.blit(text, (self.X_POS + 50, self.Y_POS + 40))
            n = self.font.render(self.name, False, (0, 0, 0))
            screen.blit(n, (self.X_POS + 50, self.Y_POS + 10))

    def next_text(self):
        self.text_index += 1
        self.letter_index = 0

        if self.text_index >= len(self.texts):
            self.reading = False
