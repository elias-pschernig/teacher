import main
static import rgba
import tile

class Parameters:
    float radius
    float hairlength
    float hairg
    float forehead
    float jaw
    float chin
    float headw
    float foreheadg
    float jawg
    float ching
    float hairtop
    float eyedistance
    float clothg
    LandColor color
    LandColor haircolor
    LandColor skincolor

def parameters_new -> Parameters*:
    Parameters *self; land_alloc(self)
    self.radius = 50
    self.hairlength = 1.25
    self.forehead = 0.7
    self.jaw = 0.5
    self.chin = 0.56
    self.headw = 0.8
    self.foreheadg = 1.48
    self.jawg = -0.5
    self.ching = -2.85
    self.hairtop = 0.4
    self.hairg = 0
    self.eyedistance = 0.4
    self.clothg = -0.78
    self.color = land_color_rgba(1, .2, .3, 1)
    self.haircolor = land_color_rgba(0.5, 0.3, 0.1, 1)
    self.skincolor = land_color_rgba(1, 0.8, 0.7, 1)
    return self

static def create_frame(Tile *tile, Parameters *pams, int frame):
    int w = tile.w
    int hairw = pams.radius * 2
    int top = pams.radius * pams.hairtop
    int fw1 = pams.radius * pams.headw
    int fa2 = pams.radius * pams.headw * tan(pams.foreheadg * LAND_PI / 10)
    int fa3 = pams.radius * pams.jaw * tan(pams.jawg * LAND_PI / 10)
    int fa4 = pams.radius * pams.chin * tan(pams.ching * LAND_PI / 10)
    int fh1 = pams.radius * pams.forehead
    int fh2 = pams.radius * pams.jaw
    int fh3 = pams.radius * pams.chin

    tile.color = pams.color

    int body_radius = pams.radius * 4 / 5
    int body_height = body_radius * 3.0 / 4
    int leg_height = pams.radius * 30 / 50
    int head = fh1 + fh2 + fh3 + 5

    tile.border = (w - hairw) / 2
    tile.tall = top + head + body_height + leg_height + 6

    rgba_start(tile.rgba, tile.w, tile.h)

    #rgba_setcolor(0, 0, 1)
    #rgba_fill(tile.w, 0, 0, tile.w)

    rgba_moveto((w - hairw) / 2, tile.h - top - head - body_height - leg_height - 6)

    # hair
    rgba_push()
    rgba_setcolor(pams.haircolor.r, pams.haircolor.g, pams.haircolor.b)
    rgba_circle(hairw, hairw)
    rgba_moverel(0, hairw / 2)
    int hl = pams.hairlength * pams.radius
    int ha = pams.radius * pams.hairlength * tan(pams.hairg * LAND_PI / 10)
    if frame == 5:
        rgba_moverel(-ha, -hl)
        rgba_fill(hairw + ha * 2, ha, -ha, hl)
    else:
        rgba_fill(hairw, -ha, ha, hl)
    rgba_pop()

    rgba_moverel(hairw / 2, top)

    # face
    rgba_push()
    rgba_setcolor(pams.skincolor.r, pams.skincolor.g, pams.skincolor.b)
    rgba_moverel(fw1 / -2, 0)
    rgba_fill(fw1, -fa2, fa2, fh1)
    rgba_moverel(-fa2, fh1)
    int topjaw = fw1 + fa2 * 2
    if topjaw + fa3 * 2 < 5:
        fa3 = (5 - topjaw) / 2
    rgba_fill(topjaw, -fa3, fa3, fh2)
    rgba_moverel(-fa3, fh2)
    int topchin = fw1 + fa2 * 2 + fa3 * 2
    if topchin + fa4 * 2 < 0:
        fa4 = -topchin / 2
    rgba_fill(topchin, -fa4, fa4, fh3)
    rgba_pop()

    # 012345678901234
    # ..____..____..
    # ..|  |..|  |..
    # ..|__|..|__|..
    #
    rgba_push()
    rgba_moverel(0, pams.radius * 0.6)
    # left/right eye
    for int i in range(2):
        int ex = (i * 2 - 1) * pams.radius * pams.eyedistance
        int eh = 13
        if frame == 6:
            eh = 4
        rgba_push()
        rgba_moverel(ex - 10, 0)
        rgba_setcolor(0, 0, 0)
        rgba_circle(20, 17)
        rgba_push()
        rgba_moverel(0, 16 - eh)
        rgba_setcolor(1, 1, 1)
        rgba_circle(20, eh)
        rgba_pop()
        rgba_setcolor(0, 0, 0)
        rgba_moverel(6, 6)
        rgba_circle(8, 8)
        rgba_moverel(pams.radius * -6.0 / 50, -3 - 7)
        rgba_hline(pams.radius * 0.4)
        rgba_pop()
    rgba_pop()

    # nose
    rgba_push()
    rgba_setcolor(0, 0, 0)
    rgba_moverel(-4, fh1 + fh2 - 1)
    rgba_putpixel()
    rgba_moverel(7, 0)
    rgba_putpixel()
    rgba_pop()

    # mouth
    rgba_push()
    rgba_setcolor(0, 0, 0)
    rgba_moverel(-10, fh1 + fh2 - 5)
    if frame == 6:
        rgba_moverel(0, 10)
        rgba_arc(20, 20, pi * 1.5, pi * 2.5)
    else:
        rgba_arc(20, 20, pi / 2, pi * 1.5)
    rgba_pop()

    rgba_setcolor(pams.color.r, pams.color.g, pams.color.b)
    # body

    rgba_push()
    rgba_moverel(0, head)
    rgba_moverel(-body_radius / 2, 0)
    rgba_circle(body_radius, body_radius)
    rgba_moverel(0, body_radius / 2)
    #-5 = 20 * tan(x * pi / 10)
    int ba = body_radius / 2 * tan(pams.clothg * LAND_PI / 10)
    rgba_fill(body_radius, ba, -ba, body_radius / 2)
    rgba_pop()

    # neck
    rgba_push()
    rgba_moverel(0, head - pams.radius / 5)
    rgba_moverel(pams.radius * -11.0 / 50, 0)
    rgba_fill(pams.radius * 22.0 / 50, 3, -3, pams.radius * 15 / 50)
    rgba_pop()

    # legs
    for int i in range(2):
        rgba_push()
        int ex = (i * 2 - 1)
        rgba_moverel(ex * pams.radius * 17 / 50 - pams.radius / 10, head + body_height)
        int f2 = frame - 2
        if frame == 5 or frame == 6:
            f2 = 3
        else:
            f2 *= ex
        rgba_fill(pams.radius / 5, 0, 0, leg_height + f2 * 2)
        rgba_pop()

    # arms
    for int i in range(2):
        int ex = (i * 2 - 1)
        rgba_push()
        rgba_moverel(ex * pams.radius / 5, head + 5)
        rgba_moverel((i - 1) * leg_height, 0)
        rgba_fill(leg_height, 0, 0, pams.radius / 5)
        rgba_pop()

    tile_make(tile)

