import curses
import random
import stats
import main

STAT_MAP = {
    "at": "stage_at",
    "de": "stage_de",
    "sp_at": "stage_spa",
    "sp_de": "stage_spd_def",
    "spd": "stage_spd",
    "eva": "stage_eva"
}

ENEMY_MAP = {
    "at": "enat",
    "de": "endf",
    "sp_at": "enspat",
    "sp_de": "enspdefence",
    "spd": "enspd",
    "eva": "eneva"
}

def battle_setup(stdscr):
    pool = mons.copy()
    p_mon, p_moves = select_pokemon_and_moves(stdscr, pool, "Player")
    e_mon, e_moves = select_pokemon_and_moves(stdscr, pool, "Enemy")
    player = BattleMon(p_mon, 50, p_moves)
    enemy = BattleMon(e_mon, 50, e_moves)
    return afightui(stdscr, player, enemy)

VISIBLE = 4

def select_from_list_scroll(stdscr, items, title, show_type=False, show_desc=False):
    scroll = 0
    cursor = 0
    while True:
        stdscr.clear()
        safe_addstr(stdscr, 0, 0, title)
        safe_addstr(stdscr, 1, 0, "-"*40)
        for i in range(VISIBLE):
            idx = scroll + i
            if idx >= len(items):
                break
            item = items[idx]
            if hasattr(item, "call"):
                name = item.call().capitalize()
                t2 = "" if getattr(item, "type2", "nil") == "nil" else f"/{item.type2.capitalize()}"
                line = f"{name} - {item.type.capitalize()}{t2}"
            elif hasattr(item, "type"):
                name = item.name.capitalize()
                line = f"{name} - {item.type.capitalize()}"
            else:
                name = item[0].strip('"').capitalize()
                line = f"{name} - {item[-1]}" if show_desc else name
            prefix = "> " if i == cursor else "  "
            safe_addstr(stdscr, 2+i, 0, prefix + line)
        key = stdscr.getch()
        curses.napms(100)
        if key == curses.KEY_UP:
            if cursor > 0: cursor -= 1
            elif scroll > 0: scroll -= 1
        elif key == curses.KEY_DOWN:
            if cursor < min(VISIBLE-1, len(items)-1):
                if scroll + cursor + 1 < len(items): cursor += 1
            elif scroll + VISIBLE < len(items): scroll += 1
        elif key == ord("z"):
            return scroll + cursor

