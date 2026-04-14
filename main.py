import stats
import curses
import time
import fightui
import overworld
import mysterygift

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
curses.init_pair(8, curses.COLOR_BLACK, curses.COLOR_WHITE)
curses.init_pair(9, curses.COLOR_BLACK, curses.COLOR_RED)
curses.init_pair(10, curses.COLOR_BLACK, curses.COLOR_YELLOW)
curses.init_pair(11, curses.COLOR_BLACK, curses.COLOR_GREEN)
curses.init_pair(12, curses.COLOR_BLACK, curses.COLOR_BLUE)
curses.init_pair(13, curses.COLOR_GREEN, curses.COLOR_WHITE)
curses.init_pair(14, curses.COLOR_YELLOW, curses.COLOR_WHITE)
curses.init_pair(15, curses.COLOR_RED, curses.COLOR_WHITE)


#variables
textspeed = 0.01
VISIBLE = 10
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
        "-->POKETHON<--",
        "Debug Battle",
        "Overworld",
        "Pokedex [PLACEHOLDER]",
        "Settings",
        "Mystery Gift",
        "Start Game [NOT AVAILABLE]"
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
        elif key == curses.KEY_DOWN and y < 5:
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
            elif y == 5:
                mysterygift.gifted(stdscr)

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
            "idk bro battle animations???",
            "dkkuuygdskhjnvdguiyjdaydf",
            "back"
        ]
        for i in range(4):
            text = menu[i].ljust(9)
            if i == y:
                stdscr.attron(curses.color_pair(1))
                stdscr.addstr(i, 0, f"< {text} >")
                stdscr.attroff(curses.color_pair(1))
            else:
                stdscr.addstr(i, 0, f" {text} ")

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
                
def draw_stats(stdscr, mon, start_x):
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
    pair_id = 20  # avoid conflict with other pairs
    for t, color in type_colors.items():
        curses.init_pair(pair_id, color, -1)
        color_pairs[t] = curses.color_pair(pair_id)
        pair_id += 1

    # Title
    title = mon.call().capitalize()
    stdscr.addstr(0, start_x, title)

    divider = "━" * 30
    stdscr.addstr(1, start_x, divider)

    type1 = mon.type.capitalize()
    type2 = (mon.type2 or "").capitalize()

    stdscr.addstr(2, start_x, f"{type1}", color_pairs.get(type1, curses.A_NORMAL))
    stdscr.addstr(2, start_x + 12, f"{type2}", color_pairs.get(type2, curses.A_NORMAL))

    stdscr.addstr(4, start_x, f"HP: {mon.hp}")
    stdscr.addstr(5, start_x, f"ATK: {mon.at}")
    stdscr.addstr(6, start_x, f"SP ATK: {mon.sp_at}")
    stdscr.addstr(7, start_x, f"DEF: {mon.de}")
    stdscr.addstr(8, start_x, f"SP DEF: {mon.sp_de}")
    stdscr.addstr(9, start_x, f"SPD: {mon.spd}")

    stdscr.addstr(3, start_x, divider)

def mon_menu(stdscr):
    curses.curs_set(0)
    stdscr.keypad(True)

    scrollno = 0
    cursor = 0

    while True:
        stdscr.clear()

        # LEFT SIDE (list)
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

        # RIGHT SIDE (stats)
        selected_idx = scrollno + cursor
        if selected_idx < TOTAL:
            draw_stats(stdscr, mons[selected_idx], 30)  # 30 = right side offset

        stdscr.addstr(VISIBLE + 1, 0, "X = back")

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

        elif key == ord("x"):
            break

        stdscr.refresh()
    
def main(stdscr):
    height, width = stdscr.getmaxyx()

    if height != 24 or width != 80:
        stdscr.clear()
        stdscr.addstr(0, 0, "For this game, it requires your terminal to be 80x24!")
        stdscr.addstr(1, 0, f"Current Size: {height} x {width}")
        stdscr.addstr(3, 0, "Sorry For The Inconvenience!")
        stdscr.refresh()
        stdscr.getch()
        return

    stdscr.addstr(0, 0, "Size is correct, Loading...")
    mainm(stdscr)

while True:
    curses.wrapper(main)

#test
print("hi")
print(stats.mon1.call())
import curses
