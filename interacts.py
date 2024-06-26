from sprite_main import *


class Interacts(AnimSprite):
    def __init__(self, game, path=None, pos=None,
                 wscale=0.6, hscale=0.6, shift=0.38, anim_time=180, inter_type=None, iden=None):
        super().__init__(game, path, pos, wscale, hscale, shift, anim_time)
        self.inter_type = inter_type
        self.iden = iden
        self.frame_count = 0
        if self.inter_type == 'gate':
            self.unlocked_images = self.get_images(self.path + '/lvl1')
        #
        self.KEYED_IMAGE = pg.image.load('assets/anim_sprites/stands/LKEYFULL.PNG').convert_alpha()
        self.NO_IMAGE = pg.image.load('assets/anim_sprites/NOTEX.PNG').convert_alpha()
        self.aur_pos = -5
        self.aur_fin_state = False
        self.proxes = self.game.proxes

    def update(self):
        self.check_anim_time()
        self.get_sprite()
        key = pg.key.get_pressed()
        if key[pg.K_e]:
            self.check_type()
        if self.game.system.aur_trigger or key[pg.K_l]:
            self.form_aureole()
            # self.game.interface.aureole()  # old
        if self.game.system.crusade_state:
            self.game.system.end_crusade()

    def check_type(self):
        if self.inter_type == 'gate':
            self.gate_check()
        if self.inter_type == 'stand':
            self.stand_check()
        if self.inter_type == 'weapon':
            self.weapon_check()
        if self.game.system.aur_trigger2 and self.inter_type == 'aureole':
            self.aureole_check()

    def gate_check(self):
        if self.game.system.retreat_state:
            for adj in self.game.player.get_adjs():
                if adj in self.proxes.gates:
                    gate = self.proxes.gates[adj]
                    #
                    if self.frame_count < len(self.unlocked_images) - 1:
                        self.unlocked_images.rotate(-1)
                        self.image = self.unlocked_images[0]
                        self.frame_count += 1
                    elif self.frame_count == len(self.unlocked_images) - 1:
                        self.game.player.gate_fullopen = True
                        gate[0] = True
                        self.game.system.crusade_state = True

    def stand_check(self):
        for thing in self.proxes.locks:
            lock = self.proxes.locks[thing]
            for item in self.proxes.stands:
                stand = self.proxes.stands[item]
                # if lock id = stand id, and stand id = sprite id
                if lock[1] == stand[1] and stand[1] == self.iden:  # a bit close for now
                    # if pos = stand pos and key id true
                    if self.game.player.map_pos == item and lock[0]:
                        stand[0] = True
                        self.image = self.KEYED_IMAGE
                        if self.gate_prep_check():
                            self.game.system.aur_trigger = True

    def weapon_check(self):
        for item in self.proxes.pickups:
            pickup = self.proxes.pickups[item]
            # if thing id = sprite id
            if pickup[1] == self.iden:  # a bit close for now
                # if pos = thing pos
                if self.game.player.map_pos == item:
                    if not pickup[0]:
                        self.image = self.NO_IMAGE
                        weapon = self.game.weapon
                        weapon.first_find = False
                        weapon.draw_switch = True
                        weapon.INVENTORY[pickup[2]] = True
                        self.weapon_prep_check(pickup[2])
                        pickup[0] = True

    def form_aureole(self):
        if self.inter_type == 'aureole':
            if self.anim_trigger:
                if not self.aur_fin_state:
                    self.x, self.y = self.game.player.get_an_adjs()[0], self.game.player.get_an_adjs()[1]
                    self.x += 0.5
                    self.y += 0.5
                    self.aur_fin_state = True
                else:
                    if self.aur_pos == 1:
                        self.game.system.aur_trigger2 = True
                    else:
                        self.aur_pos += 0.5
                self.SPRITE_HSHIFT = self.aur_pos

    def aureole_check(self):
        if self.game.player.map_pos == (int(self.x), int(self.y)):
            self.image = self.NO_IMAGE
            system = self.game.system
            system.aureole_state = True

    def gate_prep_check(self):
        for item in self.proxes.stands:
            stand = self.proxes.stands[item]
            if not stand[0]:
                return False
        return True

    def weapon_prep_check(self, pickup):
        weapon = self.game.weapon
        if pickup == 1:
            weapon.type = 'katana'
        if pickup == 2:
            weapon.type = 'shotgun'
