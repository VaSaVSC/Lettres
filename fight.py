from math import sqrt
import pygame


class Fight:

    def __init__(self, player, monster):
        self.player = player
        self.monster = monster
        self.player_can_attack = None
        self.fight_index = 0

    def fight(self):
        if self.monster.speed <= self.player.stats.speed:
            self.player_can_attack = True
        else:
            self.player_can_attack = False

    def dmg_blocked(self, resistance):
        return (sqrt(resistance) * 7) / 100