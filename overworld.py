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
        "name": "Player",
        "money": 1000
    },
    "pokedex": {
        "seen": [],
        "caught": []
    }
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

#placeholder stuff
name = "Red"
tmlist= ("")
pp= [ 
    {1,1,1,1}
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
hpstorage = [-1,-1]
TEXT_SPEED = 0.02
class MonOver:
    def __init__(self,rotation, id, name, moves, level, exp, maxexp):
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
    
    def menu(self):
        return f"{self.name} -- [HP {'FULL' if hpstorage[0] == -1 else hpstorage[0]}] -- [ EXP {self.exp}/{self.maxexp} LVL {self.level}]"
    
    def expgain(self,stdscr, gainedexp):
        self.exp += gainedexp
        if self.exp >= self.maxexp:
            show_dialogue(stdscr, ["Level Up!"])
            self.exp=0
            self.level+=1

Mon1 = MonOver(
    rotation=1,
    id=1,
    name="Bulbasaur",
    moves=[340,340,340,340],
    level=5,
    exp=67,
    maxexp=69,
)

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
        "player": {
            "name": name
        },
        "pokemon": [
            Mon1.to_dict()
        ],
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
    hpstorage[0] = -1
    fightui.pplist = [-1,-1,-1,-1]
def create_rooms():
    # ROOM 1
    npcs1 = {
        (2, 5): (NPC_ICON, ["hello!", "welcome to room 1"]),
        (2, 6): (NURSE, ["healing...",lambda: heal_player(), "done!"]),
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

    grass2 = {(6,6), (6,7), (7,6), (7,7)}

    room2 = Room(20, 10, npcs2, grass2)

    room1.doors[(0, 10)] = (room2, 9, 10)
    room2.doors[(9, 10)] = (room1, 0, 10)

    return room1
def menu(stdscr): 
    h, w = stdscr.getmaxyx()
    safe_addstr(stdscr, 10, 0, "+" + "━"*78 + "+") 
    safe_addstr(stdscr, 11, 0, Mon1.menu()) 
    safe_addstr(stdscr, 18, 0, datetime.datetime.now())
    safe_addstr(stdscr, 21, 0, "+" + "━"*78 + "+") 
    stdscr.refresh()

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
            for dy, dx in [(-1,0),(1,0),(0,-1),(0,1)]:
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
                    Mon1.expgain(stdscr, 9)

def save_menu(stdscr):#options menu but only save for now 
    curses.curs_set(0)

    options = ["Save Game", "Among Us", "Options", "Pokédex", "Cancel", "M. Gift"]
    y = 0

    while True:
        h, w = stdscr.getmaxyx()
        start_x = w - 25  # right side

        # draw box
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

# load player
name = save_data["player"]["name"]

# load pokemon
loaded_mons = load_pokemon(save_data)

if loaded_mons:
    Mon1 = loaded_mons[0]  

# load inventory
inventory = save_data.get("inventory", [])

# load pp
fightui.pplist = save_data.get("pp", [-1, -1, -1, -1])