import main
import map
import game
import tile
import particle

enum KidState:
    Wandering
    Following
    Stopping
    Studying
    Crazy
    Sitting
    Crying
    Monster
    Dancing

class Player:
    int tid
    float x, y
    float dx, dy
    int jump
    int frame
    bool climbing with 1
    bool falling with 1
    bool flying with 1
    KidState state
    int attention_span
    char *name
    int wx, wy
    int kid
    int ladders
    int homex, homey
    int dig

    bool seen
    float seen_x, seen_y

static int ladder
global int gravity = 1

def player_create(int tid) -> Player*:
    Player *self; land_alloc(self)
    self.tid = tid
    return self

def kid_command(Player *self, KidState state, bool named):
    if self.state == state or self.state == Studying or self.state == Crazy:
        return
    if self.state == Crying or self.state == Monster:
        if not named:
            return
        if state != Stopping:
            return
    self.state = state
    self.attention_span = 600
    if state == Stopping:
        self.attention_span = 1200
    if state == Studying:
        self.attention_span = 300

def distance(Player *self, float *rx, *ry, tx, ty) -> float:
    Game *g = game_global()
    Map *m = g.map
    int dx = tx - self.x
    int dy = ty - self.y
    if dx > m.w * m.tw / 2: dx -= m.w * m.tw
    if dx < -m.w * m.tw / 2: dx += m.w * m.tw
    if dy > m.h * m.th / 2: dy -= m.h * m.th
    if dy < -m.h * m.th / 2: dy += m.h * m.th
    if rx: *rx = dx
    if ry: *ry = dy
    return sqrt(dx * dx + dy * dy)

def kid_distance(Player *self, float *rx, *ry) -> float:
    return distance(self, rx, ry, game_global()->player->x, game_global()->player->y)

def player_get_under(Player *self) -> Tile*:
    Tile *most_important = None
    Map *map = game_global()->map
    Tile *pt = tile_by_id(self.tid)
    int dx[] = {pt.border, pt.w - 1 - pt.border, pt.border, pt.w - 1 - pt.border}
    int dy[] = {pt.h - 10 - 100, pt.h - 10 - 100, pt.h - 10, pt.h - 10}
    for int i in range(4):
        int x = map_tx(self.x + dx[i])
        int y = map_ty(self.y + dy[i])
        int tid = map_get(map, x, y)
        Tile *t = tile_by_id(tid)
        if t:
            if t.climb:
                most_important = t
            else:
                return t

    return most_important

def player_place_at_start(Player *self, int x, y, Map *map):
    #Tile *t = tile_by_id(self.tid)
    self.x = (map.start_x + x) * map.tw
    self.y = (map.start_y + y) * map.th - 256
    self.homex = self.x
    self.homey = self.y
    map_crowd(map, self.x, self.y)

def player_collision(Player *self) -> bool:
    Tile *t = player_get_under(self)
    if t and not t.climb:
        return True
    return False

def player_ladder(Player *self):
    if not ladder:
        ladder = tile_by_name("ladder")
    Game *g = game_global()
    int x = map_tx(self.x + 64)
    int y = map_ty(self.y + 256 - 10)
    int tid = map_get(g.map, x, y)
    if tid == 0:
        if self.ladders == 0:
            return
        tid = map_get(g.map, x, y + gravity)
        if tid == 0:
            return
        map_put(g.map, x, y, ladder)
        particle_smoke(x * 128 + 64, y * 128 + 64, 64)
        land_sound_play(g.toc, 1, 0, 1)
        self.ladders--
    elif tid == ladder:
        if self.ladders >= 25:
            return
        tid = map_get(g.map, x, y - gravity)
        if tid == ladder:
            return
        map_put(g.map, x, y, 0)
        particle_smoke(x * 128 + 64, y * 128 + 64, 64)
        land_sound_play(g.toc, 1, 0, 1)
        self.ladders++

def player_dig(Player *self, int kx):
    Game *g = game_global()
    int x = map_tx(self.x + 64 + kx * 128)
    int y = map_ty(self.y + 256 - 10)
    int tid = map_get(g.map, x, y)
    if tid == g.earth->id:
        self.dig ++
        particle_smoke(self.x + 64 + kx * 64, self.y + 256 - 70, 1)
        if self.dig % 10 == 1:
            land_sound_play(g.toc, 0.5, 0, 0.5)
        if self.dig >= 100:
            map_put(g.map, x, y, 0)
            land_sound_play(g.knock, 1, 0, 1)
            self.dig = 0

