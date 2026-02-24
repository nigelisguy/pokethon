import curses
import random
import stats
import main


STAT_DISPLAY = {
    "at": "Attack",
    "de": "Defense",
    "sp_at": "Special Attack",
    "sp_de": "Special Defense",
    "spd": "Speed",
    "eva": "Evasion",
    "acc": "Accuracy"
}
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

def effect_heal_self(stdscr, user):
    heal = user.max_hp // 2
    user.hp = min(user.max_hp, user.hp + heal)
    textbox(stdscr, f"{user.name()} regained health!")

def apply_status(status_list, new_status, clears=None):
    if new_status in status_list:
        return
    if clears:
        for s in clears:
            if s in status_list:
                status_list.remove(s)
    status_list.append(new_status)

def poison(target):
    apply_status(target.statuses, "poison", ["burn", "sleep", "confuse", "flinch"])
def poison_enemy(target):
    apply_status(target.statuses, "poison", ["burn", "sleep", "confuse", "flinch"])

def para(target):
    apply_status(target.statuses, "paralyze", ["burn", "sleep", "bind", "confuse", "flinch"])

def para_enemy(target):
    apply_status(target.statuses, "paralyze", ["burn", "sleep", "confuse", "flinch"])

def burn(target):
    apply_status(target.statuses, "burn", ["poison", "sleep", "confuse", "flinch"])

def burn_enemy(target):
    apply_status(target.statuses, "burn", ["poison", "sleep", "confuse", "flinch"])

def sleep(target):
    apply_status(target.statuses, "sleep", ["poison", "burn", "confuse", "flinch"])

def sleep_enemy(target):
    apply_status(target.statuses, "sleep", ["poison", "burn", "confuse", "flinch"])

def bind(target):
    apply_status(target.statuses, "bind")

def bind_enemy(target):
    apply_status(target.statuses, "bind")

def confuse(target):
    apply_status(target.statuses, "confuse", ["poison", "burn", "sleep", "flinch"])

def confuse_enemy(target):
    apply_status(target.statuses, "confuse", ["poison", "burn", "sleep", "flinch"])

def flinch(target):
    apply_status(target.statuses, "flinch")

def flinch_enemy(target):
    apply_status(target.statuses, "flinch")

EFFECT_HANDLERS = {
    "poison_self": lambda s, u, t: poison(u),
    "poison_enemy": lambda s, u, t: poison(t),
    "burn_self": lambda s, u, t: burn(u),
    "burn_enemy": lambda s, u, t: burn(t),
    "sleep_self": lambda s, u, t: sleep(u),
    "sleep_enemy": lambda s, u, t: sleep(t),
}



