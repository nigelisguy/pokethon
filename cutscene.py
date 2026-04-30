import curses
import time
from pathlib import Path


TITLE_ART = [
    "         █████████           ",
    "      █████#####█████        ",
    "    ███#############███      ",
    "   ███#####█████#####███     ",
    "    █████████   █████████      ",
    "    ███     █████     ███      ",
    "     ███             ███       ",
    "       █████     █████         ",
    "          █████████            ",
]


BACKGROUND_STARS = [
    (2, 6, "."),
    (4, 58, "."),
    (6, 18, "*"),
    (8, 67, "."),
    (10, 8, "."),
    (12, 62, "*"),
    (14, 23, "."),
    (16, 71, "."),
    (18, 11, "*"),
]


def safe_addstr(stdscr, y, x, text, attr=0):
    try:
        h, w = stdscr.getmaxyx()
        if not (0 <= y < h):
            return
        if not (0 <= x < w):
            return
        stdscr.addstr(y, x, str(text)[: max(0, w - x)], attr)
    except curses.error:
        return


def center_x(stdscr, text):
    _, w = stdscr.getmaxyx()
    return max(0, (w - len(text)) // 2)


def init_cutscene_colors():
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(30, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(31, curses.COLOR_WHITE, -1)
    curses.init_pair(32, curses.COLOR_CYAN, -1)
    curses.init_pair(33, curses.COLOR_YELLOW, -1)


def flash_white(stdscr, duration_ms=120):
    h, w = stdscr.getmaxyx()
    stdscr.attron(curses.color_pair(30))
    for y in range(h):
        safe_addstr(stdscr, y, 0, " " * w, curses.color_pair(30))
    stdscr.attroff(curses.color_pair(30))
    stdscr.refresh()
    curses.napms(duration_ms)


def draw_background(stdscr, phase=0):
    h, w = stdscr.getmaxyx()
    for index, (y, x, char) in enumerate(BACKGROUND_STARS):
        if y >= h or x >= w:
            continue
        attr = curses.color_pair(33) if (phase + index) % 3 == 0 else curses.color_pair(31)
        safe_addstr(stdscr, y, x, char, attr)


def art_line_for_phase(line, phase, line_index):
    chars = list(line)
    highlight = (phase + line_index * 3) % (len(chars) + 8)

    for i, char in enumerate(chars):
        if char == "#" and highlight - 2 <= i <= highlight:
            chars[i] = "@"
        elif char == "█" and (i + phase + line_index) % 11 == 0:
            chars[i] = "▓"

    return "".join(chars)


def draw_title(stdscr, phase=0, show_prompt=True, visible_lines=None):
    stdscr.clear()
    h, _ = stdscr.getmaxyx()
    top = max(1, (h - len(TITLE_ART) - 6) // 2)
    draw_background(stdscr, phase)

    for i, line in enumerate(TITLE_ART):
        if visible_lines is not None and i >= visible_lines:
            break
        rendered_line = art_line_for_phase(line, phase, i)
        safe_addstr(stdscr, top + i, center_x(stdscr, rendered_line), rendered_line, curses.color_pair(31))

    title = "POKéTERMINAL"
    subtitle = "PreAlpha v0.6"
    prompt = "Press Z"

    title_attr = curses.color_pair(32) | curses.A_BOLD
    if phase % 2 == 0:
        title_attr |= curses.A_BLINK

    safe_addstr(stdscr, top - 2, center_x(stdscr, title), title, title_attr)
    safe_addstr(stdscr, top + len(TITLE_ART) + 1, center_x(stdscr, subtitle), subtitle, curses.color_pair(33))
    if show_prompt:
        safe_addstr(stdscr, top + len(TITLE_ART) + 3, center_x(stdscr, prompt), prompt, curses.A_BOLD)

    stdscr.refresh()


def animate_title_intro(stdscr):
    for visible_lines in range(1, len(TITLE_ART) + 1):
        draw_title(stdscr, phase=visible_lines, show_prompt=False, visible_lines=visible_lines)
        curses.napms(70)

    for phase in range(4):
        draw_title(stdscr, phase=phase, show_prompt=True)
        curses.napms(80)


def title_screen(stdscr):
    curses.curs_set(0)
    stdscr.keypad(True)
    init_cutscene_colors()

    flash_white(stdscr, 160)
    stdscr.clear()
    stdscr.refresh()
    curses.napms(80)
    animate_title_intro(stdscr)

    blink_on = True
    last_toggle = time.time()
    phase = 0

    while True:
        stdscr.timeout(120)
        key = stdscr.getch()

        if key == ord("c"):
            stdscr.timeout(-1)
            show_readme(stdscr)
            draw_title(stdscr, phase=phase, show_prompt=blink_on)
            blink_on = True
            last_toggle = time.time()
            continue

        if key in (ord("z"), ord("x"), ord("\n"), curses.KEY_ENTER):
            flash_white(stdscr, 90)
            stdscr.timeout(-1)
            return

        now = time.time()
        if now - last_toggle < 0.35:
            continue

        last_toggle = now
        blink_on = not blink_on
        phase += 1
        draw_title(stdscr, phase=phase, show_prompt=blink_on)


def show_readme(stdscr):
    curses.curs_set(0)
    stdscr.keypad(True)

    readme_path = Path(__file__).with_name("README.md")
    try:
        lines = readme_path.read_text(encoding="utf-8").splitlines()
    except OSError:
        lines = ["README.md could not be opened or is missing."]

    scroll = 0

    while True:
        stdscr.clear()
        height, width = stdscr.getmaxyx()
        body_height = max(1, height - 2)
        max_scroll = max(0, len(lines) - body_height)

        for row in range(body_height):
            idx = scroll + row
            if idx >= len(lines):
                break
            safe_addstr(stdscr, row, 0, lines[idx][: max(1, width - 1)])

        footer = "README  UP/DOWN scroll  X/C back"
        safe_addstr(stdscr, height - 1, 0, footer[: max(1, width - 1)])
        stdscr.refresh()

        key = stdscr.getch()
        if key == curses.KEY_UP and scroll > 0:
            scroll -= 1
        elif key == curses.KEY_DOWN and scroll < max_scroll:
            scroll += 1
        elif key == curses.KEY_PPAGE:
            scroll = max(0, scroll - body_height)
        elif key == curses.KEY_NPAGE:
            scroll = min(max_scroll, scroll + body_height)
        elif key in (ord("x"), ord("c")):
            break
