import main
static import game

class Camera:
    float x, y
    int w, h

def camera_new(int w, h) -> Camera*:
    Camera *self; land_alloc(self)
    self.w = w
    self.h = h
    return self

def camera_x(Camera *self, float px) -> float:
    Game *game = game_global()
    float x = px - self.x
    int mw = game.map->w * game.map->tw
    if x > mw / 2: x -= mw
    if x < -mw / 2: x += mw
    return x

def camera_y(Camera *self, float py) -> float:
    Game *game = game_global()
    float y = py - self.y
    int mh = game.map->h * game.map->th
    if y > mh / 2: y -= mh
    if y < -mh / 2: y += mh
    return y
