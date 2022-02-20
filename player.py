import pygame
import random as rd
from copy import deepcopy

from animation import AnimateSprite
from monster import Stats


class Entity(AnimateSprite):

    def __init__(self, name, x, y, life):
        super().__init__(name)
        self.image = self.get_image(0, 0)
        self.image.set_colorkey([0, 0, 0])
        self.rect = self.image.get_rect()
        self.position = [x, y]
        self.feet = pygame.Rect(0, 0, self.rect.width * 0.5, 12)
        self.old_position = self.position.copy()
        self.life = life
        self.max_life = life

    def save_location(self):
        self.old_position = self.position.copy()

    def get_location(self):
        return self.position

    def move_right(self):
        if self.speed > 0:
            self.change_animation('right')
        self.position[0] += self.speed

    def move_left(self):
        if self.speed > 0:
            self.change_animation('left')
        self.position[0] -= self.speed

    def move_up(self):
        if self.speed > 0:
            self.change_animation('up')
        self.position[1] -= self.speed

    def move_down(self):
        if self.speed > 0:
            self.change_animation('down')
        self.position[1] += self.speed

    def update(self):
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom

    def move_back(self):
        self.position = self.old_position
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom


class Player(Entity):

    def __init__(self, event):
        super().__init__("gob", 0, 0, 5)
        self.name = "gob"
        self.event = event
        self.stats = Stats(10, 5, 0, 3, 2, 99, 6)
        self.fight_stats = Stats(10, 5, 0, 3, 2, 99, 6)
        self.base_stats = Stats(10, 5, 0, 3, 2, 99, 6)
        self.attacks = ["Quichon tactique", "Sieste stratégique", "Lancer de gobelet", "Jus du Coq"]
        self.xp = 0
        self.level = 1
        self.xp_needed_to_level_up = 100
        self.status = ""
        self.fight_image = pygame.image.load("./fight_sprites/gob.png")
        self.fight_image = pygame.transform.scale(self.fight_image, (350, 350))
        self.gold = 50
        self.mono = False
        self.sleep = 0
        self.parch = 0

    def set_stats(self):
        self.stats.hp += 50
        self.stats.ad += 15
        self.stats.ap += 15
        self.stats.armor += 12
        self.stats.rm += 12
        self.stats.chance -= 10
        if self.stats.chance < 2:
            self.stats.chance = 2
        self.stats.speed += 10

    def fight_event(self):
        pygame.event.post(self.event)

    def base_stats_(self):
        self.stats = deepcopy(self.fight_stats)
        self.status = ""

    def xp_needed(self):
        self.xp_needed_to_level_up += 50

    def mono_switch(self):
        self.sprite_sheet = pygame.image.load(f"./sprites/{self.name}{self.mode}.png")
        self.images = {
            'down': self.get_images(0),
            'left': self.get_images(32),
            'right': self.get_images(64),
            'up': self.get_images(96)
        }

    def change_sprite(self):
        self.sprite_sheet = pygame.image.load(f"./sprites/{self.name}{self.mode}.png")
        self.images = {
            'down': self.get_images(0),
            'left': self.get_images(32),
            'right': self.get_images(64),
            'up': self.get_images(96)
        }
        #self.dialog = texts[self.name + self.mode]


def refactor(name):
    if name == "d":
        return "Dèdèle"
    name = name[0].upper() + name[1:]
    return name


class PNJ(Entity):

    def __init__(self, name, nb_points, speed, random_move=False):
        super().__init__(name, 0, 0, 1)
        self.nb_points = nb_points
        self.name = name
        self.refact_name = refactor(name)
        self.dialog = ""
        self.speed = speed
        self.base_speed = speed
        self.points = []
        self.current_point = 0
        self.mode = "0"
        self.random_move = random_move

    def move(self):
        current_point = self.current_point
        target_point = self.current_point + 1

        if target_point >= self.nb_points:
            target_point = 0

        current_rect = self.points[current_point]
        target_rect = self.points[target_point]

        if current_rect.y < target_rect.y and abs(current_rect.x - target_rect.x) < 3:
            self.move_down()

        elif current_rect.y > target_rect.y and abs(current_rect.x - target_rect.x) < 3:
            self.move_up()

        elif current_rect.x > target_rect.x and abs(current_rect.y - target_rect.y) < 3:
            self.move_left()

        elif current_rect.x < target_rect.x and abs(current_rect.y - target_rect.y) < 3:
            self.move_right()

        if self.rect.colliderect(target_rect):
            self.current_point = target_point

    def random_moving(self, walls, collide):
        rand1 = rd.randint(1, 100)
        if rand1 > 98:
            rand2 = rd.randint(1, 4)
            rand3 = rd.randint(1, 5)
            if rand2 == 1:
                for i in range(rand3):
                    if self.pnj_collide(walls, collide, "up"):
                        self.move_up()
            elif rand2 == 2:
                for i in range(rand3):
                    if self.pnj_collide(walls, collide, "down"):
                        self.move_down()
            elif rand2 == 3:
                for i in range(rand3):
                    if self.pnj_collide(walls, collide, "right"):
                        self.move_right()
            elif rand2 == 4:
                for i in range(rand3):
                    if self.pnj_collide(walls, collide, "left"):
                        self.move_left()
            else:
                self.move_back()

    def pnj_collide(self, walls, collide, direction):
        if direction == "up":
            feet = pygame.Rect(self.position[0], self.position[1] - self.speed, self.rect.width * 0.5, 12)
        elif direction == "down":
            feet = pygame.Rect(self.position[0], self.position[1] + self.speed, self.rect.width * 0.5, 12)
        elif direction == "right":
            feet = pygame.Rect(self.position[0] + self.speed, self.position[1], self.rect.width * 0.5, 12)
        else:
            feet = pygame.Rect(self.position[0] - self.speed, self.position[1], self.rect.width * 0.5, 12)
        if feet.collidelist(walls) > -1 or feet.collidelist(collide) > -1:
            self.move_back()
            return False
        return True

    def tp_spawn(self):
        location = self.points[self.current_point]
        self.position[0] = location.x
        self.position[1] = location.y
        self.save_location()

    def load_points(self, tmx_data):
        for num in range(1, self.nb_points + 1):
            point = tmx_data.get_object_by_name(f"{self.name}_path{num}")
            rect = pygame.Rect(point.x, point.y, point.width, point.height)
            self.points.append(rect)

    def change_sprite(self, texts):
        self.sprite_sheet = pygame.image.load(f"./sprites/{self.name}{self.mode}.png")
        self.images = {
            'down': self.get_images(0),
            'left': self.get_images(32),
            'right': self.get_images(64),
            'up': self.get_images(96)
        }
        self.dialog = texts[self.name + self.mode]
