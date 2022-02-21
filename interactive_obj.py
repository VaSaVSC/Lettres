import pygame


class Obj:

    def __init__(self, name, typeColl, dialog, x, y, width, height):
        self.dialog = dialog
        self.type = typeColl
        self.name = name
        self.refact_name = self.refactor(name)
        self.rect = pygame.Rect(x, y, width, height)

    def refactor(self, name):
        if self.type == "panel":
            numb = name[len(name)-1]
            if '0' <= numb <= '9':
                return "Panneau " + numb
            else:
                return "Panneau"
        elif self.type == "door":
            return "Porte"