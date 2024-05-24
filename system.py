class System:
    def __init__(self, game):
        self.game = game
        #
        self.aureole_state = False
        self.retreat_state = False
        self.crusade_state = False
        #
        # self.monster = Monster
        self.THRESHOLD = 200
        self.END_POS = (37, 23)
        self.aur_trigger = False
        self.aur_trigger2 = False

    def end_crusade(self):
        if self.game.player.map_pos == self.END_POS:
            self.game.running = False
            self.aur_trigger = False
            self.aur_trigger2 = False
            self.game.player.x, self.game.player.y = 1.5, 3.5

    def check_secrets(self):
        count = 0
        total = 0
        for item in self.game.proxes.secrets:
            total += 1
            secret = self.game.proxes.secrets[item]
            if secret[0]:
                count += 1
        return count, total
        # sec_file = open('secrets.txt', 'a+')
        # sec_file.write(str(count))
        # sec_file.close()


# interacts > interface; sprite, mons > gate > system  (crusade state next)
# insert UIs
