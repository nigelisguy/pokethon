# stats.py - middleman idk

import json
from pathlib import Path

# Basic Mon and Moves classes
class Mon:
    def __init__(self, name, type, type2, hp, at, de, sp_at, sp_de, spd, mon_id=None, base_exp=0):
        self.id = mon_id
        self.base_exp = base_exp
        self.name = name
        self.type = type
        self.type2 = type2
        self.hp = hp
        self.at = at
        self.de = de
        self.sp_at = sp_at
        self.sp_de = sp_de
        self.spd = spd

    def call(self):
        return f"{self.name}"

class Moves:
    def __init__(self, name, type, pp, pow, acc, attack, defence, spattack, spdefence, speed,
                 evasion, enattack, endefence, enspattack, enspdefence, enspeed, emevasion, emaccuracy,
                 weather, eneffect, hitpriority, secondacc, repeatedhit, maxhealth, critstage, desc):
        self.name = name
        self.type = type
        self.pp = pp
        self.pow = pow
        self.acc = acc
        self.at = attack
        self.de = defence
        self.sp_at = spattack
        self.sp_de = spdefence
        self.spd = speed
        self.eva = evasion
        self.enat = enattack
        self.endf = endefence
        self.enspat = enspattack
        self.enspdef = enspdefence
        self.enspd = enspeed
        self.eneva = emevasion
        self.emac = emaccuracy
        self.weather = weather
        self.enefc = eneffect
        self.hitprio = bool(hitpriority)
        self.secondacc = secondacc
        self.rhit = bool(repeatedhit)
        self.mhp = maxhealth
        self.crits = critstage
        self.desc = desc

    def call(self):
        return f"{self.name:<20} - {self.desc}"

    def nameself(self):
        return f"{self.name:<20} - {self.type}"

# Minimal RenderImage class used by sprite loader and UI
import curses
import textwrap
class RenderImage:
    def __init__(self, front_art, back_art, palettes, default_color=1, width=25, height=11):
        self.width = width
        self.height = height
        self.front = self._build_grid(front_art)
        self.back = self._build_grid(back_art)
        self.palettes = palettes
        self.default_color = default_color

    def _build_grid(self, art):
        art = textwrap.dedent(art or "").strip("\n").split("\n") if art else []
        grid = []
        for i in range(self.height):
            if i < len(art):
                line = art[i][:self.width].ljust(self.width)
            else:
                line = " " * self.width
            grid.append(line)
        return grid

    def draw(self, stdscr, sprite="front", variant="normal", char_map=None):
        if sprite == "front":
            start_y, start_x = 2, 2
        else:
            start_y, start_x = 2, 53
        color_map = self.palettes.get(variant, self.palettes.get("normal", {}))
        art = self.front if sprite == "front" else self.back
        for y, line in enumerate(art):
            for x, ch in enumerate(line):
                draw_char = char_map.get(ch, ch) if char_map else ch
                color = color_map.get(ch, self.default_color)
                try:
                    stdscr.addstr(start_y + y, start_x + x, draw_char, curses.color_pair(color))
                except curses.error:
                    pass

# placeholder sprite
placeholder = RenderImage(front_art="", back_art="", palettes={"normal":{}, "shiny":{}}, width=25, height=11)

# Defaults that other modules may rely on; JSON loaders will override when data present
SELECTED_OVERWORLD = "map1"
POKEMON_CENTER_ROOM_ID = "map1"
POKEMON_CENTER_PLAYER_POS = (3, 6)
POKEMON_CENTER_NURSE_POS = (2, 6)
SHOP_ITEMS = {}
TRAINER_REWARDS = {}
MAP_ROOMS = {}

# Data directory preference: use data/ if present
_DATA_DIR = Path(__file__).parent / "data"
if not _DATA_DIR.exists():
    _DATA_DIR = Path(__file__).parent

# Load pokedata.json -> mon{n}
try:
    with open(_DATA_DIR / "pokedata.json", "r") as f:
        _pokedata = json.load(f).get("pokemon", [])
    for p in _pokedata:
        _id = int(p.get("id"))
        globals()[f"mon{_id}"] = Mon(
            p.get("name", ""), p.get("type", "nil"), p.get("type2", "nil"),
            p.get("hp", 0), p.get("at", 0), p.get("de", 0),
            p.get("sp_at", 0), p.get("sp_de", 0), p.get("spd", 0),
            mon_id=_id, base_exp=p.get("base_exp", 0)
        )
except Exception:
    pass

