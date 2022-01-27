class Fight:

    def __init__(self, player, monster):
        self.player = player
        self.monster = monster

    def fight(self):
        while self.player.hp != 0 or self.monster.hp != 0:
            print("mdr")
        self.player.base_stats()
