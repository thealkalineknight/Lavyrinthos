import pygame as pg


class Sound:
    def __init__(self, game):
        self.game = game
        pg.mixer.init()
        self.ost_path = 'assets/sound/levelost'
        self.levelost_1 = pg.mixer.Sound(self.ost_path + '/ENTER_DUNGEON.mp3')
        self.levelost_2 = pg.mixer.Sound(self.ost_path + '/THE_HALLS_DARKEN.mp3')
        self.SOUND_BANK = {1: self.levelost_1, 2: self.levelost_2}

    def theme_song(self):
        curr_theme = self.SOUND_BANK[self.game.CRUSADE]
        if self.game.running:
            curr_theme.play(-1)
        else:
            curr_theme.stop()

