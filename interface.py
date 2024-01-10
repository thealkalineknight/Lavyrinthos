from settings import *
import pygame as pg


class Interface:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.btn_w, self.btn_h = 300, 100
        self.MAIN_SCR = self.convert_tex('assets/interface/UIMAINSC.png', (WIDTH, HEIGHT))
        self.BTN_NEW = self.convert_tex('assets/interface/BTNNEW.png', (self.btn_w, self.btn_h))
        self.PRE_MODE = True
        self.MAIN_MODE = False
        self.key_count = 0
        self.time_prev = pg.time.get_ticks()
        self.key_trigger = False
        self.key_time = 150

    def update(self):
        if self.PRE_MODE:
            self.pre_mode()

    def draw(self):
        if self.PRE_MODE:
            self.draw_premode()

    def draw_premode(self):
        self.screen.blit(self.MAIN_SCR, (0, 0))
        self.screen.blit(self.BTN_NEW, (HWIDTH - self.btn_w / 2, 250))

    def pre_mode(self):

        key = pg.key.get_pressed()
        if self.key_count < 0 or self.key_count > 3:
            self.key_count = 0

        self.limit_key_time()
        if self.key_trigger:
            if key[pg.K_DOWN]:
                self.key_count += 1
            if key[pg.K_UP]:
                self.key_count -= 1

        if key[pg.K_RETURN]:
            if self.key_count == 2:
                self.PRE_MODE = False
                self.MAIN_MODE = True

    def limit_key_time(self):
        self.key_trigger = False
        time_now = pg.time.get_ticks()
        if time_now - self.time_prev > self.key_time:
            self.time_prev = time_now
            self.key_trigger = True

    @staticmethod
    def convert_tex(path, res=(MAX_TEX, MAX_TEX)):
        texture = pg.image.load(path).convert_alpha()
        return pg.transform.scale(texture, res)
