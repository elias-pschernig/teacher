import land.land

macro float LandFloat
macro pi LAND_PI

def print(char const *str, ...):
    va_list args
    va_start(args, str)
    vprintf(str, args)
    va_end(args)
    printf("\n")
