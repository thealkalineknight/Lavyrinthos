from sprite_main import *


class Monster(AnimSprite):
    def __init__(self, game, path=None, pos=None,
                 wscale=0.6, hscale=0.6, shift=0.38, animation_time=180, angle=0, health=100,
                 mon_type=None, dir_range=6):
        super().__init__(game, path, pos, wscale, hscale, shift, animation_time, angle)
        self.health = health
        self.mon_type = mon_type
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
        self.DEATH_IMAGE = pg.image.load(self.path + '/death/9.PNG').convert_alpha()
        self.alive_state = True
        self.dying_state = False
        #
        self.curr_sector = self.game.sector.Sector0
        self.curr_ssector = self.curr_sector
        #
        self.frame_counter = 0
        self.size = 10  # these vars temp
        self.speed = 0.05  # 0.1  #0.01  # sus
        self.loop_i = 0
        #
        self.DIR_RANGE = dir_range
        self.dir_orient = 0
        self.ray_value = self.DIR_RANGE + 1
        self.RANGED_DIST = 4
        self.MELEE_DIST = 1
        #
        self.prev_time = pg.time.get_ticks()
        self.ANY_DIST = False
        self.see_player = False
        self.out_search = True
        self.in_search = False
        self.cons_swap = False
        self.cons_i = 0
        self.snooze_state = False
        self.health_lock = True
        print(self.health, self.mon_type)

    def update(self):
        self.check_sector()
        self.check_anim_time()
        self.get_sprite()
        self.on_run()
        # self.game.interface.aureole()

    def on_run(self):
        if self.alive_state:
            self.super_det()
        else:
            self.image = self.DEATH_IMAGE
        if self.dying_state and self.alive_state:
            self.get_death()

    def super_det(self):
        if self.mon_type == 'common':
            if self.DLIM:
                self.timed_event()
                self.anim_main()
                self.simp_det_move()
            else:
                self.snooze_state = True
        if self.mon_type == 'boss':
            self.timed_event()
            self.anim_main()
            self.determine_move()
            if self.game.system.aureole_state:
                self.vulnerable()

    def timed_event(self):
        if not self.attack_state:
            curr_time = pg.time.get_ticks()
            if curr_time - self.prev_time >= 5000:
                self.prev_time = curr_time
                self.ray_value = self.DIR_RANGE + 1

    def anim_main(self):
        self.get_ang_index(self.angle)
        self.idle_images = self.perspectives[self.angle_index]
        self.animate(self.idle_images)

    # the timer function allows the monster to target player even if behind wall until ray value refreshes

    def simp_det_move(self):
        if self.out_search and self.in_search:
            simple = 0
        # ------------------------------------
        player_x, player_y = int(self.game.player.x), int(self.game.player.y)
        monster_x, monster_y = int(self.x), int(self.y)
        if (abs(monster_x - player_x)) + (abs(monster_y - player_y)) < self.DIR_RANGE:
            self.ANY_DIST = True
            self.snooze_state = False
            self.raycast()
            self.get_attacked()
            if self.ray_value < self.DIR_RANGE:
                self.out_search = False
                self.in_search = True
                self.moving((player_x, player_y))
                self.attacker(self.ray_value)
            else:
                self.out_search = True
        else:
            self.ANY_DIST = False
            self.out_search = True
            self.snooze_state = True

    def determine_move(self):
        if self.out_search and self.in_search:
            self.search_switcher()
        # ------------------------------------
        player_x, player_y = int(self.game.player.x), int(self.game.player.y)
        monster_x, monster_y = int(self.x), int(self.y)
        if (abs(monster_x - player_x)) + (abs(monster_y - player_y)) < self.DIR_RANGE:
            self.ANY_DIST = True
            self.raycast()
            if not self.health_lock:
                self.get_attacked()
            if self.ray_value < self.DIR_RANGE:
                self.out_search = False
                self.in_search = True
                self.moving((player_x, player_y))
                self.attacker(self.ray_value)
            else:
                self.out_search = True
                self.route_moving()
        else:
            self.ANY_DIST = False
            self.out_search = True
            self.route_moving()

    def vulnerable(self):
        if self.health > self.game.system.THRESHOLD:
            self.health_lock = False
            # print('anim aureole affected')
        if self.health <= self.game.system.THRESHOLD:
            if self.health > 0:
                self.health_lock = True
            # print('retreat while disappear anim')  # retreat state
            self.game.system.retreat_state = True
            # temp: grayed this func, and vulnerable turn on. obj config health

    def get_death(self):
        self.move_state = False
        self.animate(self.death_images)
        if self.anim_trigger:
            if self.frame_counter < len(self.death_images) - 2:
                self.frame_counter += 1
            else:
                self.alive_state = False

    # right now, it is any dist, no determiner until diff weapon types
    def get_attacked(self):
        self.draw_ray_cast()
        dmg = self.game.weapon.deliver_dmg
        if self.health < 0:
            self.dying_state = True
        elif dmg > 0:
            if self.weapon_ray():
                if 500 > self.screen_pos[0] > 100:
                    self.health -= dmg
                    print('hit')
                    if self.mon_type == 'boss':
                        self.game.system.SAVE_DMG += self.game.weapon.deliver_dmg
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

    def search_switcher(self):
        waypoints = self.curr_sector.waypoints
        curr1 = waypoints[self.loop_i][0]
        curr2 = waypoints[self.loop_i][1]
        cons_dist = 100
        mons_x, mons_y = int(self.x), int(self.y)
        i = 0
        for cons in waypoints:
            cons_calc = (abs(mons_x - cons[0])) + (abs(mons_y - cons[1]))
            if cons_calc < cons_dist:
                cons_dist = cons_calc
                self.cons_i = i
            i += 1
        curr_dist = (abs(mons_x - curr1)) + (abs(mons_y - curr2))
        if cons_dist > curr_dist:
            self.cons_swap = True
        self.in_search = False

    def route_moving(self):
        goal_node = self.curr_sector.waypoints[self.loop_i]
        if self.cons_swap:
            goal_node = self.curr_sector.waypoints[self.cons_i]
            self.loop_i = self.cons_i
            print('swapped')
            self.cons_swap = False
        # ------------------------------------
        if goal_node == self.map_pos:
            self.loop_i += 1
        elif self.loop_i < len(self.curr_sector.waypoints) - 1:
            self.moving(goal_node)
        else:
            self.loop_i = 0
            print('loop again')

    def moving(self, goal):
        if self.move_state:
            next_pos = self.game.pathfinding.get_path(self.map_pos, goal)
            if next_pos not in self.game.obj_config.positions:
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
        sec1 = self.game.sector.Sector1
        if sec1.x1 < self.x < sec1.x2:
            if sec1.y1 < self.y < sec1.y2:
                self.curr_sector = sec1
        sec2 = self.game.sector.Sector2
        if sec2.x1 < self.x < sec2.x2:
            if sec2.y1 < self.y < sec2.y2:
                self.curr_sector = sec2

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

    def weapon_ray(self):
        if self.game.player.map_pos == self.map_pos:
            return True

        wall_dist_v, wall_dist_h = 0, 0
        player_dist_v, player_dist_h = 0, 0

        px, py, = self.game.player.pos
        px_map, py_map = self.game.player.map_pos

        ray_angle = self.theta

        sin_a = math.sin(ray_angle)
        cos_a = math.cos(ray_angle)

        # hor
        y_hor, dy = (py_map + 1, 1) if sin_a > 0 else (py_map - 1e-6, -1)

        hor_depth = (y_hor - py) / (sin_a + 0.0001)
        x_hor = px + hor_depth * cos_a

        delta_depth = dy / (sin_a + 0.0001)
        dx = delta_depth * cos_a

        for i in range(MAX_DEPTH):
            hor_grid = int(x_hor), int(y_hor)
            if hor_grid == self.map_pos:
                player_dist_h = hor_depth
                break
            if hor_grid in self.game.map.cor_map:
                wall_dist_h = hor_depth
                break
            x_hor += dx
            y_hor += dy
            hor_depth += delta_depth

        # vert
        x_vert, dx = (px_map + 1, 1) if cos_a > 0 else (px_map - 1e-6, -1)

        vert_depth = (x_vert - px) / cos_a
        y_vert = py + vert_depth * sin_a

        delta_depth = dx / cos_a
        dy = delta_depth * sin_a

        for i in range(MAX_DEPTH):
            tile_vert = int(x_vert), int(y_vert)
            if tile_vert == self.map_pos:
                player_dist_v = vert_depth
                break
            if tile_vert in self.game.map.cor_map:
                wall_dist_v = vert_depth
                break
            x_vert += dx
            y_vert += dy
            vert_depth += delta_depth

        player_dist = max(player_dist_v, player_dist_h)
        wall_dist = max(wall_dist_v, wall_dist_h)

        if 0 < player_dist < wall_dist or not wall_dist:
            return True
        return False

    def draw_ray_cast(self):
        scale = self.game.map.scale
        pg.draw.circle(self.game.screen, 'red', (scale * self.x, scale * self.y), 15)
        if self.weapon_ray():
            pg.draw.line(self.game.screen, 'orange', (scale * self.game.player.x, scale * self.game.player.y),
                         (scale * self.x, scale * self.y), 5)

    @property
    def map_pos(self):
        return int(self.x), int(self.y)
