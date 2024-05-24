from settings import *
import pygame as pg


class ObjRend:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.wall_tex = self.init_wall_tex()
        self.bg_offset = 0
        self.sky_image = self.convert_tex('assets/background/SKY.PNG', (WIDTH, HHEIGHT))
        self.ground_image = self.convert_tex('assets/background/FSAND.PNG', (WIDTH, HHEIGHT))
        self.digit_prep = [self.convert_tex(f'assets/interface/nums/NUM{i}.PNG', (50, 50))
                           for i in range(10)]
        self.DIGIT_IMGS = dict(zip(map(str, range(10)), self.digit_prep))
        self.PERCENT_IMG = self.convert_tex('assets/interface/nums/NUMPER.PNG', (50, 50))
        self.r2112 = 12

    def draw(self):
        self.draw_bg()
        self.render_objs()

    def draw_bg(self):
        # print(self.bg_offset + 4.5 * self.game.player.rel, (self.bg_offset + 4.5 * self.game.player.rel) % WIDTH)
        self.bg_offset = (self.bg_offset + 4.5 * self.game.player.rel) % WIDTH  # del rel for moving sky

        self.screen.blit(self.sky_image, (-self.bg_offset, 0))  # neg sign must go here or blinking
        self.screen.blit(self.sky_image, (-self.bg_offset + WIDTH, 0))

        self.screen.blit(self.ground_image, (-self.bg_offset, HHEIGHT))
        self.screen.blit(self.ground_image, (-self.bg_offset + WIDTH, HHEIGHT))

    def render_objs(self):
        # obj_list = self.game.raycasting.obj_rend_list  # for testing without touch-up
        obj_list = sorted(self.game.raycasting.obj_rend_list, key=lambda t: t[0], reverse=True)
        for depth, image, pos in obj_list:
            self.screen.blit(image, pos)

    def draw_nums(self, item, x, y, percent):
        num = str(item)
        offset = 0
        for i, char in enumerate(num):
            self.screen.blit(self.DIGIT_IMGS[char], ((i * 40) + x, y))
            offset = i + 1
        if percent:
            self.screen.blit(self.PERCENT_IMG, ((offset * 40) + x, y))

    def init_wall_tex(self):
        return {  # don't use 0, creates empty space
            1: self.convert_tex('assets/walls/WLIME.PNG'),
            2: self.convert_tex('assets/walls/WLIMEK1.PNG'),
            3: self.convert_tex('assets/walls/WLIMEK2.PNG'),
            4: self.convert_tex('assets/walls/ENTRY.PNG'),
            5: self.convert_tex('assets/walls/b.jpg'),  # props
            6: self.convert_tex('assets/walls/WLIMELOC.PNG'),  # secret
            7: self.convert_tex('assets/walls/NOTEX.PNG'),  # gates
            # 8: self.convert_tex('assets/walls/NOTEX.PNG'),  # sprite  # dont need these anymore
            9: self.convert_tex('assets/walls/WLIMEOPN.PNG'),  # secret open  # but save notex for something else
            10: self.convert_tex('assets/walls/animwalls/LITLIME1.PNG'),
            11: self.convert_tex('assets/walls/animwalls/LITLIME2.PNG'),
            12: self.convert_tex('assets/walls/animwalls/LITLIME3.PNG'),
            13: self.convert_tex('assets/walls/animwalls/LITLIME4.PNG'),
            20: self.convert_tex('assets/walls/SHLIME0.PNG'),
            21: self.convert_tex('assets/walls/SHLIME1.PNG'),
            22: self.convert_tex('assets/walls/SHLIME2.PNG'),
            23: self.convert_tex('assets/walls/SHLIME3.PNG'),
            24: self.convert_tex('assets/walls/SHLIME4.PNG'),
            25: self.convert_tex('assets/walls/SHLIME5.PNG'),
            26: self.convert_tex('assets/walls/SHLIME6.PNG'),
            27: self.convert_tex('assets/walls/transwalls/BRLIME1.PNG'),
            28: self.convert_tex('assets/walls/transwalls/BRLIME2.PNG'),
            29: self.convert_tex('assets/walls/transwalls/WINLIME.PNG'),
            30: self.convert_tex('assets/walls/VLIMEB1.PNG'),
            31: self.convert_tex('assets/walls/VLIMEB2.PNG'),
            32: self.convert_tex('assets/walls/VLIMEB3.PNG'),
            33: self.convert_tex('assets/walls/VLIMEB4.PNG'),
            34: self.convert_tex('assets/walls/VLIMEB5.PNG'),
            35: self.convert_tex('assets/walls/VLIMEG1.PNG'),
            36: self.convert_tex('assets/walls/VLIMEG2.PNG'),
            37: self.convert_tex('assets/walls/VLIMEG3.PNG'),
            38: self.convert_tex('assets/walls/VLIMEG4.PNG'),
            39: self.convert_tex('assets/walls/VLIMEG5.PNG'),
            40: self.convert_tex('assets/walls/VLIMEG6.PNG')
        }

    @staticmethod
    def convert_tex(path, res=(MAX_TEX, MAX_TEX)):
        texture = pg.image.load(path).convert_alpha()
        return pg.transform.scale(texture, res)
