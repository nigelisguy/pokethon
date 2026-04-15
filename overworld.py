import curses
import time
import random
import battlehandler
import fightui
import datetime
import json
import os

SAVE_FILE = "save.json"

DEFAULT_SAVE = {
    "settings": {
        "textspeed": 0.01
    },
    "player": {
        "name": "placeholder!",
    },
    "pokedex": {
        "seen": [],
        "caught": []
    },
    "pokemon": [],
    "pcmons": [],
    "inventory": [
        {"potion": 5},
        {"pokeball": 5}
    ],
    "pp": [-1, -1, -1, -1]
}


def load_save():
    if not os.path.exists(SAVE_FILE):
        return DEFAULT_SAVE.copy()

    try:
        with open(SAVE_FILE, "r") as f:
            data = json.load(f)

        return merge_defaults(data, DEFAULT_SAVE)

    except (json.JSONDecodeError, IOError):
        return DEFAULT_SAVE.copy()


def save_game(data):
    temp_file = SAVE_FILE + ".tmp"

    with open(temp_file, "w") as f:
        json.dump(data, f, indent=4)

    os.replace(temp_file, SAVE_FILE)


def merge_defaults(data, default):
    """fills missing keys safely"""
    for key, value in default.items():
        if key not in data:
            data[key] = value
        elif isinstance(value, dict):
            merge_defaults(data[key], value)
    return data


name = "Red"
tmlist = ("")
pp = [
    {1, 1, 1, 1}
]
inventory = [
    {"potion": 1},
    {"fullheal": 1},
    {"pokeball": 5},
    {"XATTACK idk": 67}
]

PLAYER = "@"
GRASS = "#"
NURSE = "♥"
ENEMY = "☺"
POKEMON = "█"
NPC_ICON = "☺"
hpstorage = [-1, -1, -1, -1, -1, -1]
last_battle_slot = 0
TEXT_SPEED = 0.02


class MonOver:
    def __init__(self, rotation, id, name, moves, level, exp, maxexp):
        self.ord = rotation
        self.id = id
        self.name = name
        self.moves = moves
        self.level = level
        self.exp = exp
        self.maxexp = maxexp

    def to_dict(self):
        return {
            "rotation": self.ord,
            "id": self.id,
            "name": self.name,
            "moves": self.moves,
            "level": self.level,
            "exp": self.exp,
            "maxexp": self.maxexp
        }

    def menu(self, hp_value=-1, slot_number=None):
        hp_text = "HEALED!" if hp_value == -1 else hp_value
        prefix = f"{slot_number}. " if slot_number is not None else "" #idk might use in future
        return f"{self.name:^12} -- [HP {hp_text:^3}] -- [ EXP {self.exp:^4}/{self.maxexp:^4} LVL {self.level:^3}]"

    def expgain(self, stdscr, gainedexp):
        show_dialogue(stdscr, [f"{self.name} gained {gainedexp} EXP!"])
        self.exp += gainedexp
        while self.exp >= self.maxexp:
            self.exp -= self.maxexp
            self.level += 1
            show_dialogue(stdscr, [f"{self.name} leveled up to LVL {self.level}!"])

    def copy(self):
        return MonOver(
            rotation=self.ord,
            id=self.id,
            name=self.name,
            moves=list(self.moves),
            level=self.level,
            exp=self.exp,
            maxexp=self.maxexp
        )


DEFAULT_PARTY = [
    MonOver(rotation=1, id=1, name="Bulbasaur", moves=[340, 340, 340, 340], level=5, exp=67, maxexp=69),
    MonOver(rotation=2, id=5, name="boy", moves=[340, 340, 340, 340], level=5, exp=67, maxexp=69),
    MonOver(rotation=3, id=9, name="Mewing", moves=[340, 340, 340, 340], level=5, exp=67, maxexp=69),
    MonOver(rotation=4, id=1, name="Bulbasaur", moves=[340, 340, 340, 340], level=5, exp=67, maxexp=69),
    MonOver(rotation=5, id=1, name="Bulbasaur", moves=[340, 340, 340, 340], level=5, exp=67, maxexp=69),
    MonOver(rotation=6, id=1, name="Bulbasaur", moves=[340, 340, 340, 340], level=5, exp=67, maxexp=69),
]

party_mons = [mon.copy() for mon in DEFAULT_PARTY]


def ensure_hpstorage_size(size=6):
    while len(hpstorage) < size:
        hpstorage.append(-1)
    if len(hpstorage) > size:
        del hpstorage[size:]


