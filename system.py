from proxes import *


class System:
    def __init__(self, game):
        self.game = game
        self.LEGEND = 1
        self.CRUSADE = 1
        #
        self.aureole_state = False
        self.retreat_state = False
        self.crusade_state = False
        #
        # self.monster = Monster
        self.THRESHOLD = 200
        self.END_POS = (23, 13)

    def end_crusade(self):
        # if self.game.player.map_pos == self.END_POS:
        ui = 0
        terminate = 0
        self.configure()  # crusade phase where?

    def configure(self):
        self.CRUSADE += 1

    def check_secrets(self):
        count = 0
        for item in Proxes.locks:
            lock = Proxes.locks[item]
            if lock[0]:
                count += 1
        sec_file = open('secrets.txt', 'a+')
        sec_file.write(str(count))
        sec_file.close()


# interacts > interface; sprite, mons > gate > system  (crusade state next)
# insert UIs
