from sprite_main import *


class Weapon(AnimSprite):
    def __init__(self, game, path='assets/anim_sprites/pickups/stick/STICK1.png', scale=1.8, anim_time=90):
        super().__init__(game=game, path=path, wscale=scale, anim_time=anim_time)
        self.images = deque(
            [pg.transform.smoothscale(img, (self.image.get_width() * scale, self.image.get_height() * scale))
             for img in self.images])
        self.scale = scale
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
        #
        self.RANGE = 1
        self.DMG = 20
        self.deliver_dmg = 0
        self.type = ''
        #
        self.stick_images = self.get_images('assets/anim_sprites/pickups/stick')
        self.shotgun_images = self.get_images('assets/anim_sprites/pickups/shotgun')
        self.weapon_images = None

    def update(self):
        self.check_anim_time()
        self.animate_atk()
        self.weapon_up()
        self.right_click()

    def right_click(self):
        if self.right_clicked:
            if self.is_up:
                self.weapon_down()
            else:
                self.weapon_up()

    def draw(self):
        if self.draw_switch:
            if not self.is_up and not self.first_find:
                self.type_checker()
                self.weapon_up()
            self.game.screen.blit(self.image, self.weapon_pos)

    def animate_atk(self):
        self.deliver_dmg = 0
        if self.ready_atk and self.is_up:
            self.scale = 0.5
            self.animate(self.weapon_images)
                # if self.frame_counter == self.num_images:
                #    self.determine_atk()
                #    self.frame_counter = 0
                #    self.ready_atk = False

    def determine_atk(self):
        # determine weapon type here-ish
        # REM range is a prop
        self.deliver_dmg = self.DMG

    def attack_event(self, event):
        # self.anim_trigger = False
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.ready_atk = True
            if event.button == 3:
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
                if not self.first_find:
                    self.pos_inc += 2
                else:
                    self.pos_inc += 10
                self.weapon_pos = (HWIDTH - self.POS_W // 2, HEIGHT - self.pos_inc)

    def weapon_down(self):
        if self.is_up and self.right_clicked:
            if self.pos_inc2 < 0:
                self.right_clicked = False
                self.weapon_pos = (HWIDTH - self.POS_W // 2, HEIGHT - self.pos_inc2)
                self.is_up = False
                self.pos_inc2 = self.images[0].get_height()
            else:
                self.pos_inc2 -= 10
                self.weapon_pos = (HWIDTH - self.POS_W // 2, HEIGHT - self.pos_inc2)

    def type_checker(self):
        if self.type == 'katana':
            self.weapon_images = self.stick_images
            self.DMG = 20
        if self.type == 'shotgun':
            self.weapon_images = self.shotgun_images
            self.DMG = 50
            # self.num_images = len(self.images)

        # images() based structs or just modify in above
