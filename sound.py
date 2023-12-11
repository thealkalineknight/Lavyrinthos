import pygame as pg


class Sound:
    def __init__(self, game):
        self.game = game
        pg.mixer.init()
        self.ost_path = 'assets/sound/levelost'
        self.levelost_1 = pg.mixer.Sound(self.ost_path + '/ENTER_DUNGEON.mp3')

    def theme_song(self):
        self.levelost_1.play(-1)
