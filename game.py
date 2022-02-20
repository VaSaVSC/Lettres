import os
import pygame
import random as rd

from animation import AnimateSprite
from fight import poisoned, burned
from dialog import DialogBox
from inventory import Inventory, use_item, Item
from map import MapManager
from player import Player


class Game:
    X_POS = 40
    Y_POS = 580

    def __init__(self):

        # affichage de la fenêtre du jeu
        self.screen = pygame.display.set_mode((800, 800))
        pygame.display.set_caption("Gobzer vs Calvoche")

        # pygame.mixer.music.load('./audio/sound.mp3')
        # pygame.mixer.music.play(-1) # -1 = infini

        self.font = pygame.font.Font("./dialogs/dialog_font.ttf", 15)
        self.font_fight = pygame.font.Font("./dialogs/dialog_font.ttf", 17)
        self.font_fight2 = pygame.font.Font("./dialogs/dialog_font.ttf", 25)
        self.box = pygame.image.load("./dialogs/dialog_box.png")
        self.dialog_box = DialogBox(self.box)
        self.box = pygame.transform.scale(self.box, (750, 200))

        self.intro1 = "N = nouvelle partie"
        self.intro2 = "S = charger le jeu depuis la dernière sauvegarde"
        self.intro3 = "Q = quitter le jeu"

        self.load_from_saved_game = False

        # générer le joueur
        self.fight_event = pygame.event.Event(pygame.USEREVENT)
        self.player = None

        self.inventory = None

        self.map_manager = None

        self.state = None

        self.man_inventory1 = "E = quitter l'inventaire"
        self.man_inventory2 = "A = utiliser item"
        self.man_inventory3 = "Z/S = item précédent/suivant"
        self.man_inventory4 = "P = sauvegarde"
        self.inventory_index = 0

        self.fight = pygame.image.load("./ath_assets/fight_background.png")
        self.fight = pygame.transform.scale(self.fight, (800, 800))
        self.fight_buttons = pygame.image.load("./ath_assets/buttons.png")
        self.fight_buttons = pygame.transform.scale(self.fight_buttons, (700, 100))
        self.atk_bg = pygame.image.load("./ath_assets/atk_bg.jpg")

        self.hair = pygame.image.load("./ath_assets/meche.png")
        self.hair = pygame.transform.scale(self.hair, (64, 64))
        self.gob = pygame.image.load("./sprites/gob5.png")
        self.gob = pygame.transform.scale(self.gob, (64, 64))
        self.death_bg = pygame.image.load("./ath_assets/death_bg.jpg")
        self.wasted = pygame.image.load("./ath_assets/wasted.png")
        self.calvoche = AnimateSprite("calvoche", change_dim=True, width=135, height=165)
        self.calv1 = self.calvoche.get_image(0, 82, h=40)
        self.calv1 = pygame.transform.scale(self.calv1, (64, 80))
        self.calv1.set_colorkey([0, 0, 0])
        self.calv2 = self.calvoche.get_image(37, 82, h=40)
        self.calv2 = pygame.transform.scale(self.calv2, (64, 80))
        self.calv2.set_colorkey([0, 0, 0])
        self.player_sprite = None

        self.inventory_display = pygame.image.load("./ath_assets/inventory.png")
        self.inventory_display = pygame.transform.scale(self.inventory_display, (700, 350))
        self.inventory_opened = False
        self.fighting = False
        self.can_handle_input = True
        self.can_handle_inventory_input = False
        self.can_handle_fight_input = False
        self.quit_while_fighting = False

        self.store_display = pygame.image.load("./ath_assets/magasin.png")
        self.store_display = pygame.transform.scale(self.store_display, (700, 650))
        self.store_opened = False
        self.can_handle_store_input = False

        self.key_timeout = dict()

        self.coin = pygame.image.load("./ath_assets/coin.png")
        self.coin = pygame.transform.scale(self.coin, (50, 50))

    # le jeu tourne --------------------------------------------------------------
    def run(self, was_dead=False):

        starting = True
        while starting and not was_dead:
            self.screen.blit(self.box, (self.X_POS, self.Y_POS - 200))
            n = self.font.render(self.intro1, False, (0, 0, 0))
            self.screen.blit(n, (self.X_POS + 50, self.Y_POS - 140))
            n = self.font.render(self.intro2, False, (0, 0, 0))
            self.screen.blit(n, (self.X_POS + 50, self.Y_POS - 110))
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_n:
                        starting = False
                    if event.key == pygame.K_s:
                        if os.stat("./loading/save_player.txt").st_size > 0 and \
                                os.stat("./loading/save_map.txt").st_size > 0:
                            self.load_from_saved_game = True
                        starting = False

        self.load_player(self.load_from_saved_game)

        self.load_inventory(self.load_from_saved_game)

        self.load_maps(self.load_from_saved_game)

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
            self.gold_update()
            self.show_inventory()
            self.show_fight()
            self.show_store()
            if self.quit_while_fighting:
                break
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if self.map_manager.check_pnj_collisions(self.dialog_box) == 1:
                            self.close_open_store()
                        self.map_manager.check_interactive_obj_collisions(self.dialog_box)
                    elif event.key == pygame.K_0 or event.key == pygame.K_1 or \
                            event.key == pygame.K_2 or event.key == pygame.K_3 or \
                            event.key == pygame.K_4 or event.key == pygame.K_5 or \
                            event.key == pygame.K_6 or event.key == pygame.K_7 or \
                            event.key == pygame.K_8 or event.key == pygame.K_9:
                        self.handle_store_input(event.key)
                    elif event.key == pygame.K_e and self.store_opened == False:
                        self.close_open_inventory()
                    elif event.key == pygame.K_w:
                        self.map_manager.launch_fight()
                        self.close_open_fight()
                    elif event.key == pygame.K_z or event.key == pygame.K_s or \
                            event.key == pygame.K_a or event.key == pygame.K_p:
                        self.handle_inventory_input(event.key)
                elif event.type == self.fight_event.type:
                    self.close_open_fight()

            clock.tick(60)

        pygame.quit()

    # le chargement du joueur, des cartes et de l'inventaire -----------------------------------------------
    def load_player(self, from_save):
        self.player = Player(self.fight_event)
        self.player_sprite = pygame.transform.scale(self.player.images["right"][1], (64, 64))
        if from_save:
            self.decrypt_saving("player")

    def load_inventory(self, from_save):
        self.inventory = Inventory()
        self.load_items()
        if from_save:
            self.decrypt_saving("inventory")

    def load_items(self):
        with open("loading/items.txt") as data:
            s = ""
            str = []
            b = False
            for line in data:
                line = line.rstrip('\n')
                if len(line) == 0:
                    continue
                if line[len(line) - 1] == ':':
                    if b:
                        self.inventory.all_items[s] = str
                    else:
                        b = True
                    str = line.split(':')
                    s = str[0]
                    self.inventory.all_items[s] = ""
                elif line[len(line) - 1] == ';':
                    str = line.split(';')
                    self.inventory.all_items[s + "_refact"] = str[0]
                    str = []
                else:
                    str.append(line)
            self.inventory.all_items[s] = str

    def load_maps(self, from_save):
        self.map_manager = MapManager(self.screen, self.player, self.inventory)
        if from_save:
            self.decrypt_saving("map")
            self.map_manager.tp_player(from_save=from_save)
        else:
            self.map_manager.tp_player()

    def save(self):
        with open("loading/save_player.txt", 'wt') as data:
            data.write("self.player.position = " + str(self.player.get_location()) + "\n")
            data.write("self.player.life = " + str(self.player.life) + "\n")
            data.write("self.player.stats.hp = " + str(self.player.stats.hp) + "\n")
            data.write("self.player.stats.ad = " + str(self.player.stats.ad) + "\n")
            data.write("self.player.stats.ap = " + str(self.player.stats.ap) + "\n")
            data.write("self.player.stats.armor = " + str(self.player.stats.armor) + "\n")
            data.write("self.player.stats.rm = " + str(self.player.stats.rm) + "\n")
            data.write("self.player.stats.chance = " + str(self.player.stats.chance) + "\n")
            data.write("self.player.stats.speed = " + str(self.player.stats.speed) + "\n")
            data.write("self.player.gold = " + str(self.player.gold) + "\n")
            data.write("self.player.level = " + str(self.player.level) + "\n")
            data.write("self.player.xp = " + str(self.player.xp) + "\n")
            data.write("self.player.xp_needed_to_level_up = " + str(self.player.xp_needed_to_level_up) + "\n")

        with open("loading/save_inventory.txt", 'wt') as data:
            acc = 0
            for item in self.inventory.items:
                data.write("self.inventory.add_item(Item('" + item.name + "', False, pygame.Rect(0, 0, 0, 0), '" +
                           item.type + "'))\n")
                data.write("self.inventory.items[" + str(acc) + "].number = " + str(item.number) + "\n")
                acc += 1

        with open("loading/save_map.txt", 'wt') as data:
            data.write("self.map_manager.current_map = '" + self.map_manager.current_map + "'\n")
            for m in self.map_manager.maps:
                acc = 0
                for pnj in self.map_manager.maps[m].pnjs:
                    if pnj.mode != '0':
                        data.write("self.map_manager.maps['" + m + "'].pnjs[" +
                                   str(acc) + "].mode = '" + pnj.mode + "'\n")
                        data.write("self.map_manager.maps['" + m + "'].pnjs[" +
                                   str(acc) + "].change_sprite(self.map_manager.maps['" + m + "'].texts)\n")
                    acc += 1
                acc = 0
                for item in self.map_manager.maps[m].items:
                    if not item.should_appear:
                        data.write("self.map_manager.maps['" + m + "'].items[" +
                                   str(acc) + "].should_appear = " + str(item.should_appear) + "\n")
                        self.map_manager.maps[m].group.add(item)
                        data.write("self.map_manager.maps['" + m + "'].group.remove(self.map_manager.maps['" +
                                   m + "'].items[" + str(acc) + "])\n")
                        self.map_manager.maps[m].group.remove(item)
                    acc += 1

    def decrypt_saving(self, start):
        with open(f'loading/save_{start}.txt') as data:
            for line in data:
                line = line.rstrip('\n')
                exec(line)

    # interactions sur la carte actuelle ----------------------------------------------------------
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

    def gold_update(self):
        self.screen.blit(self.coin, (700, 30))
        gold = str(self.player.gold)
        n = self.font_fight2.render(gold, False, "#c6c704")
        self.screen.blit(n, (650, 40))

    def life_update(self):
        for i in range(self.player.life):
            self.screen.blit(self.hair, (50 + i * 48, 30))
        if self.player.life != 0:
            self.player.mode = str(5 - self.player.life)
            self.player.change_sprite()
        if self.player.life == 0:
            self.player.mono_switch()
            dead = True
            acc = 0
            index = 0
            clock = 0
            while dead:
                self.screen.blit(self.death_bg, (0, 0))
                self.screen.blit(self.gob, (100, 200))
                if index == 0:
                    self.screen.blit(self.calv1, (600 - acc, 200))
                    if clock >= 100:
                        index += 1
                        clock = 0
                else:
                    self.screen.blit(self.calv2, (600 - acc, 200))
                    if clock >= 100:
                        index = 0
                        clock = 0
                clock += 5
                acc += 0.5
                if 600 - acc <= 100:
                    dead = False
                pygame.display.flip()
            wait_for_action = True
            while wait_for_action:
                self.screen.blit(self.death_bg, (0, 0))
                self.screen.blit(self.wasted, (163, 100))
                self.screen.blit(self.box, (self.X_POS, self.Y_POS - 200))
                n = self.font.render(self.intro1, False, (0, 0, 0))
                self.screen.blit(n, (self.X_POS + 50, self.Y_POS - 140))
                n = self.font.render(self.intro2, False, (0, 0, 0))
                self.screen.blit(n, (self.X_POS + 50, self.Y_POS - 110))
                n = self.font.render(self.intro3, False, (0, 0, 0))
                self.screen.blit(n, (self.X_POS + 50, self.Y_POS - 80))
                pygame.display.flip()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        return
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:
                            pygame.quit()
                            return
                        elif event.key == pygame.K_n:
                            wait_for_action = False
                        elif event.key == pygame.K_s:
                            if os.stat("./loading/save_player.txt").st_size > 0 and \
                                    os.stat("./loading/save_map.txt").st_size > 0:
                                self.load_from_saved_game = True
                            wait_for_action = False
                        self.run(was_dead=True)

    # méthodes relatives à l'inventaire ----------------------------------------------------
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
                    if use_item(self.inventory.items[self.inventory_index], self.player) == 1:
                        if self.inventory.items[self.inventory_index].number == 1 and \
                                self.inventory_index == len(self.inventory.items) - 1:
                            self.inventory_index -= 1
                            self.inventory.remove_item(self.inventory.items[self.inventory_index + 1])
                        else:
                            self.inventory.remove_item(self.inventory.items[self.inventory_index])
                if self.inventory_index == -1:
                    self.inventory_index = 0

            if pressed == pygame.K_p:
                self.save()

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
            self.screen.blit(x, (380, 200 + 20 * i))

    def show_inventory(self):
        if self.inventory_opened:
            self.screen.blit(self.inventory_display, (40, 100))
            self.screen.blit(self.box, (self.X_POS, self.Y_POS))
            n = self.font.render(self.man_inventory1, False, (0, 0, 0))
            self.screen.blit(n, (self.X_POS + 50, self.Y_POS + 40))
            n = self.font.render(self.man_inventory2, False, (0, 0, 0))
            self.screen.blit(n, (self.X_POS + 50, self.Y_POS + 70))
            n = self.font.render(self.man_inventory3, False, (0, 0, 0))
            self.screen.blit(n, (self.X_POS + 50, self.Y_POS + 100))
            n = self.font.render(self.man_inventory4, False, (0, 0, 0))
            self.screen.blit(n, (self.X_POS + 50, self.Y_POS + 130))
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

    def close_open_store(self):
        if self.store_opened:
            self.store_opened = False
            self.can_handle_input = True
            self.can_handle_store_input = False
        else:
            self.can_handle_inventory_input = False
            self.store_opened = True
            self.can_handle_input = False
            self.can_handle_store_input = True

    def show_store(self):
        if self.store_opened:
            self.screen.blit(self.store_display, (50, 0))
            n = self.font.render("0   Lotion de repousse       20$", False, (0, 0, 0))
            self.screen.blit(n, (85, 60))
            n = self.font.render("1   Pastis                               10$", False, (0, 0, 0))
            self.screen.blit(n, (85, 185))
            n = self.font.render("2   Potion                              13$", False, (0, 0, 0))
            self.screen.blit(n, (85, 305))
            n = self.font.render("3   Vieille Cara                     13$", False, (0, 0, 0))
            self.screen.blit(n, (85, 425))
            n = self.font.render("4   Tournevis                       11$", False, (0, 0, 0))
            self.screen.blit(n, (85, 540))
            n = self.font.render("5   Citron                              20$", False, (0, 0, 0))
            self.screen.blit(n, (435, 60))
            n = self.font.render("6   Anguille                           10$", False, (0, 0, 0))
            self.screen.blit(n, (435, 185))
            n = self.font.render("7   Slip sale                          13$", False, (0, 0, 0))
            self.screen.blit(n, (435, 305))
            n = self.font.render("8   Presse-Ail                       13$", False, (0, 0, 0))
            self.screen.blit(n, (435, 425))
            n = self.font.render("9   Foreuse                           11$", False, (0, 0, 0))
            self.screen.blit(n, (435, 540))

            self.screen.blit(self.coin, (670, 596))
            gold = str(self.player.gold)
            n = self.font.render(gold, False, "#c6c704")
            self.screen.blit(n, (630, 614))
            # if len(self.inventory.items) > 0:
            #    self.blit_inventory(self.inventory_index)

    def handle_store_input(self, pressed):
        if self.can_handle_store_input:

            if pressed == pygame.K_0 and self.player.gold >= 20:
                pastis = Item("lotion", False, pygame.rect.Rect(-10, -10, 1, 1), "item2")
                self.inventory.add_item(pastis)
                self.player.gold -= 20

            if pressed == pygame.K_1 and self.player.gold >= 10:
                pastis = Item("pastis", False, pygame.rect.Rect(-10, -10, 1, 1), "item2")
                self.inventory.add_item(pastis)
                self.player.gold -= 10

            if pressed == pygame.K_2 and self.player.gold >= 13:
                pastis = Item("potion", False, pygame.rect.Rect(-10, -10, 1, 1), "item2")
                self.inventory.add_item(pastis)
                self.player.gold -= 13

            if pressed == pygame.K_3 and self.player.gold >= 13:
                pastis = Item("old_carapils", False, pygame.rect.Rect(-10, -10, 1, 1), "item2")
                self.inventory.add_item(pastis)
                self.player.gold -= 13

            if pressed == pygame.K_4 and self.player.gold >= 11:
                pastis = Item("tournevis", False, pygame.rect.Rect(-10, -10, 1, 1), "item2")
                self.inventory.add_item(pastis)
                self.player.gold -= 11

            if pressed == pygame.K_5 and self.player.gold >= 20:
                pastis = Item("citron", False, pygame.rect.Rect(-10, -10, 1, 1), "item2")
                self.inventory.add_item(pastis)
                self.player.gold -= 20

            if pressed == pygame.K_6 and self.player.gold >= 10:
                pastis = Item("anguille", False, pygame.rect.Rect(-10, -10, 1, 1), "item2")
                self.inventory.add_item(pastis)
                self.player.gold -= 10

            if pressed == pygame.K_7 and self.player.gold >= 13:
                pastis = Item("slip", False, pygame.rect.Rect(-10, -10, 1, 1), "item2")
                self.inventory.add_item(pastis)
                self.player.gold -= 13

            if pressed == pygame.K_8 and self.player.gold >= 13:
                pastis = Item("presse", False, pygame.rect.Rect(-10, -10, 1, 1), "item2")
                self.inventory.add_item(pastis)
                self.player.gold -= 13

            if pressed == pygame.K_9 and self.player.gold >= 11:
                pastis = Item("foreuse", False, pygame.rect.Rect(-10, -10, 1, 1), "item2")
                self.inventory.add_item(pastis)
                self.player.gold -= 11

    # méthodes relatives aux combats ------------------------------------------------------------------
    def show_fight(self):
        acc = 0
        acc2 = 0
        go_down = True
        atk_index = 0
        t0 = pygame.time.get_ticks()
        attack = False
        status = False
        status1 = False
        status2 = False
        first = None
        second = None
        color_status_player = (0, 0, 0)
        color_status_monster = (0, 0, 0)
        while self.fighting:
            self.screen.blit(self.fight, (0, 0))
            self.screen.blit(self.player.fight_image, (50, 200 + acc))
            self.screen.blit(self.map_manager.fight.monster.image, (425, 20 + acc))
            if self.player.status != "":
                if self.player.status == "poison":
                    color_status_player = (148, 0, 211)
                elif self.player.status == "burn":
                    color_status_player = (255, 140, 0)
                elif self.player.status == "freeze":
                    color_status_player = (135, 206, 250)
                elif self.player.status == "sleep":
                    color_status_player = (192, 192, 192)
                else:
                    color_status_player = (255, 255, 0)
            if self.map_manager.fight.monster.status != "":
                if self.map_manager.fight.monster.status == "poison":
                    color_status_monster = (148, 0, 211)
                elif self.map_manager.fight.monster.status == "burn":
                    color_status_monster = (255, 140, 0)
                elif self.map_manager.fight.monster.status == "freeze":
                    color_status_monster = (135, 206, 250)
                elif self.map_manager.fight.monster.status == "sleep":
                    color_status_monster = (192, 192, 192)
                else:
                    color_status_monster = (255, 255, 0)
            n = self.font_fight.render("Gobzer    HP: " + str(self.player.stats.hp) + "    LVL: " +
                                       str(self.player.level), False, color_status_player)
            self.screen.blit(n, (460, 515))
            n = self.font_fight.render(self.map_manager.fight.monster.refact_name + "    HP: " +
                                       str(int(self.map_manager.fight.monster.stats.hp)) + "    LVL: " +
                                       str(self.map_manager.fight.monster.level), False, color_status_monster)
            self.screen.blit(n, (15, 123))
            if self.map_manager.fight.fight_index == 0:
                n = self.font_fight2.render(self.map_manager.fight.monster.spawn_sentence, False, (0, 0, 0))
                self.screen.blit(n, (self.X_POS, self.Y_POS + 110))
            elif self.map_manager.fight.fight_index == 1:
                self.screen.blit(self.fight_buttons, (self.X_POS + 5, self.Y_POS + 75))
            elif self.map_manager.fight.fight_index == 2:
                self.screen.blit(self.atk_bg, (150, 150))
                acc1 = 0
                acc3 = 1
                for atk in self.player.attacks:
                    n = self.font_fight2.render(str(acc3) + " = " + atk, False, (0, 0, 0))
                    self.screen.blit(n, (170, 170 + acc1))
                    acc1 += 50
                    acc3 += 1
                n = self.font_fight2.render("B = retour", False, (0, 0, 0))
                self.screen.blit(n, (170, 600))
            elif self.map_manager.fight.fight_index == 3:
                self.screen.blit(self.atk_bg, (150, 150))
                acc1 = 0
                for item in self.inventory.items:
                    if item.fight_item:
                        n = self.font_fight2.render(item.refact_name, False, (0, 0, 0))
                        self.screen.blit(n, (170, 170 + acc1))
                        acc1 += 50
                n = self.font_fight2.render("B = retour", False, (0, 0, 0))
                self.screen.blit(n, (170, 600))
            elif self.map_manager.fight.fight_index == 4:
                self.map_manager.fight.fight()
                if self.map_manager.fight.player_can_attack:
                    first = self.player
                    second = self.map_manager.fight.monster
                else:
                    first = self.map_manager.fight.monster
                    second = self.player
                if acc2 == 0 and status1 and first.status != "sleep":
                    if first == self.player:
                        self.map_manager.fight.use_attack(self.player.attacks[atk_index], first, second)
                    else:
                        self.map_manager.fight.use_attack(self.map_manager.fight.monster.attack_chosen, first, second)
                    acc2 = 1
                if not attack and status1:
                    if first == self.player:
                        n = self.font_fight2.render("Vous utilisez l'attaque " +
                                                    self.player.attacks[atk_index] + ".", False, (0, 0, 0))
                        self.screen.blit(n, (self.X_POS, self.Y_POS + 110))
                    else:
                        n = self.font_fight2.render(self.map_manager.fight.monster.refact_name + " lance " +
                                                    self.map_manager.fight.monster.attack_chosen + ".", False, (0, 0, 0))
                        self.screen.blit(n, (self.X_POS, self.Y_POS + 110))
                if pygame.time.get_ticks() - t0 > 2000 and not attack and status1 and second.status != "sleep":
                    if first == self.player:
                        self.map_manager.fight.use_attack(self.map_manager.fight.monster.attack_chosen, second, first)
                    else:
                        self.map_manager.fight.use_attack(self.player.attacks[atk_index], second, first)
                    attack = True
                if attack and status1:
                    if first == self.player:
                        n = self.font_fight2.render(self.map_manager.fight.monster.refact_name + " lance " +
                                                    self.map_manager.fight.monster.attack_chosen + ".", False, (0, 0, 0))
                        self.screen.blit(n, (self.X_POS, self.Y_POS + 110))
                    else:
                        n = self.font_fight2.render("Vous utilisez l'attaque " +
                                                    self.player.attacks[atk_index] + ".", False, (0, 0, 0))
                        self.screen.blit(n, (self.X_POS, self.Y_POS + 110))
                if pygame.time.get_ticks() - t0 > 4000:
                    acc2 = 0
                    attack = False
                    if status1 and status2:
                        if poisoned(self.map_manager.fight.monster) or poisoned(self.player) or \
                                burned(self.map_manager.fight.monster) or burned(self.player):
                            status = True
                        status1 = False
                    elif not status1 and status2:
                        status2 = False
                if not status1 and not status2 and status:
                    n = self.font_fight2.render("Le poison ou la brûlure agit.", False, (0, 0, 0))
                    self.screen.blit(n, (self.X_POS, self.Y_POS + 110))
                if pygame.time.get_ticks() - t0 > 5000:
                    if (self.player.status == "sleep" or self.player.status == "freeze") and self.player.sleep > 0:
                        self.player.sleep -= 1
                        if self.player.sleep == 0:
                            self.player.status = ""
                    if (self.map_manager.fight.monster.status == "sleep" or self.map_manager.fight.monster.status == "freeze")\
                            and self.map_manager.fight.monster.sleep > 0:
                        self.map_manager.fight.monster.sleep -= 1
                        if self.map_manager.fight.monster.sleep == 0:
                            self.map_manager.fight.monster.status = ""
                    self.map_manager.fight.fight_index = 1

            if acc + 200 >= 250:
                go_down = False
            if acc <= 0:
                go_down = True
            if go_down:
                acc += 0.3
            else:
                acc -= 0.3
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit_while_fighting = True
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and self.map_manager.fight.fight_index < 1:
                        self.map_manager.fight.fight_index = 1
                    elif self.map_manager.fight.fight_index == 1 and \
                            (event.key == pygame.K_a or event.key == pygame.K_z or event.key == pygame.K_e):
                        if event.key == pygame.K_a:
                            self.map_manager.fight.fight_index = 2
                        elif event.key == pygame.K_z:
                            self.map_manager.fight.fight_index = 3
                        else:
                            escape_chance = pow(5 / 6, self.map_manager.fight.monster.level)
                            if rd.randint(100, 150) * escape_chance > 70:
                                self.player.base_stats_()
                                self.map_manager.fight.monster.base_stats_()
                                self.close_open_fight()
                            else:
                                self.map_manager.fight.fight_index = 1
                    elif self.map_manager.fight.fight_index == 2 and \
                            (pygame.K_1 <= event.key <= pygame.K_4 or event.key == pygame.K_b):
                        if event.key == pygame.K_b:
                            self.map_manager.fight.fight_index = 1
                        else:
                            if event.key == pygame.K_1:
                                atk_index = 0
                            elif event.key == pygame.K_2:
                                atk_index = 1
                            elif event.key == pygame.K_3:
                                atk_index = 2
                            else:
                                atk_index = 3
                            self.map_manager.fight.fight_index = 4
                            t0 = pygame.time.get_ticks()
                            status = False
                            status1 = True
                            status2 = True
                            self.map_manager.fight.monster.choose_attack()
                    elif self.map_manager.fight.fight_index == 3 and \
                            (pygame.K_1 <= event.key <= pygame.K_4 or event.key == pygame.K_b):
                        if event.key == pygame.K_b:
                            self.map_manager.fight.fight_index = 1
            if self.player.stats.hp <= 0 or self.map_manager.fight.monster.stats.hp <= 0:
                self.player.base_stats_()
                self.map_manager.fight.monster.base_stats_()
                if self.player.stats.hp <= 0:
                    self.player.life -= 1
                else:
                    n = self.map_manager.fight.monster.level - self.player.level
                    self.player.xp += self.map_manager.fight.monster.level*2 + n
                    if self.player.xp >= self.player.xp_needed_to_level_up:
                        self.player.level += 1
                        self.player.set_stats()
                        self.player.xp_needed()
                    print(self.map_manager.fight.monster.name)
                    self.player.gold += self.map_manager.fight.monster.level*2 + n
                print(self.player.xp)
                self.close_open_fight()

    def close_open_fight(self):
        if self.fighting:
            self.fighting = False
            self.can_handle_input = True
            self.can_handle_fight_input = False
            self.map_manager.clock = pygame.time.get_ticks()
        else:
            self.fighting = True
            self.can_handle_input = False
            self.can_handle_fight_input = True

    def can_be_pressed(self, key, timeout):
        current_time = pygame.time.get_ticks()
        if self.key_timeout[key] > current_time:
            return False
        self.key_timeout[key] = current_time + timeout
        return True
