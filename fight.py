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


def paralyzed(target):
    if target.status == "paralyzed":
        if rd.randint(1, 10) > 7:
            return False
    return True


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

    def dmg_blocked(self, atk, resistance):
        return atk - atk * (sqrt(resistance) * 7) / 100
        # return 0

    def use_attack(self, attack, source, target):
        n = 0
        if rd.randint(1, target.stats.chance) > 8:
            if attack == "Quichon tactique":
                # n = int(np.floor(source.stats.ap / 3 * self.dmg_blocked(target.stats.rm)))
                n = int(np.floor(self.dmg_blocked(source.stats.ap / 3, target.stats.rm)))
                if n < 1:
                    n = 1
                target.stats.hp -= n
                source.stats.hp += (source.fight_stats.hp - source.stats.hp) / 4
            elif attack == "Lancer de gobelet":
                # n = int(np.floor(source.stats.ad / 3 - self.dmg_blocked(target.stats.armor)))
                n = int(np.floor(self.dmg_blocked(source.stats.ad / 2, target.stats.armor)))
                if n < 1:
                    n = 1
                target.stats.hp -= n
            elif attack == "Jus du Coq":
                # n = int(np.floor(source.stats.ap / 2 - self.dmg_blocked(target.stats.rm)))
                n = int(np.floor(self.dmg_blocked(source.stats.ap / 3, target.stats.rm)))
                if n < 1:
                    n = 1
                target.stats.hp -= n
                if target.status == "" and rd.randint(0, 10) > 6:
                    if target.status == "":
                        target.status = "poison"
            elif attack == "Eyes contact":
                if target.status == "" and rd.randint(1, 10) > 3:
                    target.status = "paralyzed"
                    target.stats.speed /= 2
            elif attack == "Affond de trop":
                if target.status == "" and rd.randint(1, 10) > 4:
                    target.status = "sleep"
                    target.sleep = rd.randint(1, 3)
            elif attack == "Bagarre en Carolo":
                # n = int(np.floor(source.stats.ad - self.dmg_blocked(target.stats.armor)))
                n = int(np.floor(self.dmg_blocked(source.stats.ad, target.stats.armor)))
                if n < 1:
                    n = 1
                target.stats.hp -= n
                source.stats.hp -= n / 3
            elif attack == "Glissade alcoolisee":
                # n = int(np.floor(source.stats.ad / 4 - self.dmg_blocked(target.stats.armor)))
                n = int(np.floor(self.dmg_blocked(source.stats.ad / 4, target.stats.armor)))
                if n < 1:
                    n = 1
                source.stats.hp -= n
                source.stats.ap *= 2
            elif attack == "Non habes":
                if rd.randint(1, 10) > 9:
                    target.stats.hp -= target.stats.hp
            elif attack == "Biere trop froide":
                # n = int(np.floor(source.stats.ap / 4 - self.dmg_blocked(target.stats.rm)))
                n = int(np.floor(self.dmg_blocked(source.stats.ap / 4, target.stats.rm)))
                if n < 1:
                    n = 1
                target.stats.hp -= n
                if target.status == "" and rd.randint(1, 10) > 3:
                    target.status = "freeze"
                    target.sleep = rd.randint(1, 3)
            elif attack == "Dynamogifle":
                # n = int(np.floor(source.stats.ad / 2 - self.dmg_blocked(target.stats.armor)))
                n = int(np.floor(self.dmg_blocked(source.stats.ad / 2, target.stats.armor)))
                if n < 1:
                    n = 1
                target.stats.hp -= n
                if target.status == "" and rd.randint(1, 10) > 5:
                    target.status = "burn"
                    target.stats.ad -= target.stats.ad/4
            elif attack == "Patate de forain":
                # n = int(np.floor(source.stats.ad - self.dmg_blocked(target.stats.armor)))
                n = int(np.floor(self.dmg_blocked(source.stats.ad, target.stats.armor)))
                if n < 1:
                    n = 1
                target.stats.hp -= n
            elif attack == "Coma ethylique":
                if target.status == "":
                    target.status = "sleep"
                    target.sleep = rd.randint(1, 3)
            elif attack == "OH DJADJA":
                # n = int(np.floor(source.stats.ap - self.dmg_blocked(target.stats.rm)))
                n = int(np.floor(self.dmg_blocked(source.stats.ap, target.stats.rm)))
                if n < 1:
                    n = 1
                target.stats.hp -= n
            elif attack == "Blanc de blanc":
                # n = int(np.floor(source.stats.ap / 4 - self.dmg_blocked(target.stats.rm)))
                n = int(np.floor(self.dmg_blocked(source.stats.ap / 4, target.stats.rm)))
                if n < 1:
                    n = 1
                target.stats.hp -= n
                if target.status == "" and rd.randint(0, 10) > 8:
                    if target.status == "":
                        target.status = "poison"
            elif attack == "Balayette":
                # n = int(np.floor((source.stats.hp / 5 + source.stats.ad / 5) - self.dmg_blocked(target.stats.armor)))
                n = int(np.floor(self.dmg_blocked(source.stats.hp / 5 + source.stats.ad / 5, target.stats.armor)))
                if n < 1:
                    n = 1
                target.stats.hp -= n
            elif attack == "Danse sur le podium":
                # n = int(np.floor((source.stats.ap + 5) - self.dmg_blocked(target.stats.rm)))
                n = int(np.floor(self.dmg_blocked(source.stats.ap + 5, target.stats.rm)))
                if n < 1:
                    n = 1
                target.stats.hp -= n
            elif attack == "Je t'aime <3":
                if source.stats.chance > 19:
                    source.stats.chance -= 10
                # n = int(np.floor((source.stats.ap / 2) - self.dmg_blocked(target.stats.rm)))
                n = int(np.floor(self.dmg_blocked(source.stats.ap / 2, target.stats.rm)))
                if n < 1:
                    n = 1
                target.stats.hp -= n
            elif attack == "Lance-caca":
                # n = int(np.floor(source.stats.ad - self.dmg_blocked(target.stats.armor)))
                n = int(np.floor(self.dmg_blocked(source.stats.ad + 15, target.stats.armor)))
                if n < 1:
                    n = 1
                target.stats.hp -= n
        if attack == "Chante faux":
            if target.stats.ad <= 10:
                target.stats.ad = 1
            else:
                target.stats.ad -= 10
            target.stats.rm -= 5
            if target.stats.rm <= 0:
                target.stats.rm = 1
            # n = int(np.floor((source.stats.ap / 5) - self.dmg_blocked(target.stats.rm)))
            n = int(np.floor(self.dmg_blocked(source.stats.ap / 5, target.stats.rm)))
            if n < 1:
                n = 1
            target.stats.hp -= n
        elif attack == "Sieste strategique":
            if source.status == "paralyzed":
                source.stats.speed *= 2
            source.status = "sleep"
            source.sleep = 3
            source.stats.hp = source.fight_stats.hp
        elif attack == "Pils chaude":
            source.stats.armor += 5
            source.stats.rm += 5
        elif attack == "Speciale temperee":
            source.stats.armor += 7
            source.stats.rm += 7
            source.stats.ap += 3
        elif attack == "Une bonne Trappiste":
            source.stats.armor += 10
            source.stats.rm += 10
            source.stats.ap += 3
            source.stats.ad += 3
        elif attack == "Billet de 10 par terre":
            if source.stats.chance > 14:
                source.stats.chance -= 5
        elif attack == "Sol trop humide":
            target.stats.speed -= 5
        elif attack == "Bibitive":
            source.stats.speed += 5
            if source.stats.chance > 11:
                source.stats.chance -= 2
        elif attack == "Estafette":
            source.stats.hp += 10
            source.stats.ad += 5
        #print(n)