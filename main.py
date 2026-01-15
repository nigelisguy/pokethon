import stats
import curses
import time
textspeed = 0.05
def printdelay(text):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(textspeed) 

def mainm(stdscr):
    curses.curs_set(0)
    stdscr.keypad(True)
    curses.start_color()
    curses.use_default_colors()

    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_RED)

    menu = [
        "--pokethon--",
        "fighttest",
        "pokedex ",
        "settings"
    ]

    y = 1
    cell_width = 11

    while True:
        stdscr.clear()

        for i in range(4):
            text = menu[i].ljust(9)
            if i == y:
                stdscr.attron(curses.color_pair(1))
                stdscr.addstr(i * 2, 0, f"> {text}")
                stdscr.attroff(curses.color_pair(1))
            else:
                stdscr.addstr(i * 2, 0, f" {text} ")

        key = stdscr.getch()

        if key == curses.KEY_UP and y > 1:
            y -= 1
        elif key == curses.KEY_DOWN and y < 3:
            y += 1
        elif key == ord("z"):
            if y ==2:
                printdelay("wip")
            elif y ==1:
                fightui(stdscr)
            elif y==3:
                setting(stdscr)

def setting(stdscr):
    global textspeed
    curses.curs_set(0)
    stdscr.keypad(True)
    curses.start_color()
    curses.use_default_colors()

    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_RED)

    y = 0
    cell_width = 11

    while True:
        stdscr.clear()
        menu = [
        f"text speed {textspeed:.2f}",
        "wip",
        "wip",
        "back"
        ]
        for i in range(4):
            text = menu[i].ljust(9)
            if i == y:
                stdscr.attron(curses.color_pair(1))
                stdscr.addstr(i * 2, 0, f"< {text} >")
                stdscr.attroff(curses.color_pair(1))
            else:
                stdscr.addstr(i * 2, 0, f" {text} ")

        key = stdscr.getch()

        if key == curses.KEY_UP and y > 0:
            y -= 1
        elif key == curses.KEY_DOWN and y < 3:
            y += 1
        elif key == curses.KEY_LEFT and y == 0:
            if textspeed > 0:
                textspeed -= 0.05
        elif key == curses.KEY_RIGHT and y == 0:  
            if textspeed < 1:  
                textspeed += 0.05
        elif key == ord("z"):
            if y == 3:
                break
            else:
                printdelay("wip")
                


def fightui(stdscr):
    curses.curs_set(0)
    stdscr.keypad(True)

    grid = [
        ["--Fight--", "---Bag---"],
        ["-Pokémon-", "---Run---"]
    ]

    x = 0
    y = 0
    cell_width = 11

    while True:
        stdscr.clear()

        for j in range(2):
            for i in range(2):
                text = grid[j][i].ljust(9)

                if i == x and j == y:
                    cell = f"[{text}]"
                else:
                    cell = f" {text} "

                stdscr.addstr(j * 2, i * cell_width, cell)

        key = stdscr.getch()

        if key == curses.KEY_UP and y > 0:
            y -= 1
        elif key == curses.KEY_DOWN and y < 1:
            y += 1
        elif key == curses.KEY_LEFT and x > 0:
            x -= 1
        elif key == curses.KEY_RIGHT and x < 1:
            x += 1
        elif key == ord("q"):
            break

def fightui(stdscr):
    curses.curs_set(0)
    stdscr.keypad(True)

    grid = [
        ["--Fight--", "---Bag---"],
        ["-Pokémon-", "---Run---"]
    ]

    x = 0
    y = 0
    cell_width = 11

    while True:
        stdscr.clear()

        for j in range(2):
            for i in range(2):
                text = grid[j][i].ljust(9)

                if i == x and j == y:
                    cell = f"[{text}]"
                else:
                    cell = f" {text} "

                stdscr.addstr(j * 2, i * cell_width, cell)

        key = stdscr.getch()

        if key == curses.KEY_UP and y > 0:
            y -= 1
        elif key == curses.KEY_DOWN and y < 1:
            y += 1
        elif key == curses.KEY_LEFT and x > 0:
            x -= 1
        elif key == curses.KEY_RIGHT and x < 1:
            x += 1
        elif key == ord("q"):
            break

        stdscr.refresh()
while True:
    curses.wrapper(mainm)

#var

print("hi")
print(stats.mon1.call())