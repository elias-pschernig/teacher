import main
import map
import camera
import player
static import names
static import brick
static import earth
static import monster
static import ladder
static import cloud
static import music
import particle
import girl
static LandRunner *_runner
static import ctype
static import title

class Game:
    Map *map
    Camera *camera
    Player *player
    Player *monster

    Parameters *pams

    int kids_count
    Player **kids

    int time

    char *command
    int letter_time
    int command_time

    LandFont *small
    LandFont *large

    Tile *brick
    Tile *ladder
    Tile *earth

    Tile *overview
    int lx, ly

    int inclass

    LandSound *ring
    LandSound *ding
    LandSound *knock 
    LandSound *toc
    LandSound *classroom
    LandSound *laugh
    LandSound *cry

    bool music

    float noisy
    float noisy_time

    bool title
    bool won

static Game *game

def game_global -> Game*:
    return game

def start(int kids):
    map_generate(game.map)
    game.kids_count = kids
    game.kids = land_calloc(game.kids_count * sizeof *game.kids)
    for int i in range(game.kids_count):
        Tile *tile = girl_create_kid(i)
        game.kids[i] = player_create(tile.id)
        game.kids[i]->name = land_strdup(name_pick(tile.female))
        player_place_at_start(game.kids[i], (i % 5) - 2,
            (i / 5) + 1, game.map)
        kid_command(game.kids[i], Studying, False)
        game.kids[i]->kid = i

    game.player = player_create(tile_by_name("girl"))
    game.player.ladders = 25
    player_place_at_start(game.player, 0, 0, game.map)

    game.monster = player_create(tile_by_name("monster"))
    player_place_at_start(game.monster, 64, 64, game.map)
    game.monster.ladders = 100
    game.title = False

def init(LandRunner *runner):
    land_alloc(game)
    game.title = True
    game.music = True
    game.small = land_font_load("data/galaxy.ttf", 14)
    game.large = land_font_load("data/galaxy.ttf", 32)
    game.ring = land_sound_load("data/alarm.ogg")
    game.ding = land_sound_load("data/ding.ogg")
    game.knock = land_sound_load("data/knock.ogg")
    game.toc = land_sound_load("data/toc.ogg")
    game.classroom = land_sound_load("data/classroom.ogg")
    game.laugh = land_sound_load("data/laugh.ogg")
    game.cry = land_sound_load("data/cry.ogg")
    game.command = land_strdup("")
    game.camera = camera_new(land_display_width(), land_display_height())
    game.map = map_create(128, 128, 128, 128)
    game.brick = brick_orange_create()
    brick_white_create()
    game.ladder = ladder_create()
    game.pams = parameters_new()
    girl_create(game.pams)
    cloud_create()
    sparkle_create()
    tear_create()
    monster_create()
    game.earth = earth_create()
    game.overview = map_create_overview_tile(game.map)

def enter(LandRunner *runner):
    pass

#static def param(float *p, minv, maxv, d):
#    if land_key(LandKeyLeftShift) or land_key(LandKeyRightShift):
#        d = -d
#    *p += d
#    if *p < minv:
#        *p = maxv
#    if *p > maxv:
#        *p = minv
#    girl_create(game.pams)