TYPE_EFFECTIVENESS = {
    "normal": {"normal": 1,"fight": 1,"flying": 1,"poison": 1,"ground": 1,"rock": 0.5,"bug": 1,"ghost": 0,"steel": 0.5,"fire": 1,"water": 1,"grass": 1,"electric": 1,"psychic": 1,"ice": 1,"dragon": 1,"dark": 1 },
    "fight": {"normal": 2,"fight": 1,"flying": 0.5,"poison": 0.5,"ground": 1,"rock": 2,"bug": 0.5,"ghost": 0,"steel": 2,"fire": 1,"water": 1,"grass": 1,"electric": 1,"psychic": 0.5,"ice": 2,"dragon": 1,"dark": 2 },
    "flying": {"normal": 1,"fight": 2,"flying": 1,"poison": 1,"ground": 1,"rock": 0.5,"bug": 2,"ghost": 1,"steel": 0.5,"fire": 1,"water": 1,"grass": 2,"electric": 0.5,"psychic": 1,"ice": 1,"dragon": 1,"dark": 1},
    "poison": {"normal": 1,"fight": 1,"flying": 1,"poison": 0.5,"ground": 0.5,"rock": 0.5,"bug": 1,"ghost": 0.5,"steel": 0,"fire": 1,"water": 1,"grass": 2,"electric": 1,"psychic": 1,"ice": 1,"dragon": 1,"dark": 1},
    "ground": {"normal": 1,"fight": 1,"flying": 0,"poison": 2,"ground": 1,"rock": 2,"bug": 0.5,"ghost": 1,"steel": 2,"fire": 2,"water": 1,"grass": 0.5,"electric": 2,"psychic": 1,"ice": 1,"dragon": 1,"dark": 1},
    "rock": {"normal": 1,"fight": 0.5,"flying": 2,"poison": 1,"ground": 0.5,"rock": 1,"bug": 2,"ghost": 1,"steel": 0.5,"fire": 2,"water": 1,"grass": 1,"electric": 1,"psychic": 1,"ice": 2,"dragon": 1,"dark": 1},
    "bug": {"normal": 1,"fight": 0.5,"flying": 0.5,"poison": 0.5,"ground": 1,"rock": 1,"bug": 1,"ghost": 0.5,"steel": 0.5,"fire": 0.5,"water": 1,"grass": 2,"electric": 1,"psychic": 2,"ice": 1,"dragon": 1,"dark": 2},
    "ghost": {"normal": 0,"fight": 1,"flying": 1,"poison": 1,"ground": 1,"rock": 1,"bug": 1,"ghost": 2,"steel": 0.5,"fire": 1,"water": 1,"grass": 1,"electric": 1,"psychic": 2,"ice": 1,"dragon": 1,"dark": 0.5},
    "steel": {"normal": 1,"fight": 1,"flying": 1,"poison": 1,"ground": 1,"rock": 2,"bug": 1,"ghost": 1,"steel": 0.5,"fire": 0.5,"water": 0.5,"grass": 1,"electric": 0.5,"psychic": 1,"ice": 2,"dragon": 1,"dark": 1},
    "fire": {"normal": 1,"fight": 1,"flying": 1,"poison": 1,"ground": 1,"rock": 0.5,"bug": 2,"ghost": 1,"steel": 2,"fire": 0.5,"water": 0.5,"grass": 2,"electric": 1,"psychic": 1,"ice": 2,"dragon": 0.5,"dark": 1},
    "water": {"normal": 1,"fight": 1,"flying": 1,"poison": 1,"ground": 2,"rock": 2,"bug": 1,"ghost": 1,"steel": 1,"fire": 2,"water": 0.5,"grass": 0.5,"electric": 1,"psychic": 1,"ice": 1,"dragon": 0.5,"dark": 1},
    "grass": {"normal": 1,"fight": 1,"flying": 0.5,"poison": 0.5,"ground": 2,"rock": 2,"bug": 0.5,"ghost": 1,"steel": 0.5,"fire": 0.5,"water": 2,"grass": 0.5,"electric": 1,"psychic": 1,"ice": 1,"dragon": 0.5,"dark": 1},
    "electric": {"normal": 1,"fight": 1,"flying": 2,"poison": 1,"ground": 0,"rock": 1,"bug": 1,"ghost": 1,"steel": 1,"fire": 1,"water": 2,"grass": 0.5,"electric": 0.5,"psychic": 1,"ice": 1,"dragon": 0.5,"dark": 1},
    "psychic": {"normal": 1,"fight": 2,"flying": 1,"poison": 2,"ground": 1,"rock": 1,"bug": 1,"ghost": 1,"steel": 0.5,"fire": 1,"water": 1,"grass": 1,"electric": 1,"psychic": 0.5,"ice": 1,"dragon": 1,"dark": 0},
    "ice": {"normal": 1,"fight": 1,"flying": 2,"poison": 1,"ground": 2,"rock": 1,"bug": 1,"ghost": 1,"steel": 0.5,"fire": 0.5,"water": 0.5,"grass": 2,"electric": 1,"psychic": 1,"ice": 0.5,"dragon": 2,"dark": 1},
    "dragon": {"normal": 1,"fight": 1,"flying": 1,"poison": 1,"ground": 1,"rock": 1,"bug": 1,"ghost": 1,"steel": 0.5,"fire": 1,"water": 1,"grass": 1,"electric": 1,"psychic": 1,"ice": 1,"dragon": 2,"dark": 1},
    "dark": {"normal": 1,"fight": 0.5,"flying": 1,"poison": 1,"ground": 1,"rock": 1,"bug": 1,"ghost": 2,"steel": 0.5,"fire": 1,"water": 1,"grass": 1,"electric": 1,"psychic": 2,"ice": 1,"dragon": 1,"dark": 0.5}
}

