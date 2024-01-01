import pygame as pg
from settings import *
import math
import os
from collections import deque


class SpriteMain:
    def __init__(self, game, path=None,
                 pos=(0, 0), wscale=0.7, hscale=0.7, shift=0.27):
        self.game = game
        self.player = game.player
        self.x, self.y = pos
        self.SPRITE_WSCALE = wscale
        self.SPRITE_HSCALE = hscale
        self.SPRITE_HSHIFT = shift
        self.dx, self.dy, self.theta, self.screen_x, self.dist, self.norm_dist = 0, 0, 0, 0, 1, 1
        self.image = pg.image.load(path).convert_alpha()
        self.IMG_WID = self.image.get_width()
        self.IMG_HWID = self.image.get_width() // 2
        self.IMG_RATIO = self.IMG_WID / self.image.get_height()
        self.sprite_hwid = 0
        self.sprite_ang = 0
        self.screen_pos = 0
        self.DLIM = False

    def update(self):
        self.get_sprite()

    def get_sprite(self):
        dx = self.x - self.player.x
        dy = self.y - self.player.y
        vis_span = max(self.game.raycasting.vis_spans)
        self.DLIM = False

        dlim = max(abs(dx), abs(dy))

        if dlim <= vis_span:
            self.DLIM = True
            self.dx, self.dy = dx, dy
            self.theta = math.atan2(dy, dx)

            self.sprite_ang = math.degrees(self.theta)

            delta = self.theta - self.player.angle
            if (dx > 0 and self.player.angle > math.pi) or (dx < 0 and dy < 0):
                delta += math.tau

            delta_rays = delta / DELTA_ANGLE
            self.screen_x = (HNUM_RAYS + delta_rays) * SCALE  # initial xpos

            self.dist = math.hypot(dx, dy)
            self.norm_dist = self.dist * math.cos(delta)
            if -self.IMG_HWID < self.screen_x < (WIDTH + self.IMG_HWID):
                if 0.5 < self.norm_dist:
                    self.get_sprite_projection()

    def get_sprite_projection(self):
        proj = SCREEN_DIST / self.norm_dist
        proj_width, proj_height = proj * self.IMG_RATIO * self.SPRITE_WSCALE, proj * self.SPRITE_HSCALE

        image = pg.transform.scale(self.image, (proj_width, proj_height))

        self.sprite_hwid = proj_width // 2
        height_shift = proj_height * self.SPRITE_HSHIFT
        self.screen_pos = self.screen_x - self.sprite_hwid, HHEIGHT - proj_height // 2 + height_shift
        self.game.raycasting.obj_rend_list.append((self.norm_dist, image, self.screen_pos))


class AnimSprite(SpriteMain):
    def __init__(self, game, path=None,
                 pos=(0, 0), wscale=0.8, hscale=0.8, shift=0.15, anim_time=120):
        super().__init__(game, path, pos, wscale, hscale, shift)
        self.anim_time = anim_time
        self.path = path.rsplit('/', 1)[0]
        self.images = self.get_images(self.path)
        self.anim_time_prev = pg.time.get_ticks()
        self.anim_trigger = False

    def update(self):
        super().update()
        self.check_anim_time()
        self.animate(self.images)

    def animate(self, images):
        if self.anim_trigger:
            images.rotate(-1)
            self.image = images[0]

    def check_anim_time(self):
        self.anim_trigger = False
        anim_time_now = pg.time.get_ticks()
        if anim_time_now - self.anim_time_prev > self.anim_time:
            self.anim_time_prev = anim_time_now
            self.anim_trigger = True

    def get_images(self, path):
        images = deque()
        for file_name in os.listdir(path):
            if os.path.isfile(os.path.join(path, file_name)):
                img = pg.image.load(path + '/' + file_name).convert_alpha()
                images.append(img)
        return images
