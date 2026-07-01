import os
import sys

def find_project_root(start_path=None):
    if start_path is None:
        script_path = os.path.abspath(__file__)
    else:
        script_path = os.path.abspath(start_path)
    current = os.path.dirname(script_path)
    
    max_depth = 10
    depth = 0
    while current != os.path.dirname(current) and depth < max_depth:
        stats_exists = os.path.exists(os.path.join(current, "stats.py"))
        main_exists = os.path.exists(os.path.join(current, "main.py"))
        data_exists = os.path.exists(os.path.join(current, "data", "pokedata.json"))
        
        if stats_exists and main_exists and data_exists:
            return current
        current = os.path.dirname(current)
        depth += 1
    
    return os.path.dirname(script_path)

PROJECT_ROOT = find_project_root()
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import stats
import curses
import time
import fightui
import overworld
import mysterygift
import cutscene
import subprocess

if not getattr(mysterygift, "REQUESTS_AVAILABLE", True):
    print("Tip: install 'requests' to enable Mystery Gift (recommended): pip install requests or pip3 install requests")
    time.sleep(2)
    try:
        cols = os.get_terminal_size().columns
        print('\n' + ('-' * cols))
    except OSError:
        print('\n' + ('-' * 80))

try:
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
    try:
        curses.init_color(10, 1000, 500, 0)
        curses.init_pair(16, 10, -1) # orange (filled)
        curses.init_color(11, 900, 850, 700)
        curses.init_pair(17, 11, -1) #beige(?)
        curses.init_pair(18, curses.COLOR_BLACK, -1)
        curses.init_color(12, 600, 300, 0)
        curses.init_pair(19, 12, -1) #brown
        curses.init_pair(20, curses.COLOR_BLACK, curses.COLOR_BLACK)
        curses.init_pair(21, curses.COLOR_WHITE, curses.COLOR_WHITE)
        curses.init_color(13, 400, 800, 400)
        curses.init_pair(22, 13, -1)
        curses.init_color(14, 0, 500, 0)
        curses.init_pair(23, 14, -1)
        curses.init_color(15, 500, 700, 1000)
        curses.init_pair(24, 15, -1)
        curses.init_color(16, 0, 200, 700)
        curses.init_pair(25, 16, -1)
        curses.init_color(17, 1000, 600, 700)
        curses.init_pair(26, 17, -1)
        curses.init_color(18, 600, 0, 800)
        curses.init_pair(27, 18, -1)
        curses.init_color(19, 800, 600, 1000)
        curses.init_pair(28, 19, -1)
        curses.init_color(20, 500, 500, 500)
        curses.init_pair(29, 20, -1)
        curses.init_color(21, 250, 250, 250)
        curses.init_pair(30, 21, -1)
        curses.init_color(22, 1000, 800, 600)
        curses.init_pair(31, 22, -1)
        curses.init_color(23, 800, 600, 400)
        curses.init_pair(32, 23, -1)
        curses.init_color(24, 1000, 850, 0)
        curses.init_pair(33, 24, -1)
        curses.init_color(25, 700, 0, 0)
        curses.init_pair(34, 25, -1)
        curses.init_color(26, 0, 700, 700)
        curses.init_pair(35, 26, -1)
        curses.init_color(27, 600, 1000, 800)
        curses.init_pair(36, 27, -1)
        curses.init_color(28, 400, 200, 0)
        curses.init_pair(37, 28, -1)
        curses.init_color(29, 1000, 1000, 600)
        curses.init_pair(38, 29, -1)
    except (curses.error, OSError, ValueError):
        pass
except (curses.error, OSError):
    pass

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

def launch_tool(script_path):
    curses.endwin()
    # Resolve relative paths using PROJECT_ROOT
    if not os.path.isabs(script_path):
        full_path = os.path.join(PROJECT_ROOT, script_path)
    else:
        full_path = script_path
    subprocess.run([sys.executable, full_path])

