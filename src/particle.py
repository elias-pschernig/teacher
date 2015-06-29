import game
import tile

class Particle:
    Tile *t
    float x, y, dx, dy, ax, ay
    int end_time
    float angle
    bool add

static Particle particles[1024]
static int particle_n

def particle_smoke(float x, y, int n):
    for int jn in range(n):
        int i = particle_n
        Particle *p = particles + i
        particle_n++
        particle_n &= 1023
        p.x = x
        p.y = y
        p.t = tile_by_id(tile_by_name("cloud"))
        p.end_time = game_global()->time + 120
        float a = land_rnd(0, 2 * pi)
        p.dx = cos(a) * 5
        p.dy = sin(a) * 2
        p.ax = 0
        p.ay = 0
        p.angle = 0
        p.add = False

def particle_sparkle(float x, y, int n):
    for int jn in range(n):
        int i = particle_n
        Particle *p = particles + i
        particle_n++
        particle_n &= 1023
        p.x = x
        p.y = y
        p.t = tile_by_id(tile_by_name("sparkle"))
        p.end_time = game_global()->time + 120
        p.dx = land_rnd(-2, 2)
        p.dy = -5
        p.ax = 0
        p.ay = 0.1
        p.angle = land_rnd(0, 2 * pi)
        p.add = True

def particle_tear(float x, y, int dx, dy, float ay):
    for int jn in range(1):
        int i = particle_n
        Particle *p = particles + i
        particle_n++
        particle_n &= 1023
        p.x = x
        p.y = y
        p.t = tile_by_id(tile_by_name("tear"))
        p.end_time = game_global()->time + 90
        p.dx = dx
        p.dy = dy
        p.ax = 0
        p.ay = ay
        p.angle = 0
        p.add = True


def particle_draw_all(Camera *cam):
    
    Game *game = game_global()
    for int i in range(1024):
        Particle *p = particles + i
        if game.time > p.end_time:
            continue
        float x = camera_x(game.camera, p.x)
        float y = camera_y(game.camera, p.y)
        float a = (p.end_time - game.time) / 60.0
        if a > 1:
            a = 1
        if p.add: land_blend(LAND_BLEND_ADD)
        else: land_blend(LAND_BLEND_TINT)
        land_image_draw_rotated_tinted(p.t->pic, x - p.t->w / 2,
            y - p.t->h / 2, p.angle, a, a, a, a)
    land_blend(LAND_BLEND_TINT)

def particle_move_all:
    Game *game = game_global()
    for int i in range(1024):
        Particle *p = particles + i
        if game.time > p.end_time:
            continue
        p.x += p.dx
        p.y += p.dy
        p.dx += p.ax
        p.dy += p.ay
