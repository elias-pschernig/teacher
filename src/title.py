import game

def title_tick:
    pass

static def E(char const *x):
    land_color(1, 0.5, 0, 1)
    land_write(x)
    land_color(1, 1, 1, 1)

static def LN():
    land_text_pos(10, land_text_y_pos())

def title_draw:
    Game *game = game_global()
    float cx = game->camera->w / 2
    float cy = game->camera->h / 2

    land_font_set(game.large)
    land_text_pos(cx, 10)
    land_color(1, 0.4, 0.7, 1)
    land_print_center("Speedhack 2015")
    land_font_set(game.small)
    land_color(1, 1, 1, 1)
    land_print_center("allegro.cc entry by elias a.k.a.")
    land_color(1, 0.9, 0, 1)
    land_font_set(game.large)
    land_print_center("Allefant")
    land_font_set(game.small)
    land_color(1, 0.5, 0, 1)
    land_print_center("with musical and other help from andrea a.k.a.")
    land_font_set(game.large)
    land_print_center("AK")

    land_font_set(game.small)
    land_text_pos(10, 150)
    land_color(1, 1, 1, 1)
    land_print("You are Ms. Teacher, the classroom teacher of class 1a. Type commands on the keyboard to tell your students what to do.")
    land_write("Whenever you find a student just wandering around, tell them to ")
    E("follow")
    land_print(" you.")
    LN()
    land_write("If a kid is running around in the classroom, tell them to ")
    E("sit")
    land_print(" down again.")
    LN()
    land_write("If your class is making too much noise, tell them to be ")
    E("quiet")
    land_print(".")
    LN()
    land_write("If one of them starts crying, ")
    land_color(0, 0.5, 1, 1)
    land_write("call them by their name")
    land_color(1, 1, 1, 1)
    land_write(" followed by ")
    E("stop")
    land_print(" to calm them down, lest the happy monster appear to cheer them up.")
    LN()
    land_print("(It also will make them stop following the monster.)")
    land_write("If you ever know a kid must be nearby but can't find them, ask ")
    E("where are you?")
    land_print(" and they should reveal themselves.")
    LN()

    land_print("")
    land_print("You can also carry 25 ladders and side dig into earth.")

    land_print("")
    land_print("F1 to toggle music, Esc to go back to menu.")
    land_print("Cursor keys to move, Shift keys to build.")

    land_font_set(game.large)
    land_text_pos(cx, cy)
    land_color((game.time / 10) % 3 ? 1 : 0, 0, 0, 1)
    land_print_center("Type easy/medium/hard to start a game with 20/25/30 students!")
    if game.player:
        land_print_center("Type continue to continue a current game.")
    land_color(1, 0, 0, 1)
    land_print_center("%s", game.command)

    int tid = tile_by_name("girl")
    Tile *t = tile_by_id(tid)
    land_image_draw(t.frames[0], cx - 64, cy + 30)
