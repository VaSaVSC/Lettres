from dataclasses import dataclass
import pygame
import pytmx
import pyscroll
from typing import List

from src.player import PNJ


@dataclass
class Portal:
    origin: str
    origin_point: str
    dest: str
    dest_point: str


@dataclass
class Map:
    name: str
    walls: List[pygame.Rect]
    group: pyscroll.PyscrollGroup
    tmx_data: pytmx.TiledMap
    portals: List[Portal]
    pnjs: List[PNJ]


class MapManager:

    def __init__(self, screen, player):
        self.maps = dict()
        self.screen = screen
        self.player = player
        self.current_map = "world1"

        self.register_map("world1", portals=[
            Portal(origin="world1", origin_point="w1_h1_enter",
                   dest="world1_house1", dest_point="w1_h1_enterP")
        ],  pnjs=[
            PNJ("paul", nb_points=4)])
        self.register_map("world1_house1", portals=[
            Portal(origin='world1_house1', origin_point="w1_h1_exit",
                   dest="world1", dest_point="w1_h1_exitP")
        ])
        self.tp_player("player")

    def check_collisions(self):
        #portails
        for portal in self.get_map().portals:
            if portal.origin == self.current_map:
                point = self.get_object(portal.origin_point)
                rect = pygame.Rect(point.x, point.y, point.width, point.height)

                if self.player.feet.colliderect(rect):
                    copy_portal = portal
                    self.current_map = portal.dest
                    self.tp_player(copy_portal.dest_point)

        # collisions
        for sprite in self.get_group().sprites():
            if sprite.feet.collidelist(self.get_walls()) > -1:
                sprite.move_back()

    def tp_player(self, name):
        point = self.get_object(name)
        self.player.position[0] = point.x
        self.player.position[1] = point.y
        self.player.save_location()

    def register_map(self, name, portals=[], pnjs=[]):
        # charger la carte
        tmx_data = pytmx.util_pygame.load_pygame(f"../Lettres/map/{name}.tmx")
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 2

        walls = []
        for obj in tmx_data.objects:
            if obj.type == "collisions":
                walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        # groupes de calques
        group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=4)
        group.add(self.player)
        for pnj in pnjs:
            group.add(pnj)

        # nouveau Map obj
        self.maps[name] = Map(name, walls, group, tmx_data, portals, pnjs)

    def get_map(self):
        return self.maps[self.current_map]

    def get_group(self):
        return self.get_map().group

    def get_walls(self):
        return self.get_map().walls

    def get_object(self, name):
        return self.get_map().tmx_data.get_object_by_name(name)

    def draw(self):
        self.get_group().draw(self.screen)
        self.get_group().center(self.player.rect.center)

    def update(self):
        self.get_group().update()
        self.check_collisions()
