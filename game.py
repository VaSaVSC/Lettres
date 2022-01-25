import pygame

from dialog import DialogBox
from inventory import Inventory, use_item
from map import MapManager
from player import Player


class Game:

    X_POS = 40
    Y_POS = 580

    def __init__(self):

        # affichage de la fenêtre du jeu
        self.screen = pygame.display.set_mode((800, 800))
        pygame.display.set_caption("Gobzer vs Calvoche")

        self.font = pygame.font.Font("./dialogs/dialog_font.ttf", 15)
        self.box = pygame.image.load("./dialogs/dialog_box.png")
        self.dialog_box = DialogBox(self.box)
        self.box = pygame.transform.scale(self.box, (750, 200))

        self.intro1 = "N = nouvelle partie"
        self.intro2 = "S = charger le jeu depuis la dernière sauvegarde"

        self.load_from_saved_game = False

        # générer le joueur
        self.fight_event = pygame.event.Event(pygame.USEREVENT)
        self.player = self.load_player(self.load_from_saved_game)

        self.inventory = self.load_inventory(self.load_from_saved_game)

        self.map_manager = self.load_maps(self.load_from_saved_game)

        self.man_inventory1 = "E = quitter"
        self.man_inventory2 = "A = utiliser item"
        self.man_inventory3 = "Z & S = item précédent/suivant"
        self.inventory_index = 0

        self.fight = pygame.image.load("./ath_assets/fight_background.png")
        self.fight = pygame.transform.scale(self.fight, (800, 800))

        self.hair = pygame.image.load("./ath_assets/meche.png")
        self.hair = pygame.transform.scale(self.hair, (64, 64))

        self.item = pygame.image.load("./items/item.png")
        self.item = pygame.transform.scale(self.item, (32, 32))

        self.inventory_display = pygame.image.load("./ath_assets/inventory.png")
        self.inventory_display = pygame.transform.scale(self.inventory_display, (700, 350))
        self.inventory_opened = False
        self.fighting = False
        self.can_handle_input = True
        self.can_handle_inventory_input = False
        self.can_handle_fight_input = False

    # le chargement du joueur, des cartes et de l'inventaire
    def load_player(self, from_save):
        if not from_save:
            return Player(self.fight_event)
        else:
            return Player(self.fight_event)

    def load_inventory(self, from_save):
        if not from_save:
            return Inventory()
        else:
            return Inventory()

    def load_maps(self, from_save):
        if not from_save:
            return MapManager(self.screen, self.player, self.inventory)
        else:
            return MapManager(self.screen, self.player, self.inventory)

    def save(self):
        with open("loading/save.txt", 'wt') as data:
            data.write("print('issou')")

    def decrypt_saving(self):
        with open("loading/save.txt", 'r') as data:
            for line in data:
                exec(line)

    # interactions sur la carte actuelle
    def update(self):
        if self.can_handle_input:
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

    # méthodes relatives à l'inventaire
    def handle_inventory_input(self, pressed):
        if self.can_handle_inventory_input:

            if pressed == pygame.K_z:
                if self.inventory_index > 0:
                    self.inventory_index -= 1

            if pressed == pygame.K_s:
                if self.inventory_index < len(self.inventory.items) - 1:
                    self.inventory_index += 1

            if pressed == pygame.K_a:
                if len(self.inventory.items) > 0 and self.inventory.items[self.inventory_index].number > 0:
                    use_item(self.inventory.items[self.inventory_index], self.player)
                    if self.inventory.items[self.inventory_index].number == 1 and \
                            self.inventory_index == len(self.inventory.items) - 1:
                        self.inventory_index -= 1
                        self.inventory.remove_item(self.inventory.items[self.inventory_index + 1])
                    else:
                        self.inventory.remove_item(self.inventory.items[self.inventory_index])
                if self.inventory_index == -1:
                    self.inventory_index = 0

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
            self.screen.blit(n, (self.X_POS + 50, self.Y_POS + 60))
            n = self.font.render(self.man_inventory2, False, (0, 0, 0))
            self.screen.blit(n, (self.X_POS + 50, self.Y_POS + 90))
            n = self.font.render(self.man_inventory3, False, (0, 0, 0))
            self.screen.blit(n, (self.X_POS + 50, self.Y_POS + 120))
            if len(self.inventory.items) > 0:
                self.blit_inventory(self.inventory_index)

    def close_open_inventory(self):
        if self.inventory_opened:
            self.inventory_opened = False
            self.can_handle_input = True
            self.can_handle_inventory_input = False
        else:
            self.inventory_opened = True
            self.can_handle_input = False
            self.can_handle_inventory_input = True

    # méthodes relatives aux combats
    def show_fight(self):
        if self.fighting:
            self.screen.blit(self.fight, (0, 0))

    def close_open_fight(self):
        if self.fighting:
            self.fighting = False
            self.can_handle_input = True
            self.can_handle_fight_input = False
        else:
            self.fighting = True
            self.can_handle_input = False
            self.can_handle_fight_input = True

    # le jeu tourne
    def run(self):

        starting = True
        while starting:
            self.screen.blit(self.box, (self.X_POS, self.Y_POS - 200))
            n = self.font.render(self.intro1, False, (0, 0, 0))
            self.screen.blit(n, (self.X_POS + 50, self.Y_POS - 140))
            n = self.font.render(self.intro2, False, (0, 0, 0))
            self.screen.blit(n, (self.X_POS + 50, self.Y_POS - 110))
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_n:
                        starting = False
                    if event.key == pygame.K_s:
                        self.load_from_saved_game = True
                        starting = False

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
            self.show_fight()
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
                    if event.key == pygame.K_w:
                        self.close_open_fight()
                    if event.key == pygame.K_z or event.key == pygame.K_s or event.key == pygame.K_a:
                        self.handle_inventory_input(event.key)
                # elif event.type == self.fight_event.type:
                #    self.close_open_fight()

            clock.tick(60)

        pygame.quit()
