from interacts import *
from monster import *


class System:
    def __init__(self, game):
        self.game = game
        self.LEGEND = None
        self.CRUSADE = None
        #
        self.puzzle_state = False
        self.fought_state = False
        self.crusade_state = False
        #
        self.monster = Monster
        self.gate_check = Interacts.gate_prep_check(game)
        self.end_pos = (0, 100)

    def puzzle(self):
        if self.gate_check:
            if self.monster.return_type == 'boss':
                self.game.interface.aureole()
                if self.puzzle_state:
                    self.monster.health = 101
                    if self.monster.health == 60:
                        self.fought()

    def fought(self):
        if self.monster.return_type == 'boss':
            null = 0
            ui = 0
            play_prox_raise = 0
            self.fought_state = True  # in gate check
            self.end_crusade()

    def end_crusade(self):
        if self.game.player.map_pos == self.end_pos:
            ui = 0
            terminate = 0
            self.configure()

    def configure(self):
        o = 0
