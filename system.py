from monster import *


class System:
    def __init__(self, game):
        self.game = game
        self.LEGEND = None
        self.CRUSADE = None
        #
        self.aureole_state = False
        self.fought_state = False
        self.crusade_state = False
        #
        # self.monster = Monster
        self.end_pos = (0, 100)

    def puzzle(self):
        self.game.interface.aureole()
        #
        if self.aureole_state:
            o = 0
            # mons ; weaken() : if sys; threshold state: mons ; lock up, recede, sys; fought st

    def end_crusade(self):
        if self.game.player.map_pos == self.end_pos:
            ui = 0
            terminate = 0
            self.configure()  # crusade phase where?

    def configure(self):
        o = 0
