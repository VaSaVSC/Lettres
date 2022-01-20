import pygame


class Item(pygame.sprite.Sprite):

    def __init__(self, name, should_appear, rect):
        super().__init__()
        self.name = name
        self.refact_name = ""
        self.info = []
        self.dialog = ""
        self.should_appear = should_appear
        self.is_carried = False
        self.can_be_carried = False
        self.rect = rect
        self.position = [0, 0]
        self.tp_spawn()
        self.old_position = self.position.copy()
        self.feet = pygame.Rect(rect.x, rect.y, rect.width*0.5, 12)
        self.image = pygame.image.load("./items/item.png")
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


class Inventory(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.items = []
        self.all_items = dict()

    def add_item(self, item):
        b = False
        index = 0
        for i in self.items:
            if i.name == item.name:
                b = True
                index = item.index
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
