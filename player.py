from settings import *
import pygame as pg
import math
from proxes import *


class Player:
    def __init__(self, game):
        self.game = game
        self.x, self.y = PLYR_POS
        self.angle = PLYR_ANGLE
        self.rel = 0
        self.secret_open = False
        self.gate_fullopen = False
        self.prev_time = pg.time.get_ticks()
        #
        self.health = 100

    def update(self):
        self.small_events()
        self.mouse_control()
        self.movement()

    def small_events(self):
        self.interact_event()
        self.timed_event()

    def interact_event(self):
        key = pg.key.get_pressed()
        if key[pg.K_e]:
            for adj in self.get_adjs():
                if adj in Proxes.locks:
                    lock = Proxes.locks[adj]
                    lock[0] = True

    def timed_event(self):
        if self.map_pos not in self.game.map.secret_map:
            curr_time = pg.time.get_ticks()
            if curr_time - self.prev_time >= 5000 and self.secret_open:
                self.secret_open = False
                self.prev_time = curr_time

    # -------------------------

    def mouse_control(self):
        mx, my = pg.mouse.get_pos()
        if mx < MOUSE_LBORD or mx > MOUSE_RBORD:
            pg.mouse.set_pos([HWIDTH, HHEIGHT])
        self.rel = pg.mouse.get_rel()[0]
        self.rel = max(-MOUSE_MAXREL, min(MOUSE_MAXREL, self.rel))
        self.angle += self.rel * MOUSE_SENS * self.game.dtime

    def movement(self):
        cos_a = math.cos(self.angle)
        sin_a = math.sin(self.angle)
        speed = PLYR_SPD * self.game.dtime
        speed_cos = cos_a * speed
        speed_sin = sin_a * speed
        dx, dy = 0, 0

        key = pg.key.get_pressed()
        if key[pg.K_w]:
            dx += speed_cos
            dy += speed_sin
        if key[pg.K_s]:
            dx -= speed_cos
            dy -= speed_sin
        if key[pg.K_a]:
            dx += speed_sin
            dy -= speed_cos
        if key[pg.K_d]:
            dx -= speed_sin
            dy += speed_cos

        if key[pg.K_LEFT]:
            self.angle -= PLYR_RSPD * self.game.dtime
        if key[pg.K_RIGHT]:
            self.angle += PLYR_RSPD * self.game.dtime

        self.angle %= math.tau
        self.can_walk(dx, dy)

    # -------------------------
    def can_walk(self, dx, dy):
        scale = PLYR_SCALE / self.game.dtime
        if self.get_unwall_cors(int(self.x + dx * scale), int(self.y)):
            self.x += dx
        if self.get_unwall_cors(int(self.x), int(self.y + dy * scale)):
            self.y += dy

        if self.get_secret_cors(int(self.x + dx * scale), int(self.y)) and self.secret_open:
            self.x += dx
        if self.get_secret_cors(int(self.x), int(self.y + dy * scale)) and self.secret_open:
            self.y += dy

        if self.get_gate_cors(int(self.x + dx * scale), int(self.y)) and self.gate_fullopen:
            self.x += dx

        if self.get_gate_cors(int(self.x), int(self.y + dy * scale)) and self.gate_fullopen:
            self.y += dy

    def get_unwall_cors(self, x, y):
        return (x, y) not in self.game.map.cor_map

    def get_secret_cors(self, x, y):
        key = pg.key.get_pressed()
        if key[pg.K_e]:
            for adj in self.get_adjs():
                if adj in Proxes.secrets:
                    secret = Proxes.secrets[adj]
                    secret[0] = True
                    self.secret_open = True
        return (x, y) in self.game.map.secret_map

    def get_gate_cors(self, x, y):
        return (x, y) in self.game.map.gate_map

    def get_adjs(self):
        ways = [-1, 0], [0, -1], [1, 0], [0, 1]  # [-1, -1], [1, -1], [1, 1], [-1, 1]
        area = [(self.map_pos[0] + dx, self.map_pos[1] + dy) for dx, dy in ways]
        area.append(self.map_pos)
        return area

    # -------------------------

    def draw(self):
        pg.draw.line(self.game.screen, 'yellow', (self.x * self.game.map.scale, self.y * self.game.map.scale),
                     (self.x * self.game.map.scale + WIDTH * math.cos(self.angle),
                      self.y * self.game.map.scale + WIDTH * math.sin(self.angle)), 2)
        pg.draw.circle(self.game.screen, 'green', (self.x * self.game.map.scale, self.y * self.game.map.scale), 5)

    @property
    def pos(self):
        return self.x, self.y

    @property
    def map_pos(self):
        return int(self.x), int(self.y)