def type_multiplier(move_type, defender):
    mult = 1.0
    chart = TYPE_EFFECTIVENESS.get(move_type, {})
    mult *= chart.get(defender.base.type, 1.0)
    if defender.base.type2 != "nil":
        mult *= chart.get(defender.base.type2, 1.0)
    return mult

mons = [getattr(stats, f"mon{i}") for i in range(1, 152) if hasattr(stats, f"mon{i}")]
moves_list = [
    stats.move1,
    stats.move2,
    stats.move3,
    stats.move4
]


def safe_addstr(stdscr, y, x, text):
    h, w = stdscr.getmaxyx()
    if 0 <= y < h and 0 <= x < w:
        stdscr.addstr(y, x, str(text)[: w - x])

def draw_divider(stdscr, y):
    h, w = stdscr.getmaxyx()
    safe_addstr(stdscr, y, 0, "=" * w)

def textbox(stdscr, text):
    h, w = stdscr.getmaxyx()
    top = max(0, h - 4)
    safe_addstr(stdscr, top, 0, "+" + "-" * (w - 2) + "+")
    safe_addstr(stdscr, top + 1, 0, "|" + " " * (w - 2) + "|")
    safe_addstr(stdscr, top + 2, 0, "+" + "-" * (w - 2) + "+")
    line = ""
    for ch in text:
        line += ch
        safe_addstr(stdscr, top + 1, 2, line[: w - 4])
        stdscr.refresh()
        curses.napms(int(main.textspeed*1000))
    while True:
        if stdscr.getch() == ord("z"):
            break
        
def redraw_battle(stdscr, player, enemy, menu_pos=0):
    stdscr.clear()
    draw_header(stdscr, player, enemy)
    draw_main_menu(stdscr, menu_pos)
    stdscr.refresh()

PHYSICAL_TYPES = ["normal", "fight", "poison", "ground", "flying", "bug", "rock", "ghost", "steel"]
SPECIAL_TYPES = ["fire", "water", "electric", "grass", "ice", "psychic", "dragon", "dark"]

class BattleMove:
    def __init__(self, move):
        self.name = move.name.capitalize()
        self.type = move.type.lower()
        self.pp_max = move.pp
        self.pp = move.pp
        self.power = move.pow
        self.acc = move.acc
        self.desc = move.desc

        self.at = move.at
        self.de = move.de
        self.sp_at = move.sp_at
        self.sp_de = move.sp_de
        self.spd = move.spd
        self.eva = move.eva

        self.enat = move.enat
        self.endf = move.endf
        self.enspat = move.enspat
        self.enspdef = move.enspdef
        self.enspd = move.enspd
        self.eneva = move.eneva

        self.hitprio = move.hitprio
        self.rhit = move.rhit
        self.crits = move.crits

        if self.type in PHYSICAL_TYPES:
            self.category = "physical"
        elif self.type in SPECIAL_TYPES:
            self.category = "special"
        else:
            self.category = "status"

class BattleMon:
    def __init__(self, base, level, moves):
        self.base = base
        self.level = level
        self.status = "OK"
        self.max_hp = int(((2*base.hp*level)/100) + level + 10)
        self.hp = self.max_hp
        self.at = int(((2*base.at*level)/100) + 5)
        self.de = int(((2*base.de*level)/100) + 5)
        self.spa = int(((2*base.sp_at*level)/100) + 5)      
        self.spd_def = int(((2*base.sp_de*level)/100) + 5)  
        self.spd = int(((2*base.spd*level)/100) + 5)      
        self.moves = [BattleMove(m) for m in moves]

        # Temporary battle stage stats
        self.stage_at = 0       
        self.stage_de = 0     
        self.stage_spa = 0   
        self.stage_spd_def = 0  
        self.stage_spd = 0    
        self.stage_eva = 0      
        self.stage_acc = 0     

    def name(self):
        return self.base.name
 
