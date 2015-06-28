import main
static import bumpmap
static import rgba
import tile

def brick_create(char const *name, int bw, bh, float red, green, blue) -> Tile*:
    int w = 128
    int h = 128
    Tile *tile = tile_create(name, w, h)

    for int y in range(h):
        for int x in range(w):
            uint8_t *p = rgba_p(tile.rgba, x, y, w)
            int bx, by
            by = y % bh
            bx = x
            if y / bh % 2:
                bx += bw / 2
            bx %= bw
            if by == 0 or bx == 0:
                rgba_color(0.7, 0.7, 0.6, p)
            elif by == bh - 1 or bx == bw - 1:
                rgba_color(0.3, 0.3, 0.2, p)
            elif bx <= 2 or by <= 2 or bx >= bw - 3 or by >= bh - 3:
                rgba_color(0.5, 0.5, 0.5, p)
            else:
                rgba_color(red, green, blue, p)

    Bumpmap *bumpmap = bumpmap_create(w, h)
    bumpmap_perlin(bumpmap, 4.0, 4.0)
    bumpmap_light(bumpmap)
    bumpmap_mul_tile(bumpmap, tile, None, 0.25, 1)
    bumpmap_destroy(bumpmap)

    land_image_set_rgba_data(tile.pic, tile.rgba)
    land_free(tile.rgba)

    tile.climb = True
    return tile

def brick_orange_create -> Tile*:
    return brick_create("brick", 64, 32, 1, 0.6, 0.2)

def brick_white_create -> Tile*:
    return brick_create("brick2", 128, 64, 0.9, 0.8, 0.8)
