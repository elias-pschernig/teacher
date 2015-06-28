import main
static import rgba
import tile
static import bumpmap

static def create_frame(Tile *tile, int frame):
    int w = tile.w
    int h = tile.h

    rgba_start(tile.rgba, tile.w, tile.h)

    float r = 108
    float cx = w / 2
    float cy = h / 2

    rgba_moveto(cx - r, cy - r)
    rgba_setcolor(0.1, 0.1, 0.8)
    rgba_circle(r * 2, r * 2)

    Bumpmap *bumpmap = bumpmap_create(w, h)
    bumpmap_perlin(bumpmap, 16.0, 16.0)
    bumpmap_sphere(bumpmap, cx, cy, r)
    bumpmap_light(bumpmap)
    bumpmap_mul_tile(bumpmap, tile, None, 0.2, 1)
    bumpmap_destroy(bumpmap)

    for int i in range(90):
        float a = 2 * pi * i / 90.0
        float x = cos(a) * (r + 10)
        float y = sin(a) * (r + 10)
        rgba_moveto(cx + x - 10, cy + y - 10)
        #if a < pi * 0.5 or a > pi * 1.5: a -= pi * 0.5
        #else: a += pi * 0.5
        if x > 15: a -= 0.5 * pi
        elif x < -15: a += 0.5 * pi
        else: continue
        rgba_setcolor(0, 0, 1)
        rgba_arc(20, 20, a, a + pi)
        rgba_setcolor(0.1, 0.1, 1)
        rgba_moverel(0, -1)
        rgba_arc(20, 20, a, a + pi)
        rgba_setcolor(0.2, 0.2, 1)
        rgba_moverel(0, -1)
        rgba_arc(20, 20, a, a + pi)

    for int i in range(2):
        rgba_setcolor(1, 1, 0)
        rgba_moveto(cx + (i * 2 - 1) * 60, cy)
        rgba_moverel(-30, -30 )
        rgba_moverel(0, frame - 2)
        rgba_circle(60, 60)
        rgba_setcolor(0, 0, 0)
        rgba_moverel(30 - 25, 30 - 15)
        rgba_circle(50, 30)

    tile.border = 70
    tile_make(tile)

def monster_create -> Tile*:
    Tile *tile = tile_create("monster", 256, 256)
    tile_frames(tile, 7)
    for int i in range(tile.n):
        tile_frame(tile)
        create_frame(tile, i)
    return tile