def confirm_menu(stdscr, title, detail, warning="ALL DATA WILL BE ERASED."):
    y = 1
    options = ["No", "Yes"]

    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, title)
        stdscr.addstr(2, 0, detail)
        if warning:
            stdscr.addstr(3, 0, warning)

        for i, option in enumerate(options):
            if i == y:
                stdscr.attron(curses.color_pair(1))
                stdscr.addstr(6 + i, 0, f"> {option}")
                stdscr.attroff(curses.color_pair(1))
            else:
                stdscr.addstr(6 + i, 0, f"  {option}")

        key = stdscr.getch()

        if key == curses.KEY_UP and y > 0:
            y -= 1
        elif key == curses.KEY_DOWN and y < len(options) - 1:
            y += 1
        elif key == ord("z"):
            return y == 1
        elif key == ord("x"):
            return False


def debug_randomizer_menu(stdscr):
    y = 0
    options = [
        ("normal", "Normal", "Standard Pokémon but no restrictions on moves"),
        ("random", "Random", "Pokemon and moves are random; level is fixed at 50 ;)"),
        ("crazy_random", "Crazy Random", "Pokemon, moves, and levels roll freely. Good luck..."),
    ]

    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, "SELECT GAME MODE")

        for i, (_, label, detail) in enumerate(options):
            prefix = "> " if i == y else "  "
            if i == y:
                stdscr.attron(curses.color_pair(1))
                stdscr.addstr(2 + i, 0, f"{prefix}{label}")
                stdscr.attroff(curses.color_pair(1))
            else:
                stdscr.addstr(2 + i, 0, f"{prefix}{label}")
            stdscr.addstr(2 + i, 18, detail)

        key = stdscr.getch()

        if key == curses.KEY_UP and y > 0:
            y -= 1
        elif key == curses.KEY_DOWN and y < len(options) - 1:
            y += 1
        elif key == ord("x"):
            return None
        elif key == ord("z"):
            return options[y][0]


def overworld_save_menu(stdscr):
    y = 0

    while True:
        has_save = overworld.save_exists()
        options = ["Continue", "New Save","Back"] if has_save else ["New Save", "Back"]

        stdscr.clear()
        stdscr.addstr(0, 0, "MAIN MENU")
        stdscr.addstr(2, 0, f"Save slot: {'save.json' if has_save else 'empty'}")

        if y >= len(options):
            y = len(options) - 1

        for i, option in enumerate(options):
            if i == y:
                stdscr.attron(curses.color_pair(1))
                stdscr.addstr(4 + i, 0, f"> {option}")
                stdscr.attroff(curses.color_pair(1))
            else:
                stdscr.addstr(4 + i, 0, f"  {option}")

        key = stdscr.getch()

        if key == curses.KEY_UP and y > 0:
            y -= 1
        elif key == curses.KEY_DOWN and y < len(options) - 1:
            y += 1
        elif key == ord("x"):
            return
        elif key == ord("z"):
            choice = options[y]

            if choice == "Continue":
                overworld.reset_game_state()
                overworld.overworld(stdscr)
            elif choice == "New Save":
                if not has_save or confirm_menu(stdscr, "CREATE NEW SAVE?", "Your current save will be deleted."):
                    if cutscene.new_save_intro(stdscr):
                        overworld.overworld(stdscr)
            elif choice == "Delete Save":
                if confirm_menu(stdscr, "DELETE SAVE?", "This will delete save.json."):
                    overworld.delete_save()
                    y = 0
            elif choice == "Back":
                return

def safe_addstr(stdscr, y, x, text, color=0):
    try:
        h, w = stdscr.getmaxyx()
        if y < h and x < w:
            stdscr.addstr(y, x, str(text)[:w - x], curses.color_pair(color) if color else 0)
    except curses.error:
        pass

def draw_box(stdscr, y, x, height, width, title=""):
    safe_addstr(stdscr, y, x, "+" + "-" * (width - 2) + "+")
    for row in range(1, height - 1):
        safe_addstr(stdscr, y + row, x, "|")
        safe_addstr(stdscr, y + row, x + width - 1, "|")
    safe_addstr(stdscr, y + height - 1, x, "+" + "-" * (width - 2) + "+")
    if title:
        safe_addstr(stdscr, y, x + 2, f" {title} ")

