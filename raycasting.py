import pygame as pg
from settings import *
from proxes import *


class RayCasting:
    def __init__(self, game):
        self.game = game
        self.obj_rend_list = []
        self.raycast_result = []
        self.wall_tex = self.game.obj_rend.wall_tex
        self.vis_spans = []
        self.secret_value = 0, 0
        self.lock_value = 0, 0

    def update(self):
        self.raycast()
        self.prep_wall_rend()

    def raycast(self):
        self.raycast_result = []
        self.vis_spans = []
        vert_tex, hor_tex = 1, 1
        px, py = self.game.player.pos
        x_map, y_map = self.game.player.map_pos
        ray_angle = self.game.player.angle - HFOV + 0.00001

        for ray in range(NUM_RAYS):
            sin_a = math.sin(ray_angle)
            cos_a = math.cos(ray_angle)

            # verts -------------------------------

            x_vert, dx = (x_map + 1, 1) if cos_a > 0 else (x_map - 1e-5, -1)
            vert_depth = (x_vert - px) / cos_a
            y_vert = py + vert_depth * sin_a

            player_depth = dx / cos_a
            dy = player_depth * sin_a

            for i in range(MAX_DEPTH):
                vert_grid = int(x_vert), int(y_vert)
                if vert_grid in Proxes.secrets:
                    self.secret_value = vert_grid
                if vert_grid in Proxes.locks:
                    self.lock_value = vert_grid

                if vert_grid in self.game.map.cor_map:
                    if vert_grid in self.game.map.trans_map:
                        vert_tex = self.game.map.cor_map[vert_grid]
                        break
                    else:
                        vert_tex = self.game.map.cor_map[vert_grid]
                        break
                x_vert += dx
                y_vert += dy
                vert_depth += player_depth

            # hors -------------------------------

            y_hor, dy = (y_map + 1, 1) if sin_a > 0 else (y_map - 1e-5, -1)
            hor_depth = (y_hor - py) / sin_a
            x_hor = px + hor_depth * cos_a

            player_depth = dy / sin_a
            dx = player_depth * cos_a

            for i in range(MAX_DEPTH):
                hor_grid = int(x_hor), int(y_hor)
                if hor_grid in Proxes.secrets:
                    self.secret_value = hor_grid
                if hor_grid in Proxes.locks:
                    self.lock_value = hor_grid

                if hor_grid in self.game.map.cor_map:
                    if hor_grid in self.game.map.trans_map:
                        hor_tex = self.game.map.cor_map[hor_grid]
                        break
                    else:
                        hor_tex = self.game.map.cor_map[hor_grid]
                        break
                x_hor += dx
                y_hor += dy
                hor_depth += player_depth

            if vert_depth < hor_depth:
                self.vis_spans.append(vert_depth)
                depth, texture = vert_depth, vert_tex
                y_vert %= 1
                offset = y_vert if cos_a > 0 else (1 - y_vert)
            else:
                self.vis_spans.append(hor_depth)
                depth, texture = hor_depth, hor_tex
                x_hor %= 1
                offset = (1 - x_hor) if sin_a > 0 else x_hor

            depth *= math.cos(self.game.player.angle - ray_angle)

            proj_height = SCREEN_DIST / (depth + 0.0001)

            self.raycast_result.append((depth, proj_height, texture, offset))

            ray_angle += DELTA_ANGLE

            # pg.draw.line(self.game.screen, 'yellow', (100 * px, 100 * py),
            #             (100 * px + 100 * depth * cos_a, 100 * py + 100 * depth * sin_a), 2)

            # pg.draw.rect(self.game.screen, 'darkblue', (ray * SCALE, HHEIGHT - proj_height // 2,
            #                                            SCALE, proj_height))

    def prep_wall_rend(self):
        self.obj_rend_list = []
        for ray, values in enumerate(self.raycast_result):
            depth, proj_height, texture, offset = values

            # conv to func when done
            if self.secret_value in Proxes.secrets:
                secret = Proxes.secrets[self.secret_value]
                if secret[0]:
                    if self.game.player.secret_open and texture == 6:
                        texture = 9

            if self.lock_value in Proxes.locks:
                lock = Proxes.locks[self.lock_value]
                if lock[0]:
                    if texture == 2:
                        texture = 3

            if proj_height < HEIGHT:
                wall_column = self.wall_tex[texture].subsurface(
                    offset * (MAX_TEX - SCALE), 0, SCALE, MAX_TEX
                )
                wall_column = pg.transform.scale(wall_column, (SCALE, proj_height))
                wall_pos = (ray * SCALE, HHEIGHT - proj_height // 2)
            else:
                texture_height = MAX_TEX * HEIGHT / proj_height
                wall_column = self.wall_tex[texture].subsurface(
                    offset * (MAX_TEX - SCALE), HMAX_TEX - texture_height // 2,
                    SCALE, texture_height
                )
                wall_column = pg.transform.scale(wall_column, (SCALE, HEIGHT))
                wall_pos = (ray * SCALE, 0)

            self.obj_rend_list.append((depth, wall_column, wall_pos))
