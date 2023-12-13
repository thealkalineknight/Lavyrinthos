from sprite_main import *
from sectors import *


class Monster(AnimSprite):
    def __init__(self, game, path=None, pos=None,
                 wscale=0.6, hscale=0.6, shift=0.38, animation_time=180, angle=None, health=100):
        super().__init__(game, path, pos, wscale, hscale, shift, animation_time)
        self.angle = angle
        self.health = health
        self.angle_index = 0
        self.idle_fo = self.get_images(self.path + '/front on')
        self.idle_fl = self.get_images(self.path + '/front left')
        self.idle_sl = self.get_images(self.path + '/side left')
        self.idle_bl = self.get_images(self.path + '/back left')
        self.idle_bo = self.get_images(self.path + '/back on')
        self.idle_br = self.get_images(self.path + '/back right')
        self.idle_sr = self.get_images(self.path + '/side right')
        self.idle_fr = self.get_images(self.path + '/front right')
        self.perspectives = {0: self.idle_fo, 1: self.idle_fl, 2: self.idle_sl, 3: self.idle_bl,
                             4: self.idle_bo, 5: self.idle_br, 6: self.idle_sr, 7: self.idle_fr}
        self.idle_images = None
        self.move_state = True
        #
        self.atk_fo = self.get_images(self.path + '/front on/atk')
        self.atk_fl = self.get_images(self.path + '/front left/atk')
        self.atk_sl = self.get_images(self.path + '/side left/atk')
        self.atk_bl = self.get_images(self.path + '/back left/atk')
        self.atk_bo = self.get_images(self.path + '/back on/atk')
        self.atk_br = self.get_images(self.path + '/back right/atk')
        self.atk_sr = self.get_images(self.path + '/side right/atk')
        self.atk_fr = self.get_images(self.path + '/front right/atk')
        self.atk_perspectives = {0: self.atk_fo, 1: self.atk_fl, 2: self.atk_sl, 3: self.atk_bl,
                                 4: self.atk_bo, 5: self.atk_br, 6: self.atk_sr, 7: self.atk_fr}
        self.atk_images = None
        self.attack_state = False
        #
        self.death_images = self.get_images(self.path + '/death')
        self.DEATH_IMAGE = self.NO_IMAGE = pg.image.load(self.path + '/death/9.PNG').convert_alpha()
        self.alive_state = True
        self.dying_state = False
        #
        self.sector = Sector.Sector0
        self.ssector = Sector.Sector0
        #
        self.frame_counter = 0
        self.size = 10  # these vars temp
        self.speed = 0.05  # 0.1  # sus
        self.loop_i = 0
        #
        self.DIR_RANGE = 6
        self.dir_orient = 0
        self.ray_value = self.DIR_RANGE + 1
        self.RANGED_DIST = 4
        self.MELEE_DIST = 1
        #
        self.prev_time = pg.time.get_ticks()
        self.ANY_DIST = False
        self.see_player = False

    def update(self):
        self.check_sector()
        self.check_anim_time()
        self.get_sprite()
        self.on_run()

    def on_run(self):
        if self.alive_state:
            self.timed_event()
            self.anim_main()
            self.determine_move()
        else:
            self.image = self.DEATH_IMAGE

    def timed_event(self):
        if not self.attack_state:
            curr_time = pg.time.get_ticks()
            if curr_time - self.prev_time >= 5000:
                self.prev_time = curr_time
                self.ray_value = self.DIR_RANGE + 1

    def anim_main(self):
        if self.sprite_ang < 0:
            self.sprite_ang += 360

        if self.sprite_ang < 22.5 or 337.5 < self.sprite_ang < 360:
            self.angle_index = self.angle
            self.idle_images = self.perspectives[self.angle_index]

        if 22.4 < self.sprite_ang < 67.5:
            self.angle_index = self.angle + 1
            if self.angle_index > 7:
                self.angle_index -= 8
            self.idle_images = self.perspectives[self.angle_index]

        if 67.4 < self.sprite_ang < 112.5:
            self.angle_index = self.angle + 2
            if self.angle_index > 7:
                self.angle_index -= 8
            self.idle_images = self.perspectives[self.angle_index]

        if 112.4 < self.sprite_ang < 157.5:
            self.angle_index = self.angle + 3
            if self.angle_index > 7:
                self.angle_index -= 8
            self.idle_images = self.perspectives[self.angle_index]

        if 157.4 < self.sprite_ang < 202.5:
            self.angle_index = self.angle + 4
            if self.angle_index > 7:
                self.angle_index -= 8
            self.idle_images = self.perspectives[self.angle_index]

        if 202.4 < self.sprite_ang < 247.5:
            self.angle_index = self.angle + 5
            if self.angle_index > 7:
                self.angle_index -= 8
            self.idle_images = self.perspectives[self.angle_index]

        if 247.4 < self.sprite_ang < 292.5:
            self.angle_index = self.angle + 6
            if self.angle_index > 7:
                self.angle_index -= 8
            self.idle_images = self.perspectives[self.angle_index]

        if 292.4 < self.sprite_ang < 337.5:
            self.angle_index = self.angle + 7
            if self.angle_index > 7:
                self.angle_index -= 8
            self.idle_images = self.perspectives[self.angle_index]

        self.animate(self.idle_images)

    # the timer function allows the monster to target player even if behind wall until ray value refreshes
    def determine_move(self):
        # ------------------------------------ test stuff
        ray = True
        key = pg.key.get_pressed()
        if key[pg.K_l]:
            ray = False
        # ------------------------------------
        player_x, player_y = int(self.game.player.x), int(self.game.player.y)
        monster_x, monster_y = int(self.x), int(self.y)
        if (abs(monster_x - player_x)) + (abs(monster_y - player_y)) < self.DIR_RANGE:
            self.ANY_DIST = True
            self.raycast()
            self.get_attacked()
            if self.ray_value < self.DIR_RANGE and ray:  # test on end
                self.moving((player_x, player_y))
                self.attacker(self.ray_value)
            else:
                self.route_moving()
        else:
            self.ANY_DIST = False
            self.route_moving()
        # ----------------------------------
        key = pg.key.get_pressed()
        if key[pg.K_p]:
            self.moving((player_x, player_y))
        if key[pg.K_o]:
            self.route_moving()

    # right now, it is any dist, no determiner until diff weapon types
    def get_attacked(self):
        dmg = self.game.weapon.deliver_dmg
        if self.health < 0:
            self.move_state = False
            self.dying_state = True
            self.animate(self.death_images)
            if self.anim_trigger:
                if self.frame_counter < len(self.death_images) - 2:
                    self.frame_counter += 1
                else:
                    self.alive_state = False
        elif dmg > 0:
            self.health -= dmg
        # no hurt anim lol

    def attacker(self, ray_value):
        if ray_value < self.RANGED_DIST:
            if not self.dying_state:
                self.move_state = True
                self.attack_state = True
                bow = 0
                # PUTTING GUN in melee temp because real will walk and range atk
                if ray_value < self.MELEE_DIST:
                    self.move_state = False
                    sword = 0
                    self.atk_images = self.atk_perspectives[self.angle_index]
                    self.animate(self.atk_images)
                    if self.ANY_DIST and not self.see_player:
                        self.move_state = True
        else:
            self.move_state = True
            self.attack_state = False
            # when not in ray range, freezes

    def route_moving(self):
        goal_node = self.sector.waypoints[self.loop_i]
        if goal_node == self.map_pos:
            self.loop_i += 1
        elif self.loop_i < len(self.sector.waypoints) - 1:
            self.moving(goal_node)
        else:
            self.loop_i = 0
            print('loop again')

    def moving(self, goal):
        if self.move_state:
            next_pos = self.game.pathfinding.get_path(self.map_pos, goal)
            self.anim_dir(next_pos)
            next_x, next_y = next_pos
            pg.draw.rect(self.game.screen, 'blue', (self.game.map.scale * next_x, self.game.map.scale * next_y,
                                                        self.game.map.scale, self.game.map.scale))
            angle = math.atan2(next_y + 0.5 - self.y, next_x + 0.5 - self.x)
            dx = math.cos(angle) * self.speed
            dy = math.sin(angle) * self.speed
            self.check_wall_collision(dx, dy)

    def anim_dir(self, next_pos):
        if next_pos[1] - self.map_pos[1] != 0:
            if next_pos[1] - self.map_pos[1] < 0:
                if next_pos[0] - self.map_pos[0] < 0:
                    self.dir_orient = 225  # 'up_left'
                    self.angle = 7
                elif next_pos[0] - self.map_pos[0] > 0:
                    self.dir_orient = 315  # 'up_right'
                    self.angle = 5
                else:
                    self.dir_orient = 270  # 'up'
                    self.angle = 6
                # down
            if next_pos[1] - self.map_pos[1] > 0:
                if next_pos[0] - self.map_pos[0] < 0:
                    self.dir_orient = 135  # 'down_left'
                    self.angle = 1
                elif next_pos[0] - self.map_pos[0] > 0:
                    self.dir_orient = 45  # 'down_right'
                    self.angle = 3
                else:
                    self.dir_orient = 90  # 'down'
                    self.angle = 2

        elif next_pos[0] - self.map_pos[0] < 0:
            self.dir_orient = 180  # 'left'
            self.angle = 0
        else:  # next_pos[0] - self.map_pos[0] > 0:
            self.dir_orient = 0  # 'right'
            self.angle = 4

    def check_wall_collision(self, dx, dy):
        if self.check_wall(int(self.x + dx * self.size), int(self.y)):
            self.x += dx
        if self.check_wall(int(self.x), int(self.y + dy * self.size)):
            self.y += dy

    def check_wall(self, x, y):
        return (x, y) not in self.game.map.cor_map

    def check_sector(self):
        sec1 = Sector.Sector1
        if sec1.x1 < self.x < sec1.x2:
            if sec1.y1 < self.y < sec1.y2:
                self.sector = sec1
                ssec1 = sec1.SSector1
                ssec2 = sec1.SSector2
                ssec3 = sec1.SSector3
                if ssec1.x1 < self.x < ssec1.x2:
                    if ssec1.y1 < self.y < ssec1.y2:
                        self.ssector = ssec1
                if ssec2.x1 < self.x < ssec2.x2:
                    if ssec2.y1 < self.y < ssec2.y2:
                        self.ssector = ssec2
                if ssec3.x1 < self.x < ssec3.x2:
                    if ssec3.y1 < self.y < ssec3.y2:
                        self.ssector = ssec3

    def raycast(self):
        self.see_player = False
        px, py = self.x, self.y
        x_map, y_map = self.map_pos

        ang_offset = math.radians(self.dir_orient)
        angle = PLYR_ANGLE + ang_offset
        ray_angle = angle - HFOV + 0.00001

        player_dist_v, player_dist_h = 0, 0

        for ray in range(NUM_RAYS):
            sin_a = math.sin(ray_angle)
            cos_a = math.cos(ray_angle)

            x_vert, dx = (x_map + 1, 1) if cos_a > 0 else (x_map - 1e-5, -1)
            vert_depth = (x_vert - px) / cos_a
            y_vert = py + vert_depth * sin_a

            player_depth = dx / cos_a
            dy = player_depth * sin_a

            for i in range(MAX_DEPTH):
                vert_grid = int(x_vert), int(y_vert)
                if vert_grid in self.game.map.cor_map:
                    break
                if vert_grid == self.game.player.map_pos:
                    player_dist_v = vert_depth
                    self.ray_value = max(player_dist_v, player_dist_h)
                    self.see_player = True
                    break
                x_vert += dx
                y_vert += dy
                vert_depth += player_depth

            # hors

            y_hor, dy = (y_map + 1, 1) if sin_a > 0 else (y_map - 1e-5, -1)
            hor_depth = (y_hor - py) / sin_a
            x_hor = px + hor_depth * cos_a

            player_depth = dy / sin_a
            dx = player_depth * cos_a

            for i in range(MAX_DEPTH):
                hor_grid = int(x_hor), int(y_hor)
                if hor_grid in self.game.map.cor_map:
                    break
                if hor_grid == self.game.player.map_pos:
                    player_dist_h = hor_depth
                    self.ray_value = max(player_dist_v, player_dist_h)
                    self.see_player = True
                    break
                x_hor += dx
                y_hor += dy
                hor_depth += player_depth

            if vert_depth < hor_depth:
                depth = vert_depth
            else:
                depth = hor_depth

            pg.draw.line(self.game.screen, 'yellow', (self.game.map.scale * px, self.game.map.scale * py),
                         (self.game.map.scale * px + self.game.map.scale * depth * cos_a,
                          self.game.map.scale * py + self.game.map.scale * depth * sin_a), 2)

            depth *= math.cos(self.game.player.angle - ray_angle)

            ray_angle += DELTA_ANGLE

    @property
    def map_pos(self):
        return int(self.x), int(self.y)