import stats
import curses
import time
import fightui

# Global variables
textspeed = 0.05
VISIBLE = 4
mons = [
    getattr(stats, f"mon{i}")
    for i in range(1, 152)
    if hasattr(stats, f"mon{i}")
]
TOTAL = len(mons)


def printdelay(text):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(textspeed)


def main_menu(stdscr):
    curses.curs_set(0)
    stdscr.keypad(True)
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_BLUE, -1)

    menu_items = ["--Pokethon--", "FightTest", "Pokedex", "Settings"]
    selected = 1

    while True:
        stdscr.clear()

        for i, text in enumerate(menu_items):
            display = text.capitalize()
            if i == selected:
                stdscr.attron(curses.color_pair(1))
                stdscr.addstr(i * 2, 0, f"> {display}")
                stdscr.attroff(curses.color_pair(1))
            else:
                stdscr.addstr(i * 2, 0, f"  {display}")

        key = stdscr.getch()

        if key == curses.KEY_UP and selected > 1:
            selected -= 1
        elif key == curses.KEY_DOWN and selected < 3:
            selected += 1
        elif key == ord("z"):
            if selected == 1:
                fightui.battle_setup(stdscr)  # call battle
            elif selected == 2:
                mon_menu(stdscr)
            elif selected == 3:
                setting_menu(stdscr)


def setting_menu(stdscr):
    global textspeed
    curses.curs_set(0)
    stdscr.keypad(True)
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_BLUE, -1)

    options = [f"text speed {textspeed:.2f}", "wip", "wip", "back"]
    selected = 0

    while True:
        stdscr.clear()
        for i, text in enumerate(options):
            text_display = text.ljust(9)
            if i == selected:
                stdscr.attron(curses.color_pair(1))
                stdscr.addstr(i * 2, 0, f"< {text_display} >")
                stdscr.attroff(curses.color_pair(1))
            else:
                stdscr.addstr(i * 2, 0, f" {text_display} ")

        key = stdscr.getch()

        if key == curses.KEY_UP and selected > 0:
            selected -= 1
        elif key == curses.KEY_DOWN and selected < 3:
            selected += 1
        elif key == curses.KEY_LEFT and selected == 0 and textspeed > 0:
            textspeed -= 0.05
        elif key == curses.KEY_RIGHT and selected == 0 and textspeed < 1:
            textspeed += 0.05
        elif key == ord("z"):
            if selected == 3:
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

    divider = "-" * 70
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

        elif key == ord("q"):
            break

        stdscr.refresh()


if __name__ == "__main__":
    curses.wrapper(main_menu)