def debug_message(stdscr, text):
    safe_addstr(stdscr, 22, 2, " " * 76)
    safe_addstr(stdscr, 22, 2, text)
    stdscr.refresh()

def prompt_text(stdscr, prompt, initial=""):
    curses.echo()
    curses.curs_set(1)
    safe_addstr(stdscr, 21, 2, " " * 76)
    safe_addstr(stdscr, 22, 2, " " * 76)
    safe_addstr(stdscr, 21, 2, prompt)
    safe_addstr(stdscr, 22, 2, f"> {initial}")
    stdscr.move(22, 4 + len(str(initial)))
    value = stdscr.getstr(22, 4, 40).decode("utf-8").strip()
    curses.noecho()
    curses.curs_set(0)
    return value if value else str(initial)

def prompt_int(stdscr, prompt, initial, min_value=None, max_value=None):
    value = prompt_text(stdscr, prompt, initial)
    try:
        number = int(value)
    except ValueError:
        debug_message(stdscr, "That needs to be a number.")
        stdscr.getch()
        return initial

    if min_value is not None:
        number = max(min_value, number)
    if max_value is not None:
        number = min(max_value, number)
    return number

def select_from_list(stdscr, items, title):
    cursor = 0
    view = 0
    while True:
        stdscr.clear()
        safe_addstr(stdscr, 0, 0, title)
        safe_addstr(stdscr, 1, 0, "#" * 40)
        visible = 18

        if view > 0:
            safe_addstr(stdscr, 3, 0, "▲")

        for i in range(visible):
            idx = view + i
            if idx >= len(items):
                break
            value_id, display = items[idx]
            prefix = "> " if idx == cursor else "  "
            safe_addstr(stdscr, 4 + i, 0, prefix + display[:78])

        if view + visible < len(items):
            safe_addstr(stdscr, 22, 0, "▼")

        stdscr.refresh()
        key = stdscr.getch()

        if key == curses.KEY_UP and cursor > 0:
            cursor -= 1
            if cursor < view:
                view = cursor
        elif key == curses.KEY_DOWN and cursor < len(items) - 1:
            cursor += 1
            if cursor >= view + visible:
                view = cursor - visible + 1
        elif key == ord("z"):
            return items[cursor][0]
        elif key == ord("x"):
            return None

def wrap_debug_text(text, width):
    words = str(text).split()
    lines = []
    line = ""

    for word in words:
        if not line:
            line = word
        elif len(line) + len(word) + 1 <= width:
            line += " " + word
        else:
            lines.append(line)
            line = word

    if line:
        lines.append(line)

    return lines or [""]

def mon_name(mon_id):
    mon = getattr(stats, f"mon{mon_id}", None)
    return mon.name.capitalize() if mon is not None else f"Mon {mon_id}"

def move_info(move_id):
    if move_id == 0:
        return "No move", "Empty move slot."

    move = getattr(stats, f"move{move_id}", None)
    if move is None:
        return f"Move {move_id}", "Unknown move id."

    return move.name.capitalize(), move.desc

def move_label(move_id):
    name, _ = move_info(move_id)
    return f"{move_id:03d} {name}"

def default_debug_mon(mon_id=1, level=5):
    stat_block = getattr(stats, f"mon{mon_id}", None)
    abilities = getattr(stat_block, "abilities", []) if stat_block is not None else []
    default_ability_id = abilities[0] if abilities else None

    return {
        "rotation": 1,
        "id": mon_id,
        "name": mon_name(mon_id).lower(),
        "moves": [340, 340, 340, 340],
        "level": level,
        "exp": 0,
        "maxexp": level * level * level,
        "ability": default_ability_id,
        "held_item": None,
    }

