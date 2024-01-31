from monster import *


class System:
    def __init__(self, game):
        self.game = game
        self.LEGEND = None
        self.CRUSADE = None
        #
        self.aureole_state = False
        self.retreat_state = False
        self.crusade_state = False
        #
        # self.monster = Monster
        self.THRESHOLD = 200
        self.END_POS = (0, 100)

    def end_crusade(self):
        if self.game.player.map_pos == self.END_POS:
            ui = 0
            terminate = 0
            self.configure()  # crusade phase where?

    def configure(self):
        o = 0

# interacts > interface; sprite, mons > gate > system  (crusade state next)
# insert UIs
