from copy import deepcopy
from dataclasses import dataclass

import pygame.image
from numpy import floor
import random as rd


@dataclass
class Stats:
    hp: int
    ad: int
    ap: int
    armor: int
    rm: int
    chance: int
    speed: int


@dataclass
class StatsGrowth:
    hp_growth: int
    ad_growth: int
    ap_growth: int
    armor_growth: int
    rm_growth: int
    chance_growth: int
    speed_growth: int


def random_factor(growing):
    rand = rd.randint(5, 20)
    return floor(rand/10 * growing)


class Monster:

    def __init__(self, name, level, attacks, refact_name):
        self.name = name
        self.refact_name = refact_name
        self.stats = None
        self.stats_g = None
        self.fight_stats = None
        self.status = ""
        self.level = level
        self.level_range = self.monster_level_range(level)
        self.attacks = attacks
        self.image = pygame.image.load(f'./fight_sprites/{name}.png')
        self.image = pygame.transform.scale(self.image, (350, 350))
        self.spawn_sentence = ""
        self.loose_sentence = ""
        self.win_sentence = ""
        self.sleep = 0
        self.attack_chosen = ""

    def set_stats(self, hp, ad, ap, armor, rm, chance, speed):
        self.stats = Stats(hp, ad, ap, armor, rm, chance, speed)
        self.fight_stats = deepcopy(self.stats)

    def set_stats_g(self, hp, ad, ap, armor, rm, chance, speed):
        self.stats_g = StatsGrowth(hp, ad, ap, armor, rm, chance, speed)

    def real_stats(self):
        self.set_stats(self.stats.hp + random_factor(self.stats_g.hp_growth * (self.level-1)),
                       self.stats.ad + random_factor(self.stats_g.ad_growth * (self.level-1)),
                       self.stats.ap + random_factor(self.stats_g.ap_growth * (self.level-1)),
                       self.stats.armor + random_factor(self.stats_g.armor_growth * (self.level-1)),
                       self.stats.rm + random_factor(self.stats_g.rm_growth * (self.level-1)),
                       self.stats.chance - random_factor(self.stats_g.chance_growth * (self.level-1)),
                       self.stats.speed + random_factor(self.stats_g.speed_growth * (self.level-1)))

    def base_stats_(self):
        self.stats = deepcopy(self.fight_stats)
        self.status = ""

    def monster_level_range(self, level):
        if level == 1:
            return {1, 2}
        else:
            return {level, level + 1, level + 2}

    def choose_attack(self):
        rand = rd.randint(0, 3)
        self.attack_chosen = self.attacks[rand]