def damage_calc(attacker, defender, move):
    if move.power <= 0:
        return 0

    if move.category == "physical":
        atk = apply_stage(attacker.at, attacker.stage_at)
        defense = apply_stage(defender.de, defender.stage_de)
    elif move.category == "special":
        atk = apply_stage(attacker.spa, attacker.stage_spa)
        defense = apply_stage(defender.spd_def, defender.stage_spd_def)
    else:  
        return 0 

    base = (((2 * attacker.level) / 5 + 2) * move.power * atk / defense) / 50 + 2
    modifier = random.uniform(0.85, 1.0) * type_multiplier(move.type, defender)
    dmg = int(base * modifier)

    defender.hp = max(0, defender.hp - dmg)
    return dmg

def select_from_list(stdscr, items, title, show_type=False, show_desc=False):
    cursor = 0
    while True:
        stdscr.clear()
        safe_addstr(stdscr, 0, 0, title)
        safe_addstr(stdscr, 1, 0, "-"*40)
        for i in range(min(4, len(items))):
            item = items[i]
            if hasattr(item, "call"):
                name = item.call().capitalize()
                t2 = "" if item.type2=="nil" else f"/{item.type2.capitalize()}"
                line = f"{name} - {item.type.capitalize()}{t2}"
            else:
                name = item[0].strip('"').capitalize()
                line = f"{name} - {item[-1]}" if show_desc else name
            prefix = "> " if i==cursor else "  "
            safe_addstr(stdscr, i+2, 0, prefix + line)
        key = stdscr.getch()
        if key==curses.KEY_UP and cursor>0: cursor-=1
        elif key==curses.KEY_DOWN and cursor<len(items)-1: cursor+=1
        elif key==ord("z"): return cursor

def select_pokemon_and_moves(stdscr, pool, label):
    idx = select_from_list_scroll(stdscr, pool, f"{label} Pokémon", show_type=True)
    mon = pool.pop(idx)
    chosen = []
    for i in range(4):
        m = select_from_list_scroll(stdscr, moves_list, f"{mon.call().capitalize()} Move {i+1}", show_desc=True)
        chosen.append(moves_list[m])
    return mon, chosen

def apply_stage(stat, stage):
    if stage >= 0:
        return stat * (2 + stage) / 2
    else:
        return stat * 2 / (2 - stage)

#draw pls work aahssahhshsahsadds
def draw_header(stdscr, player, enemy):
    left = f"{player.base.name} [{player.status}] HP {player.hp}/{player.max_hp}"
    right = f"{enemy.base.name} [{enemy.status}] HP {enemy.hp}/{enemy.max_hp}"  
    safe_addstr(stdscr, 0, 0, f"{left} ------ {right}")
    draw_divider(stdscr, 1)

def draw_main_menu(stdscr, menu_pos):
    menu = ["Fight","Bag","Pokémon","Run"]
    row_start = 2
    col_spacing = 25
    for i, item in enumerate(menu):
        row = row_start + i//2
        col = (i%2)*col_spacing
        text = f">[{item}]<" if i==menu_pos else f"[{item}]"
        safe_addstr(stdscr, row, col, text)
    draw_divider(stdscr, row_start+2)