def tick(LandRunner *runner):
    if game.music:

        if game.title:
            music_play_tune_if_not(music_tune3)
        else:
            if game.kids[0]->state == Studying or game.kids[0]->state == Crazy:
                music_play_tune_if_not(music_tune4)
            else:
                if music_current() == music_tune1:
                    if music_repeats() >= 1:
                        music_play_tune_if_not(music_tune3)
                elif music_current() == music_tune2:
                    if music_repeats() >= 1:
                        music_play_tune_if_not(music_tune3)
                else:
                    music_play_tune_if_not(music_tune3)

        music_tick()
    if land_closebutton(): land_quit()
    if land_key_pressed(LandKeyEscape):
        if game.title: land_quit()
        else: game.title = True
    int kx = 0
    int ky = 0
    int ka = 0
    if land_key(LandKeyRight): kx++
    if land_key(LandKeyLeft): kx--
    if land_key(LandKeyUp): ky--
    if land_key(LandKeyDown): ky++
    if land_key_pressed(LandKeyLeftShift) or land_key_pressed(LandKeyRightShift): ka = 2
    elif land_key(LandKeyLeftShift) or land_key(LandKeyRightShift): ka = 1

    while not land_keybuffer_empty():
        int k, u
        land_keybuffer_next(&k, &u)
        if u >= 32 and u < 127:
            if game.time > game.letter_time:
                game.command[0] = 0
            int s = land_utf8_count(game.command)
            game.command = land_utf8_realloc_insert(game.command, s, u)
            game.letter_time = game.time + 60
            game.command_time = game.time + 180

    if game.time > game.command_time:
        game.command[0] = 0

    if game.title:
        title_tick()

        if land_equals(game.command, "easy"): start(20)
        if land_equals(game.command, "medium"): start(25)
        if land_equals(game.command, "hard"): start(30)
        if land_equals(game.command, "continue"):
            if game.player:
                game.title = False
            
        game.time++
        return
    
    player_input(game.player, kx, ky, 0)
    game.camera.x = game.player.x - game.camera.w / 2 + game.map.tw / 2
    game.camera.y = game.player.y + 128 - game.camera.h / 2 + game.map.th / 2

    if land_key_pressed(LandKeyFunction + 1):
        game.music = not game.music

    particle_move_all()

    if kx == 0:
        int lx = map_tx(game.player.x + 64)
        int ly = map_ty(game.player.y + 256 - 10)
        if ka == 2:
            player_ladder(game.player)
            game.lx = lx
            game.ly = ly
        elif ka:
            if lx != game.lx or ly != game.ly:
                player_ladder(game.player)
                game.lx = lx
                game.ly = ly
    else:
        if ka:
            player_dig(game.player, kx)

    player_input(game.monster, 0, 0, 2)

    if game.inclass == game.kids_count and game.kids[0]->state == Sitting:
        if not game.won:
            game.won = True
            for int i in range(game.kids_count):
                Player *kid = game.kids[i]
                kid.state = Dancing
                kid.attention_span = 10

    game.inclass = 0
    game.noisy = 0
    int mini = -1
    float mind = 0
    bool command_successful = False
    for int i in range(game.kids_count):
        Player *kid = game.kids[i]
        if kid.state == Sitting or kid.state == Studying or kid.state == Dancing:
            game.inclass++
        if kid.state == Sitting:
            float v = 1 - kid.attention_span / 3600.0
            if v < 0:
                v = 0
            game.noisy += v
        char *c = game.command
        bool named = False
        float d = kid_distance(kid, None, None)
        kid.seen = False
        if kid.state != Sitting:
            if mini == -1 or d < mind:
                mind = d
                mini = i
        if d < 1280:
            kid.seen_x = kid.x
            kid.seen_y = kid.y
            kid.seen = True
        if d < 500 and game.command[0]:
            int f = game.command[0]
            game.command[0] = toupper(f)
            if land_starts_with(game.command, kid.name):
                c = game.command + strlen(kid.name) + 1
                named = True
            else:
                game.command[0] = f
            if land_equals(c, "follow"):
                kid_command(kid, Following, named)
                command_successful = True
            if land_equals(c, "stop"):
                kid_command(kid, Stopping, named)
                command_successful = True
            if land_equals(c, "sit"):
                kid_command(kid, Sitting, named)
                command_successful = True
            if land_equals(c, "quiet"):
                if kid.state == Sitting:
                    kid.attention_span = 3600
                    command_successful = True
        player_input(kid, 0, 0, 1)

        if i == 0:
            if kid.state == Studying and kid.attention_span == 1:
                land_sound_loop(game.ring, 2, 0, 1)
            if kid.state == Crazy and kid.attention_span == 1:
                land_sound_stop(game.ring)

    if command_successful:
        game.command[0] = 0

    if land_equals(game.command, "where are you?"):
        if mini != -1:
            Player *kid = game.kids[mini]
            kid.seen_x = kid.x
            kid.seen_y = kid.y
            kid.seen = True
        game.command[0] = 0

    if game.noisy < 5 and game.time < game.noisy_time:
        land_sound_stop(game.classroom)
        game.noisy_time = game.time
    if game.noisy >= 5 and game.time > game.noisy_time:
        game.noisy_time = game.time + land_sound_seconds(game.classroom) * 60
        float v = game.noisy / 10.0
        if v > 1:
            v = 1
        land_sound_play(game.classroom, v, 0, 1)

    #if land_key_pressed('h'): param(&game.pams.hairlength, 0, 2, 0.1)
    #if land_key_pressed('g'): param(&game.pams.hairg, -1, 1, 0.1)
    #if land_key_pressed('t'): param(&game.pams.hairtop, 0.2, 0.8, 0.1)
    #if land_key_pressed('e'): param(&game.pams.eyedistance, 0.3, 0.5, 0.05)
    #if land_key_pressed('w'): param(&game.pams.headw, 0.5, 1.2, 0.1)
    #if land_key_pressed('r'): param(&game.pams.radius, 30, 50, 1)
    #if land_key_pressed('1'): param(&game.pams.forehead, 0.1, 1, 0.01)
    #if land_key_pressed('2'): param(&game.pams.jaw, 0.1, 1, 0.01)
    #if land_key_pressed('3'): param(&game.pams.chin, 0.1, 1, 0.01)
    #if land_key_pressed('4'): param(&game.pams.foreheadg, 0, 2, 0.1)
    #if land_key_pressed('5'): param(&game.pams.jawg, -2, 1, 0.1)
    #if land_key_pressed('6'): param(&game.pams.ching, -3, 1, 0.1)

    game.time++

