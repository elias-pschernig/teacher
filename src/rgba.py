import main

macro rgba_C(x):
    x <= 0 ? 0 : x >= 1 ? 255 : (int)(x * 256)

class State:
    uint8_t *p
    int l, h
    uint8_t r, g, b, a
    int x, y
    float scale

State state
static State pushed[8]
static int pushed_i

def rgba_push:
    pushed[pushed_i++] = state

def rgba_pop:
    state = pushed[--pushed_i]

def rgba_get(float *bumpmap, int x, y, w, h) -> float:
    return bumpmap[imod(x, w) + w * imod(y, h)]

def rgba_color(float r, g, b, uint8_t *p):
    p[0] = rgba_C(r)
    p[1] = rgba_C(g)
    p[2] = rgba_C(b)
    p[3] = 255

def rgba_p(uint8_t *p, int x, y, w) -> uint8_t*:
    return p + (y * w + x) * 4

def rgba_coloradd(float r, g, b, uint8_t *p):
    r += p[0] / 255.0
    p[0] = rgba_C(r)
    g += p[1] / 255.0
    p[1] = rgba_C(g)
    b += p[2] / 255.0
    p[2] = rgba_C(b)

def rgba_colormul(float r, g, b, uint8_t *p):
    r *= p[0] / 255.0
    p[0] = rgba_C(r)
    g *= p[1] / 255.0
    p[1] = rgba_C(g)
    b *= p[2] / 255.0
    p[2] = rgba_C(b)

def rgba_alpha(float a, uint8_t *p):
    float r = a * p[0] / 255.0
    p[0] = rgba_C(r)
    float g = a * p[1] / 255.0
    p[1] = rgba_C(g)
    float b = a * p[2] / 255.0
    p[2] = rgba_C(b)
    p[3] = rgba_C(a)

def rgba_start(uint8_t *p, int l, h):
    state.p = p
    state.l = l
    state.h = h
    state.scale = 1
    state.x = 0
    state.y = 0

def rgba_putpixel:
    if state.x < 0 or state.y < 0: return
    if state.x >= state.l or state.y >= state.h: return
    uint8_t *p = rgba_p(state.p, state.x, state.y, state.l)
    p[0] = state.r
    p[1] = state.g
    p[2] = state.b
    p[3] = state.a

def rgba_fill(int wi, lx, rx, hi):
    if hi == 0: return
    int ox = state.x
    int oy = state.y
    if hi < 0:
        hi = -hi
        state.y -= hi
    int y2 = state.y + hi - 1
    float wl = lx
    float wr = rx
    float h = hi
    float gl = wl / h
    float gr = wr / h
    float xl = ox + 0.5
    float xr = ox + wi - 1 + 0.5
    rgba_hline(wi)
    while state.y != y2:
        state.y++
        xl += gl
        xr += gr
        rgba_moveto(floor(xl), state.y)
        rgba_hline(floor(xr) - floor(xl) + 1)
    state.x = ox
    state.y = oy

def rgba_moveto(int x, y):
    state.x = x
    state.y = y

def rgba_scale(float s):
    state.scale = s

def rgba_moverel(int x, y):
    state.x += x
    state.y += y

def rgba_setcolor(float r, g, b):
    state.r = rgba_C(r)
    state.g = rgba_C(g)
    state.b = rgba_C(b)
    state.a = 255

def rgba_lineto(int x, y):
    """
      0 1 2 3
    0 x x
    1     x x
    2
    3
    """
    float w = x - state.x
    float h = y - state.y
    if fabs(w) > fabs(h):
        float g = h / fabs(w)
        float yp = state.y + 0.5
        int d = state.x > x ? -1 : 1
        while state.x != x:
            state.x += d
            yp += g
            state.y = floor(yp)
            rgba_putpixel()
    else:
        float g = w / fabs(h)
        float xp = state.x + 0.5
        int d = state.y > y ? -1 : 1
        while state.y != y:
            state.y += d
            xp += g
            state.x = floor(xp)
            rgba_putpixel()

def rgba_hline(int w):
    if state.y >= state.h:
        return
    for int i in range(w):
        rgba_putpixel()
        rgba_moverel(1, 0)

def rgba_circle(int w, h):
    """
    w = 4
    cx = 2
    ww = 4
    i = 0 -> x = -1.5
    i = 1 -> x = -0.5
    i = 2 -> x = 0.5
    i = 3 -> x = 1.5
    i = 4 -> x = 2.5
    01234
    xxxx
    xxxx
    xxxx
    """
    int ox = state.x
    int oy = state.y
    float cx = w * 0.5
    float cy = h * 0.5
    float ww = w * w / 4.0
    float hh = h * h / 4.0
    for int j in range(h):
        for int i in range(w):
            float x = i + 0.5 - cx
            float y = j + 0.5 - cy
            if x * x / ww + y * y / hh < 1.0:
                rgba_moveto(ox + i, oy + j)
                rgba_putpixel()
    state.x = ox
    state.y = oy

def rgba_arc(int w, h, float a1, a2):
    """
    0° = up
    90° = right

    cos 0° -> 1, cos 90° -> 0
    sin 0° -> 0, sin 90° -> 1

    w = 4
    x = 0
        left = 0.5
        right = 3.5
        cx = 2.0
        r = 1.5 
    0 1 2 3 4 5
     x x x x
    
    """
    int ox = state.x
    int oy = state.y
    int n = (w + h) / 2.0 * (a2 - a1) / 4.0
    if n < 2:
        n = 2
    float cx = ox + w * 0.5
    float cy = oy + h * 0.5
    float rx = (w - 1) * 0.5
    float ry = (h - 1) * 0.5
    for int i in range(0, n + 1):
        float a = a1 + (a2 - a1) * i / n
        float x = sin(a) * rx
        float y = cos(a) * -ry
        if i == 0:
            rgba_moveto(floor(cx + x), floor(cy + y))
        else:
            rgba_lineto(floor(cx + x), floor(cy + y))
    state.x = ox
    state.y = oy
