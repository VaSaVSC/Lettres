import fnmatch
from dataclasses import dataclass
import pygame
import pytmx
import pyscroll
import os

from typing import List

from interactive_obj import Obj
from inventory import Item
from player import PNJ


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
    texts: dict()
    interactive_obj: List[Obj]
    items: List[Item]
    collide: List[pygame.Rect]


def check_type(type_t, type_list):
    for e in type_list:
        if e == type_t:
            return True
    return False


class MapManager:

    def __init__(self, screen, player, inventory):
        self.maps = dict()
        self.screen = screen
        self.player = player
        self.inventory = inventory
        self.load_items()
        self.current_map = "start"

        self.register_map("start", portals=[
            Portal(origin="start", origin_point="s_w1_exit",
                   dest="world1", dest_point="s_w1_exitP")
        ])

        self.register_map("world1", portals=[
            Portal(origin="world1", origin_point="w1_h1_enter",
                   dest="world1_house1", dest_point="w1_h1_enterP"),
            Portal(origin="world1", origin_point="s_w1_enter",
                   dest="start", dest_point="s_w1_enterP")
        ],  pnjs=[
            PNJ("paul", nb_points=4, speed=1)
        ])

        self.register_map("world1_house1", portals=[
            Portal(origin='world1_house1', origin_point="w1_h1_exit",
                   dest="world1", dest_point="w1_h1_exitP")
        ],  pnjs=[
            PNJ("andreas", nb_points=4, speed=2)
        ])

        self.tp_player("player")
        self.tp_pnjs()

    def load_items(self):
        with open("./texts/items.txt") as data:
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
                    self.inventory.all_items[s+"_refact"] = str[0]
                    str = []
                else:
                    str.append(line)
            self.inventory.all_items[s] = str

    def check_pnj_collisions(self, dialog_box):
        for sprite in self.get_group().sprites():
            if type(sprite) == PNJ and sprite.feet.colliderect(self.player.rect):
                dialog_box.execute(sprite.refact_name, False, sprite.dialog)
            if type(sprite) == Item and sprite.can_be_carried:
                dialog_box.execute(sprite.name, True, sprite.dialog)
                sprite.should_appear = False
                sprite.is_carried = True
                self.inventory.add_item(sprite)
                self.get_group().remove(sprite)
                self.tp_items()

    def check_interactive_obj_collisions(self, dialog_box):
        for obj in self.get_map().interactive_obj:
            if obj.rect.colliderect(self.player.rect):
                dialog_box.execute(obj.refact_name, False, obj.dialog)

    def check_collisions(self):

        # portails
        for portal in self.get_map().portals:
            if portal.origin == self.current_map:
                point = self.get_object(portal.origin_point)
                rect = pygame.Rect(point.x, point.y, point.width, point.height)

                if self.player.feet.colliderect(rect):
                    copy_portal = portal
                    self.current_map = portal.dest
                    self.tp_player(copy_portal.dest_point)

        # collisions
        pnj_speed = []
        for sprite in self.get_group().sprites():
            if type(sprite) is PNJ:
                pnj_speed.append(sprite.speed)
                if sprite.feet.colliderect(self.player.rect):
                    sprite.speed = 0
                else:
                    sprite.speed = sprite.base_speed

            if sprite.feet.collidelist(self.get_walls()) > -1 and type(sprite) != Item:
                sprite.move_back()

            if type(sprite) == Item and sprite.feet.colliderect(self.player.rect):
                self.player.move_back()
                sprite.move_back()
                sprite.can_be_carried = True

        if self.player.feet.collidelist(self.get_map().collide) > -1:
            self.player.move_back()

    def tp_player(self, name):
        point = self.get_object(name)
        self.player.position[0] = point.x
        self.player.position[1] = point.y
        self.player.save_location()
        self.tp_items()

    def register_map(self, name, portals=[], pnjs=[]):

        type_list = {'panel'}

        # charger les textes
        texts = dict()
        for filename in os.listdir("texts"):
            if fnmatch.fnmatch(filename, f'{name}.txt'):
                with open(f'./texts/{filename}') as data:
                    s = ""
                    str = []
                    b = False
                    for line in data:
                        line = line.rstrip('\n')
                        if len(line) == 0:
                            continue
                        if line[len(line) - 1] == ':':
                            if b:
                                texts[s] = str
                                str = []
                            else:
                                b = True
                            string = line.split(':')
                            s = string[0]
                            texts[s] = ""
                        else:
                            str.append(line)
                    texts[s] = str

        # charger la carte
        tmx_data = pytmx.util_pygame.load_pygame(f"./map/{name}.tmx")
        index = []
        acc = 0
        for ln in tmx_data.layernames:
            if "XXX" in ln:
                index.append(acc)
            acc += 1

        collide = []
        for i in index:
            for x in range(tmx_data.width):
                for y in range(tmx_data.height):
                    if tmx_data.get_tile_image(x, y, i) is not None:
                        collide.append(pygame.rect.Rect(x*16, y*16, 16, 16))

        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 2

        walls = []
        interactive_obj = []
        items = []
        for obj in tmx_data.objects:
            if obj.type == "collisions":
                walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
            if check_type(obj.type, type_list):
                interactive_obj.append(Obj(obj.name, obj.type, texts[obj.name], obj.x, obj.y, obj.width, obj.height))
            if obj.type == "item":
                items.append(Item(obj.name, True, pygame.Rect(obj.x, obj.y, obj.width, obj.height)))

        # groupes de calques
        group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=4)
        group.add(self.player)
        for pnj in pnjs:
            pnj.dialog = texts[pnj.name]
            group.add(pnj)
        for i in items:
            i.dialog = texts[i.name]
            group.add(i)

        # nouveau Map obj
        self.maps[name] = Map(name, walls, group, tmx_data, portals, pnjs, texts,
                              interactive_obj, items, collide)

    def get_map(self):
        return self.maps[self.current_map]

    def get_group(self):
        return self.get_map().group

    def get_walls(self):
        return self.get_map().walls

    def get_object(self, name):
        return self.get_map().tmx_data.get_object_by_name(name)

    def tp_pnjs(self):
        for m in self.maps:
            map_data = self.maps[m]
            pnjs = map_data.pnjs

            for pnj in pnjs:
                pnj.load_points(map_data.tmx_data)
                pnj.tp_spawn()

    def tp_items(self):
        for i in self.get_map().items:
            if i.should_appear:
                i.tp_spawn()
            else:
                i.position = [None] * 2

    def draw(self):
        self.get_group().draw(self.screen)
        self.get_group().center(self.player.rect.center)

    def update(self):
        self.get_group().update()
        self.check_collisions()

        for pnj in self.get_map().pnjs:
            pnj.move()