def normalize_party():
    global party_mons
    party_mons = [mon for mon in party_mons if mon is not None][:6]
    while len(party_mons) < 6:
        default_index = len(party_mons)
        party_mons.append(DEFAULT_PARTY[default_index].copy())


def sync_party_slots():
    global Mon1, Mon2, Mon3, Mon4, Mon5, Mon6
    normalize_party()
    Mon1, Mon2, Mon3, Mon4, Mon5, Mon6 = party_mons[:6]


def get_party():
    return party_mons[:6]


def get_party_mon(index):
    if 0 <= index < len(party_mons):
        return party_mons[index]
    return None


def reorder_party(old_index, new_index):
    if not (0 <= old_index < len(party_mons) and 0 <= new_index < len(party_mons)):
        return

    mon = party_mons.pop(old_index)
    party_mons.insert(new_index, mon)

    hp = hpstorage.pop(old_index)
    hpstorage.insert(new_index, hp)

    sync_party_slots()


sync_party_slots()


class Room:
    def __init__(self, width, height, npcs=None, grass_tiles=None, doors=None):
        self.width = width
        self.height = height
        self.npcs = npcs or {}
        self.grass_tiles = grass_tiles or set()
        self.doors = doors or {}


def safe_addstr(stdscr, y, x, text):
    try:
        h, w = stdscr.getmaxyx()
        if y < h and x < w:
            stdscr.addstr(y, x, str(text)[:w - x])
    except curses.error:
        pass


def type_text(stdscr, text):
    h, w = stdscr.getmaxyx()
    stdscr.move(h - 2, 2)
    stdscr.clrtoeol()

    for char in text:
        stdscr.addstr(char)
        stdscr.refresh()
        time.sleep(TEXT_SPEED)


def build_save():
    return {
        "settings": {
            "textspeed": 0.01
        },
        "player": {
            "name": name
        },
        "pokedex": {
            "seen": [],
            "caught": []
        },
        "pokemon": [mon.to_dict() for mon in get_party()],
        "pcmons": [],
        "inventory": inventory,
        "pp": fightui.pplist
    }


def show_dialogue(stdscr, lines):
    h, w = stdscr.getmaxyx()

    for line in lines:
        if callable(line):
            line()
            continue

        safe_addstr(stdscr, h - 3, 0, "╔" + "═" * (w - 2) + "╗")
        safe_addstr(stdscr, h - 2, 0, "║" + " " * (w - 2) + "║")
        safe_addstr(stdscr, h - 1, 0, "╚" + "═" * (w - 2) + "╝")

        type_text(stdscr, line)

        while True:
            key = stdscr.getch()
            if key == ord("z"):
                break

    stdscr.clear()


def draw(stdscr, room, py, px):
    stdscr.clear()

    for y in range(room.height):
        for x in range(room.width):
            char = "෴"
            color = curses.color_pair(4)

            if (y, x) in room.grass_tiles:
                char = GRASS

            if (y, x) in room.npcs:
                char = room.npcs[(y, x)][0]
                color = curses.color_pair(6)

            if (y, x) in room.doors:
                char = "D"
                color = curses.color_pair(5)

            if y == py and x == px:
                char = PLAYER
                color = curses.color_pair(7)

            stdscr.addstr(y, x * 2, char, color)

    stdscr.refresh()


def heal_player():
    ensure_hpstorage_size()
    for i in range(6):
        hpstorage[i] = -1
    fightui.pplist = [-1, -1, -1, -1]


def create_rooms():
    npcs1 = {
        (2, 5): (NPC_ICON, ["hello!", "welcome to room 1"]),
        (2, 6): (NURSE, ["healing...", lambda: heal_player(), "done!"]),
    }

    grass1 = set()
    for y in range(5, 10):
        for x in range(5, 10):
            grass1.add((y, x))

    room1 = Room(20, 10, npcs1, grass1)

    npcs2 = {
        (1, 1): (NPC_ICON, ["you made it to room 2"]),
        (3, 3): (ENEMY, ["jdvb hcc hcdhcbhcbdh"]),
    }

    grass2 = {(6, 6), (6, 7), (7, 6), (7, 7)}

    room2 = Room(20, 10, npcs2, grass2)

    room1.doors[(0, 10)] = (room2, 9, 10)
    room2.doors[(9, 10)] = (room1, 0, 10)

    return room1