def normalize_debug_party(data):
    party = data.setdefault("pokemon", [])
    for i, mon in enumerate(party):
        mon.setdefault("rotation", i + 1)
        mon.setdefault("id", 1)
        mon.setdefault("name", mon_name(mon["id"]).lower())
        mon.setdefault("moves", [340, 340, 340, 340])
        while len(mon["moves"]) < 4:
            mon["moves"].append(0)
        mon["moves"] = mon["moves"][:4]
        mon.setdefault("level", 5)
        mon.setdefault("exp", 0)
        mon.setdefault("maxexp", mon["level"] * mon["level"] * mon["level"])

        # New fields for Ability + Held Item
        if "ability" not in mon:
            stat_block = getattr(stats, f"mon{mon.get('id', 1)}", None)
            abilities = getattr(stat_block, "abilities", []) if stat_block is not None else []
            mon["ability"] = abilities[0] if abilities else None

        mon.setdefault("held_item", None)

        mon["rotation"] = i + 1

def build_save_debug_rows(data):
    rows = [
        {"section": "Player", "label": "Name", "value": lambda: data["player"].get("name", ""), "kind": "name"},
    ]

    for i, mon in enumerate(data.setdefault("pokemon", [])):
        title = f"Party {i + 1}"
        rows.extend([
            {"section": title, "label": "Species", "value": lambda mon=mon: f"{mon.get('id', 1):03d} {mon_name(mon.get('id', 1))}", "kind": "mon_id", "index": i},
            {"section": title, "label": "Level", "value": lambda mon=mon: mon.get("level", 1), "kind": "mon_level", "index": i},
            {"section": title, "label": "EXP", "value": lambda mon=mon: mon.get("exp", 0), "kind": "mon_exp", "index": i},
            {"section": title, "label": "Max EXP", "value": lambda mon=mon: mon.get("maxexp", 1), "kind": "mon_maxexp", "index": i},
            {
                "section": title,
                "label": "Held Item",
                "value": lambda mon=mon: (stats.ITEMS.get(mon.get("held_item"), {}).get("name", None) or (mon.get("held_item") or "None")),
                "kind": "mon_held_item",
                "index": i,
            },
            {
                "section": title,
                "label": "Ability",
                "value": lambda mon=mon: (stats.ABILITIES.get(mon.get("ability"), {}).get("name", None) or (mon.get("ability") or "None")),
                "kind": "mon_ability",
                "index": i,
            },
        ])
        for move_i in range(4):
            rows.append({
                "section": title,
                "label": f"Move {move_i + 1}",
                "value": lambda mon=mon, move_i=move_i: move_label(mon.get("moves", [340, 340, 340, 340])[move_i]),
                "kind": "mon_move",
                "index": i,
                "move_index": move_i,
            })

    for bag in data.setdefault("inventory", []):
        for item_name in bag:
            rows.append({
                "section": "Inventory",
                "label": item_name.replace("_", " ").title(),
                "value": lambda bag=bag, item_name=item_name: bag.get(item_name, 0),
                "kind": "item",
                "bag": bag,
                "item_name": item_name,
            })

    rows.extend([
        {"section": "Flags", "label": "Picked Items", "value": lambda: len(data.get("picked_items", [])), "kind": "clear_list", "key": "picked_items"},
        {"section": "Flags", "label": "Cut Trees", "value": lambda: len(data.get("cut_trees", [])), "kind": "clear_list", "key": "cut_trees"},
    ])
    return rows

