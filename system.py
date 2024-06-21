class System:
    def __init__(self, game):
        self.game = game
        #
        self.aureole_state = False
        self.retreat_state = False
        self.crusade_state = False
        #
        self.THRESHOLD = 200
        self.END_POS = (37, 23)
        self.aur_trigger = False
        self.aur_trigger2 = False
        self.SAVE_DMG = 0

    def end_crusade(self):
        if self.game.player.map_pos == self.END_POS:
            self.game.running = False
            self.aur_trigger = False
            self.aur_trigger2 = False
            self.aureole_state = False
            self.retreat_state = False
            self.crusade_state = False
            self.game.player.gate_fullopen = False

    def adv_level(self, crusade):
        if crusade == 2:
            self.game.player.x, self.game.player.y = 1.5, 13.5
            self.THRESHOLD = 100
            self.END_POS = (35, 1)
        if crusade == 3:
            self.game.player.x, self.game.player.y = 5, 6
            self.THRESHOLD = 0
            self.END_POS = (-10, -10)  # aka youre not finishing this game >:(

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
