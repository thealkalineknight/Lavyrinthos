from interacts import *
from monster import *


class ObjConfig:
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

        add_sprite(SpriteMain(game, path=self.static_sprite_path + '/ENTRY.PNG', pos=(4, 3.5),
                              wscale=1.2, hscale=1.2, shift=0.001))
        add_sprite(SpriteMain(game, path=self.static_sprite_path + '/mech/LKEYEMPT.PNG', pos=(33.8, 23)))
        add_sprite(SpriteMain(game, path=self.static_sprite_path + '/mech/LKEYEMPT.PNG', pos=(33.8, 24)))

        # add_sprite(AnimSprite(game, path=self.anim_sprite_path + '/gates/lvl1/LVL1EX2.PNG', pos=(4, 3.5),
        #                      wscale=1.2, hscale=1.2, shift=0.001, anim_time=200))

        add_interact(Interacts(game, path=self.anim_sprite_path + '/gates/LVL1EX1.PNG', pos=(1.5, 0.8),
                               wscale=1.5, hscale=1.5, shift=-0.1, anim_time=200, inter_type='gate'))
        # add_sprite(SpriteMain(game, path=self.static_sprite_path + '/mech/LKEYEMPT.PNG', pos=(3.5, 3.5)))
        add_interact(Interacts(game, path=self.anim_sprite_path + 'stands/LKEYEMPT.PNG', pos=(1.5, 7),
                               wscale=0.7, hscale=0.7, shift=0.27, inter_type='stand', iden=1))
        add_interact(Interacts(game, path=self.anim_sprite_path + 'stands/LKEYEMPT.PNG', pos=(1.5, 4),
                               wscale=0.7, hscale=0.7, shift=0.27, inter_type='stand', iden=2))

        add_monster(Monster(game, path=self.monster_path + '/dummy/dum init.png', pos=(14, 16.5),
                            wscale=1, hscale=1, shift=0.1, angle=0, mon_type='boss'))
        # should be for determining wake up trigger on start, maybe don't need to program anything (play test)

        # pos=(29.5, 3.5)

        add_interact(Interacts(game, path=self.anim_sprite_path + 'pickups/ITSTICK.PNG', pos=(1.5, 5),
                               wscale=0.05, hscale=0.05, shift=5, inter_type='weapon', iden=1))

        add_interact(Interacts(game, path=self.anim_sprite_path + 'pickups/ITSHOT.JPG', pos=(5, 3.5),
                               wscale=0.05, hscale=0.05, shift=5, inter_type='weapon', iden=2))

        add_monster(Monster(game, path=self.monster_path + '/hamster/ham init.png', pos=(4.5, 3.5),
                            wscale=0.7, hscale=0.7, shift=0.5, angle=4, mon_type='common', dir_range=10))

    def update(self):
        self.positions = {monster.map_pos for monster in self.monster_list if monster.alive_state}
        [sprite.update() for sprite in self.sprite_list]
        [interact.update() for interact in self.interact_list]
        [monster.update() for monster in self.monster_list]

    def add_sprite(self, sprite):
        self.sprite_list.append(sprite)

    def add_interact(self, inter):
        self.interact_list.append(inter)

    def add_monster(self, mon):
        self.monster_list.append(mon)
