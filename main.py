import stats
import curses
import time
import fightui
import overworld
import battlehandler
print(fightui.__file__)

#colors
curses.initscr()
curses.start_color()
curses.use_default_colors()
curses.init_pair(1, curses.COLOR_WHITE, -1)
curses.init_pair(2, curses.COLOR_YELLOW, -1)
curses.init_pair(3, curses.COLOR_CYAN, -1)
curses.init_pair(4, curses.COLOR_GREEN, -1)
curses.init_pair(5, curses.COLOR_MAGENTA, -1)
curses.init_pair(6, curses.COLOR_BLUE, -1)
curses.init_pair(7, curses.COLOR_RED, -1)

#variables
textspeed = 0.01
VISIBLE = 4
mons = [
    getattr(stats, f"mon{i}")
    for i in range(1, 152)
    if hasattr(stats, f"mon{i}")
]
TOTAL = len(mons)

def main(stdscr):
    import fightui
    battle_data = fightui.battle_setup(stdscr)
def printdelay(text):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(textspeed) 
def mainm(stdscr):
    import fightui
    curses.curs_set(0)
    stdscr.keypad(True)
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_BLUE, -1)

    menu = [
        "--Pokethon--",
        "Debug Battle",
        "Overworld",
        "Pokedex",
        "Settings"
    ]

    y = 1

    while True:
        stdscr.clear()
        for i in range(len(menu)):
            text = menu[i].capitalize()  
            if i == y:
                stdscr.attron(curses.color_pair(1))
                stdscr.addstr(i * 1, 0, f"> {text}")
                stdscr.attroff(curses.color_pair(1))
            else:
                stdscr.addstr(i * 1, 0, f"  {text}")

        key = stdscr.getch()

        if key == curses.KEY_UP and y > 1:
            y -= 1
        elif key == curses.KEY_DOWN and y < 4:
            y += 1
        elif key == ord("z"):
            if y == 3:
                mon_menu(stdscr)
            elif y == 1:  
                import fightui
                fightui.battle_setup(stdscr)
            elif y == 4:
                setting(stdscr)
            elif y == 2:
                overworld.overworld(stdscr)

def setting(stdscr):
    global textspeed
    curses.curs_set(0)
    stdscr.keypad(True)
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_BLUE, -1)

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
                textspeed -= 0.01
        elif key == curses.KEY_RIGHT and y == 0:
            if textspeed < 1:
                textspeed += 0.01
        elif key == ord("z"):
            if y == 3:
                break
            else:
                printdelay("wip")

def draw_stats(stdscr, mon, dexno):
    curses.start_color()
    curses.use_default_colors()

    type_colors = {
        "Fire": curses.COLOR_RED,
        "Ground": curses.COLOR_YELLOW,
        "Rock": curses.COLOR_YELLOW,
        "Fighting": curses.COLOR_MAGENTA,
        "Electric": curses.COLOR_YELLOW,
        "Bug": curses.COLOR_GREEN,
        "Grass": curses.COLOR_GREEN,
        "Water": curses.COLOR_BLUE,
        "Flying": curses.COLOR_CYAN,
        "Ice": curses.COLOR_CYAN,
        "Dragon": curses.COLOR_MAGENTA,
        "Psychic": curses.COLOR_MAGENTA,
        "Poison": curses.COLOR_MAGENTA,
        "Ghost": curses.COLOR_MAGENTA,
        "Dark": curses.COLOR_BLACK,
        "Normal": curses.COLOR_WHITE,
        "Steel": curses.COLOR_WHITE
    }

    color_pairs = {}
    pair_id = 1
    for t, color in type_colors.items():
        curses.init_pair(pair_id, color, -1)
        color_pairs[t] = curses.color_pair(pair_id)
        pair_id += 1

    stdscr.clear()
    h, w = stdscr.getmaxyx()

    title = mon.call().capitalize()
    stdscr.addstr(0, 0, title)

    divider = "━" * 70 
    stdscr.addstr(1, 0, divider)

    col1, col2, col3, col4 = 0, 14, 30, 50

    type1 = mon.type.capitalize()
    type2 = (mon.type2 or "").capitalize()
    stdscr.addstr(2, col1, f"{type1:<12}", color_pairs.get(type1, curses.A_NORMAL))
    stdscr.addstr(2, col2, f"| HP: {mon.hp:<5}")
    stdscr.addstr(2, col3, f"| Attack: {mon.at:<5}")
    stdscr.addstr(2, col4, f"| Sp. Atk: {mon.sp_at:<5}")

    stdscr.addstr(3, col1, f"{type2:<12}", color_pairs.get(type2, curses.A_NORMAL))
    stdscr.addstr(3, col2, f"| Speed: {mon.spd:<5}")
    stdscr.addstr(3, col3, f"| Defense: {mon.de:<5}")
    stdscr.addstr(3, col4, f"| Sp. Def: {mon.sp_de:<5}")

    stdscr.addstr(4, 0, divider)

    stdscr.addstr(5, 0, "#placeholder")

    stdscr.addstr(h - 1, 0, "Press X to go back")
    stdscr.refresh()

    while True:
        if stdscr.getch() == ord("x"):
            break

def mon_menu(stdscr):
    curses.curs_set(0)
    stdscr.keypad(True)

    scrollno = 0
    cursor = 0

    while True:
        stdscr.clear()

        for i in range(VISIBLE):
            idx = scrollno + i
            if idx >= TOTAL:
                break

            dexno = idx + 1
            name = mons[idx].call().capitalize()

            line = f"{dexno:03d} {name}"

            if i == cursor:
                stdscr.addstr(i, 0, f"> {line}")
            else:
                stdscr.addstr(i, 0, f"  {line}")

        stdscr.addstr(VISIBLE + 1, 0, "Press Z to see Stats!")

        key = stdscr.getch()

        if key == curses.KEY_UP:
            if cursor > 0:
                cursor -= 1
            elif scrollno > 0:
                scrollno -= 1

        elif key == curses.KEY_DOWN:
            if cursor < VISIBLE - 1 and scrollno + cursor + 1 < TOTAL:
                cursor += 1
            elif scrollno + VISIBLE < TOTAL:
                scrollno += 1

        elif key == ord("z"):
            idx = scrollno + cursor
            draw_stats(stdscr, mons[idx], idx + 1)

        elif key == ord("x"):
            break

        stdscr.refresh()

while True:
    curses.wrapper(mainm)

#test
print("hi")
print(stats.mon1.call())