import perlin
static import rgba
import tile
import voronoi
import stencil

class Bumpmap:
    int w, h
    float *bumpmap
    float *lightmap

def bumpmap_create(int w, h) -> Bumpmap*:
    Bumpmap *self; land_alloc(self)
    self.w = w
    self.h = h
    self.bumpmap = land_calloc(w * h * sizeof *self.bumpmap)
    self.lightmap = land_calloc(w * h * sizeof *self.lightmap)
    return self

def bumpmap_light(Bumpmap *self):
    int w = self.w
    int h = self.h
    for int y in range(h):
        for int x in range(w):
            float a1 = rgba_get(self.bumpmap, x + 1, y, w, h)
            float a2 = rgba_get(self.bumpmap, x - 1, y, w, h)
            float a3 = rgba_get(self.bumpmap, x, y + 1, w, h)
            float a4 = rgba_get(self.bumpmap, x, y - 1, w, h)

            self.lightmap[x + y * w] = a2 + a4 - a1 - a3

def bumpmap_nolight(Bumpmap *self):
    int w = self.w
    int h = self.h
    for int y in range(h):
        for int x in range(w):

            self.lightmap[x + y * w] = rgba_get(self.bumpmap, x, y, w, h)

def bumpmap_outline(Bumpmap *self):
    int w = self.w
    int h = self.h
    for int y in range(h):
        for int x in range(w):

            float v = rgba_get(self.bumpmap, x, y, w, h)
            v = 1 - v * v
            self.bumpmap[x + y * w] = v

def bumpmap_sphere(Bumpmap *self, float cx, cy, r):
    int w = self.w
    int h = self.h
    for int y in range(h):
        for int x in range(w):
            float px = x - cx
            float py = y - cy
            float zz = r * r - px * px - py * py
            if zz < 0:
                continue
            float z = sqrt(zz)
            self.bumpmap[x + w * y] -= z

def bumpmap_perlin(Bumpmap *self, float xs, ys):
    int w = self.w
    int h = self.h
    Perlin *noise = perlin_create(w / xs, h / ys)
    for int y in range(h):
        for int x in range(w):
            self.bumpmap[x + w * y] = perlin_at(noise, x / xs, y / ys)
    perlin_destroy(noise)

def bumpmap_voronoi(Bumpmap *self, int n, float randomness):
    int w = self.w
    int h = self.h
    Voronoi *noise = voronoi_create(w, h, n, randomness)
    for int y in range(h):
        for int x in range(w):
            self.bumpmap[x + w * y] = voronoi_at(noise, x, y)
    voronoi_destroy(noise)

def bumpmap_mul_tile(Bumpmap *self, Tile *tile, Stencil *mask,
        float mul, add):
    int w = self.w
    int h = self.h
    for int y in range(h):
        for int x in range(w):
            float v = self.lightmap[x + w * y]
            if mask:
                v *= mask.mask[x + w * y]
            v *= mul
            v += add
            rgba_colormul(v, v, v, tile.rgba + (y * w + x) * 4)

def bumpmap_destroy(Bumpmap *self):
    land_free(self.bumpmap)
    land_free(self.lightmap)
    land_free(self)
