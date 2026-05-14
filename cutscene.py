import curses
import random
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
    subtitle = "vA0.7.2"
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
    flash_white(stdscr, 200)
    stdscr.clear()
    safe_addstr(stdscr, 13, 30, "NOT BY NINTENDO OR GAMEFREAK", curses.color_pair(8) | curses.A_BOLD)
    stdscr.refresh()
    curses.napms(1200)

    flash_white(stdscr, 200)
    stdscr.clear()
    safe_addstr(stdscr, 13, 30, "GAMEFREAK      983-2026", curses.color_pair(8))
    safe_addstr(stdscr, 14, 30, "POKEMON        1996-2026", curses.color_pair(8))
    safe_addstr(stdscr, 15, 30, "POKETERMINAL   2026", curses.color_pair(8))
    stdscr.refresh()
    curses.napms(1200)

    stdscr.clear()
    safe_addstr(stdscr, 13, 30, "skdish Presents", curses.color_pair(8) | curses.A_BOLD)
    stdscr.refresh()
    curses.napms(1000)

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


def prompt_input(stdscr, prompt, default=""):
    curses.curs_set(1)
    stdscr.keypad(True)
    entry = list(default)
    cursor = len(entry)
    consecutive_z = 0

    while True:
        stdscr.clear()
        h, w = stdscr.getmaxyx()
        safe_addstr(stdscr, 1, 2, prompt)
        display = ''.join(entry) or '_'
        safe_addstr(stdscr, 3, 2, display)
        safe_addstr(stdscr, 5, 2, "Press Z 3 times in a row to confirm, X to cancel")
        safe_addstr(stdscr, 6, 2, f"Z confirms after 3 taps: {consecutive_z}/3")
        stdscr.move(3, 2 + cursor)
        stdscr.refresh()

        key = stdscr.getch()
        if key == ord("z"):
            consecutive_z += 1
            entry.insert(cursor, "z")
            cursor += 1
            if consecutive_z >= 3:
                del entry[cursor - 3:cursor]
                curses.curs_set(0)
                return ''.join(entry).strip() or default
        elif key in (ord("\n"), curses.KEY_ENTER):
            curses.curs_set(0)
            return ''.join(entry).strip() or default
        elif key == ord("x"):
            curses.curs_set(0)
            return default
        elif key in (curses.KEY_BACKSPACE, 127, 8):
            consecutive_z = 0
            if cursor > 0:
                cursor -= 1
                entry.pop(cursor)
        elif key == curses.KEY_LEFT and cursor > 0:
            consecutive_z = 0
            cursor -= 1
        elif key == curses.KEY_RIGHT and cursor < len(entry):
            consecutive_z = 0
            cursor += 1
        elif 32 <= key <= 126:
            consecutive_z = 0
            entry.insert(cursor, chr(key))
            cursor += 1


def prompt_menu(stdscr, title, options):
    curses.curs_set(0)
    stdscr.keypad(True)
    selected = 0

    while True:
        stdscr.clear()
        safe_addstr(stdscr, 1, 2, title)
        for index, option in enumerate(options):
            prefix = "> " if index == selected else "  "
            safe_addstr(stdscr, 3 + index, 2, prefix + option)
        safe_addstr(stdscr, 3 + len(options) + 1, 2, "Z = choose   X = back")
        stdscr.refresh()

        key = stdscr.getch()
        if key == curses.KEY_UP and selected > 0:
            selected -= 1
        elif key == curses.KEY_DOWN and selected < len(options) - 1:
            selected += 1
        elif key == ord("z"):
            return selected
        elif key == ord("x"):
            return None


def new_save_intro(stdscr):
    import overworld
    curses.curs_set(0)
    stdscr.keypad(True)

    show_dialogue = overworld.show_dialogue if hasattr(overworld, 'show_dialogue') else None

    if show_dialogue:
        stdscr.clear()
        stdscr.refresh()
        show_dialogue(stdscr, [
            "Hello there! Welcome to the world of Pokémon!",
            "My name is Oak. People call me the Pokémon Professor.",
            "This world is full of creatures called Pokémon,",
            "and you, from what I heard, want to be a Pokémon Trainer! ",
            "Very well, today is the day you start your Pokémon journey.",
        ])

    player_name = prompt_input(stdscr, "What is your name?", "Jeff")
    rival_name = prompt_input(stdscr, "What is your rival's name?", "Malfoy")
    if show_dialogue:
        show_dialogue(stdscr, [
            f"Right! So your name is {player_name}.",
            f"Your rival will be called {rival_name}.",
        ])

    starter_options = ["Bulbasaur (A Grass/Poison Toad)", "Charmander (A Fire Lizard)", "Squirtle (A Water Turtle)"]
    starter_idx = prompt_menu(stdscr, "Choose your starter Pokémon:", starter_options)
    if starter_idx is None:
        return False

    starter_names = ["Bulbasaur", "Charmander", "Squirtle"]
    starter_ids = [1, 4, 7]
    starter_id = starter_ids[starter_idx]
    starter_name = starter_names[starter_idx]
    shinytag = True if random.randint(1,4096) == 1 else False

    if show_dialogue:
        show_dialogue(stdscr, [
            f"Excellent choice! {starter_name} is a fine Pokémon.",
            "Use Z to confirm selections, X to cancel, C for menu,",
            "and Arrow keys to move around the world.",
            "In battle, use Z to select a move and X to return.",
            "Moves descriptions can be viewed by pressing C on the move.",
        ])

    player_name = player_name or "Jeff"
    rival_name = rival_name or "Malfoy"
    data = overworld.copy.deepcopy(overworld.DEFAULT_SAVE)
    data["player"]["name"] = player_name
    data["player"]["rival"] = rival_name
    starter_mon = {
        "rotation": 1,
        "id": starter_id,
        "name": starter_name,
        "moves": [340],
        "level": 5,
        "exp": 0,
        "maxexp": 125,
        "shiny": shinytag,
        "ability": overworld.default_mon_ability(starter_id),
        "held_item": None,
    }
    data["pokemon"] = [starter_mon]
    data["pokedex"]["seen"] = [starter_id]
    data["pokedex"]["caught"] = []
    data["pokedex"]["seen_shiny"] = []
    data["pokedex"]["caught_shiny"] = []

    overworld.save_game(data)
    overworld.reset_game_state(data)

    if show_dialogue:
        show_dialogue(stdscr, [
            f"All set, {player_name}! Your adventure begins now.",
            "Good luck out there!",
        ])

    return True


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
