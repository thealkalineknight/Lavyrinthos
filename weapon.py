from sprite_main import *


class Weapon(AnimSprite):
    def __init__(self, game, path='assets/anim_sprites/NOTEX.PNG', wscale=1.8, hscale=1.8, anim_time=90):
        super().__init__(game=game, path=path, wscale=wscale, hscale=hscale, anim_time=anim_time)
        self.STICK_PATH = self.get_images('assets/anim_sprites/pickups/stick')
        self.SHOT_PATH = self.get_images('assets/anim_sprites/pickups/shotgun')
        self.STICK_IMAGES = deque(
            [pg.transform.smoothscale(img, (self.image.get_width() * wscale, self.image.get_height() * hscale))
             for img in self.STICK_PATH])
        self.SHOT_IMAGES = deque(
            [pg.transform.smoothscale(img, (self.image.get_width() * wscale, self.image.get_height() * hscale))
             for img in self.SHOT_PATH])
        self.images = deque(
            [pg.transform.smoothscale(img, (self.image.get_width() * wscale, self.image.get_height() * hscale))
             for img in self.images])
        self.pos_inc = 0
        self.POS_W = self.images[0].get_width()
        self.weapon_pos = (0, 0)
        # (HWIDTH - self.images[0].get_width() // 2, HEIGHT - self.images[0].get_height())
        self.num_images = len(self.images)
        self.frame_counter = 0
        self.draw_switch = False  # will determine which weapon file path in future too
        self.is_up = False
        self.ready_atk = False
        self.first_find = False
        self.pos_inc2 = self.images[0].get_height()
        self.right_clicked = False
        self.firing_state = False
        #
        self.RANGE = 1
        self.DMG = 20
        self.deliver_dmg = 0
        self.type = ''
        self.INVENTORY = {1: False, 2: False}

    def update(self):
        self.check_anim_time()
        self.animate_atk()
        self.swapper()

    def swapper(self):
        if self.right_clicked:
            if self.is_up:
                self.weapon_down()
            else:
                self.weapon_up()
        key = pg.key.get_pressed()

        if key[pg.K_1] and self.INVENTORY[1]:
            self.type = 'katana'
            self.type_checker()
        if key[pg.K_2] and self.INVENTORY[2]:
            self.type = 'shotgun'
            self.type_checker()

    def draw(self):
        if self.draw_switch:
            if not self.is_up and not self.first_find:
                self.type_checker()
                self.weapon_up()
            if self.is_up and not self.first_find:
                self.weapon_down()
                if not self.is_up:
                    self.type_checker()
                    self.weapon_up()
            self.game.screen.blit(self.images[0], self.weapon_pos)

    def animate_atk(self):
        self.deliver_dmg = 0
        if self.ready_atk and self.is_up:
            self.firing_state = True
            if self.anim_trigger:
                self.images.rotate(-1)
                self.image = self.images[0]
                self.frame_counter += 1
                if self.frame_counter == self.num_images:
                    self.determine_atk()
                    self.frame_counter = 0
                    self.firing_state = False
                    self.ready_atk = False

    def determine_atk(self):
        # determine weapon type here-ish
        # REM range is a prop
        self.deliver_dmg = self.DMG

    def attack_event(self, event):
        self.anim_trigger = False
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1 and not self.right_clicked:
                self.ready_atk = True
            elif event.button == 3 and not self.firing_state:
                self.ready_atk = False
                self.right_clicked = True

    def weapon_up(self):
        if (not self.is_up and self.right_clicked) or (not self.is_up and not self.first_find):
            limit = self.images[0].get_height()
            if self.pos_inc >= limit:
                self.pos_inc = limit
                self.weapon_pos = (HWIDTH - self.POS_W // 2, HEIGHT - self.pos_inc)
                self.is_up = True
                self.pos_inc = 0
                self.right_clicked = False
                if not self.first_find:
                    self.first_find = True
            else:
                self.pos_inc += 20
                self.weapon_pos = (HWIDTH - self.POS_W // 2, HEIGHT - self.pos_inc)

    def weapon_down(self):
        if (self.is_up and self.right_clicked) or (self.is_up and not self.first_find):
            if self.pos_inc2 < 0:
                self.right_clicked = False
                self.weapon_pos = (HWIDTH - self.POS_W // 2, HEIGHT - self.pos_inc2)
                self.is_up = False
                self.pos_inc2 = self.images[0].get_height()
            else:
                self.pos_inc2 -= 20
                self.weapon_pos = (HWIDTH - self.POS_W // 2, HEIGHT - self.pos_inc2)

    def type_checker(self):
        if self.type == 'katana':
            self.images = self.STICK_IMAGES
            self.DMG = 20
            self.num_images = len(self.images)
        if self.type == 'shotgun':
            self.images = self.SHOT_IMAGES
            self.DMG = 50
            self.num_images = len(self.images)