def draw_party_panel(stdscr, selected_index=None, moving_index=None):
    safe_addstr(stdscr, 10, 0, "+" + "━" * 78 + "+")
    for index, mon in enumerate(get_party()):
        hp_value = hpstorage[index] if index < len(hpstorage) else -1
        marker = ">"
        if moving_index == index:
            marker = "?"
        elif selected_index != index:
            marker = " "

        safe_addstr(stdscr, 11 + index, 0, f"{marker} {mon.menu(hp_value, index + 1)}")

    now = datetime.datetime.now()
    date_str = now.strftime("%d %B, %Y - %H:%M:%S")
    safe_addstr(stdscr, 18, 0, date_str)
    safe_addstr(stdscr, 21, 0, "+" + "━" * 78 + "+")


def menu(stdscr):
    draw_party_panel(stdscr)
    stdscr.refresh()


def party_menu(stdscr):
    selected = 0
    moving = None

    while True:
        draw(stdscr, create_rooms(), -100, -100)
        draw_party_panel(stdscr, selected_index=selected, moving_index=moving)
        safe_addstr(stdscr, 22, 0, "IN PARTY MENU")
        stdscr.refresh()

        key = stdscr.getch()

        if key == curses.KEY_UP and selected > 0:
            selected -= 1
        elif key == curses.KEY_DOWN and selected < len(get_party()) - 1:
            selected += 1
        elif key == ord("x"):
            return
        elif key == ord("z"):
            if moving is None:
                moving = selected
            else:
                reorder_party(moving, selected)
                moving = None
                selected = min(selected, len(get_party()) - 1)


def overworld(stdscr):
    curses.curs_set(0)
    stdscr.keypad(True)
    curses.start_color()

    current_room = create_rooms()
    py, px = 0, 0

    while True:
        draw(stdscr, current_room, py, px)
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

        if 0 <= ny < current_room.height and 0 <= nx < current_room.width:
            if (ny, nx) not in current_room.npcs:
                py, px = ny, nx

        if (py, px) in current_room.doors:
            current_room, py, px = current_room.doors[(py, px)]

        if key == ord("z"):
            for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                check = (py + dy, px + dx)
                if check in current_room.npcs:
                    show_dialogue(stdscr, current_room.npcs[check][1])

        if key == ord("c"):
            save_menu(stdscr)

        if (py, px) in current_room.grass_tiles:
            if random.random() < 0.2:
                show_dialogue(stdscr, ["A wild Pokémon appeared!"])
                result = battlehandler.run_battle(stdscr, 1)
                if result == "win":
                    active_mon = get_party_mon(last_battle_slot)
                    if active_mon is not None:
                        active_mon.expgain(stdscr, 9)


def save_menu(stdscr):
    curses.curs_set(0)

    options = ["Save Game", "Pokémon", "Options", "Pokédex", "Cancel", "M. Gift"]
    y = 0

    while True:
        h, w = stdscr.getmaxyx()
        start_x = w - 25

        for i in range(6):
            stdscr.addstr(i, start_x, " " * 24)

        stdscr.addstr(0, start_x, " OPTIONS MENU ")

        for i, opt in enumerate(options):
            if i == y:
                stdscr.addstr(i + 2, start_x, f"> {opt}")
            else:
                stdscr.addstr(i + 2, start_x, f"  {opt}")

        stdscr.refresh()
        key = stdscr.getch()

        if key == curses.KEY_UP and y > 0:
            y -= 1
        elif key == curses.KEY_DOWN and y < len(options) - 1:
            y += 1
        elif key == ord("z"):
            if y == 0:
                data = build_save()
                save_game(data)
                show_dialogue(stdscr, ["Game Saved!"])
                break
            elif y == 1:
                party_menu(stdscr)
                current_room = create_rooms()
                break
            else:
                break
        elif key == ord("x"):
            break


def load_pokemon(data):
    mons = []

    for mon_data in data.get("pokemon", []):
        mon = MonOver(
            rotation=mon_data["rotation"],
            id=mon_data["id"],
            name=mon_data["name"],
            moves=mon_data["moves"],
            level=mon_data["level"],
            exp=mon_data["exp"],
            maxexp=mon_data["maxexp"]
        )
        mons.append(mon)

    return mons


save_data = load_save()

name = save_data["player"]["name"]

loaded_mons = load_pokemon(save_data)

if loaded_mons:
    party_mons = loaded_mons[:6]
else:
    party_mons = [mon.copy() for mon in DEFAULT_PARTY]

inventory = save_data.get("inventory", [])

fightui.pplist = save_data.get("pp", [-1, -1, -1, -1])
ensure_hpstorage_size()
sync_party_slots()
