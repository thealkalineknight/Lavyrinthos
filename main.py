import sys
from map import *
from proxes import *
from player import *
from raycasting import *
from sectors import *
from objectrenderer import *
from obj_config import *
from sound import *
from pathfinding import *
from weapon import *
from interface import *
from system import *
from map2 import *
from proxes2 import *
from sectors2 import *
from obj_config2 import *


class Game:
    def __init__(self):
        pg.init()
        pg.mouse.set_visible(False)
        self.screen = pg.display.set_mode(RES)
        self.clock = pg.time.Clock()
        self.dtime = 1
        self.new_game()
        self.running = True

    def new_game(self):  # if calls property from other class, list after
        self.CRUSADE = 1
        self.map = Map(self)
        self.proxes = Proxes
        self.player = Player(self)
        self.obj_rend = ObjRend(self)  # must before raycasting
        self.raycasting = RayCasting(self)
        self.sector = Sector
        self.obj_config = ObjConfig(self)
        self.pathfinding = Pathfinding(self)
        self.weapon = Weapon(self)
        self.sound = Sound(self)
        self.interface = Interface(self)
        self.system = System(self)

    def run(self):  # undefeatable True loop, must either weld with draw() or depend on variable
        self.theme()
        while True:
            if not self.running:
                self.theme()
                self.pausing()
            else:
                self.update()
                self.draw()
                self.check_events()

    def update(self):
        self.player.update()
        self.map.update()
        self.raycasting.update()
        self.obj_config.update()
        self.weapon.update()
        self.dtime = self.clock.tick(FPS)
        pg.display.set_caption(f'{self.clock.get_fps():.1f}')

    def draw(self):
        pg.display.flip()
        self.obj_rend.draw()
        self.weapon.draw()
        # self.screen.fill('black')
        # self.map.draw()
        # self.player.draw()

    def pausing(self):
        ui = self.interface
        ui.INTER_MODE = True
        while ui.INTER_MODE:
            pg.display.flip()
            ui.update()
            ui.draw()
            self.check_events()
        if ui.MAIN_MODE:
            self.CRUSADE += 1
            self.refresh_game()
            self.system.crusade_state = False
            self.running = True
            self.run()

    def refresh_game(self):
        self.map = self.prep_class('map')
        self.proxes = self.prep_class('prox')
        self.sector = self.prep_class('sec')
        self.obj_config = self.prep_class('obj')
        self.pathfinding = Pathfinding(self)

    def prep_class(self, mode):  # obj rend sky ground ; interface ; sys ; main
        book = {}
        if mode == 'map':
            book = {1: Map(self), 2: Map2(self)}
        if mode == 'prox':
            book = {1: Proxes, 2: Proxes2}
        if mode == 'sec':
            book = {1: Sector, 2: Sector2}
        if mode == 'obj':
            book = {1: ObjConfig(self), 2: ObjConfig2(self)}
        # print(self.CRUSADE)
        return book[self.CRUSADE]

    def pre_mode(self):
        ui = self.interface
        while ui.PRE_MODE:
            pg.display.flip()
            ui.update()
            ui.draw()
            self.check_events()
        if ui.MAIN_MODE:
            self.run()

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()
            self.weapon.attack_event(event)

    def theme(self):
        self.sound.theme_song()


if __name__ == '__main__':
    game = Game()
    game.pre_mode()


# problems:
# new game() placement, while True, window open connected to level running; loading screen
