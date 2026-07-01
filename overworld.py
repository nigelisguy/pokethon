import curses
import time
import random
import battlehandler
import fightui
import stats
import datetime
import json
import os
import copy

SAVE_FILE = "save.json"

def mon_name(mon_id):
    mon = getattr(stats, f"mon{mon_id}", None)
    return mon.name.capitalize() if mon is not None else f"Mon {mon_id}"
pc_boxes = [
    [] 
]
current_box = 0
BOX_SIZE = 30

DEFAULT_SAVE = {
    "settings": {
        "textspeed": 0.01
    },
    "player": {
        "name": "placeholder!",
    },
    "location": {
        "room_id": "map1",
        "y": 0,
        "x": 0
    },
    "pokedex": {
        "seen": [],
        "caught": [],
        "seen_shiny": [],
        "caught_shiny": []
    },
    "pokemon": [],
    "pcmons": [[]],
    "inventory": [
        {"potion": 5},
        {"pokeball": 5},
        {"tera_orb": 1}
    ],
    "money": 3000,
    "picked_items": [],
    "cut_trees": [],
    "battled_trainers": [],
    "pp": [-1, -1, -1, -1],
    "tera_orb_charged": True,
    "pcmons": [[mon.to_dict() for mon in box] for box in pc_boxes]
}


def load_save():
    if not os.path.exists(SAVE_FILE):
        return copy.deepcopy(DEFAULT_SAVE)

    try:
        with open(SAVE_FILE, "r") as f:
            data = json.load(f)

        return merge_defaults(data, copy.deepcopy(DEFAULT_SAVE))
    

    except (json.JSONDecodeError, IOError):
        return copy.deepcopy(DEFAULT_SAVE)
    


def save_game(data):
    temp_file = SAVE_FILE + ".tmp"
    with open(temp_file, "w") as f:
        json.dump(data, f, indent=4)

    os.replace(temp_file, SAVE_FILE)


def save_exists():
    return os.path.exists(SAVE_FILE)


def delete_save():
    if os.path.exists(SAVE_FILE):
        os.remove(SAVE_FILE)
    reset_game_state(copy.deepcopy(DEFAULT_SAVE))


def create_new_save():
    data = copy.deepcopy(DEFAULT_SAVE)
    save_game(data)
    reset_game_state(data)


def merge_defaults(data, default):
    for key, value in default.items():
        if key not in data:
            data[key] = value
        elif isinstance(value, dict):
            merge_defaults(data[key], value)
    return data


name = "Red"
tmlist = ("")
pp = [1, 1, 1, 1]
PLAYER = "@"
GRASS = "#"
WATER = "~"
ITEM = "●"
CUT_TREE = "▲"
REAL_TREE = "⬜"
ICE = "❄"
BLOCK = "◼"
HILL_CHARS = {
    "up": "↑",
    "down": "↓",
    "left": "←",
    "right": "→",
}
HILL_COLOR_PAIR = 16
HILL_COLOR = 16
LEGENDARY = "M"
NURSE = "♥"
ENEMY = "☺"
POKEMON = "#"
NPC_ICON = "☺"
hpstorage = [-1, -1, -1, -1, -1, -1]
last_battle_slot = 0
TEXT_SPEED = 0.02
battled_trainers = set()
picked_items = set()
cut_trees = set()
money = 3000
pokedex_seen = set()
pokedex_caught = set()
pokedex_seen_shiny = set()
pokedex_caught_shiny = set()
LEVEL_UP_DATA = {}


def load_level_up_data():
    path = os.path.join(os.path.dirname(__file__), "data", "levellingup.json")
    if not os.path.exists(path):
        return {}

    try:
        with open(path, "r") as f:
            data = json.load(f)
    except (json.JSONDecodeError, IOError):
        return {}

    return data.get("pokemon", data) if isinstance(data, dict) else {}


def level_up_entry(mon_id):
    return LEVEL_UP_DATA.get(str(mon_id), {})


def move_name(move_id):
    move = getattr(stats, f"move{move_id}", None)
    return move.name.capitalize() if move is not None else f"Move {move_id}"


def normalize_move_slots(moves):
    normalized = []
    for move_id in moves:
        try:
            move_id = int(move_id)
        except (TypeError, ValueError):
            continue

        if move_id > 0:
            normalized.append(move_id)

    return normalized[:4]


def reset_pp_slot(slot):
    while len(fightui.pplist) <= slot:
        fightui.pplist.append(-1)
    fightui.pplist[slot] = -1


LEVEL_UP_DATA = load_level_up_data()


# NPC Preset Dialogue
NPC_PRESETS = {
    "pokemon_centre_lady": (
        "♥",
        [
            "Welcome to the Pokémon Center!",
            "We'll heal your Pokémon back to full health.",
            "HEAL_PLAYER",
            "Your Pokémon are all healed!",
        ],
    ),
    "shop_keeper": (
        "☺",
        ["Welcome to the Poké Mart!"],
        "SHOP",
    ),
    "trainer": (
        "☺",
        ["Let's battle!"],
        0,  # trainer_id will be set when placing
    ),
}


def default_mon_ability(mon_id):
    stat_block = getattr(stats, f"mon{mon_id}", None)
    abilities = getattr(stat_block, "abilities", []) if stat_block is not None else []
    return abilities[0] if abilities else None


class MonOver:
    def __init__(self, rotation, id, name, moves, level, exp, maxexp=-1, shiny=False, ability=None, held_item=None, tera_type=None):
        self.ord = rotation
        self.id = id
        self.name = name
        self.moves = normalize_move_slots(moves)
        self.level = level
        self.exp = exp
        self.shiny = shiny
        self.ability = ability if ability is not None else default_mon_ability(id)
        self.held_item = held_item
        # tera_type: if None, defaults to the mon's primary type when BattleMon is created
        self.tera_type = tera_type
        if maxexp == -1:
            self.maxexp = level*level*level
        else:
            self.maxexp = maxexp

    def to_dict(self):
        return {
            "rotation": self.ord,
            "id": self.id,
            "name": self.name,
            "moves": self.moves,
            "level": self.level,
            "exp": self.exp,
            "maxexp": self.maxexp,
            "shiny": self.shiny,
            "ability": self.ability,
            "held_item": self.held_item,
            "tera_type": self.tera_type
        }

    def menu(self, hp_value=-1, slot_number=None):
        base_stats = getattr(stats, f"mon{self.id}")
        max_hp = int(((2 * base_stats.hp * self.level) / 100) + self.level + 10)
        current_hp = max_hp if hp_value == -1 else hp_value
        current_hp = max(0, min(current_hp, max_hp))
        bar_length = 10
        hp_filled = int((current_hp / max_hp) * bar_length) if max_hp > 0 else 0
        hp_bar = "█" * hp_filled + "░" * (bar_length - hp_filled)
        exp_filled = int((self.exp / self.maxexp) * bar_length) if self.maxexp > 0 else 0
        exp_filled = max(0, min(exp_filled, bar_length))
        exp_bar = "█" * exp_filled + "░" * (bar_length - exp_filled)
        prefix = f"{slot_number}. " if slot_number is not None else "" #idk might use in future
        shiny_marker = "✦ " if getattr(self, "shiny", False) else ""
        return (
            f"{prefix}{shiny_marker}{self.name:<10} -- [HP {current_hp:>3}/{max_hp:<3}] "
            f"[{hp_bar}] -- [EXP {exp_bar}] LVL {self.level}"
        )

    def learn_move(self, stdscr, move_id):
        try:
            move_id = int(move_id)
        except (TypeError, ValueError):
            return

        if move_id <= 0 or not hasattr(stats, f"move{move_id}"):
            return

        self.moves = normalize_move_slots(self.moves)
        if move_id in self.moves:
            return

        learned = move_name(move_id)
        if len(self.moves) < 4:
            self.moves.append(move_id)
            reset_pp_slot(len(self.moves) - 1)
            show_dialogue(stdscr, [f"{self.name} learned {learned}!"])
            return

        forgotten_id = self.moves.pop(0)
        self.moves.append(move_id)
        fightui.pplist = fightui.pplist[1:4] + [-1]
        show_dialogue(stdscr, [
            f"{self.name} learned {learned}!",
            f"It forgot {move_name(forgotten_id)}.",
        ])

    def apply_level_up_moves(self, stdscr):
        learnset = level_up_entry(self.id).get("learnset", {})
        for move_id in learnset.get(str(self.level), []):
            self.learn_move(stdscr, move_id)

    def try_evolve(self, stdscr):
        evolution = level_up_entry(self.id).get("evolution")
        if not isinstance(evolution, dict):
            return

        try:
            evolve_level = int(evolution.get("level", 0))
            evolved_id = int(evolution.get("into", 0))
        except (TypeError, ValueError):
            return

        if evolve_level <= 0 or evolved_id <= 0 or self.level < evolve_level:
            return

        evolved_stats = getattr(stats, f"mon{evolved_id}", None)
        if evolved_stats is None:
            return

        old_name = self.name
        self.id = evolved_id
        self.name = evolved_stats.name.capitalize()
        show_dialogue(stdscr, [f"What? {old_name} is evolving!", f"{old_name} evolved into {self.name}!"])

    def expgain(self, stdscr, gainedexp):
        show_dialogue(stdscr, [f"{self.name} gained {gainedexp} EXP!"])
        self.exp += gainedexp
        while self.exp >= self.maxexp:
            self.exp -= self.maxexp
            self.level += 1
            self.maxexp = self.level*self.level*self.level
            show_dialogue(stdscr, [f"{self.name} leveled up to LVL {self.level}!"])
            self.apply_level_up_moves(stdscr)
            self.try_evolve(stdscr)

    def copy(self):
        return MonOver(
            rotation=self.ord,
            id=self.id,
            name=self.name,
            moves=list(self.moves),
            level=self.level,
            exp=self.exp,
            maxexp=self.maxexp,
            shiny=self.shiny,
            ability=self.ability,
            held_item=self.held_item,
            tera_type=self.tera_type
        )