def edit_debug_row(stdscr, data, row):
    kind = row["kind"]

    if kind == "name":
        data["player"]["name"] = prompt_text(stdscr, "Player name", data["player"].get("name", "Red"))

    elif kind == "mon_id":
        mon = data["pokemon"][row["index"]]
        mon["id"] = prompt_int(stdscr, "Pokemon species id 1-151", mon.get("id", 1), 1, 151)
        mon["name"] = mon_name(mon["id"]).lower()
        # When species changes, keep ability/held_item as-is (user intent) but defaults will re-apply on normalize.

    elif kind == "mon_level":
        mon = data["pokemon"][row["index"]]
        mon["level"] = prompt_int(stdscr, "Pokemon level 1-100", mon.get("level", 1), 1, 100)
        mon["maxexp"] = max(mon.get("maxexp", 1), mon["level"] * mon["level"] * mon["level"])

    elif kind == "mon_exp":
        mon = data["pokemon"][row["index"]]
        mon["exp"] = prompt_int(stdscr, "Current EXP", mon.get("exp", 0), 0)

    elif kind == "mon_maxexp":
        mon = data["pokemon"][row["index"]]
        mon["maxexp"] = prompt_int(stdscr, "EXP needed for next level", mon.get("maxexp", 1), 1)

    elif kind == "mon_move":
        mon = data["pokemon"][row["index"]]
        while len(mon["moves"]) < 4:
            mon["moves"].append(0)
        mon["moves"][row["move_index"]] = prompt_int(stdscr, "Move id, 0 for no move", mon["moves"][row["move_index"]], 0)

    elif kind == "mon_held_item":
        mon = data["pokemon"][row["index"]]
        current = mon.get("held_item")

        held_items = []
        for item_id, entry in getattr(stats, "ITEMS", {}).items():
            if not isinstance(entry, dict):
                continue
            section = entry.get("section")
            effect = entry.get("effect")
            if section == "Held Items" or effect == "held":
                display = entry.get("name") or item_id.replace("_", " ").title()
                held_items.append((item_id, display))

        held_items.sort(key=lambda x: x[1].lower())
        items = [("NONE", "None")] + held_items

        chosen = select_from_list(stdscr, items, "Select Held Item")
        if chosen is None:
            return
        mon["held_item"] = None if chosen == "NONE" else chosen

    elif kind == "mon_ability":
        mon = data["pokemon"][row["index"]]
        current = mon.get("ability")

        abilities = []
        abilities_dict = getattr(stats, "ABILITIES", {})
        for ability_id, entry in abilities_dict.items():
            if not isinstance(entry, dict):
                continue
            display = entry.get("name") or ability_id.replace("_", " ").title()
            abilities.append((ability_id, display))

        abilities.sort(key=lambda x: x[1].lower())
        items = [("NONE", "None")] + abilities

        chosen = select_from_list(stdscr, items, "Select Ability")
        if chosen is None:
            return
        mon["ability"] = None if chosen == "NONE" else chosen

    elif kind == "item":
        row["bag"][row["item_name"]] = prompt_int(stdscr, "Item quantity", row["bag"].get(row["item_name"], 0), 0)

    elif kind == "clear_list":
        data[row["key"]] = []
        debug_message(stdscr, f"Cleared {row['label']}.")
        stdscr.getch()

def add_debug_party_mon(stdscr, data):
    party = data.setdefault("pokemon", [])
    if len(party) >= 6:
        debug_message(stdscr, "Party is full.")
        stdscr.getch()
        return

    mon_id = prompt_int(stdscr, "New Pokemon species id 1-151", 1, 1, 151)
    level = prompt_int(stdscr, "New Pokemon level 1-100", 5, 1, 100)
    party.append(default_debug_mon(mon_id, level))
    normalize_debug_party(data)

def delete_debug_party_mon(stdscr, data, row):
    if not row or "index" not in row:
        return
    party = data.get("pokemon", [])
    index = row["index"]
    if 0 <= index < len(party):
        removed = party.pop(index)
        normalize_debug_party(data)
        debug_message(stdscr, f"Removed {removed.get('name', 'Pokemon')}.")
        stdscr.getch()

