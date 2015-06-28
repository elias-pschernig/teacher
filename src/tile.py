import main
import stencil
import rgba

class Tile:
    int id
    uint8_t *rgba
    LandImage *pic
    int n, i
    LandImage **frames
    int w, h
    bool climb with 1
    int border
    int tall
    bool female
    LandColor color

static int next_id = 1
static LandHash *by_name
static LandArray *by_id

def tile_by_name(char const *name) -> int:
    Tile *t = land_hash_get(by_name, name)
    if t: return t.id
    return 0

def tile_make(Tile *self):
    land_image_set_rgba_data(self.pic, self.rgba)
    land_free(self.rgba)
    if self.n and self.i < self.n:
        self.frames[self.i++] = self.pic
    self.rgba = None

def tile_frame(Tile *self):
    if not self.rgba:
        self.pic = land_image_new(self.w, self.h)
        self.rgba = land_calloc(self.w * self.h * 4)

def tile_by_id(int id) -> Tile*:
    Tile *t = land_array_get_nth(by_id, id)
    return t

def tile_create(char const *name, int w, h) -> Tile*:
    if not by_name:
        by_name = land_hash_new()
        by_id = land_array_new()
        land_array_add(by_id, None)
            
    int id = tile_by_name(name)
    Tile *self = tile_by_id(id)
    if not self:
        land_alloc(self)
        self.id = next_id++
        land_hash_insert(by_name, name, self)
        land_array_add(by_id, self)
    self.w = w
    self.h = h
    self.i = 0
    tile_frame(self)
    return self

def tile_frames(Tile *self, int n):
    self.n = n
    self.frames = land_calloc(n * sizeof *self.frames)

def tile_paste(Tile *self, char const *name):
    int tid = tile_by_name(name)
    Tile *from = tile_by_id(tid)
    if not from:
        return
    memmove(self.rgba, from.rgba, self.w * self.h * 4)

def tile_cut(Tile *self, Stencil *stencil):
    int w = self.w
    int h = self.h
    for int y in range(h):
        for int x in range(w):
            uint8_t *p = rgba_p(self.rgba, x, y, w)
            float a = stencil.mask[x + stencil.w * y]
            rgba_alpha(a, p)

macro M(x, y) ((m & (x)) == (y))

def tile_render(Tile *self, float x, y, int m):
    """
    
    01 02 04
    08    10
    20 40 80 

    0
    1 2 3
    4 5 6
    7 8 9

    x x x
    x x x x x x
    x x x x x x
    x x x x x x
    """
    if not self.frames:
        land_image_draw(self.pic, x, y)
        return
    int f = 0
    if   M(0x5a, 0x00): f = 0
    elif M(0x0a, 0x00): f = 1
    elif M(0x12, 0x00): f = 3
    elif M(0x48, 0x00): f = 7
    elif M(0x50, 0x00): f = 9
    elif M(0x02, 0x00): f = 2
    elif M(0x08, 0x00): f = 4
    elif M(0x10, 0x00): f = 6
    elif M(0x40, 0x00): f = 8
    elif M(0x5a, 0x5a): f = 5
    land_image_draw(self.frames[f], x, y)
