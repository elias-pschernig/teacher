import main
static import bumpmap
static import rgba
import tile

def cloud_create -> Tile*:
    int w = 128
    int h = 128
    Tile *tile = tile_create("cloud", w, h)

    for int y in range(h):
        for int x in range(w):
            uint8_t *p = rgba_p(tile.rgba, x, y, w)
            float dx = w / 2 - (x + 0.5)
            float dy = h / 2 - (y + 0.5)
            float d = sqrt(dx * dx + dy * dy) / (w / 2)
            d *= 0.2
            float v = 0.2 - d
            if v < 0:
                v = 0
            rgba_color(1, 1, 1, p)
            rgba_alpha(v, p)

    land_image_set_rgba_data(tile.pic, tile.rgba)
    land_free(tile.rgba)

    return tile


def sparkle_create -> Tile*:
    int w = 32
    int h = 32
    Tile *tile = tile_create("sparkle", w, h)

    for int y in range(h):
        for int x in range(w):
            uint8_t *p = rgba_p(tile.rgba, x, y, w)
            float dx = w / 2 - (x + 0.5)
            float dy = h / 2 - (y + 0.5)
            float d = sqrt(dx * dx + dy * dy) / (w / 2)
            float a = atan2(dy, dx)
            float star = sin(a * 6) + 1
            float v = 1 - d - star
            if v < 0:
                v = 0
            rgba_color(1, 1, 1, p)
            rgba_alpha(v, p)

    land_image_set_rgba_data(tile.pic, tile.rgba)
    land_free(tile.rgba)

    return tile

def tear_create -> Tile*:
    int w = 32
    int h = 32
    Tile *tile = tile_create("tear", w, h)

    for int y in range(h):
        for int x in range(w):
            uint8_t *p = rgba_p(tile.rgba, x, y, w)
            float dx = w / 2 - (x + 0.5)
            float dy = h / 2 - (y + 0.5)
            float d = sqrt(dx * dx + dy * dy) / (w / 2)
            float v = 1 - d * d * d * d
            if v < 0:
                v = 0
            rgba_color(0.5, 0.7, 1, p)
            rgba_alpha(v, p)

    land_image_set_rgba_data(tile.pic, tile.rgba)
    land_free(tile.rgba)

    return tile