DEFAULT_PARTY = [
    MonOver(rotation=1, id=1, name="Bulbasaur", moves=[340], level=5, exp=0),
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


def sync_party_slots():
    global Mon1, Mon2, Mon3, Mon4, Mon5, Mon6
    normalize_party()
    party = get_party() 
    Mon1, Mon2, Mon3, Mon4, Mon5, Mon6 = party

def get_party():
    party = party_mons[:6]
    while len(party) < 6:
        party.append(None)
    return party

def get_party_mon(index):
    party = get_party()
    if 0 <= index < len(party):
        return party[index]
    return None

def add_to_party_or_pc(stdscr, mon):
    global party_mons

    if len(party_mons) < 6:
        party_mons.append(mon)
        show_dialogue(stdscr, [f"{mon.name} was added to your party!"])
    else:
        add_to_pc(mon)
        show_dialogue(stdscr, [f"Party full! {mon.name} was sent to the PC."])

    sync_party_slots()

def item_label(item_name):
    item_data = stats.ITEMS.get(item_name, {})
    if isinstance(item_data, dict) and item_data.get("name"):
        return item_data["name"]
    return item_name.replace("_", " ").title()

ITEM_DESCRIPTIONS = {
    "potion": "Restores 20 HP to one Pokemon during battle.",
    "pokeball": "A ball used to catch wild Pokemon.",
    "fullheal": "Clears all status conditions from one Pokemon.",
    "hm_cut": "Lets any Pokemon with sharp claws cut down small trees in the overworld. Not be confused with TM CUT.",
    "hm_swim": "Unlike HM Surf, this makes you walk on water. Don't ask.",
    "map": "A map of the region. ",
    "item": "an item. who would have thought.",
}

BAG_SECTIONS = [
    ("Pokeballs", {"pokeball"}),
    ("Recover", {"potion", "fullheal"}),
    ("Key Items", {"hm_cut", "hm_swim", "map"}),
    ("Held Items", set()),
    ("Other", set()),
]


def item_description(item_name):
    item_data = stats.ITEMS.get(item_name, {})
    if isinstance(item_data, dict) and item_data.get("description"):
        return item_data["description"]
    return ITEM_DESCRIPTIONS.get(item_name, "No description yet.")


def inventory_entries():
    entries = []
    for item in inventory:
        for name, quantity in item.items():
            if quantity > 0:
                entries.append((name, quantity))
    return entries


def bag_section_for_item(item_name):
    item_data = stats.ITEMS.get(item_name, {})
    if isinstance(item_data, dict) and item_data.get("section"):
        return item_data["section"]

    for section_name, section_items in BAG_SECTIONS:
        if section_name != "Other" and item_name in section_items:
            return section_name
    return "Other"


def inventory_entries_for_section(section_name):
    return [
        (name, quantity)
        for name, quantity in inventory_entries()
        if bag_section_for_item(name) == section_name
    ]


def add_item(item_name, amount=1):
    for item in inventory:
        if item_name in item:
            item[item_name] += amount
            return

    inventory.append({item_name: amount})

def has_item(item_name):
    return any(item.get(item_name, 0) > 0 for item in inventory)

def spend_money(amount):
    global money
    if money < amount:
        return False

    money -= amount
    return True

def add_money(amount):
    global money
    money += amount

def lose_blackout_money():
    global money
    lost = money // 10
    money -= lost
    return lost

def battle_spiral_animation(stdscr, room=None, py=None, px=None):
    height, width = stdscr.getmaxyx()
    if room is not None and py is not None and px is not None:
        draw(stdscr, room, py, px)
        menu(stdscr)
        stdscr.refresh()

    top, bottom = 0, height - 1
    left, right = 0, width - 1
    color = curses.color_pair(20) if curses.has_colors() else 0

    while top <= bottom and left <= right:
        for x in range(left, right + 1):
            safe_addstr(stdscr, top, x, " ", color)
            stdscr.refresh()
            time.sleep(0.0005)
        top += 1

        for y in range(top, bottom + 1):
            safe_addstr(stdscr, y, right, " ", color)
            stdscr.refresh()
            time.sleep(0.0005)
        right -= 1

        if top <= bottom:
            for x in range(right, left - 1, -1):
                safe_addstr(stdscr, bottom, x, " ", color)
                stdscr.refresh()
                time.sleep(0.0005)
            bottom -= 1

        if left <= right:
            for y in range(bottom, top - 1, -1):
                safe_addstr(stdscr, y, left, " ", color)
                stdscr.refresh()
                time.sleep(0.0005)
            left += 1

def pc_menu(stdscr):
    global current_box

    selected = 0

    while True:
        stdscr.clear()

        box = get_current_box()

        safe_addstr(stdscr, 0, 0, f"PC BOX {current_box + 1}")

        # draw mons
        for i in range(20):
            if i < len(box):
                mon = box[i]
                text = f"{i+1}. {mon.name} LVL {mon.level}"
            else:
                text = f"{i+1}. --- EMPTY ---"

            prefix = ">" if i == selected else " "
            safe_addstr(stdscr, 2 + i, 0, f"{prefix} {text}")

        safe_addstr(stdscr, 23, 0, "[Z] Select  [X] Exit  [←/→] Switch Box")

        stdscr.refresh()
        key = stdscr.getch()

        if key == curses.KEY_UP and selected > 0:
            selected -= 1
        elif key == curses.KEY_DOWN and selected < 19:
            selected += 1

        elif key == curses.KEY_LEFT:
            current_box = max(0, current_box - 1)
            selected = 0

        elif key == curses.KEY_RIGHT:
            if current_box < len(pc_boxes) - 1:
                current_box += 1
            else:
                pc_boxes.append([])
                current_box += 1
            selected = 0

        elif key == ord("x"):
            return

        elif key == ord("z"):
            if selected < len(box):
                pc_action_menu(stdscr, selected)

def pc_action_menu(stdscr, index):
    options = ["Withdraw", "Release", "Cancel"]
    choice = 0

    while True:
        stdscr.clear()

        for i, opt in enumerate(options):
            prefix = ">" if i == choice else " "
            safe_addstr(stdscr, 10 + i, 10, f"{prefix} {opt}")

        stdscr.refresh()
        key = stdscr.getch()

        if key == curses.KEY_UP and choice > 0:
            choice -= 1
        elif key == curses.KEY_DOWN and choice < len(options) - 1:
            choice += 1

        elif key == ord("z"):
            box = get_current_box()

            if choice == 0:  # withdraw
                if len(party_mons) >= 6:
                    show_dialogue(stdscr, ["Your party is full!"])
                    return

                mon = remove_from_pc(index)
                if mon:
                    party_mons.append(mon)
                    sync_party_slots()
                    show_dialogue(stdscr, [f"{mon.name} joined your party!"])
                return

            elif choice == 1:  # release
                confirm_release(stdscr, index)
                return

            else:
                return

        elif key == ord("x"):
            return

def confirm_release(stdscr, index):
    box = get_current_box()
    mon = box[index]

    choice = 0
    options = ["No", "Yes"]

    while True:
        stdscr.clear()
        safe_addstr(stdscr, 5, 5, f"Release {mon.name}?")

        for i, opt in enumerate(options):
            prefix = ">" if i == choice else " "
            safe_addstr(stdscr, 7 + i, 5, f"{prefix} {opt}")

        stdscr.refresh()
        key = stdscr.getch()

        if key == curses.KEY_UP and choice > 0:
            choice -= 1
        elif key == curses.KEY_DOWN and choice < 1:
            choice += 1

        elif key == ord("z"):
            if choice == 1:
                remove_from_pc(index)
                show_dialogue(stdscr, [f"{mon.name} was released..."])
            return

        elif key == ord("x"):
            return

def reorder_party(old_index, new_index):
    party = get_party()

    if party[old_index] is None:
        return

    mon = party.pop(old_index)
    party.insert(new_index, mon)

    # remove None entries before saving back
    global party_mons
    party_mons = [m for m in party if m is not None]

    hp = hpstorage.pop(old_index)
    hpstorage.insert(new_index, hp)

    sync_party_slots()

sync_party_slots()


class Room:
    def __init__(self, width, height, npcs=None, grass_tiles=None, water_tiles=None, hill_tiles=None, doors=None, items=None, cut_trees=None, trees=None, fog=None, room=None, legendary_mons=None, ice_tiles=None, block_tiles=None, room_id="room"):
        self.width = width
        self.height = height
        self.npcs = npcs or {}
        self.grass_tiles = grass_tiles or set()
        self.water_tiles = water_tiles or set()
        self.hill_tiles = hill_tiles or {}
        self.doors = doors or {}
        self.items = items or {}
        self.cut_trees = cut_trees or set()
        self.trees = trees or set()
        self.fog = fog or set()
        self.room = room or {}
        self.legendary_mons = legendary_mons or {}
        self.ice_tiles = ice_tiles or set()
        self.block_tiles = block_tiles or {}
        self.room_id = room_id


def safe_addstr(stdscr, y, x, text, color=None):
    try:
        h, w = stdscr.getmaxyx()
        if y < h and x < w:
            if color is not None:
                stdscr.addstr(y, x, str(text)[:w - x], color)
            else:
                stdscr.addstr(y, x, str(text)[:w - x])
    except curses.error:
        pass

def init_overworld_colors():
    try:
        curses.use_default_colors()
    except curses.error:
        pass

    hill_color = curses.COLOR_YELLOW
    if curses.has_colors() and curses.can_change_color() and curses.COLORS > HILL_COLOR:
        try:
            curses.init_color(HILL_COLOR, 1000, 500, 0)
            hill_color = HILL_COLOR
        except curses.error:
            hill_color = curses.COLOR_YELLOW

    try:
        curses.init_pair(HILL_COLOR_PAIR, hill_color, -1)
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


def build_save(current_room_id=None, py=None, px=None):
    party_data = [mon.to_dict() for mon in get_party() if mon is not None]
    location = copy.deepcopy(save_data.get("location", DEFAULT_SAVE["location"])) if isinstance(save_data, dict) else copy.deepcopy(DEFAULT_SAVE["location"])
    if current_room_id is not None:
        location = {
            "room_id": current_room_id,
            "y": py if py is not None else location.get("y", 0),
            "x": px if px is not None else location.get("x", 0),
        }

    return {
        "settings": {
            "textspeed": 0.01
        },
        "player": {
            "name": name
        },
        "location": location,
        "pokedex": {
            "seen": sorted(pokedex_seen),
            "caught": sorted(pokedex_caught),
            "seen_shiny": sorted(pokedex_seen_shiny),
            "caught_shiny": sorted(pokedex_caught_shiny)
        },
        "pokemon": party_data,
        "inventory": inventory,
        "money": money,
        "picked_items": sorted(picked_items),
        "cut_trees": sorted(cut_trees),
        "battled_trainers": sorted(battled_trainers),
        "pp": fightui.pplist,
        "tera_orb_charged": tera_orb_charged,
        "pcmons": [[mon.to_dict() for mon in box] for box in pc_boxes],
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

def npc_dialogue(npc):
    return npc[1]

def npc_trainer_id(npc):
    if len(npc) >= 3:
        action = npc[2]
        if isinstance(action, str) and action not in ["SHOP", "GIVE_ITEM"]:
            return action
    return None

def npc_action(npc):
    if len(npc) >= 3:
        action = npc[2]
        if isinstance(action, str):
            return action
        elif isinstance(action, list) and len(action) >= 1:
            return action
    return None

def map_object_id(room, pos):
    y, x = pos
    return f"{room.room_id}:{y}:{x}"

def is_blocked(room, pos):
    return (
        pos in room.npcs
        or (pos in room.water_tiles and not has_item("hm_swim"))
        or pos in room.hill_tiles
        or pos in room.trees
        or (pos in room.cut_trees and map_object_id(room, pos) not in cut_trees)
        or pos in room.block_tiles
    )

def try_push_block(room, py, px, block_pos, dy, dx):
    """Try to push a block. Returns True if successful, False otherwise."""
    new_block_pos = (block_pos[0] + dy, block_pos[1] + dx)
    ny, nx = new_block_pos
    
    # Check if new position is valid and not blocked
    if not (0 <= ny < room.height and 0 <= nx < room.width):
        return False
    if is_blocked(room, new_block_pos):
        return False
    
    # Don't allow pushing if another block is in the way
    if new_block_pos in room.block_tiles:
        return False
    
    # Move the block
    room.block_tiles[new_block_pos] = room.block_tiles.pop(block_pos)
    return True

def apply_ice_physics(room, py, px, dy, dx):
    ny, nx = py + dy, px + dx
    
    # Check if first step is out of bounds
    if not (0 <= ny < room.height and 0 <= nx < room.width):
        return (py, px)
    
    # If first step is not on ice, check if it's blocked before returning
    if (ny, nx) not in room.ice_tiles:
        if is_blocked(room, (ny, nx)):
            return (py, px)
        return (ny, nx)
    
    # First step is on ice and not blocked, now check if we need to slide
    if is_blocked(room, (ny, nx)):
        return (py, px)
    
    while True:
        next_ny, next_nx = ny + dy, nx + dx
        if not (0 <= next_ny < room.height and 0 <= next_nx < room.width):
            return (ny, nx)
    
        if (next_ny, next_nx) not in room.ice_tiles:
            if is_blocked(room, (next_ny, next_nx)):
                return (ny, nx)
            return (next_ny, next_nx)
        
        if is_blocked(room, (next_ny, next_nx)):
            return (ny, nx)
        
        ny, nx = next_ny, next_nx

def movement_direction(dy, dx):
    if dy == -1 and dx == 0:
        return "up"
    if dy == 1 and dx == 0:
        return "down"
    if dy == 0 and dx == -1:
        return "left"
    if dy == 0 and dx == 1:
        return "right"
    return None

def try_hill_jump(room, py, px, ny, nx):
    direction = room.hill_tiles.get((ny, nx))
    if direction is None:
        return None

    dy = ny - py
    dx = nx - px
    if movement_direction(dy, dx) != direction:
        return (py, px)

    landing = (ny + dy, nx + dx)
    ly, lx = landing
    if not (0 <= ly < room.height and 0 <= lx < room.width):
        return (py, px)
    if is_blocked(room, landing):
        return (py, px)

    return landing

def pickup_item(stdscr, room, pos):
    if pos not in room.items:
        return

    item_id = map_object_id(room, pos)
    if item_id in picked_items:
        return

    item_name, amount = room.items[pos]
    add_item(item_name, amount)
    picked_items.add(item_id)
    show_dialogue(stdscr, [f"Found {item_label(item_name)} x{amount}!"])

def handle_wild_battle_result(stdscr, result, remove_id=None):
    if isinstance(result, tuple) and result[0] == "caught":
        enemy = result[1]
        register_pokedex_caught(enemy.base.id, shiny=getattr(enemy, "shiny", False))

        active_mon = get_party_mon(last_battle_slot)
        if active_mon is not None:
            trainer_battle = enemy.enemytype == "legendary"
            gained_exp = battlehandler.calculate_exp_gain(enemy, trainer_battle=trainer_battle)
            active_mon.expgain(stdscr, gained_exp)

        new_mon = MonOver(
            rotation=len(party_mons) + 1,
            id=enemy.base.id,
            name=enemy.base.name,
            moves=list(getattr(enemy, "move_ids", [])),
            level=enemy.level,
            exp=0,
            shiny=getattr(enemy, "shiny", False),
            ability=getattr(enemy, "ability", None),
            held_item=getattr(enemy, "held_item", None)
        )

        add_to_party_or_pc(stdscr, new_mon)
        if remove_id is not None:
            picked_items.add(remove_id)

    elif result == "win":
        active_mon = get_party_mon(last_battle_slot)
        enemy = battlehandler.last_enemy
        if active_mon is not None and enemy is not None:
            trainer_battle = enemy.enemytype == "legendary"
            gained_exp = battlehandler.calculate_exp_gain(enemy, trainer_battle=trainer_battle)
            active_mon.expgain(stdscr, gained_exp)
        if remove_id is not None:
            picked_items.add(remove_id)

def run_fixed_wild_battle(stdscr, room, pos):
    if pos not in room.legendary_mons:
        return False

    encounter_id = map_object_id(room, pos)
    if encounter_id in picked_items:
        return False

    encounter = room.legendary_mons[pos]
    register_pokedex_seen(encounter["mon_id"])
    battle_spiral_animation(stdscr, room, pos[0], pos[1])
    fightui.textbox(stdscr, f"A wild {encounter['name'].capitalize()} appeared!")

    player_party = battlehandler.to_battle_party()
    active_idx = 0 if player_party and player_party[0].hp > 0 else battlehandler.active_battle_index(player_party)
    if active_idx is None:
        return "lose"

    enemy = battlehandler.create_mon(
        mon_id=encounter["mon_id"],
        level=encounter["level"],
        move_ids=encounter["moves"],
        hp=-1,
        enemytype="legendary",
        shiny=encounter.get("shiny", False)
    )
    battlehandler.last_enemy = enemy

    result = fightui.afightui(stdscr, player_party, enemy, 1, active_idx=active_idx, can_run=True)
    battlehandler.sync_player_hp(player_party)
    handle_wild_battle_result(stdscr, result, remove_id=encounter_id)
    return result

def try_cut_tree(stdscr, room, pos):
    tree_id = map_object_id(room, pos)
    if pos not in room.cut_trees or tree_id in cut_trees:
        return False

    if not has_item("hm_cut"):
        show_dialogue(stdscr, ["This tree looks cuttable.", "You need HM Cut."])
        return True

    show_dialogue(stdscr, ["Your Pokémon used HM Cut!"])
    cut_trees.add(tree_id)
    return True


def draw(stdscr, room, py, px):
    stdscr.clear()
    height, width = stdscr.getmaxyx()

    for y in range(min(room.height, height)):
        for x in range(min(room.width, width // 2)):  # x * 2 for character width
            char = "෴"
            color = curses.color_pair(4)

            if (y, x) in room.grass_tiles:
                char = GRASS

            if (y, x) in room.water_tiles:
                char = WATER
                color = curses.color_pair(6)

            if (y, x) in room.ice_tiles:
                char = ICE
                color = curses.color_pair(3)

            if (y, x) in room.hill_tiles:
                char = HILL_CHARS.get(room.hill_tiles[(y, x)], "_")
                color = curses.color_pair(HILL_COLOR_PAIR)

            object_id = map_object_id(room, (y, x))

            if (y, x) in room.items and object_id not in picked_items:
                char = ITEM
                color = curses.color_pair(7)

            if (y, x) in room.cut_trees and object_id not in cut_trees:
                char = CUT_TREE
                color = curses.color_pair(4)

            if (y, x) in room.npcs:
                char = room.npcs[(y, x)][0]
                color = curses.color_pair(6)

            if (y, x) in room.trees:
                char = REAL_TREE
                color = curses.color_pair(4)

            if (y, x) in room.fog:
                char = REAL_TREE
                color = curses.color_pair(4)

            if (y, x) in room.block_tiles:
                char = BLOCK
                color = curses.color_pair(1)

            if (y, x) in room.legendary_mons and object_id not in picked_items:
                char = LEGENDARY
                color = curses.color_pair(5)

            if (y, x) in room.doors:
                char = "D"
                color = curses.color_pair(5)

            if y == py and x == px:
                char = PLAYER
                color = curses.color_pair(7)

            try:
                safe_addstr(stdscr, y, x * 2, char, color)
            except curses.error:
                pass 

    stdscr.refresh()


def recharge_tera_orb():
    global tera_orb_charged
    tera_orb_charged = True

def consume_tera_orb():
    global tera_orb_charged
    if not tera_orb_charged:
        return False
    tera_orb_charged = False
    return True

def is_tera_orb_charged():
    global tera_orb_charged
    return tera_orb_charged

def heal_player():
    ensure_hpstorage_size()
    for i in range(6):
        hpstorage[i] = -1
    fightui.pplist = [-1, -1, -1, -1]
    recharge_tera_orb()

def blackout_to_pokemon_center(stdscr, rooms):
    lost = lose_blackout_money()
    center_room_id = getattr(stats, "POKEMON_CENTER_ROOM_ID", "map1")
    center_pos = getattr(stats, "POKEMON_CENTER_PLAYER_POS", (2, 5))
    nurse_pos = getattr(stats, "POKEMON_CENTER_NURSE_POS", (2, 6))
    center_room = rooms[center_room_id]

    show_dialogue(stdscr, [
        "You have no Pokémon left!",
        f"You blacked out and dropped ${lost}...",
        "You hurried back to the Pokémon Center!",
    ])

    py, px = center_pos
    steps = []
    step_y = 1 if nurse_pos[0] > py else -1
    for y in range(py, nurse_pos[0], step_y):
        steps.append((y, px))

    step_x = 1 if nurse_pos[1] > px else -1
    for x in range(px, nurse_pos[1], step_x):
        steps.append((nurse_pos[0], x))

    for step_y, step_x in steps:
        draw(stdscr, center_room, step_y, step_x)
        time.sleep(0.08)

    show_dialogue(stdscr, ["healing...", lambda: heal_player(), "done!"])
    return center_room, py, px

def get_current_box():
    return pc_boxes[current_box]


def add_to_pc(mon):
    for box in pc_boxes:
        if len(box) < BOX_SIZE:
            box.append(mon)
            return

    # all boxes full → create new one
    pc_boxes.append([mon])


def remove_from_pc(index):
    box = get_current_box()
    if 0 <= index < len(box):
        return box.pop(index)
    return None

def materialize_dialogue(lines):
    dialogue = []
    for line in lines:
        if line == "HEAL_PLAYER":
            dialogue.append(lambda: heal_player())
        else:
            dialogue.append(line)
    return dialogue

def create_room_registry():
    import os
    
    # Try to load from JSON first, fall back to stats
    json_path = os.path.join(os.path.dirname(__file__), "data", "leveldata.json")
    if os.path.exists(json_path):
        with open(json_path, "r") as f:
            data = json.load(f)
    else:
        data = stats.MAP_ROOMS

    rooms = {}

    for room_id, room_data in data.items():
        npcs = {}
        for pos, npc in copy.deepcopy(room_data.get("npcs", {})).items():
            # Convert string keys like "3,36" to tuple keys like (3, 36)
            if isinstance(pos, str) and "," in pos:
                tuple_pos = tuple(map(int, pos.split(",")))
            else:
                tuple_pos = pos
            npcs[tuple_pos] = (npc[0], materialize_dialogue(npc[1]), *npc[2:])

        def to_set(v):
            """Convert various formats to a set of tuples."""
            if isinstance(v, set):
                return set(tuple(x) if isinstance(x, (list, tuple)) else x for x in v)
            if isinstance(v, list):
                return set(tuple(x) if isinstance(x, (list, tuple)) else (x,) for x in v if x)
            return set()

        def to_dict(v):
            """Convert various formats to a dict with tuple keys."""
            if not v:
                return {}
            if isinstance(v, dict):
                result = {}
                for k, v2 in v.items():
                    if isinstance(k, str) and "," in k:
                        result[tuple(map(int, k.split(",")))] = v2
                    elif isinstance(k, (list, tuple)):
                        result[tuple(k)] = v2
                return result
            return {}

        rooms[room_id] = Room(
            room_data["width"],
            room_data["height"],
            npcs=npcs,
            grass_tiles=to_set(room_data.get("grass_tiles", [])),
            water_tiles=to_set(room_data.get("water_tiles", [])),
            hill_tiles=to_dict(room_data.get("hill_tiles", {})),
            items=to_dict(room_data.get("items", {})),
            cut_trees=to_set(room_data.get("cut_trees", [])),
            trees=to_set(room_data.get("trees", [])),
            fog=to_set(room_data.get("fog", [])),
            legendary_mons=to_dict(room_data.get("legendary_mons", {})),
            ice_tiles=to_set(room_data.get("ice_tiles", [])),
            block_tiles=to_dict(room_data.get("block_tiles", {})),
            room_id=room_id
        )

    # Handle doors - need to convert string keys to tuples
    for room_id, room_data in data.items():
        for pos_str, door_data in room_data.get("doors", {}).items():
            if isinstance(pos_str, str) and "," in pos_str:
                pos = tuple(map(int, pos_str.split(",")))
            else:
                pos = pos_str
            target_map, target_y, target_x = door_data
            rooms[room_id].doors[pos] = (rooms[target_map], target_y, target_x)

    return rooms

def create_rooms(start_room_id=None, return_registry=False):
    rooms = create_room_registry()
    start_room_id = start_room_id or getattr(stats, "SELECTED_OVERWORLD", "map1")
    start_room = rooms.get(start_room_id, rooms["map1"])

    if return_registry:
        return start_room, rooms

    return start_room


def saved_location(rooms):
    location = save_data.get("location", {}) if isinstance(save_data, dict) else {}
    room_id = location.get("room_id") or getattr(stats, "SELECTED_OVERWORLD", "map1")
    room = rooms.get(room_id) or rooms.get(getattr(stats, "SELECTED_OVERWORLD", "map1")) or rooms["map1"]

    spawn_y, spawn_x = stats.MAP_ROOMS.get(room.room_id, {}).get("spawn", (0, 0))
    try:
        y = int(location.get("y", spawn_y))
        x = int(location.get("x", spawn_x))
    except (TypeError, ValueError):
        y, x = spawn_y, spawn_x

    if not (0 <= y < room.height and 0 <= x < room.width):
        y, x = spawn_y, spawn_x

    return room, y, x


def draw_party_panel(stdscr, selected_index=None, moving_index=None):
    safe_addstr(stdscr, 10, 0, "#" + "#" * 78 + "#")
    for index, mon in enumerate(get_party()):
        hp_value = hpstorage[index] if index < len(hpstorage) else -1

        if mon is None:
            display = f"{index+1}. --- EMPTY SLOT ---"
        else:
            held_square = "■" if getattr(mon, "held_item", None) else " "
            # put the marker near the start of the line
            display = mon.menu(hp_value, index + 1)
            display = f"{held_square} {display}"

        marker = ">"
        if moving_index == index:
            marker = "?"
        elif selected_index != index:
            marker = " "

        safe_addstr(stdscr, 11 + index, 0, f"{marker} {display}")
    now = datetime.datetime.now()
    date_str = now.strftime("%d %B, %Y - %H:%M:%S")
    safe_addstr(stdscr, 17, 0, "#" + "#" * 78 + "#")
    safe_addstr(stdscr, 18, 0, date_str)
    safe_addstr(stdscr, 19, 0, f"Money: ${money}")
    safe_addstr(stdscr, 20, 0, "#placeholder#lol")
    safe_addstr(stdscr, 21, 0, "#" + "#" * 78 + "#")


def menu(stdscr):
    draw_party_panel(stdscr)
    stdscr.refresh()


def wrap_text(text, width):
    words = text.split()
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


def show_map(stdscr, current_room_id=None):
    """Display a visual map of the game world."""
    while True:
        stdscr.clear()
        safe_addstr(stdscr, 0, 0, "REGION MAP")
        safe_addstr(stdscr, 1, 0, "=" * 40)
        map_layout = [
            "┌─────────────┐",
            "│  Cerulean   │",
            "│    Town     │",
            "└─────┬┬──────┘",
            "      ││       ",
            "┌─────┴┴──────┐     ┌─────────────┐",
            "│   ROUTE 1   │=====│ CAVITAR CAVE│",
            "└─────┬┬──────┘     └─────────────┘",
            "      ││       ",
            "┌─────┴┴──────┐     ┌─────────────┐",
            "│   ROUTE 2   │=====│ CENDAR CITY │",
            "└─────────────┘     └─────────────┘",
        ]
        
        for i, line in enumerate(map_layout):
            safe_addstr(stdscr, 3 + i, 5, line)
        
        if current_room_id == "map1":
            safe_addstr(stdscr, 6, 7, "YOU")
        elif current_room_id == "map2":
            safe_addstr(stdscr, 14, 7, "YOU")
        
        safe_addstr(stdscr, 21, 2, "???????????")
        
        safe_addstr(stdscr, 23, 0, "[X] Close Map")
        stdscr.refresh()
        
        key = stdscr.getch()
        if key == ord("x"):
            return


def bag_menu(stdscr, current_room_id=None):
    section = 0
    selected = 0
    top = 0

    while True:
        section_name = BAG_SECTIONS[section][0]
        entries = inventory_entries_for_section(section_name)
        h, w = stdscr.getmaxyx()
        visible_rows = max(1, min(10, h - 8))
        selected = min(selected, max(0, len(entries) - 1))

        if selected < top:
            top = selected
        elif selected >= top + visible_rows:
            top = selected - visible_rows + 1

        stdscr.clear()
        safe_addstr(stdscr, 0, 0, f"BAG  < {section_name} >")
        safe_addstr(stdscr, 1, 0, "#" * min(w - 1, 50))

        if not entries:
            safe_addstr(stdscr, 3, 2, f"No items in {section_name}. lol")
        else:
            for row, (name, quantity) in enumerate(entries[top:top + visible_rows]):
                index = top + row
                marker = ">" if index == selected else " "
                text = f"{marker} {item_label(name):<18} x{quantity}"
                if index == selected:
                    stdscr.attron(curses.color_pair(1))
                    safe_addstr(stdscr, row+2, 1, text)
                    stdscr.attroff(curses.color_pair(1))
                else:
                    safe_addstr(stdscr, row+2, 1, text)


            desc_y = 5 + visible_rows
            name, quantity = entries[selected]
            safe_addstr(stdscr, desc_y, 0, "#" * min(w - 1, 50))
            safe_addstr(stdscr, desc_y+1, 2, f"{item_label(name)} x{quantity}")
            for i, line in enumerate(wrap_text(item_description(name), max(10, w - 4))[:3]):
                safe_addstr(stdscr, desc_y + 2 + i, 2, line)

        safe_addstr(stdscr, h - 1, 0, "[LEFT/RIGHT] Section  [UP/DOWN] Move  [Z] Use  [X] Back")
        stdscr.refresh()

        key = stdscr.getch()

        if key == curses.KEY_LEFT:
            section = (section - 1) % len(BAG_SECTIONS)
            selected = 0
            top = 0
        elif key == curses.KEY_RIGHT:
            section = (section + 1) % len(BAG_SECTIONS)
            selected = 0
            top = 0
        elif key == curses.KEY_UP and selected > 0:
            selected -= 1
        elif key == curses.KEY_DOWN and selected < len(entries) - 1:
            selected += 1
        elif key == ord("z") and entries:
            item_name, quantity = entries[selected]
            
            item_data = getattr(stats, "ITEMS", {}).get(item_name)
            if isinstance(item_data, dict) and item_data.get("effect") == "heal":
                heal_amount = int(item_data.get("amount", 0) or 0)
                if heal_amount <= 0:
                    show_dialogue(stdscr, [f"{item_label(item_name)} can't be used."])
                    continue

                # pick which party mon to heal
                target_selected = 0
                while True:
                    stdscr.clear()
                    safe_addstr(stdscr, 0, 0, "SELECT POKÉMON (Use item)")
                    safe_addstr(stdscr, 1, 0, "#" * min(w - 1, 50))

                    party = get_party()
                    for i, mon in enumerate(party):
                        prefix = ">" if i == target_selected else " "
                        if mon is None:
                            text = f"{prefix} {i+1}. --- EMPTY ---"
                        else:
                            base_stats = getattr(stats, f"mon{mon.id}", None)
                            max_hp = int(((2 * base_stats.hp * mon.level) / 100) + mon.level + 10) if base_stats else 0
                            text = f"{prefix} {i+1}. {mon.name}"
                            if max_hp > 0:
                                text += f" (heal +{heal_amount})"
                        safe_addstr(stdscr, 3 + i, 0, text[:w - 1])

                    stdscr.refresh()

                    k = stdscr.getch()
                    if k == curses.KEY_UP and target_selected > 0:
                        target_selected -= 1
                    elif k == curses.KEY_DOWN and target_selected < len(party) - 1:
                        target_selected += 1
                    elif k == ord("z"):
                        mon = get_party()[target_selected]
                        if mon is None:
                            continue

                        # heal best-effort: use hpstorage if present
                        # overworld tracks hp in fightui.hpstorage via the active party view only
                        try:
                            idx = target_selected
                            if 0 <= idx < len(hpstorage) and hpstorage[idx] != -1:
                                base_stats = getattr(stats, f"mon{mon.id}", None)
                                max_hp = int(((2 * base_stats.hp * mon.level) / 100) + mon.level + 10) if base_stats else 0
                                hpstorage[idx] = min(max_hp, hpstorage[idx] + heal_amount) if max_hp > 0 else hpstorage[idx]
                        except Exception:
                            pass

                        # consume item
                        for bag_entry in inventory:
                            if item_name in bag_entry:
                                bag_entry[item_name] -= 1
                                if bag_entry[item_name] <= 0:
                                    del bag_entry[item_name]
                                    if not bag_entry:
                                        inventory.remove(bag_entry)
                                break

                        show_dialogue(stdscr, [f"{mon.name} healed {heal_amount} HP!"])
                        break
                    elif k == ord("x"):
                        break

                continue

            if item_name in getattr(stats, "ITEMS", {}):
                while True:
                    stdscr.clear()
                    safe_addstr(stdscr, 0, 0, "BAG ITEM ACTION")
                    safe_addstr(stdscr, 1, 0, "#" * min(w - 1, 50))
                    safe_addstr(stdscr, 2, 0, f"Item: {item_label(item_name)} x{quantity}")
                    safe_addstr(stdscr, 4, 0, "[Z] Give to Pokémon")
                    safe_addstr(stdscr, 5, 0, "[X] Take from Pokémon")
                    safe_addstr(stdscr, 6, 0, "[C] Cancel")

                    stdscr.refresh()
                    subkey = stdscr.getch()

                    # Give from bag -> Pokémon
                    if subkey == ord("z"):
                        # Select Pokémon
                        target_selected = 0
                        while True:
                            stdscr.clear()
                            safe_addstr(stdscr, 0, 0, "SELECT POKÉMON (Give held item)")
                            safe_addstr(stdscr, 1, 0, "#" * min(w - 1, 50))
                            party = get_party()
                            # display 6 slots
                            for i, mon in enumerate(party):
                                prefix = ">" if i == target_selected else " "
                                if mon is None:
                                    text = f"{prefix} {i+1}. --- EMPTY ---"
                                else:
                                    held = " ■" if getattr(mon, "held_item", None) else ""
                                    text = f"{prefix} {i+1}. {mon.name}{held}"
                                safe_addstr(stdscr, 3 + i, 0, text)
                            safe_addstr(stdscr, 10, 0, "[UP/DOWN]  [Z] Confirm  [X] Back")
                            stdscr.refresh()

                            k = stdscr.getch()
                            if k == curses.KEY_UP and target_selected > 0:
                                target_selected -= 1
                            elif k == curses.KEY_DOWN and target_selected < len(party) - 1:
                                target_selected += 1
                            elif k == ord("z"):
                                mon = party[target_selected]
                                if mon is None:
                                    continue
                                mon.held_item = item_name
                                # spend from bag: remove one
                                # decrement quantity in inventory
                                for bag_entry in inventory:
                                    if item_name in bag_entry:
                                        bag_entry[item_name] -= 1
                                        if bag_entry[item_name] <= 0:
                                            del bag_entry[item_name]
                                            # remove empty dicts
                                            if not bag_entry:
                                                inventory.remove(bag_entry)
                                        break
                                show_dialogue(stdscr, [f"{mon.name} is now holding {item_label(item_name)}!"])
                                break
                            elif k == ord("x"):
                                break

                        break  # exit sub-menu loop after give/take/cancel

                    # Take from Pokémon -> bag
                    elif subkey == ord("x"):
                        target_selected = 0
                        while True:
                            stdscr.clear()
                            safe_addstr(stdscr, 0, 0, "SELECT POKÉMON (Take held item)")
                            safe_addstr(stdscr, 1, 0, "#" * min(w - 1, 50))
                            party = get_party()
                            for i, mon in enumerate(party):
                                prefix = ">" if i == target_selected else " "
                                if mon is None:
                                    text = f"{prefix} {i+1}. --- EMPTY ---"
                                else:
                                    held = getattr(mon, "held_item", None)
                                    held_txt = f" [{item_label(held)}]" if held else ""
                                    text = f"{prefix} {i+1}. {mon.name}{held_txt}"
                                safe_addstr(stdscr, 3 + i, 0, text)
                            safe_addstr(stdscr, 10, 0, "[UP/DOWN]  [Z] Confirm  [X] Back")
                            stdscr.refresh()

                            k = stdscr.getch()
                            if k == curses.KEY_UP and target_selected > 0:
                                target_selected -= 1
                            elif k == curses.KEY_DOWN and target_selected < len(party) - 1:
                                target_selected += 1
                            elif k == ord("z"):
                                mon = party[target_selected]
                                if mon is None:
                                    continue
                                held = getattr(mon, "held_item", None)
                                if not held:
                                    continue
                                mon.held_item = None
                                add_item(held, 1)
                                show_dialogue(stdscr, [f"{mon.name} dropped {item_label(held)}!"])
                                break
                            elif k == ord("x"):
                                break

                        break  # exit sub-menu

                    # Cancel
                    elif subkey == ord("c"):
                        break

                    else:
                        continue

            # Keep existing special-case for map
            if item_name == "map":
                show_map(stdscr, current_room_id)

        elif key == ord("x"):
            return


def shop_menu(stdscr, sold_items=None):
    """
    sold_items: list[str] of item ids the shop sells.
    If None, fall back to stats.SHOP_ITEMS.
    """
    if sold_items is None:
        items = list(stats.SHOP_ITEMS.items())
    else:
        # Don't rely on stats.SHOP_ITEMS being pre-filtered.
        # Use stats.ITEMS to fetch price for any item id the editor selected.
        items = []
        for item_id in sold_items:
            price = 0
            item = getattr(stats, "ITEMS", {}).get(item_id)
            if isinstance(item, dict):
                price = int(item.get("price", 0) or 0)
            items.append((item_id, price))

    selected = 0

    while True:
        stdscr.clear()
        safe_addstr(stdscr, 0, 0, f"POKé MART     Money: ${money}")
        safe_addstr(stdscr, 1, 0, "#" * 38)

        for i, (item_name, price) in enumerate(items):
            marker = ">" if i == selected else " "
            safe_addstr(stdscr, i + 3, 2, f"{marker} {item_label(item_name):<16} ${price}")

        safe_addstr(stdscr, 8, 0, "[Z] Buy  [X] Leave")
        stdscr.refresh()

        key = stdscr.getch()

        if key == curses.KEY_UP and selected > 0:
            selected -= 1
        elif key == curses.KEY_DOWN and selected < len(items) - 1:
            selected += 1
        elif key == ord("z"):
            item_name, price = items[selected]
            if spend_money(price):
                add_item(item_name)
                show_dialogue(stdscr, [f"Bought {item_label(item_name)}!"])
            else:
                show_dialogue(stdscr, ["Not enough money."])
        elif key == ord("x"):
            return


def party_menu(stdscr):
    selected = 0
    moving = None

    while True:
        draw(stdscr, create_rooms(), -100, -100)
        draw_party_panel(stdscr, selected_index=selected, moving_index=moving)
        safe_addstr(stdscr, 22, 0, "IN PARTY MENU")
        for y in range(0,10):
            stdscr.addstr(y, 0, "-" * 80)
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
    if not save_exists():
        import cutscene
        if not cutscene.new_save_intro(stdscr):
            return
    else:
        reset_game_state()

    curses.curs_set(0)
    stdscr.keypad(True)
    curses.start_color()
    init_overworld_colors()

    _, rooms = create_rooms(return_registry=True)
    current_room, py, px = saved_location(rooms)

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
            # Handle block pushing
            if (ny, nx) in current_room.block_tiles:
                dy, dx = ny - py, nx - px
                if try_push_block(current_room, py, px, (ny, nx), dy, dx):
                    # Block was pushed, now move player onto the block's old position
                    py, px = ny, nx
                    pickup_item(stdscr, current_room, (py, px))
            # Handle hill jumps
            elif (ny, nx) in current_room.hill_tiles:
                hill_jump = try_hill_jump(current_room, py, px, ny, nx)
                if hill_jump is not None:
                    py, px = hill_jump
                    pickup_item(stdscr, current_room, (py, px))
            # Handle normal movement and ice physics
            elif not is_blocked(current_room, (ny, nx)):
                # Check if moving onto ice
                if (ny, nx) in current_room.ice_tiles:
                    dy, dx = ny - py, nx - px
                    py, px = apply_ice_physics(current_room, py, px, dy, dx)
                else:
                    py, px = ny, nx
                pickup_item(stdscr, current_room, (py, px))

        if (py, px) in current_room.doors:
            current_room, py, px = current_room.doors[(py, px)]

        fixed_result = run_fixed_wild_battle(stdscr, current_room, (py, px))
        if fixed_result:
            if fixed_result == "lose":
                current_room, py, px = blackout_to_pokemon_center(stdscr, rooms)
            continue

        if key == ord("z"):
            for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                check = (py + dy, px + dx)
                if try_cut_tree(stdscr, current_room, check):
                    break

                if check in current_room.npcs:
                    npc = current_room.npcs[check]
                    action = npc_action(npc)
                    trainer_id = npc_trainer_id(npc)

                    if action == "SHOP" or (isinstance(action, list) and len(action) >= 1 and action[0] == "SHOP"):
                        sold_items = None
                        if isinstance(action, list) and len(action) >= 2:
                            sold_items = action[1]
                        show_dialogue(stdscr, npc_dialogue(npc))
                        shop_menu(stdscr, sold_items=sold_items)
                        break

                    elif isinstance(action, list) and len(action) >= 2 and action[0] == "GIVE_ITEM":
                        show_dialogue(stdscr, npc_dialogue(npc))
                        item_name = action[1]
                        quantity = action[2] if len(action) >= 3 else 1
                        add_item(item_name, quantity)
                        show_dialogue(stdscr, [f"Received {item_label(item_name)} x{quantity}!"])
                        break

                    if trainer_id is not None and trainer_id in battled_trainers:
                        show_dialogue(stdscr, ["We already battled."])
                        continue

                    show_dialogue(stdscr, npc_dialogue(npc))

                    if trainer_id is not None:
                        battle_spiral_animation(stdscr, current_room, py, px)
                        result = battlehandler.run_trainer_battle(stdscr, trainer_id)
                        if result == "win":
                            battled_trainers.add(trainer_id)
                            reward = stats.TRAINER_REWARDS.get(trainer_id, 100)
                            add_money(reward)
                            show_dialogue(stdscr, ["You won the trainer battle!", f"You got ${reward}!"])
                        elif result == "lose":
                            show_dialogue(stdscr, ["You lost the trainer battle..."])
                            current_room, py, px = blackout_to_pokemon_center(stdscr, rooms)
                        elif result == "run":
                            show_dialogue(stdscr, ["You ran from the trainer battle."])

                    break

        if key == ord("c"):
            spawn_room_id = save_menu(stdscr, current_room.room_id, py, px)
            if spawn_room_id in rooms:
                current_room = rooms[spawn_room_id]
                py, px = stats.MAP_ROOMS[spawn_room_id].get("spawn", (0, 0))

        if (py, px) in current_room.grass_tiles:
            if random.random() < 0.2:
                battle_spiral_animation(stdscr, current_room, py, px)
                result = battlehandler.run_battle(stdscr, current_room.room_id)
                handle_wild_battle_result(stdscr, result)
                if result == "lose":
                    current_room, py, px = blackout_to_pokemon_center(stdscr, rooms)


def debug_spawn_menu(stdscr):
    room_ids = list(stats.MAP_ROOMS.keys())
    selected = 0

    while True:
        stdscr.clear()
        safe_addstr(stdscr, 0, 0, "ROOM SELECT")
        safe_addstr(stdscr, 1, 0, "#" * 24)

        for i, room_id in enumerate(room_ids):
            marker = ">" if i == selected else " "
            spawn = stats.MAP_ROOMS[room_id].get("spawn", (0, 0))
            safe_addstr(stdscr, i + 3, 0, f"{marker} {room_id} {spawn}")

        safe_addstr(stdscr, len(room_ids) + 5, 0, "[Z] Spawn  [X] Back")
        stdscr.refresh()

        key = stdscr.getch()

        if key == curses.KEY_UP and selected > 0:
            selected -= 1
        elif key == curses.KEY_DOWN and selected < len(room_ids) - 1:
            selected += 1
        elif key == ord("z"):
            return room_ids[selected]
        elif key == ord("x"):
            return None


def save_menu(stdscr, current_room_id=None, py=None, px=None):
    curses.curs_set(0)

    options = ["Save Game", "Pokémon", "Bag", "PC", "Options", "Pokédex", "M.Gift"]
    y = 0
    debug_presses = 0

    while True:
        h, w = stdscr.getmaxyx()
        start_x = w - 14

        menu_height = len(options) + 4

        for i in range(menu_height + 1):
            safe_addstr(stdscr, i, start_x, " " * 16)

        safe_addstr(stdscr, 0, start_x, "#" * 14)
        for row in range(1, menu_height):
            safe_addstr(stdscr, row, start_x, "#")
            safe_addstr(stdscr, row, start_x + 13, "#")
        safe_addstr(stdscr, menu_height, start_x, "#" * 14)
        safe_addstr(stdscr, 1, start_x+1, "  OPTIONS")

        for i, opt in enumerate(options):
            if i == y:
                safe_addstr(stdscr, i + 3, start_x + 1, f" >{opt}")
            else:
                safe_addstr(stdscr, i + 3, start_x + 1, f"  {opt}")

        stdscr.refresh()
        key = stdscr.getch()

        if key == curses.KEY_UP and y > 0:
            y -= 1
        elif key == curses.KEY_DOWN and y < len(options) - 1:
            y += 1
        elif key == ord("c"):
            debug_presses += 1
            if debug_presses >= 5:
                return debug_spawn_menu(stdscr)
        elif key == ord("z"):
            if y == 0:
                data = build_save(current_room_id, py, px)
                save_game(data)
                show_dialogue(stdscr, ["Game Saved!"])
                return None
            elif y == 1:
                party_menu(stdscr)
                return None
            elif y == 2:
                bag_menu(stdscr, current_room_id)
            elif y == 3:
                pc_menu(stdscr)
            elif y == 5:
                pokedex_menu(stdscr)
            elif y == 6:
                import mysterygift
                mysterygift.gifted(stdscr)
            else:
                return None
        elif key == ord("x"):
            return None


def register_pokedex_seen(mon_id, shiny=False):
    global save_data
    if mon_id not in pokedex_seen:
        pokedex_seen.add(mon_id)
        if isinstance(save_data, dict):
            save_data.setdefault("pokedex", {}).setdefault("seen", [])
            save_data["pokedex"]["seen"] = sorted(pokedex_seen)

    if shiny and mon_id not in pokedex_seen_shiny:
        pokedex_seen_shiny.add(mon_id)
        if isinstance(save_data, dict):
            save_data.setdefault("pokedex", {}).setdefault("seen_shiny", [])
            save_data["pokedex"]["seen_shiny"] = sorted(pokedex_seen_shiny)


def register_pokedex_caught(mon_id, shiny=False):
    register_pokedex_seen(mon_id, shiny=shiny)
    if mon_id not in pokedex_caught:
        pokedex_caught.add(mon_id)
        if isinstance(save_data, dict):
            save_data.setdefault("pokedex", {}).setdefault("caught", [])
            save_data["pokedex"]["caught"] = sorted(pokedex_caught)

    if shiny and mon_id not in pokedex_caught_shiny:
        pokedex_caught_shiny.add(mon_id)
        if isinstance(save_data, dict):
            save_data.setdefault("pokedex", {}).setdefault("caught_shiny", [])
            save_data["pokedex"]["caught_shiny"] = sorted(pokedex_caught_shiny)


def pokemon_type_text(mon):
    types = [mon.type.capitalize()]
    if mon.type2 and mon.type2 != "nil":
        types.append(mon.type2.capitalize())
    return " / ".join(types)


def pokemon_description(mon):
    return getattr(mon, "description", getattr(mon, "desc", "No Pokédex description available."))


def pokemon_type_pairs():
    return {
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
        "Steel": 1,
    }


def draw_pokedex_sprite(stdscr, mon, sprite_side, variant, start_y, start_x):
    sprite = getattr(stats, mon.name.lower(), stats.placeholder)
    sprite.draw(stdscr, sprite_side, variant, start_y=start_y, start_x=start_x)


def pokedex_sprite_options(mon_id, include_all_shiny=False):
    options = [
        ("front", "normal", "Normal front"),
        ("back", "normal", "Normal back"),
    ]
    if include_all_shiny or mon_id in pokedex_seen_shiny:
        options.extend([
            ("front", "shiny", "Shiny front"),
            ("back", "shiny", "Shiny back"),
        ])
    return options


def draw_pokedex_detail(stdscr, mon_id, start_y, start_x, width, sprite_side="front", variant="normal", form_label="Normal front"):
    current = getattr(stats, f"mon{mon_id}", None)
    inner_width = max(12, width)
    title = f"{mon_id:03d}. ???"

    if mon_id in pokedex_seen and current is not None:
        shiny_mark = " ✦" if mon_id in pokedex_seen_shiny else ""
        status = "Caught" if mon_id in pokedex_caught else "Seen"
        if mon_id in pokedex_caught_shiny:
            status += " ✦"
        title = f"{mon_id:03d}. {current.name.capitalize()}{shiny_mark}"
        safe_addstr(stdscr, start_y, start_x, title[:inner_width])
        safe_addstr(stdscr, start_y + 1, start_x, "━" * min(30, inner_width))

        if width >= 48:
            draw_pokedex_sprite(stdscr, current, sprite_side, variant, start_y + 2, start_x)
            stat_x = start_x + 28
            stat_width = max(12, width - 28)
        else:
            stat_x = start_x
            stat_width = inner_width

        type1 = current.type.capitalize()
        type2 = "" if not current.type2 or current.type2 == "nil" else current.type2.capitalize()
        type_pairs = pokemon_type_pairs()

        safe_addstr(stdscr, start_y + 2, stat_x, f"Sprite: {form_label}"[:stat_width])
        safe_addstr(stdscr, start_y + 3, stat_x, f"Status: {status}"[:stat_width])
        try:
            stdscr.addstr(start_y + 4, stat_x, type1[:11], curses.color_pair(type_pairs.get(type1, 1)))
            if type2:
                stdscr.addstr(start_y + 4, stat_x + 12, type2[:11], curses.color_pair(type_pairs.get(type2, 1)))
        except curses.error:
            safe_addstr(stdscr, start_y + 4, stat_x, f"Type: {pokemon_type_text(current)}"[:stat_width])

        safe_addstr(stdscr, start_y + 6, stat_x, f"HP: {current.hp}"[:stat_width])
        safe_addstr(stdscr, start_y + 7, stat_x, f"ATK: {current.at}"[:stat_width])
        safe_addstr(stdscr, start_y + 8, stat_x, f"SP ATK: {current.sp_at}"[:stat_width])
        safe_addstr(stdscr, start_y + 9, stat_x, f"DEF: {current.de}"[:stat_width])
        safe_addstr(stdscr, start_y + 10, stat_x, f"SP DEF: {current.sp_de}"[:stat_width])
        safe_addstr(stdscr, start_y + 11, stat_x, f"SPD: {current.spd}"[:stat_width])

        safe_addstr(stdscr, start_y + 14, start_x, "Description"[:inner_width])
        for i, line in enumerate(wrap_text(pokemon_description(current), min(48, inner_width))[:5]):
            safe_addstr(stdscr, start_y + 16 + i, start_x, line[:inner_width])
    else:
        safe_addstr(stdscr, start_y, start_x, title[:inner_width])
        safe_addstr(stdscr, start_y + 1, start_x, "━" * min(30, inner_width))
        safe_addstr(stdscr, start_y + 2, start_x, "Status: Unknown"[:inner_width])
        safe_addstr(stdscr, start_y + 4, start_x, "Type: ???"[:inner_width])
        safe_addstr(stdscr, start_y + 6, start_x, "HP: ???"[:inner_width])
        safe_addstr(stdscr, start_y + 7, start_x, "ATK: ???"[:inner_width])
        safe_addstr(stdscr, start_y + 8, start_x, "SP ATK: ???"[:inner_width])
        safe_addstr(stdscr, start_y + 9, start_x, "DEF: ???"[:inner_width])
        safe_addstr(stdscr, start_y + 10, start_x, "SP DEF: ???"[:inner_width])
        safe_addstr(stdscr, start_y + 11, start_x, "SPD: ???"[:inner_width])
        safe_addstr(stdscr, start_y + 14, start_x, "Description"[:inner_width])
        safe_addstr(stdscr, start_y + 16, start_x, "No data yet."[:inner_width])


def pokedex_menu(stdscr):
    curses.curs_set(0)
    stdscr.keypad(True)

    total = 151
    selected = 0
    sprite_index = 0

    while True:
        stdscr.clear()
        h, w = stdscr.getmaxyx()
        left_width = 27
        detail_x = left_width + 3
        detail_width = max(20, w - detail_x)
        visible = max(1, min(total, h - 2))
        top = max(0, min(selected - visible // 2, total - visible))
        current_id = selected + 1
        sprite_options = pokedex_sprite_options(current_id)
        sprite_index %= len(sprite_options)
        sprite_side, variant, form_label = sprite_options[sprite_index]

        for row in range(visible):
            index = top + row
            if index >= total:
                break

            mon_id = index + 1
            if mon_id in pokedex_seen:
                shiny_mark = " ✦" if mon_id in pokedex_seen_shiny else ""
                label = mon_name(mon_id) + shiny_mark
            else:
                label = "???"

            marker = ">" if index == selected else " "
            safe_addstr(stdscr, row, 0, f"{marker} {mon_id:03d} {label}"[:left_width - 1])

        if w >= 55:
            for y in range(0, h - 1):
                safe_addstr(stdscr, y, left_width, "|")
            draw_pokedex_detail(stdscr, current_id, 0, detail_x, detail_width, sprite_side, variant, form_label)
        else:
            detail_y = visible + 2
            safe_addstr(stdscr, detail_y - 1, 0, "-" * max(0, w - 1))
            draw_pokedex_detail(stdscr, current_id, detail_y, 0, max(20, w - 1), sprite_side, variant, form_label)

        safe_addstr(stdscr, h - 1, 0, "Left/right = sprite, X = back")

        key = stdscr.getch()
        if key == curses.KEY_UP and selected > 0:
            selected -= 1
        elif key == curses.KEY_DOWN and selected + 1 < total:
            selected += 1
        elif key == curses.KEY_LEFT:
            sprite_index = (sprite_index - 1) % len(sprite_options)
        elif key == curses.KEY_RIGHT:
            sprite_index = (sprite_index + 1) % len(sprite_options)
        elif key == ord("x") or key == ord("z"):
            break
        stdscr.refresh()


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
            maxexp=mon_data["maxexp"],
            shiny=mon_data.get("shiny", False),
            ability=mon_data.get("ability"),
            held_item=mon_data.get("held_item")
        )
        mons.append(mon)

    return mons


def reset_game_state(data=None):
    global save_data, name, party_mons, inventory, picked_items, cut_trees, money
    global pc_boxes, current_box, battled_trainers, pokedex_seen, pokedex_caught
    global pokedex_seen_shiny, pokedex_caught_shiny

    if data is None:
        data = load_save()
    else:
        data = merge_defaults(data, copy.deepcopy(DEFAULT_SAVE))

    save_data = data
    name = save_data["player"]["name"]

    loaded_mons = load_pokemon(save_data)
    if loaded_mons:
        party_mons = loaded_mons[:6]
    else:
        party_mons = [mon.copy() for mon in DEFAULT_PARTY]

    inventory = copy.deepcopy(save_data.get("inventory", []))
    money = save_data.get("money", 3000)
    picked_items = set(save_data.get("picked_items", []))
    cut_trees = set(save_data.get("cut_trees", []))
    pokedex_seen = set(save_data.get("pokedex", {}).get("seen", []))
    pokedex_caught = set(save_data.get("pokedex", {}).get("caught", []))
    pokedex_seen_shiny = set(save_data.get("pokedex", {}).get("seen_shiny", []))
    pokedex_caught_shiny = set(save_data.get("pokedex", {}).get("caught_shiny", []))

    fightui.pplist = list(save_data.get("pp", [-1, -1, -1, -1]))

    global tera_orb_charged
    tera_orb_charged = save_data.get("tera_orb_charged", True)
    ensure_hpstorage_size()
    sync_party_slots()

    current_box = 0
    battled_trainers = set(save_data.get("battled_trainers", []))
    pc_boxes = []

    for box in save_data.get("pcmons", [[]]):
        loaded_box = []
        for mon_data in box:
            mon = MonOver(
                rotation=mon_data["rotation"],
                id=mon_data["id"],
                name=mon_data["name"],
                moves=mon_data["moves"],
                level=mon_data["level"],
                exp=mon_data["exp"],
                maxexp=mon_data["maxexp"],
                shiny=mon_data.get("shiny", False),
                ability=mon_data.get("ability"),
                held_item=mon_data.get("held_item")
            )
            loaded_box.append(mon)

        pc_boxes.append(loaded_box)

    if not pc_boxes:
        pc_boxes = [[]]


reset_game_state()
