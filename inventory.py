import pygame
import random as rd


class Item(pygame.sprite.Sprite):

    def __init__(self, name, should_appear, rect, type):
        super().__init__()
        self.type = type
        self.name = name
        self.refact_name = ""
        self.info = []
        self.dialog = ""
        self.should_appear = should_appear
        self.is_carried = False
        self.can_be_carried = False
        self.fight_item = False
        if self.type == "item3":
            self.fight_item = True
        self.rect = rect
        self.position = [0, 0]
        self.tp_spawn()
        self.old_position = self.position.copy()
        self.feet = pygame.Rect(rect.x, rect.y, rect.width*0.5, 12)
        if self.type == "item1" or self.type == "item2" or self.type == "item3":
            self.image = pygame.image.load("./items/item.png")
        elif self.type == "coffre":
            self.image = pygame.image.load("./items/coffre.png")
        self.image = pygame.transform.scale(self.image, (32, 32))
        self.image.set_colorkey([0, 0, 0])
        self.number = 0
        self.index = 0

    def tp_spawn(self):
        location = self.rect
        self.position[0] = location.x
        self.position[1] = location.y

    def move_back(self):
        self.position = self.old_position
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom


def use_item(item, player):
    if item.name == "old_carapils":
        if rd.randint(0, 100) > 95:
            player.life -= player.life
        elif rd.randint(0, 100) < 20:
            player.life = player.max_life
        elif rd.randint(0, 10) <= 2:
            player.life -= 1
        else:
            if player.life < player.max_life:
                player.life += 1
        return 1
    if item.name == "robe":
        return 0
    if item.name == "pizza":
        return 1
    if item.name == "null":
        return 1
    if item.name == "sachet":
        player.gold += rd.randint(0, 10)
        return 1
    if item.name == "trésor":
        player.gold += rd.randint(15, 40)
        return 1


class Inventory(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.items = []
        self.all_items = dict()

    def add_item(self, item):
        b = False
        index = 0
        acc = 0
        for i in self.items:
            if i.name == item.name:
                b = True
                index = acc
            acc += 1
        if b:
            self.items[index].number += 1
        else:
            item.number += 1
            item.refact_name = self.all_items[item.name+"_refact"]
            item.info = self.all_items[item.name]
            item.index = len(self.items)
            self.items.append(item)

    def remove_item(self, item):
        item.number -= 1
        if item.number == 0:
            self.items.remove(item)

    def contains(self, name):
        for i in self.items:
            if i.name == name:
                return True
        return False