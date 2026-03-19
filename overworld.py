import curses
import time
import random

WIDTH = 30
HEIGHT = 10


PLAYER = "@"
GRASS = "#"
NPC_ICON = "☺"

TEXT_SPEED = 0.02


npcs = {
    (2, 5): (NPC_ICON, ["hello!", "welcome to the test map!"]),
    (6, 20): ("⌘", ["sign", "sign2"]) #overwrite for sign, dont ask about the symbol
}

grass_tiles = set()

# touch graassss
for y in range(HEIGHT - 5, HEIGHT):
    for x in range(WIDTH - 5, WIDTH):
        grass_tiles.add((y, x))

def type_text(stdscr, text):
    h, w = stdscr.getmaxyx()
    stdscr.move(h - 2, 0)
    stdscr.clrtoeol()

    for char in text:
        stdscr.addstr(char)
        stdscr.refresh()
        time.sleep(TEXT_SPEED)

def show_dialogue(stdscr, lines):
    h, w = stdscr.getmaxyx()

    for line in lines:
        stdscr.move(h - 2, 0)
        stdscr.clrtoeol()
        type_text(stdscr, line)

        stdscr.addstr(h - 1, 0, "[Z]")
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
            color = curses.color_pair(1)  

            if (y, x) in grass_tiles:
                char = GRASS
                color = curses.color_pair(4)

            if (y, x) in npcs:
                char = npcs[(y, x)][0]
                color = curses.color_pair(3)

            if y == py and x == px:
                char = PLAYER
                color = curses.color_pair(2)

            stdscr.addstr(y, x * 2, char, color)

    stdscr.refresh()

def overworld(stdscr):
    import battlehandler
    curses.curs_set(0)
    stdscr.keypad(True)
    curses.start_color()
    curses.use_default_colors()

    curses.init_pair(1, curses.COLOR_GREEN, -1)   # ground
    curses.init_pair(2, curses.COLOR_WHITE, -1)  # player
    curses.init_pair(3, curses.COLOR_CYAN, -1)    # NPC
    curses.init_pair(4, curses.COLOR_GREEN, -1)   # grass (ew flip u)

    py, px = 0, 0

    while True:
        draw(stdscr, py, px)

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
                show_dialogue(stdscr, ["Something touched you!"])
                battlehandler.run_battle(stdscr)
