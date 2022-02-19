import fnmatch
from copy import deepcopy
from dataclasses import dataclass
import pygame
import pytmx
import pyscroll
import os
import random as rd

from typing import List

from fight import Fight
from interactive_obj import Obj
from inventory import Item
from monster import Monster
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
    fight_zone: List[pygame.Rect]
    level: int
    monsters: List[Monster]


type_list = {'panel', 'TV'}


def check_type(type_t):
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
        self.inventory_display = pygame.image.load("./ath_assets/inventory.png")

        self.monsters = dict()
        self.load_monsters()
        self.fight = None

        self.clock = pygame.time.get_ticks()

        self.current_map = "start"

        self.register_map("start", portals=[
            Portal(origin="start", origin_point="s_w1_exit",
                   dest="world1", dest_point="s_w1_exitP")
        ])

        self.register_map("world1", portals=[
            Portal(origin="world1", origin_point="w1_h1_enter",
                   dest="world1_house1", dest_point="w1_h1_enterP"),
            Portal(origin="world1", origin_point="s_w1_enter",
                   dest="start", dest_point="s_w1_enterP"),
            Portal(origin="world1", origin_point="w1_d_enter",
                   dest="dungeon", dest_point="d_w1_enterP"),
            Portal(origin="world1", origin_point="w1_des_enter",
                   dest="desert", dest_point="des_w1_enterP"),
            Portal(origin="world1", origin_point="w1_paki_enter",
                   dest="paki", dest_point="paki_w1_enterP"),
            Portal(origin="world1", origin_point="w1_plage_enter",
                   dest="plage", dest_point="plage_w1_enterP")
        ],  pnjs=[
            PNJ("paul", nb_points=4, speed=1),
            PNJ("claude", nb_points=1, speed=2, random_move=True)
        ])

        self.register_map("world1_house1", portals=[
            Portal(origin='world1_house1', origin_point="w1_h1_exit",
                   dest="world1", dest_point="w1_h1_exitP")
        ],  pnjs=[
            PNJ("andreas", nb_points=4, speed=2)
        ])

        self.register_map("dungeon", portals=[
            Portal(origin='dungeon', origin_point="d_w1_exit",
                   dest="world1", dest_point="w1_d_exitP")
        ], pnjs=[
            PNJ("darkgob", nb_points=1, speed=0),
            PNJ("adèle", nb_points=1, speed=0),
            PNJ("zoz", nb_points=1, speed=0)
        ], default_layer=3)

        self.register_map("desert", portals=[
            Portal(origin='desert', origin_point="des_w1_exit",
                   dest="world1", dest_point="w1_des_exitP"),
            Portal(origin='desert', origin_point="des_i_enter",
                   dest="ice_world", dest_point="i_des_enterP")
        ], pnjs=[
            PNJ("chloé", nb_points=1, speed=0)
        ], default_layer=3)

        self.register_map("ice_world", portals=[
            Portal(origin='ice_world', origin_point="i_des_exit",
                   dest="desert", dest_point="des_i_exitP"),
            Portal(origin='ice_world', origin_point="i_bar_enter",
                   dest="bar", dest_point="bar_i_enterP")
        ], pnjs=[
            PNJ("frans", nb_points=1, speed=0)
        ], default_layer=3)

        self.register_map("paki", portals=[
            Portal(origin='paki', origin_point="paki_w1_exit",
                   dest="world1", dest_point="w1_paki_exitP")
        ], pnjs=[
            PNJ("achille", nb_points=1, speed=0)
        ], default_layer=3)

        self.register_map("plage", portals=[
            Portal(origin='plage', origin_point="plage_w1_exit",
                   dest="world1", dest_point="w1_plage_exitP")
        ])

        self.register_map("bar", portals=[
            Portal(origin='bar', origin_point="bar_i_exit",
                   dest="ice_world", dest_point="i_bar_exitP")
        ], pnjs=[
            PNJ("raph", nb_points=1, speed=0),
            PNJ("thib", nb_points=1, speed=0)
        ], default_layer=2)

        self.tp_pnjs()

    def register_map(self, name, portals=[], pnjs=[], level=0, default_layer=5):

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
        indexXXX = []
        acc = 0
        for ln in tmx_data.layernames:
            if "XXX" in ln:
                indexXXX.append(acc)
            acc += 1

        collide = []
        for i in indexXXX:
            for x in range(tmx_data.width):
                for y in range(tmx_data.height):
                    if tmx_data.get_tile_image(x, y, i) is not None:
                        collide.append(pygame.rect.Rect(x*16, y*16, 16, 16))

        indexYYY = []
        acc = 0
        for ln in tmx_data.layernames:
            if "YYY" in ln:
                indexYYY.append(acc)
            acc += 1

        fight_zone = []
        for i in indexYYY:
            for x in range(tmx_data.width):
                for y in range(tmx_data.height):
                    if tmx_data.get_tile_image(x, y, i) is not None:
                        fight_zone.append(pygame.rect.Rect(x*16, y*16, 16, 16))

        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 2

        walls = []
        interactive_obj = []
        items = []
        for obj in tmx_data.objects:
            if obj.type == "collisions":
                walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
            if check_type(obj.type):
                interactive_obj.append(Obj(obj.name, obj.type, texts[obj.name], obj.x, obj.y, obj.width, obj.height))
            # items directement présents sur la carte
            if obj.type == "item1" or obj.type == "coffre":
                items.append(Item(obj.name, True, pygame.Rect(obj.x, obj.y, obj.width, obj.height), obj.type))
            # items qui apparaîtront suite à la complétion d'une quête
            if obj.type == "item2":
                items.append(Item(obj.name, False, pygame.Rect(obj.x, obj.y, obj.width, obj.height), obj.type))
            # items utilisables en combat, et directement présents sur la carte
            if obj.type == "item3":
                items.append(Item(obj.name, True, pygame.Rect(obj.x, obj.y, obj.width, obj.height), obj.type))

        # charger les monstres disponibles sur cette carte
        monsters = []
        for monster in self.monsters:
            if level in self.monsters[monster].level_range:
                monsters.append(monster)

        # groupes de calques
        group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=default_layer)
        group.add(self.player)
        for pnj in pnjs:
            pnj.dialog = texts[pnj.name + pnj.mode]
            group.add(pnj)
        for i in items:
            i.dialog = texts[i.name]
            group.add(i)

        # nouveau Map obj
        self.maps[name] = Map(name, walls, group, tmx_data, portals, pnjs, texts,
                              interactive_obj, items, collide, fight_zone, level, monsters)

    def load_monsters(self):
        with open("loading/monsters.txt") as data:
            for line in data:
                line = line.rstrip('\n')
                exec(line)

    def check_pnj_collisions(self, dialog_box):
        for sprite in self.get_group().sprites():
            if type(sprite) == PNJ and sprite.feet.colliderect(self.player.rect):
                dialog_box.execute(sprite.refact_name, False, sprite.dialog)
                if self.get_map().pnjs[0].name == "andreas" and self.inventory.contains("robe"): #quete de la robe
                    self.get_map().pnjs[0].mode = "1"
                    self.get_map().pnjs[0].change_sprite(self.get_map().texts)
                    for i in self.inventory.items:
                        if i.name == "robe":
                            self.inventory.remove_item(i)
                if self.get_map().pnjs[0].name == "achille":
                    return 1
            if type(sprite) == Item and sprite.can_be_carried:
                dialog_box.execute(sprite.name, True, sprite.dialog)
                sprite.should_appear = False
                sprite.is_carried = True
                self.inventory.add_item(sprite)
                self.get_group().remove(sprite)
        return 0

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

        if self.player.feet.collidelist(self.get_map().fight_zone) > -1 and pygame.time.get_ticks() - self.clock > 2000:
            rand = rd.randint(1, 10)
            if rand > 8:
                self.clock = pygame.time.get_ticks()
                self.launch_fight()

    def launch_fight(self):
        rand = rd.randint(0, len(self.get_map().monsters) - 1)
        m = self.get_map().monsters[rand]
        monster = self.monsters[m]
        monster.level = self.get_map().level
        monster.real_stats()
        self.player.fight_stats = deepcopy(self.player.stats)
        self.fight = Fight(self.player, monster)
        self.player.fight_event()

    def tp_player(self, name="player", from_save=False):
        if not from_save:
            point = self.get_object(name)
            self.player.position[0] = point.x
            self.player.position[1] = point.y
        self.player.save_location()

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

    def draw(self):
        self.get_group().draw(self.screen)
        self.get_group().center(self.player.rect.center)

    def update(self):
        self.get_group().update()
        self.check_collisions()

        for pnj in self.get_map().pnjs:
            if pnj.random_move:
                pnj.random_moving(self.get_walls(), self.get_map().collide)
            else:
                pnj.move()