def girl_create(Parameters *parameters) -> Tile*:
    Tile *tile = tile_create("girl", 128, 256)
    tile_frames(tile, 6)
    for int i in range(tile.n):
        tile_frame(tile)
        create_frame(tile, parameters, i)
    return tile

static def param(float *x, minv, maxv, step):
    *x = land_rnd(minv, maxv)

def girl_create_kid(int kid) -> Tile*:
    char name[100]
    sprintf(name, "kid%d", kid)
    Tile *tile = tile_create(name, 128, 256)

    Parameters *pams = parameters_new()
    param(&pams.hairlength, 0, 2, 0.1)
    param(&pams.hairg, -1, 1, 0.1)
    param(&pams.hairtop, 0.2, 0.8, 0.1)
    param(&pams.eyedistance, 0.4, 0.5, 0.05)
    param(&pams.headw, 0.5, 1.2, 0.1)
    param(&pams.radius, 30, 40, 1)
    param(&pams.forehead, 0.3, 1, 0.01)
    param(&pams.jaw, 0.3, 1, 0.01)
    param(&pams.chin, 0.3, 1, 0.01)
    param(&pams.foreheadg, 0.2, 1, 0.1)
    param(&pams.jawg, -1, 1, 0.1)
    param(&pams.ching, -3, 1, 0.1)

    tile.female = pams.hairlength > 1
    if tile.female:
        param(&pams.clothg, -1, 0, 0.1)
    else:
        pams.clothg = 0

    if tile.female:
        pams.color = land_color_hsv(land_rnd(0, 360), 1, 1)
    else:
        pams.color = land_color_hsv(land_rnd(0, 270), land_rnd(0, 1), 1)
    pams.haircolor = land_color_hsv(land_rnd(0, 45), land_rnd(0.5, 1),
        land_rnd(0, 1))

    int s = land_rand(0, 3)
    if s == 0:
        pams.skincolor = land_color_rgba(0.5, 0.2, 0.1, 1)
    else:
        pams.skincolor = land_color_rgba(1, 0.8, 0.7, 1)

    tile_frames(tile, 7)
    for int i in range(tile.n):
        tile_frame(tile)
        create_frame(tile, pams, i)
    return tile

