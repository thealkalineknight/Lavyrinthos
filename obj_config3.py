from interacts import *
from monster import *


class ObjConfig3:
    def __init__(self, game):
        self.game = game
        self.sprite_list = []
        self.interact_list = []
        self.monster_list = []
        self.positions = {}
        self.static_sprite_path = 'assets/static_sprites/'
        self.anim_sprite_path = 'assets/anim_sprites/'
        self.monster_path = 'assets/monster/'
        add_sprite = self.add_sprite
        add_interact = self.add_interact
        add_monster = self.add_monster

        add_interact(Interacts(game, path=self.anim_sprite_path + 'pickups/AUREOLE/TESTORB.png',
                               pos=(-10, -10), wscale=0.2, hscale=0.2, shift=0.27, anim_time=70,
                               inter_type='aureole', iden=1))

        add_monster(Monster(game, path=self.monster_path + '/dummy/dum init.png', pos=(6, 9.5),
                            wscale=1, hscale=1, shift=0.1, angle=0, mon_type='boss',
                            health=300 - self.game.system.SAVE_DMG))

        add_interact(Interacts(game, path=self.anim_sprite_path + 'stands/LKEYEMPT.PNG', pos=(3.5, 6.5),
                               wscale=0.7, hscale=0.7, shift=0.27, inter_type='stand', iden=1))

    def update(self):
        self.positions = {monster.map_pos for monster in self.monster_list if monster.alive_state
                          and not monster.snooze_state}
        [sprite.update() for sprite in self.sprite_list]
        [interact.update() for interact in self.interact_list]
        [monster.update() for monster in self.monster_list]

    def add_sprite(self, sprite):
        self.sprite_list.append(sprite)

    def add_interact(self, inter):
        self.interact_list.append(inter)

    def add_monster(self, mon):
        self.monster_list.append(mon)
