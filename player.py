import pygame

from animation import AnimateSprite
from monster import Stats


class Entity(AnimateSprite):

    def __init__(self, name, x, y, life):
        super().__init__(name)
        self.image = self.get_image(0, 0)
        self.image.set_colorkey([0, 0, 0])
        self.rect = self.image.get_rect()
        self.position = [x, y]
        self.feet = pygame.Rect(0, 0, self.rect.width*0.5, 12)
        self.old_position = self.position.copy()
        self.life = life
        self.max_life = life

    def save_location(self): self.old_position = self.position.copy()

    def get_location(self):
        return self.position

    def move_right(self):
        self.change_animation('right')
        self.position[0] += self.speed

    def move_left(self):
        self.change_animation('left')
        self.position[0] -= self.speed

    def move_up(self):
        self.change_animation('up')
        self.position[1] -= self.speed

    def move_down(self):
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
        super().__init__("player", 0, 0, 5)
        self.name = "player"
        self.event = event
        self.stats = Stats(10, 5, 0, 3, 2, 99)
        self.fight_stats = self.stats
        self.attacks = []
        self.xp = 0
        self.level = 1
        self.xp_needed_to_level_up = 10

    def set_stats(self, hp, ad, ap, armor, rm, chance, speed):
        self.stats.hp += hp
        self.stats.ad += ad
        self.stats.ap += ap
        self.stats.armor += armor
        self.stats.rm += rm
        self.stats.chance -= chance
        if self.stats.chance < 2:
            self.stats.chance = 2
        self.stats.speed += speed

    def fight_event(self):
        pygame.event.post(self.event)

    def base_stats(self):
        self.fight_stats = self.stats

    def xp_needed(self):
        self.xp_needed_to_level_up += 2 * self.level


def refactor(name):
    name = name[0].upper() + name[1:]
    return name


class PNJ(Entity):

    def __init__(self, name, nb_points, speed):
        super().__init__(name, 0, 0, 1)
        self.nb_points = nb_points
        self.name = name
        self.refact_name = refactor(name)
        self.dialog = ""
        self.speed = speed
        self.base_speed = speed
        self.points = []
        self.current_point = 0
        self.mode = 0

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

    def tp_spawn(self):
        location = self.points[self.current_point]
        self.position[0] = location.x
        self.position[1] = location.y
        self.save_location()

    def load_points(self, tmx_data):
        for num in range(1, self.nb_points+1):
            point = tmx_data.get_object_by_name(f"{self.name}_path{num}")
            rect = pygame.Rect(point.x, point.y, point.width, point.height)
            self.points.append(rect)
