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
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, _, _, _, _, _, _, _, 1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, _, _, _, _, 1, 1, 1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, _, _, _, _, 1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, _, _, _, _, 1, _, _, 1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, _, _, _, 1, _, _, 1, 1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, _, 1, 1, _, _, 1, _, 1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, _, 1, _, _, 1, _, _, 1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, _, 1, 1, _, _, 1, _, 1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, _, _, _, 1, _, 1, _, 1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, _, _, _, 1, _, 1, _, 1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, _, _, 1, _, _, 1, _, 1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, 1, 1, 1, _, _, _, 1, _, 1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [4, _, _, _, _, _, _, 1, _, 1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, 1, 1, 1, 1, _, _, 1, _, 1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, _, _, _, 1, 6, 1, _, 1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, _, _, _, 1, _, 1, _, 1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, _, _, _, 1, _, 1, _, 1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, 1, 1, 1, 1, 1, _, 1, _, 1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, _, _, _, _, _, 1, _, 1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [5, _, _, _, _, _, _, 5, _, 1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, _, _, _, _, _, 1, _, 1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, _, _, _, _, _, 1, _, 1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [5, _, _, _, _, _, _, 5, _, 1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, _, _, _, _, _, 1, _, 1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, 1, _, _, 1, 5, 1, 1, 6, 1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, _, _, _, _, _, _, _, 1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, _, _, _, _, _, _, _, 1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, _, _, _, _, _, _, _, 1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, 5, 1, 1, 1, 5, 1, 1, 5, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]


class Map2:
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
