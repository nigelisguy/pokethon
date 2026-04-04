import curses
import time
import random
import fightui

WIDTH = 20
HEIGHT = 10

pokemon=(0,0,0,0,0,0)
pokemonhp=(0,0,0,0,0,0)
exp=(0,0,0,0,0,0)
nextexp=(0,0,0,0,0,0)

PLAYER = "@"
GRASS = "#"
NURSE = "♥"
ENEMY = "☺"
IMPT = "#"
POKEMON = "█"
NPC_ICON = "☺"

TEXT_SPEED = 0.02


npcs = {
    (2, 5): (NPC_ICON, ["hello!", "welcome to the test map!","I'll give you some tips for your journey","# are people you need to meet","☺ are your normal townsfolk","some still have somethings to offer, but are not mandatory","lastly, enemies are similar to townsfolk, ","but challenge you to a pokemon battle when in range","thats really the bulk of it","If you want to hear that again, talk to me again"]), #PLACEHOLDER TIPS
    (2, 6): (NURSE, ["hello, would you like to heal your pokémon?","Ok, I'll heal them back.","Tadah! Your Pokémon are all healthy again!","We hope to see you soon!"]),
    (2, 7): (ENEMY, ["we made eye contact, now lets fight!","Oh wait, the developer hasn't implemented it yet"]),
    (2, 8): (POKEMON, ["Jigglypuff: Piu Piu Piu Piu!"]),
    (2, 9): (IMPT, ["BILL: I'm Bill, and I'm Very Important","BILL: Trust Me","Obtained the Teachy TV!","BILL: I dont want that its useless","Upon recieving it, The Teachy TV breaks instantly, rendering it unusable.","BILL: See what did i say"]),
    (6, 20): (NPC_ICON, ["psst you found me", "im the secret npc"]) 
}

grass_tiles = set()
def door(originalroom,x,y,destination):
    print("hi")


def safe_addstr(stdscr, y, x, text):
    try:
        h, w = stdscr.getmaxyx()
        if y < h and x < w:
            stdscr.addstr(y, x, str(text)[:w - x])
    except curses.error:
        pass 

# touch graassss
for y in range(HEIGHT - 5, HEIGHT):
    for x in range(WIDTH - 5, WIDTH):
        grass_tiles.add((y, x))

def type_text(stdscr, text):
    h, w = stdscr.getmaxyx()
    stdscr.move(h - 2, 2)
    stdscr.clrtoeol()

    for char in text:
        stdscr.addstr(char)
        stdscr.refresh()
        time.sleep(TEXT_SPEED)

def show_dialogue(stdscr, lines):
    h, w = stdscr.getmaxyx()

    for line in lines:
        safe_addstr(stdscr, h - 3, 0, "╔" + "═" * (w - 2) + "╗ ")
        safe_addstr(stdscr, h - 2, 0, "║" + " " * (w - 2) + "║")
        safe_addstr(stdscr, h - 1, 0, "╚" + "═" * (w - 2) + "╝")
        stdscr.clrtoeol()
        type_text(stdscr, line)
        stdscr.refresh()

        while True:
            key = stdscr.getch()
            if key == ord("z"):
                break

    stdscr.move(h - 2, 0)
    stdscr.clrtoeol()
    stdscr.move(h - 1, 0)
    stdscr.clrtoeol()

def draw(stdscr, py, px):
    stdscr.clear()

    for y in range(HEIGHT):
        for x in range(WIDTH):

            char = "෴"
            color = curses.color_pair(4)  

            if (y, x) in grass_tiles:
                char = GRASS
                color = curses.color_pair(4)

            if (y, x) in npcs:
                char = npcs[(y, x)][0]
                color = curses.color_pair(6)

            if y == py and x == px:
                char = PLAYER
                color = curses.color_pair(7)

            stdscr.addstr(y, x * 2, char, color)

    stdscr.refresh()

def overworld(stdscr):
    import battlehandler
    curses.curs_set(0)
    stdscr.keypad(True)
    curses.start_color()
    curses.use_default_colors()


    py, px = 0, 0
    while True:
        draw(stdscr, py, px)
        menu(stdscr)
        key = stdscr.getch()

        ny, nx = py, px

        if key == curses.KEY_UP:
            ny -= 1
        elif key == curses.KEY_DOWN:
            ny += 1
        elif key == curses.KEY_LEFT:
            nx -= 1
        elif key == curses.KEY_RIGHT:
            nx += 1
        elif key == ord("q"):
            break
        if 0 <= ny < HEIGHT and 0 <= nx < WIDTH:
            if (ny, nx) not in npcs:
                py, px = ny, nx

        if key == ord("z"):
            for dy, dx in [(-1,0),(1,0),(0,-1),(0,1)]:
                check = (py + dy, px + dx)
                if check in npcs:
                    show_dialogue(stdscr, npcs[check][1])

        if (py, px) in grass_tiles:
            if random.random() < 0.2:
                show_dialogue(stdscr, ["A Wild Pokémon appeared!"])
                battlehandler.run_battle(stdscr,1)
def menu(stdscr):
    h, w = stdscr.getmaxyx()
    safe_addstr(stdscr, 10, 0, "+" + "━"*78 + "+")
    safe_addstr(stdscr, 11, 0, "placeholder1 placeholder2            save,options,etcidk")
    safe_addstr(stdscr, 12, 0, "placeholder3 placeholder4")
    safe_addstr(stdscr, 13, 0, "placeholder5 placeholder6")
    safe_addstr(stdscr, 21, 0, "+" + "━"*78 + "+")
    stdscr.refresh()