def player_ground(Player *self) -> bool:
    Tile *t = player_get_under(self)
    if t:
        return True
    return False

def player_move_(Player *self, float dx, dy, bool fall) -> bool:
    Game *g = game_global()
    float ox = self.x
    float oy = self.y
    self.x += dx
    self.y += dy
    bool c
    c = fall ? player_ground(self) : player_collision(self)
    if c:
        self.x = ox
        self.y = oy
        return False
    self.x = ffmod(self.x, g.map->w * g.map->tw)
    self.y = ffmod(self.y, g.map->h * g.map->th)
    map_crowd(g.map, self.x, self.y)
    map_uncrowd(g.map, ox, oy)
    self.dig = 0
    return True

def player_transport(Player *self, float x, y):
    Game *g = game_global()
    map_uncrowd(g.map, self.x, self.y)
    self.x = x
    self.y = y
    map_crowd(g.map, self.x, self.y)

def player_teleport(Player *self):
    Game *g = game_global()
    for int t in range(100):
        int rx = land_rand(0, g.map->w - 1)
        int ry = land_rand(0, g.map->h - 1)
        if map_get(g.map, rx, ry) == 0:
            #
            #   0
            #
            # 128  x 256 - 130
            #      x
            # 256  x 256 - 10
            map_uncrowd(g.map, self.x, self.y)
            rx *= g.map->tw
            ry *= g.map->th
            self.x = rx
            self.y = ry + 127 - 256 + 10
            map_crowd(g.map, self.x, self.y)

def player_move(Player *self, float dx, dy) -> bool:
    return player_move_(self, dx, dy, False)

def player_fall(Player *self, float dx, dy) -> bool:
    return player_move_(self, dx, dy, True)

static def kid_mind(Player *self, int *kx, *ky):
    Game *g = game_global()
    if self.attention_span > 0:
        self.attention_span--
    int c = map_crowded(g.map, self.x, self.y)
    if self.state == Wandering:
        if self.attention_span == 0:
            self.wx = land_rand(-1, 1)
            if self.wx == 0 and c > 5:
                self.wx = land_rand(-1, 1)
            self.attention_span = land_rand(60, 300)
        if self.attention_span % 3 == 0:
            *kx = self.wx
    elif self.state == Following or self.state == Monster:
        float dx, dy
        if self.state == Following:
            kid_distance(self, &dx, &dy)
        else:
            distance(self, &dx, &dy, game_global()->monster->x,
                game_global()->monster->y)
        if fabs(dy) < 128:
            if dx > 150:
                *kx = 1
            if dx < -150:
                *kx = -1
        else:
            if dx > 0:
                *kx = 1
            if dx < 0:
                *kx = -1
        if dy > 128:
            *ky = 1
        if dy < 0:
            *ky = -1
        if self.attention_span == 0:
            self.state = land_rand(0, 3) == 0 ? Crying : Wandering
            if self.state == Crying:
                self.attention_span = 600
    elif self.state == Stopping:
        if self.attention_span == 0:
            self.state = Wandering
    elif self.state == Studying:
        if self.attention_span == 0:
            self.state = Crazy
            self.attention_span = 300
    elif self.state == Crazy:
        float a = self.kid * 2 * pi / g.kids_count
        a += self.attention_span * 2 * pi / 300
        float dx = cos(a) * 15
        float dy = sin(a) * 15
        player_move(self, dx, dy)
        if self.attention_span == 0:
            self.state = Wandering
            player_teleport(self)
    elif self.state == Sitting:
        Tile *mit = player_get_under(self)
        if mit and mit.id == g.brick->id:
            if c > 1:
                float dx, dy
                distance(self, &dx, &dy, self.homex, self.homey)
                if dx > 0: *kx = 1
                if dx < 0: *kx = -1
                if dy > 0: *ky = 1
                if dy < 0: *ky = -1
        else:
            self.state = Wandering
    elif self.state == Crying:
        Tile *pt = tile_by_id(self.tid)
        if g.time % 8 == 1:
            particle_tear(self.x + 20, self.y + 256 - pt.tall + 20, -1)
        if g.time % 8 == 5:
            particle_tear(self.x + 128 - 20, self.y + 256 - pt.tall + 20, 1)
    elif self.state == Dancing:
        if self.wy == 0: self.wy = -1
        if self.attention_span == 0:
            self.attention_span = land_rand(8, 12)
            self.wy *= -1
            particle_sparkle(self.x + 64, self.y + 128, 1)
        *ky = self.wy