def draw_save_debug_menu(stdscr, rows, selected, top, dirty, data):
    stdscr.clear()
    draw_box(stdscr, 0, 0, 3, 80, " Save Debug ")
    safe_addstr(stdscr, 1, 2, "save.json editor")
    safe_addstr(stdscr, 1, 56, "UNSAVED" if dirty else "saved", 7 if dirty else 4)

    draw_box(stdscr, 3, 0, 18, 49, " Values ")
    draw_box(stdscr, 3, 49, 18, 31, " Details ")

    visible = rows[top:top + 14]
    last_section = None
    screen_y = 4
    for i, row in enumerate(visible):
        if row["section"] != last_section:
            safe_addstr(stdscr, screen_y, 2, row["section"], 3)
            screen_y += 1
            last_section = row["section"]

        row_index = top + i
        marker = ">" if row_index == selected else " "
        line = f"{marker} {row['label']:<16} {str(row['value']()):>22}"
        if row_index == selected:
            stdscr.attron(curses.color_pair(1))
            safe_addstr(stdscr, screen_y, 2, line[:44])
            stdscr.attroff(curses.color_pair(1))
        else:
            safe_addstr(stdscr, screen_y, 2, line[:44])
        screen_y += 1
        if screen_y >= 20:
            break

    selected_row = rows[selected] if rows else None
    if selected_row:
        safe_addstr(stdscr, 5, 52, selected_row["section"], 3)
        safe_addstr(stdscr, 7, 52, selected_row["label"])
        safe_addstr(stdscr, 8, 52, str(selected_row["value"]())[:24])
        if selected_row["kind"] == "mon_move":
            mon = data["pokemon"][selected_row["index"]]
            move_id = mon.get("moves", [0, 0, 0, 0])[selected_row["move_index"]]
            _, desc = move_info(move_id)
            for i, line in enumerate(wrap_debug_text(desc, 24)[:4]):
                safe_addstr(stdscr, 10 + i, 52, line)

        safe_addstr(stdscr, 14, 52, f"Party: {len(data.get('pokemon', []))}/6")
        safe_addstr(stdscr, 15, 52, "Z edit/action")
        safe_addstr(stdscr, 16, 52, "C create party mon")
        safe_addstr(stdscr, 17, 52, "Del delete party mon")
        safe_addstr(stdscr, 18, 52, "S save")
        safe_addstr(stdscr, 19, 52, "X back")

    safe_addstr(stdscr, 21, 2, "UP/DOWN move  Z edit  C create mon  Delete remove mon  S save  X back")
    stdscr.refresh()

def save_debug_menu(stdscr):
    curses.curs_set(0)
    stdscr.keypad(True)

    data = overworld.load_save()
    normalize_debug_party(data)
    rows = build_save_debug_rows(data)
    selected = 0
    top = 0
    dirty = False

    while True:
        rows = build_save_debug_rows(data)
        selected = min(selected, max(0, len(rows) - 1))
        if selected < top:
            top = selected
        elif selected >= top + 14:
            top = selected - 13

        draw_save_debug_menu(stdscr, rows, selected, top, dirty, data)
        key = stdscr.getch()

        if key == curses.KEY_UP and selected > 0:
            selected -= 1
        elif key == curses.KEY_DOWN and selected < len(rows) - 1:
            selected += 1
        elif key == ord("z") and rows:
            edit_debug_row(stdscr, data, rows[selected])
            normalize_debug_party(data)
            dirty = True
        elif key == ord("c"):
            add_debug_party_mon(stdscr, data)
            dirty = True
        elif key in (curses.KEY_DC, curses.KEY_BACKSPACE, 127, 8) and rows:
            delete_debug_party_mon(stdscr, data, rows[selected])
            dirty = True
        elif key == ord("s"):
            overworld.save_game(data)
            overworld.reset_game_state(data)
            dirty = False
            debug_message(stdscr, "Saved save.json.")
            stdscr.getch()
        elif key == ord("x"):
            if dirty and not confirm_menu(stdscr, "DISCARD UNSAVED DEBUG CHANGES?", "Save debug edits have not been saved.", "Your save file on disk will not change."):
                continue
            return

def mainm(stdscr):
    import fightui
    curses.curs_set(0)
    stdscr.keypad(True)
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_BLUE, -1)
 
    menu = [
        "MENU OPTIONS",
        " [-Start Game (Unfinished)-]",
        " [---------Settings--------]",
        " [----------Battle---------]",
    ]

    y = 1

    while True:
        stdscr.clear()
        for i in range(len(menu)):
            text = menu[i] if i == 0 else menu[i]
            if i == y:
                stdscr.attron(curses.color_pair(1))
                stdscr.addstr(i * 1, 0, f"> {text}")
                stdscr.attroff(curses.color_pair(1))
            else:
                stdscr.addstr(i * 1, 0, f"  {text}")

        key = stdscr.getch()

        if key == curses.KEY_UP and y > 1:
            y -= 1
        elif key == curses.KEY_DOWN and y < len(menu) - 1:
            y += 1
        elif key == ord("c"):
            cutscene.show_readme(stdscr)
        elif key == ord("z"):
            if y == 2:
                setting(stdscr)
            elif y == 1:
                overworld_save_menu(stdscr)
            elif y == 3:
                import fightui
                randomizer_mode = debug_randomizer_menu(stdscr)
                if randomizer_mode is not None:
                    fightui.battle_setup(stdscr, randomizer_mode)
        elif key == ord("d"):
            debugmainm(stdscr)

