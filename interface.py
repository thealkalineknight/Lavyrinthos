from settings import *
import pygame as pg


class Interface:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.btn_w, self.btn_h = 300, 100
        self.btn_hw, self.btn_hh = self.btn_w // 1.5, self.btn_h // 1.5
        self.curs_w, self.curs_h = 130, 50
        self.path = 'assets/interface/'
        self.MAIN_SCR = self.convert_tex(self.path + 'UIMAINSC.png', (WIDTH, HEIGHT))
        self.CURSOR = self.convert_tex(self.path + 'CURSOR.png', (self.curs_w, self.curs_h))
        self.BTN_NEW = self.convert_tex(self.path + 'BTNNEW.png', (self.btn_w, self.btn_h))
        self.BTN_LOAD = self.convert_tex(self.path + 'BTNLOAD.png', (self.btn_w, self.btn_h))
        self.BTN_SETT = self.convert_tex(self.path + 'BTNSETT.png', (self.btn_w, self.btn_h))
        self.BTN_READ = self.convert_tex(self.path + 'BTNREAD.png', (self.btn_w, self.btn_h))
        self.MASK_BTN = self.convert_tex(self.path + 'BTNSELEC.png', (self.btn_w, self.btn_h))
        self.SETT_SCR = self.convert_tex(self.path + 'UISETTIN.png', (WIDTH, HEIGHT))
        self.TEST_ME = self.convert_tex(self.path + 'TESTME.png', (400, 500))
        self.AUREOLE = self.convert_tex(self.path + 'TESTORB.png', (100, 100))
        self.INTER_SCR = self.convert_tex(self.path + 'UIFINLV1.png', (WIDTH, HEIGHT))
        self.FIN_BTN = self.convert_tex(self.path + 'FINBTN.png', (self.btn_w, self.btn_h))
        self.FIN_CRUSD = self.convert_tex(self.path + 'FINCRUSD.png', (750, 150))
        self.FIN_SCRT = self.convert_tex(self.path + 'FINSECRT.png', (self.btn_hw, self.btn_hh))
        self.PRE_MODE = True
        self.SETT_MODE = False
        self.MAIN_MODE = False
        self.INTER_MODE = False
        self.key_count = 0
        self.time_prev = pg.time.get_ticks()
        self.key_trigger = False
        self.key_time = 130
        self.mask = False
        self.BTN_X = HWIDTH - self.btn_w / 2
        self.BTN_BANK = {0: 250, 1: 350, 2: 450, 3: 530}
        self.INTER_BANK = {0: [self.BTN_X, HEIGHT - HHEIGHT // 3]}
        self.first_boot = True
        self.aur_pos = 0

    def update(self):
        if self.SETT_MODE:
            self.sett_mode()
        elif self.PRE_MODE:
            self.pre_mode()
        elif self.INTER_MODE:
            self.inter_mode()

    def draw(self):
        if self.SETT_MODE:
            self.draw_settmode()
        elif self.PRE_MODE:
            self.draw_premode()
        elif self.INTER_MODE:
            self.draw_intermode()

    def pre_mode(self):
        key = pg.key.get_pressed()

        self.limit_key_time()
        if self.key_trigger:

            if key[pg.K_DOWN] or key[pg.K_UP]:
                self.mask = True

            if key[pg.K_DOWN]:
                self.key_count += 1
            if key[pg.K_UP]:
                self.key_count -= 1

            if key[pg.K_RETURN]:
                if self.key_count == 0:
                    if not self.first_boot:
                        self.PRE_MODE = False
                        self.MAIN_MODE = True
                        #
                        self.key_count = 0
                        self.mask = False
                        self.first_boot = True
                    else:
                        self.mask = True
                if self.key_count == 1:
                    o = 0
                if self.key_count == 2:
                    self.SETT_MODE = True
                    self.reset_select()

    def draw_premode(self):
        if self.key_count < 0 or self.key_count > 3:
            self.key_count = 0

        self.screen.blit(self.MAIN_SCR, (0, 0))
        self.screen.blit(self.BTN_NEW, (self.BTN_X, self.BTN_BANK[0]))
        self.screen.blit(self.BTN_LOAD, (self.BTN_X, self.BTN_BANK[1]))
        self.screen.blit(self.BTN_SETT, (self.BTN_X, self.BTN_BANK[2]))
        self.screen.blit(self.BTN_READ, (self.BTN_X, self.BTN_BANK[3]))
        if self.mask:
            if self.first_boot:
                self.key_count = 0
                self.first_boot = False
            self.screen.blit(self.MASK_BTN, (self.BTN_X, self.BTN_BANK[self.key_count]))
            self.screen.blit(self.CURSOR, (self.BTN_X - self.curs_w, self.BTN_BANK[self.key_count] + self.curs_h // 2))

    def sett_mode(self):
        key = pg.key.get_pressed()

        self.limit_key_time()
        if self.key_trigger:
            if key[pg.K_DOWN] or key[pg.K_UP]:
                self.mask = True

            if key[pg.K_DOWN]:
                self.key_count += 1
            if key[pg.K_UP]:
                self.key_count -= 1

            if key[pg.K_RETURN]:
                self.mask = True
                if self.key_count == 0:
                    o = 1
                if self.key_count == 2:
                    p = 9

    def draw_settmode(self):
        if self.key_count < 0 or self.key_count > 3:
            self.key_count = 0

        self.screen.blit(self.SETT_SCR, (0, 0))
        self.screen.blit(self.TEST_ME, (450, 150))

        if self.mask:
            if self.first_boot:
                self.key_count = 0
                self.first_boot = False
            self.screen.blit(self.MASK_BTN, (self.BTN_X, self.BTN_BANK[self.key_count]))
            self.screen.blit(self.CURSOR, (self.BTN_X - self.curs_w, self.BTN_BANK[self.key_count] + self.curs_h // 2))

    def inter_mode(self):
        key = pg.key.get_pressed()

        self.limit_key_time()
        if self.key_trigger:

            if key[pg.K_DOWN] or key[pg.K_UP]:
                self.mask = True

            if key[pg.K_DOWN]:
                self.key_count += 1
            if key[pg.K_UP]:
                self.key_count -= 1

            if key[pg.K_RETURN]:
                if self.key_count == 0:
                    if not self.first_boot:
                        self.INTER_MODE = False
                        self.MAIN_MODE = True
                    else:
                        self.mask = True

    def draw_intermode(self):
        if self.key_count < 0 or self.key_count > 0:
            self.key_count = 0

        self.screen.blit(self.INTER_SCR, (0, 0))
        self.screen.blit(self.FIN_CRUSD, (HWIDTH // 2, HHEIGHT // 4))
        self.screen.blit(self.FIN_SCRT, (HWIDTH // 2, HHEIGHT - HHEIGHT // 4))
        self.game.obj_rend.draw_nums(self.percent_secrets(),
                                     (HWIDTH // 2) + self.btn_hw + 10, HHEIGHT - HHEIGHT // 4 + 10, True)
        self.screen.blit(self.FIN_BTN, (self.INTER_BANK[0][0], self.INTER_BANK[0][1]))
        if self.mask:
            if self.first_boot:
                self.key_count = 0
                self.first_boot = False
            self.screen.blit(self.MASK_BTN, (self.INTER_BANK[self.key_count][0], self.INTER_BANK[self.key_count][1]))

    def percent_secrets(self):
        box = self.game.system.check_secrets()
        return int(box[0] / box[1] * 100)

    def reset_select(self):
        self.mask = False
        self.key_count = 0

    def limit_key_time(self):
        self.key_trigger = False
        time_now = pg.time.get_ticks()
        if time_now - self.time_prev > self.key_time:
            self.time_prev = time_now
            self.key_trigger = True

    def aureole(self):  # change to sprite later
        if self.aur_pos == HHEIGHT:
            self.game.system.aureole_state = True
        else:
            self.aur_pos += 1
        self.screen.blit(self.AUREOLE, (self.BTN_X, self.aur_pos))

    @staticmethod
    def convert_tex(path, res=(MAX_TEX, MAX_TEX)):
        texture = pg.image.load(path).convert_alpha()
        return pg.transform.scale(texture, res)
