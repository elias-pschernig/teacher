import main
import camera
static import game
import tile

class Map:
    int w, h
    int tw, th
    int *tiles
    int *crowded
    int start_x, start_y
    bool uptodate
    int update_time

static int brick
static int brick2
static int earth
static int ladder

def map_create(int w, h, tw, th) -> Map*:
    Map *self; land_alloc(self)
    self.w = w
    self.h = h
    self.tw = tw
    self.th = th
    self.tiles = land_calloc(w * h * sizeof *self.tiles)
    self.crowded = land_calloc(w * h * sizeof *self.crowded)
    return self

def map_tx(float x) -> int:
    Map *map = game_global()->map
    return imod(floor(x / map.tw), map.w)

def map_ty(float y) -> int:
    Map *map = game_global()->map
    return imod(floor(y / map.th), map.h)

def map_get(Map *self, int x, y) -> int:
    return self.tiles[imod(x, self.w) + self.w * imod(y, self.h)]

def map_put(Map *self, int x, y, t):
    self.tiles[imod(x, self.w) + self.w * imod(y, self.h)] = t
    self.uptodate = False

macro CROWDED self->crowded[imod(map_tx(x), self->w) + self->w * imod(map_ty(y), self->h)]

def map_crowd(Map *self, float x, y):
    CROWDED++

def map_uncrowd(Map *self, float x, y):
    CROWDED--

def map_crowded(Map *self, float x, y) -> int:
    return CROWDED

static def hole(Map *self, int x, y):
    for int j in range(-1, 2):
        for int i in range(-1, 2):
            if map_get(self, x + i, y + j) == earth:
                map_put(self, x + i, y + j, 0)

def map_generate(Map *self):
    brick = tile_by_name("brick")
    brick2 = tile_by_name("brick2")
    earth = tile_by_name("earth")
    ladder = tile_by_name("ladder")

    for int y in range(self.h):
        for int x in range(self.w):
            map_put(self, x, y, earth)

    self.start_x = self.w / 2
    self.start_y = self.h / 2
    int x = self.start_x
    int y = self.start_y
    int dx[] = {1, 0, -1, 0, 1, -1}
    int dy[] = {0, 1, 0, -1, 0, 0}

    for int u in range(30):
        for int t in range(30):
            hole(self, x, y)
            int d = land_rand(0, 5)
            x = imod(x + dx[d] * 3, self.w)
            y = imod(y + dy[d] * 3, self.h)
        hole(self, x, y)
        for int t in range(10):
            y++
            for int i in range(-1, 2):
                map_put(self, x + i, y, ladder)

    x = self.start_x
    y = self.start_y
    for int j in range(6 + 6):
        for int i in range(5 + 3):
            map_put(self, x + i - 3, y + j - 5,
                j < 3 ? brick2 : brick)

def map_render(Map *self, Camera *cam):
    """
                cam.x = 23.5
                |
0     10     20     30     40     50

tx = floor(23.5 / 10) = 2
sx = 2 * 10 - 23.5 = -3.5
"""
    int tx = floor(cam.x / self.tw)
    int ty = floor(cam.y / self.th)
    float sx = tx * self.tw - cam.x
    float sy = ty * self.th - cam.y

    while sy < cam.h:
        float lx = sx
        int ltx = tx
        while sx < cam.w:
            int cc = map_get(self, tx, ty)
            int m = 0
            int b = 1
            for int j in range(3):
                for int i in range(3):
                    if i == 1 and j == 1:
                        continue
                    int c = map_get(self, tx - 1 + i, ty - 1 + j)
                    if c == cc:
                        m += b
                    b *= 2
            Tile *t = tile_by_id(cc)
            if t:
                tile_render(t, sx, sy, m)
            int c = map_crowded(self, tx * self.tw, ty * self.th)
            if c != 0:
                land_font_set(game_global()->small)
                land_color(1, 1, 1, 1)
                land_text_pos(sx, sy)
                #land_print("%d", c)
            tx++
            sx += self.tw
        sx = lx
        tx = ltx
        ty++
        sy += self.th

def map_update_overview_tile(Map *map, Tile *tile):
    if map.uptodate:
        return
    if game_global()->time - map.update_time < 60:
        return
    int w = tile.w
    int h = tile.h

    for int y in range(h):
        for int x in range(w):
            uint8_t *p = rgba_p(tile.rgba, x, y, w)
            int tid = map_get(map, x, y)
            if tid == brick: rgba_color(1, 0.7, 0.4, p)
            elif tid == brick2: rgba_color(1, 1, 1, p)
            elif tid == earth:
                int tid2 = map_get(map, x, y - 1)
                if tid2 == 0: rgba_color(0, 1, 0, p)
                else: rgba_color(0.8, 0.5, 0.4, p)
            elif tid == ladder: rgba_color(0.8, 0.7, 0, p)
            else: rgba_color(0, 0, 0, p)

    land_image_set_rgba_data(tile.pic, tile.rgba)
    map.uptodate = True
    map.update_time = game_global()->time
    #land_free(tile.rgba)

def map_create_overview_tile(Map *map) -> Tile*:
    Tile *tile = tile_create("map", map.w, map.h)
    map_update_overview_tile(map, tile)

    return tile