def debugmainm(stdscr):
    import fightui
    curses.curs_set(0)
    stdscr.keypad(True)
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_BLUE, -1)

    menu = [
        "-->POKETHON<--",
        "Start Game",
        "Debug Battle",
        "Pokedex",
        "Settings",
        "Mystery Gift",
        "Save Debug",
        "GUI Map Editor (will close this game)",
        "GUI Sprite Editor (will close this game)",
        "Update Log(placeholder, coming soon)"
    ]

    y = 1

    while True:
        stdscr.clear()
        for i in range(len(menu)):
            text = menu[i] if i == 0 else menu[i]
            if i == y:
                stdscr.attron(curses.color_pair(1))
                stdscr.addstr(i * 1, 0, f"> {text}")
                stdscr.attroff(curses.color_pair(1))
            else:
                stdscr.addstr(i * 1, 0, f"  {text}")

        key = stdscr.getch()

        if key == curses.KEY_UP and y > 1:
            y -= 1
        elif key == curses.KEY_DOWN and y < len(menu) - 1:
            y += 1
        elif key == ord("c"):
            cutscene.show_readme(stdscr)
        elif key == ord("z"):
            if y == 3:
                mon_menu(stdscr)
            elif y == 2:  
                import fightui
                randomizer_mode = debug_randomizer_menu(stdscr)
                if randomizer_mode is not None:
                    fightui.battle_setup(stdscr, randomizer_mode)
            elif y == 4:
                setting(stdscr)
            elif y == 1:
                overworld_save_menu(stdscr)
            elif y == 5:
                mysterygift.gifted(stdscr)
            elif y == 6:
                save_debug_menu(stdscr)
            elif y == 7:
                launch_tool("devtools/pokethon_level_builder.py")
            elif y == 8:
                launch_tool("devtools/sprite_editor.py")

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
            f"TEXT SPEED {textspeed:.2f}sec",
            "SET MODE (WIP)",
            "BATTLE ANIMATIONS (WIP)",
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
                
def draw_stats(stdscr, mon, start_x, sprite_side="front", variant="normal", form_label="Normal front"):
    type_pairs = {
        "Fire": 7,
        "Ground": 2,
        "Rock": 2,
        "Fighting": 5,
        "Electric": 2,
        "Bug": 4,
        "Grass": 4,
        "Water": 6,
        "Flying": 3,
        "Ice": 3,
        "Dragon": 5,
        "Psychic": 5,
        "Poison": 5,
        "Ghost": 5,
        "Dark": 18,
        "Normal": 1,
        "Steel": 1
    }

    title = mon.call().capitalize()
    safe_addstr(stdscr, 0, start_x, title)

    divider = "━" * 30
    safe_addstr(stdscr, 1, start_x, divider)

    sprite = getattr(stats, mon.name.lower(), stats.placeholder)
    sprite.draw(stdscr, sprite_side, variant, start_y=2, start_x=start_x)

    type1 = mon.type.capitalize()
    type2 = "" if not mon.type2 or mon.type2 == "nil" else mon.type2.capitalize()

    stat_x = start_x + 28
    safe_addstr(stdscr, 2, stat_x, f"Sprite: {form_label}")
    try:
        stdscr.addstr(4, stat_x, f"{type1}", curses.color_pair(type_pairs.get(type1, 1)))
        stdscr.addstr(4, stat_x + 12, f"{type2}", curses.color_pair(type_pairs.get(type2, 1)))
    except curses.error:
        pass

    safe_addstr(stdscr, 6, stat_x, f"HP: {mon.hp}")
    safe_addstr(stdscr, 7, stat_x, f"ATK: {mon.at}")
    safe_addstr(stdscr, 8, stat_x, f"SP ATK: {mon.sp_at}")
    safe_addstr(stdscr, 9, stat_x, f"DEF: {mon.de}")
    safe_addstr(stdscr, 10, stat_x, f"SP DEF: {mon.sp_de}")
    safe_addstr(stdscr, 11, stat_x, f"SPD: {mon.spd}")

    safe_addstr(stdscr, 14, start_x, "Description")
    desc = getattr(mon, "description", getattr(mon, "desc", "No Pokédex description available."))
    for i, line in enumerate(wrap_debug_text(desc, 48)[:5]):
        safe_addstr(stdscr, 16 + i, start_x, line)