# Load moveset.json -> move{n}
try:
    with open(_DATA_DIR / "moveset.json", "r") as f:
        _moves = json.load(f).get("moves", [])
    for m in _moves:
        mid = int(m.get("id"))
        globals()[f"move{mid}"] = Moves(
            m.get("name", ""), m.get("type", ""), m.get("pp", 0), m.get("pow", 0), m.get("acc", -1),
            m.get("at", 0), m.get("de", 0), m.get("sp_at", 0), m.get("sp_de", 0), m.get("spd", 0),
            m.get("eva", 0), m.get("enat", 0), m.get("endf", 0), m.get("enspat", 0), m.get("enspdef", 0),
            m.get("enspd", 0), m.get("eneva", 0), m.get("emac", 0), m.get("weather", "nil"), m.get("enefc", "nil"),
            m.get("hitprio", False), m.get("secondacc", -1), m.get("rhit", False), m.get("maxhealth", 0),
            m.get("crits", 0), m.get("desc", "")
        )
except Exception:
    pass

# Load sprites from spritedata.json -> create globals for sprite_var names
try:
    with open(_DATA_DIR / "spritedata.json", "r") as f:
        _spr = json.load(f).get("pokemon", {})
    for key, entry in _spr.items():
        sprite_var = entry.get("sprite_var") or entry.get("name")
        sprite = entry.get("sprite", {})
        front_art = "\n".join(sprite.get("front_grid", []))
        back_art = "\n".join(sprite.get("back_grid", []))
        palettes = sprite.get("palettes", {})
        default_color = sprite.get("default_color", 1)
        width = sprite.get("width", 25)
        height = sprite.get("height", 11)
        try:
            img = RenderImage(front_art=front_art, back_art=back_art, palettes=palettes, default_color=default_color, width=width, height=height)
            if sprite_var:
                globals()[sprite_var] = img
        except Exception:
            continue
except Exception:
    pass

# Load leveldata.json -> MAP_ROOMS
try:
    with open(_DATA_DIR / "leveldata.json", "r") as f:
        _ldata = json.load(f).get("maps", {})
    _map_rooms = {}
    for room_id, data in _ldata.items():
        room = {}
        room["width"] = data.get("width", 20)
        room["height"] = data.get("height", 10)
        room["spawn"] = tuple(data.get("spawn", [0, 0]))
        # normalize collections
        def _to_tuple_list(lst):
            return set(tuple(x) for x in lst) if isinstance(lst, list) else set()
        room["grass_tiles"] = _to_tuple_list(data.get("grass_tiles", []))
        room["water_tiles"] = _to_tuple_list(data.get("water_tiles", []))
        room["cut_trees"] = _to_tuple_list(data.get("cut_trees", []))
        room["trees"] = _to_tuple_list(data.get("trees", []))
        room["fog"] = _to_tuple_list(data.get("fog", []))
        # items, doors, npcs: keys may be strings "y,x" or lists
        def _norm_map(d):
            out = {}
            for k, v in (d or {}).items():
                if isinstance(k, str) and "," in k:
                    kk = tuple(int(x) for x in k.split(","))
                else:
                    kk = tuple(k) if isinstance(k, (list, tuple)) else k
                out[kk] = v
            return out
        room["items"] = _norm_map(data.get("items", {}))
        room["doors"] = _norm_map(data.get("doors", {}))
        room["npcs"] = _norm_map(data.get("npcs", {}))
        room["hill_tiles"] = _norm_map(data.get("hill_tiles", {}))
        room["legendary_mons"] = data.get("legendary_mons", {})
        _map_rooms[room_id] = room
    if _map_rooms:
        MAP_ROOMS = _map_rooms
except Exception:
    pass

# Merge items/shop data from itemsdata.json
try:
    with open(_DATA_DIR / "itemsdata.json", "r") as f:
        _idata = json.load(f).get("items", {})
    if isinstance(_idata, dict):
        SHOP_ITEMS.update(_idata)
except Exception:
    pass

# TRAINER_REWARDS may be provided from leveldata or separate json; keep empty fallback
try:
    # If leveldata defines trainer rewards at root, merge
    with open(_DATA_DIR / "leveldata.json", "r") as f:
        _ld = json.load(f)
        if isinstance(_ld, dict) and _ld.get("trainer_rewards"):
            TRAINER_REWARDS.update(_ld.get("trainer_rewards", {}))
except Exception:
    pass

# Ensure placeholder Mon and Moves objects exist to avoid AttributeError in modules that eagerly getattr
for mon_id in range(1, 152):
    name = globals().get(f"mon{mon_id}", None)
    if name is None:
        globals()[f"mon{mon_id}"] = Mon("missing", "nil", "nil", 0, 0, 0, 0, 0, 0, mon_id, 0)

# moves: ensuring up to 388 (original code referenced up to 387/388)
for move_id in range(1, 389):
    if globals().get(f"move{move_id}", None) is None:
        globals()[f"move{move_id}"] = Moves(f"move{move_id}", "normal", 1, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, "nil", "nil", False, -1, False, 0, 0, "placeholder")

# End of stats.py
