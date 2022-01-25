from dataclasses import dataclass


@dataclass
class Stats:
    hp: int
    ad: int
    ap: int
    armor: int
    rm: int
    chance: int


class Monster(Stats):

    def __init__(self, name):
        self.name = name
        self.stats = None

    def set_stats(self, hp, ad, ap, armor, rm, chance):
        self.stats = Stats(hp, ad, ap, armor, rm, chance)