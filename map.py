import pygame as pg

# large maps cause incorrect textures on far wall.
# If any wall one space closer than the far wall, all walls to the right of obstructor will not glitch.
# Not tested for case where left does not glitch. Error not of concern right now.
# But must fix later for potential arena maps.

# when you do the finishing gate make a backdrop that leads into a dying viny forest
# unused: 20

_ = False
# | _,
num_map = [
    [1, 7, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, _, 1, 2, _, _, _, _, 1, _, 1, _, _, _, _, _, _, _, _, _, 1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, 1, 1, 1, 1, 1, _, 1, _, 1, _, _, _, _, 1, _, 1, _, _, 1, _, _, _, 1, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, _, _, _, _, 1, _, 1, _, _, 1, 1, _, _, 1, _, 1, _, 1, _, _, 1, _, 1, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, 1, 1, 1, _, 1, _, _, _, _, _, _, 1, _, 1, _, _, _, 1, 1, 5, 1, _, 1, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, 1, 5, 1, _, 1, 1, 1, _, 1, _, _, 1, _, _, _, _, _, 6, 1, 1, 1, _, 1, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, _, _, 1, _, _, _, 1, _, _, 1, _, 1, 1, _, _, _, 1, _, _, _, _, _, 1, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, 1, 1, 1, _, 1, _, 1, _, _, _, _, _, _, 1, _, _, 1, _, 1, _, _, 1, _, _, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, _, _, _, 1, _, 1, 1, 1, 1, 1, 1, _, 1, 1, 1, 1, _, 1, 1, _, 1, _, 1, 5, _, 1, _, 5, 1, _, 5, 1, 5, _, 1],
    [29, _, _, _, _, _, 29, _, 1, _, _, _, _, _, _, _, _, _, _, _, _, 1, _, 1, _, 1, _, _, 1, _, _, 1, _, _, 1, _, _, 1],
    [1, _, _, _, _, _, 1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1, _, 1, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [10, _, 1, _, 1, _, 1, _, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, _, _, _, 1, _, 1, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, 21, _, 22, _, 1, _, _, 1, _, _, _, _, _, _, _, 1, _, _, _, 1, _, 1, 1, 1, _, _, 1, 1, 1, 1, _, _, 1, 1, 1, 1],
    [29, _, 1, _, 1, _, 29, _, _, 1, _, _, 1, _, 1, 1, _, 1, _, _, 1, 1, _, _, 1, _, _, _, _, 1, 1, _, _, _, _, 1, _, 1],
    [1, _, 23, _, 24, _, 1, _, _, 1, _, _, 27, _, _, 1, _, 1, 1, 1, _, 1, _, _, 1, _, 1, 1, _, 1, 1, _, 1, 1, _, 1, 6, 1],
    [10, _, 1, _, 1, _, 1, _, _, 1, _, _, 28, _, _, 1, _, 1, _, _, _, 1, _, _, _, 1, 1, 1, _, 1, 1, 1, 1, _, _, _, _, 1],
    [1, _, 25, _, 26, _, 5, 1, _, _, _, _, 27, _, _, 1, _, 1, _, 1, 6, _, _, _, _, _, _, _, _, _, _, _, 1, _, _, _, _, 1],
    [29, _, 1, _, 1, _, _, 29, _, _, _, _, 28, _, _, 1, _, 1, _, _, 5, 1, _, 1, _, 1, _, 1, _, _, 1, _, 1, _, _, _, _, 1],
    [10, _, _, _, _, _, _, 1, _, _, _, _, 1, 5, 5, 1, _, 1, _, _, 5, 1, _, _, 1, _, 35, _, 1, 1, 1, _, 1, 1, 1, 1, _, 1],
    [1, _, _, _, _, _, _, 1, 1, 1, _, _, _, _, _, _, _, 1, _, _, 1, _, _, _, _, 35, _, _, _, _, 1, _, _, _, _, _, _, 1],
    [1, 10, 29, 1, 1, 29, 10, 2, _, 1, 1, 1, 1, 1, 1, 1, 1, 1, _, 1, _, _, _, 1, _, _, 1, _, 1, _, _, 35, 30, 31, 31, 33, 34, 1],
    [1, _, _, _, _, _, _, 1, _, _, _, _, _, _, _, _, _, _, _, 1, _, _, _, _, 1, _, 1, _, _, 35, _, 30, _, _, _, _, _, 30],
    [1, _, _, 1, 1, 1, _, _, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, _, _, _, _, _, 1, _, _, 35, _, 40, _, _, 30, _, 31, 32, 34, 31],
    [10, _, 1, _, 5, _, 1, _, 1, _, _, _, _, _, 1, _, _, _, _, _, _, _, _, _, 1, _, 1, _, _, 40, _, _, 30, _, _, _, _, 4],
    [1, _, _, _, 1, 1, _, _, _, 10, 1, _, _, _, _, _, _, _, _, _, _, _, _, 1, _, _, 40, _, 40, _, _, _, 37, _, 33, 31, 31, 31],
    [1, _, _, _, _, _, _, _, _, _, _, 10, _, _, _, 5, 5, 5, 5, _, _, _, 1, _, _, 40, _, _, _, 40, _, 38, _, _, _, _, _, 31],
    [10, _, 1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1, _, _, 35, _, 37, _, _, 37, 30, 30, 1, 31, _, 31],
    [1, _, _, 1, _, _, _, 1, 1, _, _, _, _, _, _, 5, 5, 5, 5, _, _, _, _, 1, _, _, _, _, 38, _, 39, _, _, _, _, 31, _, 32],
    [1, _, 5, 1, _, _, 1, _, _, _, _, 10, _, _, _, _, _, _, _, _, _, _, 1, _, _, _, _, 1, 36, _, _, _, _, _, _, _, _, 31],
    [1, 10, 1, 1, 1, 1, 1, 1, 1, 10, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 30, 35, 38, 36, 35, 30, 30, 1],
]


class Map:
    def __init__(self, game):
        self.game = game
        self.num_map = num_map
        self.scale = 25
        self.cor_map = {}
        self.lock_map = {}
        self.prop_map = {}
        self.secret_map = {}
        self.gate_map = {}
        self.trans_map = {}
        self.ghost_map = {}
        self.temp_vine = {}
        self.light_count = 0
        self.get_map()

    def update(self):
        self.anim_walls()

    def anim_walls(self):
        for i in self.cor_map:
            if 9 < self.cor_map[i] < 14:
                if self.light_count + self.cor_map[i] > 13:
                    self.light_count = 0
                    self.cor_map[i] = 10
                else:
                    self.cor_map[i] += self.light_count
                    self.light_count += 1

    def get_map(self):
        for j, row in enumerate(self.num_map):
            for i, value in enumerate(row):
                if value:
                    self.cor_map[(i, j)] = value
                    if value == 2:
                        self.lock_map[(i, j)] = value  # just for show
                    elif value == 5:
                        self.prop_map[(i, j)] = value  # show
                    elif value == 6:
                        self.secret_map[(i, j)] = value  # need (player py)
                    elif value == 7:
                        self.gate_map[(i, j)] = value    # need (player py)
                    elif 26 < value < 30:
                        self.trans_map[(i, j)] = value  # wip
                    elif 30 < value < 41:
                        self.temp_vine[(i, j)] = value

    def draw(self):
        [pg.draw.rect(self.game.screen, 'gray', (pos[0] * self.scale, pos[1] * self.scale, self.scale, self.scale), 2)
         for pos in self.cor_map]

        [pg.draw.rect(self.game.screen, 'green', (pos[0] * self.scale, pos[1] * self.scale, self.scale, self.scale), 2)
         for pos in self.lock_map]

        [pg.draw.rect(self.game.screen, 'blue', (pos[0] * self.scale, pos[1] * self.scale, self.scale, self.scale), 2)
         for pos in self.prop_map]

        [pg.draw.rect(self.game.screen, 'red', (pos[0] * self.scale, pos[1] * self.scale, self.scale, self.scale), 2)
         for pos in self.secret_map]

        [pg.draw.rect(self.game.screen, 'purple', (pos[0] * self.scale, pos[1] * self.scale, self.scale, self.scale), 2)
         for pos in self.trans_map]

        [pg.draw.rect(self.game.screen, 'orange', (pos[0] * self.scale, pos[1] * self.scale, self.scale, self.scale), 2)
         for pos in self.temp_vine]