static def monster_mind(Player *self, int *kx, int *ky):
    Game *game = game_global()
    if self.attention_span > 0:
        self.attention_span--
    if self.attention_span == 0:

        int tx =  map_tx(self.x + 128 + self.wx * 70)
        int ty =  map_ty(self.y + 256 - 10 - 50 + self.wy * 55)
        if self.ladders > 0:
            if map_get(game.map, tx, ty) == game.earth->id:
                map_put(game.map, tx, ty, 0)
                self.ladders--

        if game.kids[self.kid]->state != Monster:
            for int i in range(game.kids_count):
                Player *kid = game.kids[i]
                if kid.state == Crying and kid.attention_span == 0:
                    player_transport(self, kid.x, kid.y)
                    for int t in range(50):
                        player_move(self, 0, -10)
                    kid.state = Monster
                    kid.attention_span = 36000
                    self.kid = i
                    self.ladders = 100
                    break

        self.wx = land_rand(-1, 1)
        self.wy = 0
        if self.wx == 0:
            self.wy = 2 * land_rand(0, 1) - 1
        self.attention_span = land_rand(60, 300)
    self.flying = True
    *kx = self.wx
    *ky = self.wy

    if kid_distance(self, None, None) < 100:
        gravity = -1

def player_collide(Player *self, int kx, ky, int who):
    if who == 2:
        self.attention_span = 0
    else:
        if kx: self.wx = -self.wx
        if ky: self.wy = -self.wy

def player_input(Player *self, int kx, ky, int who):
    Game *game = game_global()
    if who == 1:
        kid_mind(self, &kx, &ky)
    if who == 2:
        monster_mind(self, &kx, &ky)

    self.y += gravity
    bool ground = player_ground(self)
    self.y -= gravity

    if kx:
        self.frame++

    if ky * gravity >= 0 or self.jump > 46:
        self.jump = 0

    if ky == -gravity:
        if ground or self.jump:
            self.jump++
            if who == 0:
                if self.jump == 1:
                    particle_sparkle(self.x + 64, self.y + 256, 10)
                    land_sound_play(game.ding, 0.5, 0, 4)

    Tile *mit = player_get_under(self)

    if who == 0 and mit:
        if mit.id == game.brick->id:
            gravity = 1
    
    if not mit or not mit.climb:
        if self.jump or self.climbing or self.flying:
            self.dy += ky
        elif not ground:
            self.dy += gravity
            ky = 0
    else:
        self.dy += ky

    if ky == gravity:
        self.climbing = True
    else:
        self.climbing = False

    self.falling = False

    self.dx += kx
    float lr = self.dx > 0 ? 1 : self.dx < 0 ? -1 : 0
    float xa = fabs(self.dx)
    float ud = self.dy > 0 ? 1 : self.dy < 0 ? -1 : 0
    float ya = fabs(self.dy)

    for int i in range(10):
        if xa > 0:
            if xa < 1:
                lr *= xa
            if not player_move(self, lr, 0):
                player_collide(self, lr, 0, who)
                self.dx = 0
            xa -= 1
        if ya > 0:
            if ya < 1:
                ud *= ya
            if ud * gravity > 0 and not self.climbing:
                if not player_fall(self, 0, ud):
                    player_collide(self, 0, ud, who)
                    self.dy = 0
                else:
                    self.falling = True
            else:
                if not player_move(self, 0, ud):
                    player_collide(self, 0, ud, who)
                    self.dy = 0
                    self.jump = 0
            ya -= 1

    self.dx *= 0.9
    if fabs(self.dx) < 0.1:
        self.dx = 0
    self.dy *= 0.9
    if fabs(self.dy) < 0.1:
        self.dy = 0
