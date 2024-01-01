import sys
from map import *
from player import *
from raycasting import *
from objectrenderer import *
from obj_config import *
from sound import *
from pathfinding import *
from weapon import *


class Game:
    def __init__(self):
        pg.init()
        pg.mouse.set_visible(False)
        self.screen = pg.display.set_mode(RES)
        self.clock = pg.time.Clock()
        self.dtime = 1
        self.new_game()

    def new_game(self):  # if calls property from other class, list after
        self.map = Map(self)
        self.player = Player(self)
        self.obj_rend = ObjRend(self)  # must before raycasting
        self.raycasting = RayCasting(self)
        self.obj_config = ObjConfig(self)
        self.pathfinding = Pathfinding(self)
        self.weapon = Weapon(self)
        self.sound = Sound(self)

    def run(self):
        self.theme()
        while True:
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
    game.run()
