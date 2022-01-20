import pygame
import time

from dialog import DialogBox
from inventory import Inventory
from map import MapManager
from player import Player


class Game:

    X_POS = 40
    Y_POS = 580

    def __init__(self):

        # affichage de la fenêtre du jeu
        self.screen = pygame.display.set_mode((800, 800))
        pygame.display.set_caption("Gobzer vs Calvoche")

        # générer le joueur
        self.player = Player()
        self.inventory = Inventory()
        self.map_manager = MapManager(self.screen, self.player, self.inventory)

        self.font = pygame.font.Font("./dialogs/dialog_font.ttf", 15)
        self.box = pygame.image.load("./dialogs/dialog_box.png")
        self.dialog_box = DialogBox(self.box)
        self.box = pygame.transform.scale(self.box, (750, 200))
        self.man_inventory1 = "E = quitter"
        self.man_inventory2 = "A = utiliser item"
        self.man_inventory3 = "Z & S = item précédent/suivant"
        self.inventory_index = 0

        self.hair = pygame.image.load("./ath_assets/meche.png")
        self.hair = pygame.transform.scale(self.hair, (64, 64))

        self.item = pygame.image.load("./items/item.png")
        self.item = pygame.transform.scale(self.item, (32, 32))

        self.inventory_display = pygame.image.load("./ath_assets/inventory.png")
        self.inventory_display = pygame.transform.scale(self.inventory_display, (700, 350))
        self.inventory_opened = False
        self.can_handle_input = True

    def update(self):
        self.map_manager.update()

    def handle_input(self):
        if self.can_handle_input:
            pressed = pygame.key.get_pressed()

            if pressed[pygame.K_UP] or pressed[pygame.K_z]:
                self.dialog_box.reading = False
                self.player.move_up()
            elif pressed[pygame.K_DOWN] or pressed[pygame.K_s]:
                self.dialog_box.reading = False
                self.player.move_down()
            elif pressed[pygame.K_LEFT] or pressed[pygame.K_q]:
                self.dialog_box.reading = False
                self.player.move_left()
            elif pressed[pygame.K_RIGHT] or pressed[pygame.K_d]:
                self.dialog_box.reading = False
                self.player.move_right()

    def life_update(self):
        for i in range(self.player.life):
            self.screen.blit(self.hair, (50 + i*48, 30))

    def handle_inventory_input(self):
        if not self.can_handle_input:
            pressed = pygame.key.get_pressed()

            if pressed[pygame.K_z]:
                if self.inventory_index > 0:
                    self.inventory_index -= 1

            if pressed[pygame.K_s]:
                if self.inventory_index < len(self.inventory.items) - 1:
                    self.inventory_index += 1

    def blit_inventory(self, index):
        name = self.inventory.items[index].refact_name
        name = self.font.render(name, False, (0, 0, 0))
        self.screen.blit(name, (120, 200))
        number = self.inventory.items[index].number
        n = str(number)
        numb = self.font.render(n, False, (0, 0, 0))
        self.screen.blit(numb, (300, 200))
        info = self.inventory.items[index].info
        for i in range(len(info)):
            x = self.font.render(info[i], False, (0, 0, 0))
            self.screen.blit(x, (380, 200 + 20*i))

    def show_inventory(self):
        if self.inventory_opened:
            self.screen.blit(self.inventory_display, (40, 100))
            self.screen.blit(self.box, (self.X_POS, self.Y_POS))
            n = self.font.render(self.man_inventory1, False, (0, 0, 0))
            self.screen.blit(n, (self.X_POS + 50, self.Y_POS + 20))
            n = self.font.render(self.man_inventory2, False, (0, 0, 0))
            self.screen.blit(n, (self.X_POS + 50, self.Y_POS + 50))
            n = self.font.render(self.man_inventory3, False, (0, 0, 0))
            self.screen.blit(n, (self.X_POS + 50, self.Y_POS + 80))
            if len(self.inventory.items) > 0:
                self.blit_inventory(self.inventory_index)

    def close_open_inventory(self):
        if self.inventory_opened:
            self.inventory_opened = False
            self.can_handle_input = True
        else:
            self.inventory_opened = True
            self.can_handle_input = False

    def run(self):

        # pour les fps (ici 60)
        clock = pygame.time.Clock()

        running = True
        while running:

            self.player.save_location()
            self.handle_input()
            self.update()
            self.map_manager.draw()
            self.dialog_box.render(self.screen)
            self.life_update()
            self.show_inventory()
            self.handle_inventory_input()
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.map_manager.check_pnj_collisions(self.dialog_box)
                        self.map_manager.check_interactive_obj_collisions(self.dialog_box)
                    if event.key == pygame.K_e:
                        self.close_open_inventory()

            clock.tick(60)

        pygame.quit()
