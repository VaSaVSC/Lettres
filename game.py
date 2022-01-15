import pygame
import pytmx
import pyscroll
from player import Player


class Game:

    def __init__(self):

        # affichage de la fenêtre du jeu
        self.screen = pygame.display.set_mode((800, 800))
        pygame.display.set_caption("Lettres")

        # charger la carte
        tmx_data = pytmx.util_pygame.load_pygame('test.tmx')
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 2

        # générer le joueur
        player_position = tmx_data.get_object_by_name("player")
        self.player = Player(player_position.x, player_position.y)

        # listes des objets "collisions"
        self.walls = []
        for obj in tmx_data.objects:
            if obj.type == "collisions":
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        # groupes de calques
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=1)
        self.group.add(self.player)


    def update(self):
        self.group.update()

        for sprite in self.group.sprites():
            if sprite.feet.collidelist(self.walls) > -1:
                sprite.move_back()

    def handle_input(self):
        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_UP]:
            self.player.move_up()
            self.player.change_animation('up')
        elif pressed[pygame.K_DOWN]:
            self.player.move_down()
            self.player.change_animation('down')
        elif pressed[pygame.K_LEFT]:
            self.player.move_left()
            self.player.change_animation('left')
        elif pressed[pygame.K_RIGHT]:
            self.player.move_right()
            self.player.change_animation('right')


    def run(self):

        # pour les fps
        clock = pygame.time.Clock()

        running = True

        while running:

            self.player.save_location()
            self.handle_input()
            self.update()
            self.group.center(self.player.rect)
            self.group.draw(self.screen)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            clock.tick(60)

        pygame.quit()
