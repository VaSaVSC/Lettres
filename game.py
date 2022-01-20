import pygame

from dialog import DialogBox
from inventory import Inventory
from map import MapManager
from player import Player


class Game:

    def __init__(self):

        # affichage de la fenêtre du jeu
        self.screen = pygame.display.set_mode((800, 800))
        pygame.display.set_caption("Lettres")

        # générer le joueur
        self.player = Player()
        self.inventory = Inventory()
        self.map_manager = MapManager(self.screen, self.player, self.inventory)
        self.dialog_box = DialogBox()

        self.hair = pygame.image.load("./ath_assets/meche.png")
        self.hair = pygame.transform.scale(self.hair, (64, 64))

        self.item = pygame.image.load("./items/item.png")
        self.item = pygame.transform.scale(self.item, (32, 32))

    def update(self):
        self.map_manager.update()

    def handle_input(self):
        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_UP]:
            self.dialog_box.reading = False
            self.player.move_up()
        elif pressed[pygame.K_DOWN]:
            self.dialog_box.reading = False
            self.player.move_down()
        elif pressed[pygame.K_LEFT]:
            self.dialog_box.reading = False
            self.player.move_left()
        elif pressed[pygame.K_RIGHT]:
            self.dialog_box.reading = False
            self.player.move_right()

    def life_update(self):
        for i in range(self.player.life):
            self.screen.blit(self.hair, (50 + i*48, 30))

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
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.map_manager.check_pnj_collisions(self.dialog_box)
                        self.map_manager.check_interactive_obj_collisions(self.dialog_box)

            clock.tick(60)

        pygame.quit()
