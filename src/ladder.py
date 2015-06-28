import main
static import bumpmap
static import rgba
import tile

def ladder_create -> Tile*:
    int w = 128
    int h = 128
    Tile *tile = tile_create("ladder", w, h)

    for int x in range(20):
        for int y in range(h):
            uint8_t *p = rgba_p(tile.rgba, x, y, w)
            float red = 1 - x / 40.0
            float green = 0.9 - x / 40.0
            float blue = 0
            rgba_color(red, green, blue, p + 28 * 4)
            rgba_color(red, green, blue, p + 80 * 4)

    for int y in range(10):
        for int x in range(w):
            uint8_t *p = rgba_p(tile.rgba, x, y + 10, w)
            float red = 1 - y / 20.0
            float green = 0.9 - y / 20.0
            float blue = 0
            for int i in range(8):
                rgba_color(red, green, blue, p + 4 * w * i * 32)

    Bumpmap *bumpmap = bumpmap_create(w, h)
    bumpmap_perlin(bumpmap, 2.0, 8.0)
    bumpmap_light(bumpmap)
    bumpmap_mul_tile(bumpmap, tile, None, 0.1, 1)
    bumpmap_destroy(bumpmap)

    land_image_set_rgba_data(tile.pic, tile.rgba)
    land_free(tile.rgba)

    tile.climb = True
    return tile



