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
    "pokedex": {
        "seen": [],
        "caught": []
    },
    "pokemon": [],
    "pcmons": [[]],
    "inventory": [
        {"potion": 5},
        {"pokeball": 5}
    ],
    "picked_items": [],
    "cut_trees": [],
    "pp": [-1, -1, -1, -1],
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
ITEM = "●"
CUT_TREE = "↟"
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


class MonOver:
    def __init__(self, rotation, id, name, moves, level, exp, maxexp=-1):
        self.ord = rotation
        self.id = id
        self.name = name
        self.moves = moves
        self.level = level
        self.exp = exp
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
            "maxexp": self.maxexp
        }

    def menu(self, hp_value=-1, slot_number=None):
        base_stats = getattr(stats, f"mon{self.id}")
        max_hp = int(((2 * base_stats.hp * self.level) / 100) + self.level + 10)
        current_hp = max_hp if hp_value == -1 else hp_value
        current_hp = max(0, min(current_hp, max_hp))
        bar_length = 10
        filled = int((current_hp / max_hp) * bar_length) if max_hp > 0 else 0
        hp_bar = "█" * filled + "░" * (bar_length - filled)
        prefix = f"{slot_number}. " if slot_number is not None else "" #idk might use in future
        return (
            f"{prefix}{self.name:<10} -- [HP {current_hp:>3}/{max_hp:<3}] "
            f"[{hp_bar}] -- [EXP {self.exp}/{self.maxexp} LVL {self.level}]"
        )

    def expgain(self, stdscr, gainedexp):
        show_dialogue(stdscr, [f"{self.name} gained {gainedexp} EXP!"])
        self.exp += gainedexp
        while self.exp >= self.maxexp:
            self.exp -= self.maxexp
            self.level += 1
            self.maxexp = self.level*self.level*self.level
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
    MonOver(rotation=1, id=1, name="Bulbasaur", moves=[340], level=5, exp=67),
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
    return item_name.replace("_", " ").title()

ITEM_DESCRIPTIONS = {
    "potion": "Restores 20 HP to one Pokemon during battle.",
    "pokeball": "A ball used to catch wild Pokemon.",
    "fullheal": "Clears all status conditions from one Pokemon.",
    "hm_cut": "Lets any Pokemon with sharp claws cut down small trees in the overworld. Not be confused with TM CUT.",
}

BAG_SECTIONS = [
    ("Pokeballs", {"pokeball"}),
    ("Recover", {"potion", "fullheal"}),
    ("Key Items", {"hm_cut"}),
    ("Other", set()),
]


def item_description(item_name):
    return ITEM_DESCRIPTIONS.get(item_name, "No description yet.")


def inventory_entries():
    entries = []
    for item in inventory:
        for name, quantity in item.items():
            if quantity > 0:
                entries.append((name, quantity))
    return entries


def bag_section_for_item(item_name):
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
    def __init__(self, width, height, npcs=None, grass_tiles=None, doors=None, items=None, cut_trees=None, room_id="room"):
        self.width = width
        self.height = height
        self.npcs = npcs or {}
        self.grass_tiles = grass_tiles or set()
        self.doors = doors or {}
        self.items = items or {}
        self.cut_trees = cut_trees or set()
        self.room_id = room_id


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
    party_data = [mon.to_dict() for mon in get_party() if mon is not None]

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
        "pokemon": party_data,
        "inventory": inventory,
        "picked_items": sorted(picked_items),
        "cut_trees": sorted(cut_trees),
        "pp": fightui.pplist,
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
        return npc[2]
    return None

def map_object_id(room, pos):
    y, x = pos
    return f"{room.room_id}:{y}:{x}"

def is_blocked(room, pos):
    return pos in room.npcs or (
        pos in room.cut_trees and map_object_id(room, pos) not in cut_trees
    )

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

    for y in range(room.height):
        for x in range(room.width):
            char = "෴"
            color = curses.color_pair(4)

            if (y, x) in room.grass_tiles:
                char = GRASS

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

