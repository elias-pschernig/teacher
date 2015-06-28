import main
static import bumpmap
static import rgba
import tile

static def lerp(float a, b, x) -> float:
    return a * (1 - x) + b * x

static uint8_t *base

static def create_frame(Tile *tile, int i):
    """
    0
    1 2 3
    4 5 6
    7 8 9
    """
    int w = tile.w
    int h = tile.h
    memmove(tile.rgba, base, tile.w * tile.h * 4)

    if i == 1 or i == 2 or i == 3 or i == 0:
        for int y in range(h):
            for int x in range(w):
                uint8_t *p = rgba_p(tile.rgba, x, y, w)
                float br = p[0] / 255.0
                float bg = p[1] / 255.0
                float bb = p[2] / 255.0
                float v = y * 1.0 / h

                float l = 1 - v * 5
                if l < 0:
                    l = 0
                l *= 0.2
                float e = v * 4 - 0.5
                if e < 0:
                    e = 0
                if e > 1:
                    e = 1
                rgba_color(lerp(0.1 + l, br, e), lerp(0.5 + l, bg, e),
                    lerp(0, bb, e), p)

        Bumpmap *bumpmap = bumpmap_create(w, h)
        bumpmap_perlin(bumpmap, 2.0, 16.0)
        bumpmap_light(bumpmap)
        Stencil *s = stencil_new(w, h)
        stencil_zigzag(s, 20, 60, 4)
        bumpmap_mul_tile(bumpmap, tile, s, 0.5, 1)
        bumpmap_destroy(bumpmap)
        stencil_destroy(s)

    Stencil *s = stencil_new(w, h)
    stencil_shave(s, i)
    tile_cut(tile, s)
    stencil_destroy(s)
    tile_make(tile)

def earth_create -> Tile*:
    int w = 128
    int h = 128
    Tile *tile = tile_create("earth", w, h)

    base = land_calloc(w * h * 4)

    tile_frames(tile, 10)
    tile_frame(tile)

    for int y in range(h):
        for int x in range(w):
            uint8_t *p = rgba_p(tile.rgba, x, y, w)
            rgba_color(0.5, 0.3, 0.1, p)

    Bumpmap *bumpmap = bumpmap_create(w, h)
    bumpmap_voronoi(bumpmap, w / 4, 5)
    bumpmap_outline(bumpmap)
    bumpmap_light(bumpmap)
    bumpmap_mul_tile(bumpmap, tile, None, 0.8, 1)
    bumpmap_destroy(bumpmap)

    memmove(base, tile.rgba, tile.w * tile.h * 4)

    for int i in range(0, tile.n):
        tile_frame(tile)
        create_frame(tile, i)
    
    return tile
