from math import sqrt
import numpy as np
import random as rd


def poisoned(target):
    if target.status == "poison":
        n = target.fight_stats.hp / 10
        if n < 1:
            n = 1
        target.stats.hp -= n
        return True
    return False


def burned(target):
    if target.status == "burn":
        n = target.fight_stats.hp / 15
        if n < 1:
            n = 1
        target.stats.hp -= n
        return True
    return False


class Fight:

    def __init__(self, player, monster):
        self.player = player
        self.monster = monster
        self.player_can_attack = None
        self.fight_index = 0

    def fight(self):
        if self.monster.stats.speed <= self.player.stats.speed:
            self.player_can_attack = True
        else:
            self.player_can_attack = False

    def dmg_blocked(self, resistance):
        return (sqrt(resistance) * 7) / 100

    def use_attack(self, attack, source, target):
        if attack == "Quichon tactique":
            n = int(np.floor(source.stats.ap / 3 * self.dmg_blocked(target.stats.rm)))
            if n < 1:
                n = 1
            target.stats.hp -= n
            source.stats.hp += (source.fight_stats.hp - source.stats.hp) / 4
        elif attack == "Sieste startégique":
            source.status = None
            source.stats.hp = source.fight_stats.hp
        elif attack == "Lancer de gobelet":
            n = int(np.floor(source.stats.ad / 3 * self.dmg_blocked(target.stats.armor)))
            if n < 1:
                n = 1
            target.stats.hp -= n
        elif attack == "Jus du Coq":
            n = int(np.floor(source.stats.ap / 2 * self.dmg_blocked(target.stats.rm)))
            if n < 1:
                n = 1
            target.stats.hp -= n
            rand = rd.randint(0, 10)
            if rand > 6:
                target.status = "poison"