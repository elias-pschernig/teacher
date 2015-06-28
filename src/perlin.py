import main
static import rgba

class Perlin:
    float *x
    float *y
    int w
    int h

static def cosine_lerp(float a0, a1, w) -> float:
    float ft = w * LAND_PI
    float f = (1 - cos(ft)) * 0.5
    return  a0 * (1 - f) + a1 * f

def perlin_create(int w, h) -> Perlin*:
    Perlin *self; land_alloc(self)
    self.w = w
    self.h = h
    self.x = land_calloc(w * h * sizeof *self.x)
    self.y = land_calloc(w * h * sizeof *self.y)
    for int j in range(h):
        for int i in range(w):
            float a = land_rnd(0, LAND_PI * 2)
            self.x[i + j * w] = cos(a)
            self.y[i + j * w] = sin(a)
    return self

def perlin_destroy(Perlin *self):
    land_free(self.x)
    land_free(self.y)
    land_free(self)

static def gradient_x(Perlin *self, int x, y) -> float:
    x %= self.w
    if x < 0: x += self.w
    y %= self.h
    if y < 0: y += self.h
    return self.x[x + y * self.w]

static def gradient_y(Perlin *self, int x, y) -> float:
    x %= self.w
    if x < 0: x += self.w
    y %= self.h
    if y < 0: y += self.h
    return self.y[x + y * self.w]

static def dot(Perlin *self, int ix, iy, float x, y) -> float:
     float dx = x - ix
     float dy = y - iy
 
     return dx * gradient_x(self, ix, iy) + dy * gradient_y(self, ix, iy)
 
def perlin_at(Perlin *self, float x, y) -> float:
     int x0 = floor(x)
     int x1 = x0 + 1
     int y0 = floor(y)
     int y1 = y0 + 1
     float sx = x - x0
     float sy = y - y0

     float n0, n1, ix0, ix1, value
     n0 = dot(self, x0, y0, x, y)
     n1 = dot(self, x1, y0, x, y)
     ix0 = cosine_lerp(n0, n1, sx)
     n0 = dot(self, x0, y1, x, y)
     n1 = dot(self, x1, y1, x, y)
     ix1 = cosine_lerp(n0, n1, sx)
     value = cosine_lerp(ix0, ix1, sy)

     return value

def perlin_displace(Perlin *self, float x, y, *xd, *yd):
     int x0 = floor(x)
     int x1 = x0 + 1
     int y0 = floor(y)
     int y1 = y0 + 1
     float sx = x - x0
     float sy = y - y0

     float n0, n1, ix0, ix1
     n0 = gradient_x(self, x0, y0)
     n1 = gradient_x(self, x1, y0)
     ix0 = cosine_lerp(n0, n1, sx)
     n0 = gradient_x(self, x0, y1)
     n1 = gradient_x(self, x1, y1)
     ix1 = cosine_lerp(n0, n1, sx)
     *xd = cosine_lerp(ix0, ix1, sy)

     n0 = gradient_y(self, x0, y0)
     n1 = gradient_y(self, x1, y0)
     ix0 = cosine_lerp(n0, n1, sx)
     n0 = gradient_y(self, x0, y1)
     n1 = gradient_y(self, x1, y1)
     ix1 = cosine_lerp(n0, n1, sx)
     *yd = cosine_lerp(ix0, ix1, sy)