def battle_setup(stdscr):
    pool = mons.copy()
    (p_mon, p_moves), (e_mon, e_moves) = select_teams_and_moves(
    stdscr,
    pool,
    pool.copy(),
    moves_list
    )
    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(2, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    player = BattleMon(p_mon, 50, p_moves)
    enemy = BattleMon(e_mon, 50, e_moves)
    return afightui(stdscr, player, enemy)

def status_effect_manager(stdscr, mon):
    if "poison" in mon.statuses:
        dmg = mon.max_hp // 8
        mon.hp = max(0, mon.hp - dmg)
        textbox(stdscr, f"{mon.name()} is hurt by poison!")
    if "burn" in mon.statuses:
        dmg = mon.max_hp // 16
        mon.hp = max(0, mon.hp - dmg)
        textbox(stdscr, f"{mon.name()} is hurt by its burn!")
    if "sleep" in mon.statuses:
        textbox(stdscr, f"{mon.name()} is fast asleep!")
    if "bind" in mon.statuses:
        dmg = mon.max_hp // 16
        mon.hp = max(0, mon.hp - dmg)
        textbox(stdscr, f"{mon.name()} is hurt by binding!")
    if "confuse" in mon.statuses:
        if random.random() < 0.5:
            dmg = damage_calc(mon, mon, random.choice(mon.moves))
            textbox(stdscr, f"{mon.name()} hurt itself in its confusion!")
            redraw_battle(stdscr, mon)
    if "flinch" in mon.statuses:
        textbox(stdscr, f"{mon.name()} flinched!")
        mon.statuses.remove("flinch")

def select_from_list_scroll(stdscr, items, title, show_type=False, show_desc=False):
    scroll = 0
    cursor = 0
    while True:
        stdscr.clear()
        h, w = stdscr.getmaxyx()
        visible = max(1, h - 4)  
        safe_addstr(stdscr, 0, 0, title)
        safe_addstr(stdscr, 1, 0, "-"*40)
        for i in range(visible):
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
            if cursor < min(visible-1, len(items)-1):
                if scroll + cursor + 1 < len(items): cursor += 1
            elif scroll + visible < len(items): scroll += 1
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
moves_list = [getattr(stats, f"move{i}") for i in range(1, 57)]


def safe_addstr(stdscr, y, x, text):
    try:
        h, w = stdscr.getmaxyx()
        if y < h and x < w:
            stdscr.addstr(y, x, str(text)[:w - x])
    except curses.error:
        pass 

def draw_divider(stdscr, y):
    h, w = stdscr.getmaxyx()
    safe_addstr(stdscr, y, 0, ">" * 2)

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
        self.enefc = move.enefc
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
        self.statuses = []
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

def select_teams_and_moves(stdscr, player_pool, cpu_pool, moves_list):
    player_mon=None
    cpu_mon=None
    player_moves=[None]*4
    cpu_moves=[None]*4

    col=0
    row=0

    move_menu=False
    move_cursor=0

    while True:
        stdscr.clear()

        safe_addstr(stdscr,0,5,"Player")
        safe_addstr(stdscr,0,30,"CPU")

        if move_menu:
            safe_addstr(stdscr,0,55,"Moves")

        def draw_side(x, mon, moves, selected):
            
            name = "[Select Pokémon]" if not mon else mon.call().capitalize()
            prefix = "> " if selected and row == 0 and not move_menu else "  "
            safe_addstr(stdscr, 2, x, prefix + name)

            for i in range(4):
                y = 4 + i
                mname = "-"
                if moves[i]:
                    mname = moves[i].call().capitalize()[:20] 
                prefix = "> " if selected and row == i + 1 and not move_menu else "  "
                safe_addstr(stdscr, y, x, prefix + mname)

        draw_side(5,player_mon,player_moves,col==0)
        draw_side(30,cpu_mon,cpu_moves,col==1)

        if move_menu:
            for i,m in enumerate(moves_list):
                name = m.call().capitalize()
                prefix="> " if i==move_cursor else "  "
                safe_addstr(stdscr,2+i,55,prefix+name)

        ok_prefix="> " if row==5 and not move_menu else "  "
        safe_addstr(stdscr,9,20,ok_prefix+"[ OK ]")

        key=stdscr.getch()

        if move_menu:
            if key==curses.KEY_UP and move_cursor>0:
                move_cursor-=1
            elif key==curses.KEY_DOWN and move_cursor<len(moves_list)-1:
                move_cursor+=1
            elif key==ord("z"):
                if col==0:
                    player_moves[row-1]=moves_list[move_cursor]
                else:
                    cpu_moves[row-1]=moves_list[move_cursor]
                move_menu=False
            elif key==ord("x"):
                move_menu=False
            continue

        if key==curses.KEY_UP and row>0:
            row-=1
        elif key==curses.KEY_DOWN and row<5:
            row+=1
        elif key==curses.KEY_LEFT:
            col=0
        elif key==curses.KEY_RIGHT:
            col=1

        elif key==ord("z"):
            if row==0:
                if col==0:
                    i=select_from_list_scroll(stdscr,player_pool,"Select Player Pokémon",show_type=True)
                    player_mon=player_pool.pop(i)
                else:
                    i=select_from_list_scroll(stdscr,cpu_pool,"Select CPU Pokémon",show_type=True)
                    cpu_mon=cpu_pool.pop(i)

            elif 1<=row<=4:
                move_menu=True
                move_cursor=0

            elif row==5:
                if player_mon and cpu_mon:
                    return (player_mon,player_moves),(cpu_mon,cpu_moves)
        
def apply_stage(stat, stage):
    if stage >= 0:
        return stat * (2 + stage) / 2
    else:
        return stat * 2 / (2 - stage)

#draw pls work aahssahhshsahsadds
def draw_header(stdscr, player, enemy):
    left = f"{player.base.name} [{player.statuses}] HP {player.hp}/{player.max_hp}"
    right = f"{enemy.base.name} [{enemy.statuses}] HP {enemy.hp}/{enemy.max_hp}"  
    safe_addstr(stdscr, 0, 0, f"{left} ------ {right}")
    draw_divider(stdscr, 1)

def draw_main_menu(stdscr, menu_pos, player=None, show_moves=False):
    menu = ["Fight","Pokémon","Bag","Run","Dynamax","Tera","Mega Evo","???"]
    row_start = 1
    col_spacing = 12
    # Top 2x2 menu buttons
    for i in range(4):
        row = row_start + 1 + (i // 2)
        col = (i % 2) * col_spacing
        text = f"[{menu[i]}]"
        if i == menu_pos:
            stdscr.attron(curses.color_pair(1))
            safe_addstr(stdscr, row, col, text)
            stdscr.attroff(curses.color_pair(1))
        else:
            safe_addstr(stdscr, row, col, text)

    draw_divider(stdscr, 4)

    # Bottom 1x4 buttons
    bottom_colors = [2,3,4,0]
    row = row_start + 4
    for i in range(4,8):
        col = (i-4)*col_spacing
        text = f"[{menu[i]}]"
        color = curses.color_pair(bottom_colors[i-4])
        if i == menu_pos:
            stdscr.attron(curses.color_pair(1))
            safe_addstr(stdscr, row, col, text)
            stdscr.attroff(curses.color_pair(1))
        else:
            stdscr.attron(color)
            safe_addstr(stdscr, row, col, text)
            stdscr.attroff(color)

    # Only draw moves if show_moves is True
    if show_moves and player:
        move_col = 25  # adjust horizontal position
        move_row_start = row_start + 1
        for idx, move in enumerate(player.moves):
            text = f"{idx+1}. {move.name} PP{move.pp}/{move.pp_max}"
            safe_addstr(stdscr, move_row_start + idx, move_col, text)
            
def draw_moves(stdscr, mon, highlight=-1, col=None, row_start=None):
    if col is None: col = 28
    if row_start is None: row_start = 1
    for idx, move in enumerate(mon.moves):
        text = f"{idx+1}. {move.name} PP{move.pp}/{move.pp_max}"
        if idx == highlight:
            stdscr.attron(curses.color_pair(1))
            safe_addstr(stdscr, row_start + idx, col, text)
            stdscr.attroff(curses.color_pair(1))
        else:
            safe_addstr(stdscr, row_start + idx, col, text)

def move_menu(stdscr, player, enemy):
    highlight = 0
    max_moves = len(player.moves)
    while True:
        stdscr.clear()
        draw_header(stdscr, player, enemy)
        draw_main_menu(stdscr, 0, player)  
        draw_moves(stdscr, player, highlight)
        key = stdscr.getch()

        if key == curses.KEY_UP:
            if highlight > 0:
                highlight -= 1
        elif key == curses.KEY_DOWN:
            if highlight < max_moves - 1:
                highlight += 1
        elif key == ord("x"):
            return None
        elif key == ord("z"):
            move = player.moves[highlight]
            if move.pp > 0:
                return move

def afightui(stdscr, player, enemy):
    curses.curs_set(0)
    stdscr.keypad(True)
    
    key_map = {
        ord("a"): 4,  # Dynamax
        ord("s"): 5,  # Tera
        ord("d"): 6,  # Mega Evo
        ord("f"): 7   # ???
    }

    menu_pos = 0  # top-left Fight/Pokémon/Bag/Run

    while True:
        stdscr.clear()
        draw_header(stdscr, player, enemy)
        draw_main_menu(stdscr, menu_pos, player)
        stdscr.refresh()

        key = stdscr.getch()
        curses.napms(50)

        # Navigate top 2x2 menu (Fight/Pokémon/Bag/Run)
        if key==curses.KEY_UP and menu_pos>1:
            menu_pos-=2
        elif key==curses.KEY_DOWN and menu_pos<2:
            menu_pos+=2
        elif key==curses.KEY_LEFT and menu_pos%2==1:
            menu_pos-=1
        elif key==curses.KEY_RIGHT and menu_pos%2==0:
            menu_pos+=1

        # Direct select bottom 1x4 menu with Z/X/C/V
        elif key in key_map:
            choice = key_map[key]
            textbox(stdscr, f"{['Dynamax','Tera','Mega Evo','???'][choice-4]} does not work yet")
            continue

        # Select top-left Fight
        elif key==ord("z") and menu_pos==0:
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
                if random.randint(1, 100) > move.acc and move.acc != -1:
                    textbox(stdscr, f"{user.name()} used {move.name}!")
                    textbox(stdscr, f"{user.name()} missed!")
                else:
                    textbox(stdscr, f"{user.name()} used {move.name}!")
                    if move.enefc in EFFECT_HANDLERS:
                        EFFECT_HANDLERS[move.enefc](stdscr, user, target)
                        
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
                                f"{user.name()}'s {STAT_DISPLAY[stat]} rose!"
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
                                f"{target.name()}'s {STAT_DISPLAY[stat]} fell!"
                            )

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

            status_effect_manager(stdscr, player)
            status_effect_manager(stdscr, enemy)