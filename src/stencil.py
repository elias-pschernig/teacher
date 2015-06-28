import common

class Stencil:
    int w, h
    float *mask

def stencil_new(int w, h) -> Stencil*:
    Stencil *self; land_alloc(self)
    self.w = w
    self.h = h
    self.mask = land_calloc(w * h * sizeof *self.mask)
    return self

def stencil_destroy(Stencil *self):
    land_free(self.mask)
    land_free(self)

def stencil_shave(Stencil *self, int f):
    """
    0
    1 2 3
    4 5 6
    7 8 9
    """
    for int y in range(self.h):
        for int x in range(self.w):
            float *p = self.mask + x + self.w * y
            float v2 = 1
            if f == 1 or f == 4 or f == 7 or f == 0:
                float v = x * 1.0 / self.w
                v *= 10
                v += 0.5 * sin(y * 2 * LAND_PI / self.h * 4.0)
                if v > 1: v = 1
                v2 *= v
            if f == 3 or f == 6 or f == 9 or f == 0:
                float v = 1.0 - x * 1.0 / self.w
                v *= 10
                v += 0.5 * sin(y * 2 * LAND_PI / self.h * 4.0)
                if v > 1: v = 1
                v2 *= v
            if f == 7 or f == 8 or f == 9 or f == 0:
                float v = 1.0 - y * 1.0 / self.h
                v *= 3 
                v += -0.5 + 0.5 * pow(sin(x * 2 * LAND_PI / self.w + LAND_PI / 2), 2)
                if v > 1: v = 1
                v2 *= v
            if f == 1 or f == 2 or f == 3 or f == 0:
                float v = y * 1.0 / self.h
                v *= 20
                v += 0.2 * sin(x * 2 * LAND_PI / self.w * 4.0)
                if v > 1: v = 1
                v2 *= v
            if v2 < 0: v2 = 0
            if v2 > 1: v2 = 1
            *p = v2

def stencil_zigzag(Stencil *self, int y0, y1, n):
    """
    \   \
     \   \
      \   \
       \   \

    \  /\  /
     \/  \/
    """
    float zw = self.w / n
    for int y in range(self.h):
        for int x in range(self.w):
            float *p = self.mask + x + self.w * y
            float z = fmod(x, zw)
            if z > zw / 2:
                z = zw - z
            int zy = y0 + z * (y1 - y0) * 2 / zw
            float v = y > zy ? 0 : 1
            *p = v