def create_rooms():
    npcs1 = {
        (2, 5): (NPC_ICON, ["hello!", "welcome to room 1"]),
        (2, 6): (NURSE, ["healing...", lambda: heal_player(), "done!"]),
    }

    grass1 = set()
    for y in range(5, 10):
        for x in range(5, 10):
            grass1.add((y, x))

    items1 = {
        (1, 4): ("hm_cut", 1),
        (8, 12): ("potion", 1),
    }

    cut_trees1 = {
        (4, 10),
    }

    room1 = Room(20, 10, npcs1, grass1, items=items1, cut_trees=cut_trees1, room_id="room1")

    npcs2 = {
        (1, 1): (NPC_ICON, ["you made it to room 2"]),
        (3, 3): (ENEMY, ["You there!", "Let's battle!"], "room2_guard"),
    }

    grass2 = {(6, 6), (6, 7), (7, 6), (7, 7)}

    items2 = {
        (5, 5): ("pokeball", 2),
    }

    room2 = Room(20, 10, npcs2, grass2, items=items2, room_id="room2")

    room1.doors[(0, 10)] = (room2, 9, 10)
    room2.doors[(9, 10)] = (room1, 0, 10)

    return room1


def draw_party_panel(stdscr, selected_index=None, moving_index=None):
    safe_addstr(stdscr, 10, 0, "#" + "#" * 78 + "#")
    for index, mon in enumerate(get_party()):
        hp_value = hpstorage[index] if index < len(hpstorage) else -1

        if mon is None:
            display = f"{index+1}. --- EMPTY SLOT ---"
        else:
            display = mon.menu(hp_value, index + 1)

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
    safe_addstr(stdscr, 19, 0, "Did you know? This game exists!")
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


def bag_menu(stdscr):
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

        safe_addstr(stdscr, h - 1, 0, "[LEFT/RIGHT] Section  [UP/DOWN] Move  [X] Back")
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
        elif key == ord("x"):
            return


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
            if not is_blocked(current_room, (ny, nx)):
                py, px = ny, nx
                pickup_item(stdscr, current_room, (py, px))

        if (py, px) in current_room.doors:
            current_room, py, px = current_room.doors[(py, px)]

        if key == ord("z"):
            for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                check = (py + dy, px + dx)
                if try_cut_tree(stdscr, current_room, check):
                    break

                if check in current_room.npcs:
                    npc = current_room.npcs[check]
                    trainer_id = npc_trainer_id(npc)

                    if trainer_id is not None and trainer_id in battled_trainers:
                        show_dialogue(stdscr, ["We already battled."])
                        continue

                    show_dialogue(stdscr, npc_dialogue(npc))

                    if trainer_id is not None:
                        result = battlehandler.run_trainer_battle(stdscr, trainer_id)
                        if result == "win":
                            battled_trainers.add(trainer_id)
                            show_dialogue(stdscr, ["You won the trainer battle!"])
                        elif result == "lose":
                            show_dialogue(stdscr, ["You lost the trainer battle..."])
                        elif result == "run":
                            show_dialogue(stdscr, ["You ran from the trainer battle."])

                    break

        if key == ord("c"):
            save_menu(stdscr)

        if (py, px) in current_room.grass_tiles:
            if random.random() < 0.2:
                show_dialogue(stdscr, ["A wild Pokémon appeared!"])
                result = battlehandler.run_battle(stdscr, 1)
                if isinstance(result, tuple) and result[0] == "caught":
                    enemy = result[1]

                    new_mon = MonOver(
                        rotation=len(party_mons) + 1,
                        id=enemy.base.id, 
                        name=enemy.base.name,
                        moves=list(getattr(enemy, "move_ids", [])),
                        level=enemy.level,
                        exp=0
                    )

                    add_to_party_or_pc(stdscr, new_mon)
                if result == "win":
                    active_mon = get_party_mon(last_battle_slot)
                    enemy = battlehandler.last_enemy
                    if active_mon is not None and enemy is not None:
                        gained_exp = battlehandler.calculate_exp_gain(enemy)
                        active_mon.expgain(stdscr, gained_exp)


def save_menu(stdscr):
    curses.curs_set(0)

    options = ["Save Game", "Pokémon", "Bag", "PC", "Options", "Pokédex", "M.Gift"]
    y = 0

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
            elif y == 2:
                bag_menu(stdscr)
            elif y == 3:
                pc_menu(stdscr)
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


def reset_game_state(data=None):
    global save_data, name, party_mons, inventory, picked_items, cut_trees
    global pc_boxes, current_box, battled_trainers

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
    picked_items = set(save_data.get("picked_items", []))
    cut_trees = set(save_data.get("cut_trees", []))

    fightui.pplist = list(save_data.get("pp", [-1, -1, -1, -1]))
    ensure_hpstorage_size()
    sync_party_slots()

    current_box = 0
    battled_trainers = set()
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
                maxexp=mon_data["maxexp"]
            )
            loaded_box.append(mon)

        pc_boxes.append(loaded_box)

    if not pc_boxes:
        pc_boxes = [[]]


reset_game_state()