static def draw_player(Player *p):
    Tile *t = tile_by_id(p.tid)
    int f = (p.frame >> 2) & 7
    if f > 4:
        # 0 1 2 3 4 3 2 1
        f = 8 - f
    if p.falling:
        f = 5
    if p.state == Crying:
        f = 6
    float x = camera_x(game.camera, p.x)
    float y = camera_y(game.camera, p.y)

    if gravity == 1:
        land_image_draw(t.frames[f], x, y)
    else:
        land_image_draw_rotated(t.frames[f], x + 128, y + 256 + 120, pi)

    if p.name:
        float nx = x + 64
        float ny = y + 256 - t.tall - 20
        land_font_set(game.small)
        land_text_pos(nx, ny)
        land_color_set(t.color)
        land_print_center("%s", p.name)

        if p.attention_span < 600:
            land_color(1, 0, 0, 1)
            land_line(nx - 40, ny - 5, nx - 40 + p.attention_span * 80 / 600, ny - 5)
    else:
        land_font_set(game.large)
        land_text_pos(x + 64, y + 48)
        land_color_set(t.color)
        land_print_center("%s", game.command)

def draw(LandRunner *runner):
    land_clear(0, 0, 0, 1)
    if game.title:
        title_draw()
        return
    
    map_update_overview_tile(game.map, game.overview)
    map_render(game.map, game.camera)
    draw_player(game.player)

    for int i in range(game.kids_count):
        draw_player(game.kids[i])

    draw_player(game.monster)

    particle_draw_all(game.camera)

    Player *kid0 = game.kids[0]
    land_font_set(game.large)
    land_text_pos(game.camera.w / 2, game.camera.h / 3)
    if kid0.state == Studying:
        land_color(0, 0, 0, 1)
        if kid0.attention_span > 120:
            land_print_center("Ms Teacher is teaching her class.")
        else:
            land_print_center("But then...")
    elif kid0.state == Crazy:
        float fade = 180 - kid0.attention_span
        if fade > 0:
            float f = fade / 180.0
            land_color(0, 0, 0, f)
            land_filled_rectangle(0, 0, game.camera.w, game.camera.h)
        land_color(1, 0.2, 0.4, 1)
        land_print_center("Behave during recess!")
    else:
        float x = game.camera.w - game.overview.w + 0.5
        float y = 0.5
        land_image_draw(game.overview.pic, x, y)

        for int i in range(game.kids_count):
            Player *kid = game.kids[i]
            if kid.state == Sitting:
                continue
            int p = (game.time / 6) & 1
            if kid.seen: land_color(1, p, p, 1)
            else: land_color(1, 0, 0, 1)
            float kx = x + kid.seen_x / 128
            float ky = y + kid.seen_y / 128
            land_circle(kx - 3, ky - 3, kx + 3, ky + 3)

        land_color(1, 1, 1, 1)
        land_circle(x + game.player.x / 128 - 3,
            y + game.player.y / 128 - 3,
            x + game.player.x / 128 + 3, y + game.player.y / 128 + 3)

        land_color(0, 0, 1, 1)
        land_circle(x + game.monster.x / 128 - 3,
            y + game.monster.y / 128 - 3,
            x + game.monster.x / 128 + 3, y + game.monster.y / 128 + 3)

    land_color(1, 1, 1, 1)
    land_font_set(game.small)
    land_text_pos(0, 0)
    float p = 100 * game.noisy / 10
    if p > 100: p = 100
    land_print("kids in class: %2d/%d noise level: %.0f %%",
        game.inclass, game.kids_count, p)

    land_image_draw_scaled(game.ladder.pic, 240, 0, 0.125, 0.125)
    land_text_pos(240 + 16, 0)
    land_print("%d", game.player.ladders)

    if game.won:
        land_font_set(game.large)
        land_text_pos(game.camera.w / 2, game.camera.h / 3)
        land_color(1, 0, 0, 1)
        land_print_center("Yay, all back in class!")
    
def leave(LandRunner *runner):
    pass

def destroy(LandRunner *runner):
    pass

LandRunner *def game_runner():
    if _runner: return _runner
    _runner = land_runner_new("game", init, enter, tick, draw, leave, destroy)
    land_runner_register(_runner)
    return _runner