def draw_moves(stdscr, mon, highlight=-1):
    row_start = 5
    col_spacing = 25
    for j in range(2):
        for i in range(2):
            idx = j*2 + i
            if idx >= len(mon.moves): continue
            move = mon.moves[idx]
            sel = idx == highlight
            text = f"{move.name} PP{move.pp}/{move.pp_max}"
            text = f">[{text}]<" if sel else f"[{text}]"
            safe_addstr(stdscr, row_start + j, i*col_spacing, text)
    draw_divider(stdscr, row_start + 2)

def move_menu(stdscr, player, enemy):
    highlight = 0
    while True:
        stdscr.clear()
        draw_header(stdscr, player, enemy)
        draw_main_menu(stdscr, 0)
        draw_moves(stdscr, player, highlight)
        key = stdscr.getch()
        if key == curses.KEY_UP and highlight>1: highlight-=2
        elif key == curses.KEY_DOWN and highlight<2: highlight+=2
        elif key == curses.KEY_LEFT and highlight%2==1: highlight-=1
        elif key == curses.KEY_RIGHT and highlight%2==0 and highlight+1<len(player.moves): highlight+=1
        elif key == ord("x"): return None
        elif key == ord("z"):
            move = player.moves[highlight]
            if move.pp>0: return move

def afightui(stdscr, player, enemy):
    curses.curs_set(0)
    stdscr.keypad(True)
    menu_pos = 0

    while True:
        stdscr.clear()
        draw_header(stdscr, player, enemy)
        draw_main_menu(stdscr, menu_pos)
        stdscr.refresh()

        key = stdscr.getch()
        curses.napms(100)

        if key==curses.KEY_UP and menu_pos>1:
            menu_pos-=2
        elif key==curses.KEY_DOWN and menu_pos<2:
            menu_pos+=2
        elif key==curses.KEY_LEFT and menu_pos%2==1:
            menu_pos-=1
        elif key==curses.KEY_RIGHT and menu_pos%2==0 and menu_pos+1<4:
            menu_pos+=1

        elif key==ord("z"):
            if menu_pos!=0:
                textbox(stdscr, f"{['Bag','Pokémon','Run'][menu_pos-1]} does not work yet")
                continue

            player_move = move_menu(stdscr, player, enemy)
            if player_move is None:
                continue

            usable = [m for m in enemy.moves if m.pp>0]
            enemy_move = random.choice(usable) if usable else None

            turn = sorted(
                [(player, player_move), (enemy, enemy_move)],
                key=lambda x: x[0].spd,
                reverse=True
            )

            for user, move in turn:
                if move is None or move.pp <= 0:
                    continue

                target = enemy if user == player else player
                move.pp -= 1

                redraw_battle(stdscr, player, enemy)
                textbox(stdscr, f"{user.name()} used {move.name}!")

                # --- Apply stat changes safely ---

                for stat, stage_attr in STAT_MAP.items():
                    change = getattr(move, stat, 0)
                    if change != 0:
                        setattr(
                            user,
                            stage_attr,
                            min(6, max(-6, getattr(user, stage_attr) + change))
                        )
                        textbox(
                            stdscr,
                            f"{user.name()}'s {stat.replace('_',' ').upper()} rose!"
                        )

                    en_change = getattr(move, ENEMY_MAP[stat], 0)
                    if en_change != 0:
                        setattr(
                            target,
                            stage_attr,
                            min(6, max(-6, getattr(target, stage_attr) + en_change))
                        )
                        textbox(
                            stdscr,
                            f"{target.name()}'s {stat.replace('_',' ').upper()} fell!"
                        )


                # --- Deal damage ---
                dmg = damage_calc(user, target, move)
                redraw_battle(stdscr, player, enemy)
                if dmg > 0:
                    mult = type_multiplier(move.type, target)
                    if mult > 1:
                        textbox(stdscr, "It's super effective!")
                    elif mult < 1:
                        textbox(stdscr, "It's not very effective...")

                if target.hp <= 0:
                    redraw_battle(stdscr, player, enemy)
                    textbox(stdscr, f"{target.name()} fainted!")
                    return "win" if target == enemy else "lose"
