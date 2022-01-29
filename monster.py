from dataclasses import dataclass
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


class Monster(Stats, StatsGrowth):

    def __init__(self, name, level, attacks):
        self.name = name
        self.stats = None
        self.stats_g = None
        self.level = level
        self.level_range = self.monster_level_range(level)
        self.attacks = attacks

    def set_stats(self, hp, ad, ap, armor, rm, chance, speed):
        self.stats = Stats(hp, ad, ap, armor, rm, chance, speed)

    def set_stats_g(self, hp, ad, ap, armor, rm, chance, speed):
        self.stats_g = StatsGrowth(hp, ad, ap, armor, rm, chance, speed)

    def real_stats(self):
        self.set_stats(self.hp + random_factor(self.hp_growth * self.level),
                       self.ad + random_factor(self.ad_growth * self.level),
                       self.ap + random_factor(self.ap_growth * self.level),
                       self.armor + random_factor(self.armor_growth * self.level),
                       self.rm + random_factor(self.rm_growth * self.level),
                       self.chance + random_factor(self.chance_growth * self.level),
                       self.speed + random_factor(self.speed_growth * self.level))

    def monster_level_range(self, level):
        if level == 1:
            return {1, 2}
        else:
            return {level, level + 1, level + 2}