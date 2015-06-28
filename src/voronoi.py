import main
static import rgba
static import perlin

class VoronoiXY:
    int x, y

class Voronoi:
    int *map
    float *distance
    int n
    VoronoiXY *xy
    int w
    int h
    float max_distance

static def wrap_distance(float x1, x2, wrap) -> float:
    """
    |x1    x2             |x1
    |x1              x2   |x1
    |x2              x1   |x2
    """
    float d = fabs(x2 - x1)
    float d2 = fabs(x1 + wrap - x2)
    if d2 < d: d = d2
    d2 = fabs(x2 + wrap - x1)
    if d2 < d: d = d2
    return d

static def get_closest(Voronoi *self, int x, y) -> int:
    int mi = -1
    int md = INT_MAX
    for int i in range(self.n):
        int dx = wrap_distance(self.xy[i].x, x, self.w)
        int dy = wrap_distance(self.xy[i].y, y, self.h)
        if dx * dx + dy * dy < md:
            mi = i
            md = dx * dx + dy * dy
    return mi

def voronoi_create(int w, h, n, float randomness) -> Voronoi*:
    Voronoi *self; land_alloc(self)
    self.w = w
    self.h = h
    self.map = land_calloc(w * h * sizeof *self.map)
    self.distance = land_calloc(w * h * sizeof *self.distance)
    self.n = n
    self.xy = land_calloc(n * sizeof *self.xy)
    self.max_distance = 0
    int *map2 = land_calloc(w * h * sizeof *map2)

    for int i in range(n):
        int x = land_rand(0, w - 1)
        int y = land_rand(0, h - 1)
        self.xy[i].x = x
        self.xy[i].y = y

    for int y in range(h):
        for int x in range(w):
            int i = get_closest(self, x, y)
            self.map[x + w * y] = i

    # distort a bit
    Perlin *perlin = perlin_create(w / 8, h / 8)
    for int y in range(h):
        for int x in range(w):
            float xd, yd
            perlin_displace(perlin, x / 8.0, y / 8.0, &xd, &yd)
            int dx = imod(x + xd * randomness, self.w)
            int dy = imod(y + yd * randomness, self.h)
            int i = self.map[dx + w * dy]
            map2[y * w + x] = i
    perlin_destroy(perlin)

    land_free(self.map)
    self.map = map2

    for int y in range(h):
        for int x in range(w):
            int i = self.map[x + self.w * y]
            int dx = wrap_distance(self.xy[i].x, x, self.w)
            int dy = wrap_distance(self.xy[i].y, y, self.h)
            float d = sqrt(dx * dx + dy * dy)
            self.distance[x + self.w * y] = d
            if d > self.max_distance:
                self.max_distance = d
    return self

def voronoi_destroy(Voronoi *self):
    land_free(self.map)
    land_free(self.distance)
    land_free(self.xy)
    land_free(self)

def voronoi_at(Voronoi *self, int x, y) -> float:
    float value = self.distance[x + self.w * y] / self.max_distance
    return value
