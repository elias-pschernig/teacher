import common

static import game

def imod(int x, d) -> int:
    x %= d
    if x < 0: x += d
    return x

def idiv(int x, d) -> int:
    if x < 0:
        x -= d - 1
    x /= d
    return x

def ffmod(float x, d) -> float:
    x = fmod(x, d)
    if x < 0: x += d
    return x

def realmain():
    land_init()
    land_set_display_parameters(1280, 720, LAND_WINDOWED | LAND_OPENGL)
    land_set_initial_runner(game_runner())
    land_mainloop()

land_use_main(realmain)