def mon_menu(stdscr):
    curses.curs_set(0)
    stdscr.keypad(True)

    scrollno = 0
    cursor = 0
    sprite_index = 0

    while True:
        stdscr.clear()
        h, w = stdscr.getmaxyx()
        list_width = 27
        detail_x = list_width + 3
        visible = max(1, min(TOTAL, h - 2))
        cursor = min(cursor, visible - 1)

        # LEFT SIDE (list)
        for i in range(visible):
            idx = scrollno + i
            if idx >= TOTAL:
                break

            dexno = idx + 1
            name = mons[idx].call().capitalize()
            line = f"{dexno:03d} {name}"

            if i == cursor:
                safe_addstr(stdscr, i, 0, f"> {line}"[:list_width - 1])
            else:
                safe_addstr(stdscr, i, 0, f"  {line}"[:list_width - 1])

        for y in range(0, h - 1):
            safe_addstr(stdscr, y, list_width, "|")

        # RIGHT SIDE (stats)
        selected_idx = scrollno + cursor
        if selected_idx < TOTAL:
            sprite_options = overworld.pokedex_sprite_options(selected_idx + 1, include_all_shiny=True)
            sprite_index %= len(sprite_options)
            sprite_side, variant, form_label = sprite_options[sprite_index]
            draw_stats(stdscr, mons[selected_idx], detail_x, sprite_side, variant, form_label)

        safe_addstr(stdscr, h - 1, 0, "Left/right = sprite, X = back")

        key = stdscr.getch()

        if key == curses.KEY_UP:
            if cursor > 0:
                cursor -= 1
            elif scrollno > 0:
                scrollno -= 1

        elif key == curses.KEY_DOWN:
            if cursor < visible - 1 and scrollno + cursor + 1 < TOTAL:
                cursor += 1
            elif scrollno + visible < TOTAL:
                scrollno += 1
        elif key == curses.KEY_LEFT:
            sprite_index = (sprite_index - 1) % 4
        elif key == curses.KEY_RIGHT:
            sprite_index = (sprite_index + 1) % 4

        elif key == ord("x"):
            break

        stdscr.refresh()
    
def main(stdscr):
    height, width = stdscr.getmaxyx()

    if height != 24 or width != 80:
        stdscr.clear()
        safe_addstr(stdscr, 0, 0, "For best results, run at 80x24.", color=0)
        safe_addstr(stdscr, 1, 0, f"Current Size: {height} x {width}", color=0)
        safe_addstr(stdscr, 3, 0, "Continuing anyway...", color=0)
        stdscr.refresh()
        curses.napms(600)

    stdscr.addstr(0, 0, "Size is correct, Loading...")
    stdscr.refresh()
    curses.napms(120)
    cutscene.title_screen(stdscr)
    mainm(stdscr)

while True:
    curses.wrapper(main)

#test
print("hi")
print(stats.mon1.call())
import curses

#unused dingusss
"""
       █████████
    █████#####█████
  ███#############███
 ███#####█████#####███
 █████████   █████████
 ███     █████     ███
  ███             ███
    █████     █████
       █████████
"""
"""
      █████████
    █████#####█████
 ███#############███
███#####█████#####███
█████████   █████████
███     █████     ███
 ███             ███
   █████     █████
       █████████
"""
"""
           █████████
        █████#####█████
      ███#############███
     ███#####█████#####███
    █████████   █████████
    ███     █████     ███
     ███             ███
      █████     █████
         █████████
"""
