import curses
import random
import stats
import overworld
player_result = []
enemy_result = []
EASY_OFFSET=15

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
    textbox(stdscr, f"{user.base.name.capitalize()} regained health!")

def apply_status(status_list, new_status, clears=None):
    if new_status in status_list:
        return
    if clears:
        for s in clears:
            if s in status_list:
                status_list.remove(s)
    status_list.append(new_status)


def draw_top_banner(stdscr):
    h, w = stdscr.getmaxyx()
    safe_addstr(stdscr, 0, 0, "+" + "━"*(w-2) + "+", 0)

def sdraw_top_banner(stdscr):
    h, w = stdscr.getmaxyx()
    safe_addstr(stdscr, 0, 0, "+" + "━"*(w-2) + "+", 0)
    safe_addstr(stdscr, 1, 2, "mons png here", 0)
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
    (p_mon, p_moves), (e_mon, e_moves), mode = select_teams_and_moves(
    stdscr,
    pool,
    pool.copy(),
    moves_list
    )
    curses.start_color()
    player = BattleMon(p_mon, 50, p_moves)
    enemy = BattleMon(e_mon, 50, e_moves)
    return afightui(stdscr, player, enemy, mode)

def status_effect_manager(stdscr, mon):
    if "poison" in mon.statuses:
        dmg = mon.max_hp // 8
        mon.hp = max(0, mon.hp - dmg)
        textbox(stdscr, f"{mon.base.name.capitalize()} is hurt by poison!")
    if "burn" in mon.statuses:
        dmg = mon.max_hp // 16
        mon.hp = max(0, mon.hp - dmg)
        textbox(stdscr, f"{mon.base.name.capitalize()} is hurt by its burn!")
    if "sleep" in mon.statuses:
        textbox(stdscr, f"{mon.base.name.capitalize()} is fast asleep!")
    if "bind" in mon.statuses:
        dmg = mon.max_hp // 16
        mon.hp = max(0, mon.hp - dmg)
        textbox(stdscr, f"{mon.base.name.capitalize()} is hurt by binding!")
    if "confuse" in mon.statuses:
        if random.random() < 0.5:
            dmg = damage_calc(mon, mon, random.choice(mon.moves), stdscr)
            textbox(stdscr, f"{mon.base.name.capitalize()} hurt itself in its confusion!")
            redraw_battle(stdscr, mon)
    if "flinch" in mon.statuses:
        textbox(stdscr, f"{mon.base.name.capitalize()} flinched!")
        mon.statuses.remove("flinch")

def select_from_list_scroll(stdscr, items, title, show_type=False):
    cursor = 0
    view = 0

    while True:
        stdscr.clear()
        safe_addstr(stdscr,0,5,title,0)

        visible_items = items[view:view+6]

        if view > 0:
            safe_addstr(stdscr,1,5,"▲",0)

        for i,item in enumerate(visible_items):
            idx = view + i
            name = item.call().capitalize()
            prefix = "> " if idx == cursor else "  "
            safe_addstr(stdscr,2+i,5,prefix+name,0)

        if view+6 < len(items):
            safe_addstr(stdscr,8,5,"▼",0)

        key = stdscr.getch()

        if key == curses.KEY_UP and cursor > 0:
            cursor -= 1
        elif key == curses.KEY_DOWN and cursor < len(items)-1:
            cursor += 1
        elif key == ord("z"):
            return cursor
        elif key == ord("x"):
            return None

        if cursor < view:
            view = cursor
        elif cursor >= view + 6:
            view = cursor - 5

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
moves_list = [getattr(stats, f"move{i}") for i in range(1,388)]


def safe_addstr(stdscr, y, x, text,y_offset=EASY_OFFSET):
    try:
        h, w = stdscr.getmaxyx()
        y += y_offset
        if y < h and x < w:
            stdscr.addstr(y, x, str(text)[:w - x])
    except curses.error:
        pass 

def draw_divider(stdscr, y):
    h, w = stdscr.getmaxyx()#pls delete

def textbox(stdscr, text):
    h, w = stdscr.getmaxyx()
    top = max(0, h - 4)
    safe_addstr(stdscr, top + 1, 0, "╔" + "═" * (w - 2) + "╗ ",0)
    safe_addstr(stdscr, top + 2, 0, "║" + " " * (w - 2) + "║",0)
    safe_addstr(stdscr, top + 3, 0, "╚" + "═" * (w - 2) + "╝",0)
    line = ""
    for ch in text:
        line += ch
        safe_addstr(stdscr, top + 2, 2, line[: w - 4],0)
        stdscr.refresh()
        curses.napms(int(0.01*1000))#fix textspeed thing later
    while True:
        if stdscr.getch() == ord("z"):
            break
        
def redraw_battle(stdscr, player, enemy, menu_pos=0):
    stdscr.clear()
    draw_top_banner(stdscr)
    draw_main_menu(stdscr, menu_pos, player, enemy)
    stats.substitude.draw(stdscr)
    draw_header(stdscr, player, enemy)
    stdscr.refresh()

PHYSICAL_TYPES = ["normal", "fight", "poison", "ground", "flying", "bug", "rock", "ghost", "steel"]
SPECIAL_TYPES = ["fire", "water", "electric", "grass", "ice", "psychic", "dragon", "dark"]
pplist = [-1,-1,-1,-1]
class BattleMove:
    def __init__(self, move, order):
        self.enefc = move.enefc
        self.name = move.name.capitalize()
        self.type = move.type.lower()
        self.pp_max = move.pp
        if int(pplist[order]) == -1:
            self.pp = move.pp
        else:
            self.pp = pplist[order]
        self.power = move.pow
        self.acc = move.acc
        self.desc = move.desc
        self.order = order

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
    def __init__(self, base, level, moves, hp=-1):
        self.base = base
        self.level = level
        self.statuses = []
        self.max_hp = int(((2*base.hp*level)/100) + level + 10)
        if hp is None or hp <= -1:
            self.hp = int(((2*base.hp*level)/100) + level + 10)
        else:
            self.hp = hp
        self.at = int(((2*base.at*level)/100) + 5)
        self.de = int(((2*base.de*level)/100) + 5)
        self.spa = int(((2*base.sp_at*level)/100) + 5)      
        self.spd_def = int(((2*base.sp_de*level)/100) + 5)  
        self.spd = int(((2*base.spd*level)/100) + 5)      
        self.moves = [BattleMove(move_instance, order=i) for i, move_instance in enumerate(moves)]

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
    def result(self):
        return (self.base.name, self.level, self.hp, self.max_hp, self.statuses)
 
def damage_calc(attacker, defender, move, stdscr, player=None, enemy=None):
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

    target_hp_final = max(0, defender.hp - dmg)
    while defender.hp > target_hp_final:
        defender.hp -= 1
        if defender.hp < target_hp_final:
            defender.hp = target_hp_final
        if player and enemy:
            redraw_battle(stdscr, player, enemy)
        else:
            redraw_battle(stdscr, attacker, defender)
        delay = max(1, int(1000/dmg))
        curses.napms(delay)

    return dmg

def choose_mode(stdscr):
    options = ["Player vs Player [NEW!!!!!!!!!]", "Player vs Clanker","Online, if i ever learn to use api(s)..."]
    cursor = 0

    while True:
        stdscr.clear()
        safe_addstr(stdscr, 0, 5, "Choose Mode", 0)

        for i, opt in enumerate(options):
            prefix = "> " if i == cursor else "  "
            safe_addstr(stdscr, 1+i, 5, prefix + opt, 0)

        key = stdscr.getch()

        if key == curses.KEY_UP and cursor > 0:
            cursor -= 1
        elif key == curses.KEY_DOWN and cursor < len(options) - 1:
            cursor += 1
        elif key == ord("z"):
            return cursor  
        
def select_teams_and_moves(stdscr, player_pool, cpu_pool, moves_list):
    mode = choose_mode(stdscr)
    player_mon=None
    cpu_mon=None
    player_moves=[None]*4
    cpu_moves=[None]*4

    col=0
    row=0

    move_menu=False
    move_cursor=0
    move_view=0

    while True:
        stdscr.clear()

        safe_addstr(stdscr,0,5,"Player",0)
        safe_addstr(stdscr,0,30,"CPU",0)

        if move_menu:
            menu_x = 5
            menu_y = 0
            safe_addstr(stdscr,menu_y,menu_x,"Select Move",0)

        def draw_side(x, mon, moves, selected):
            name = "[Select Pokémon]" if not mon else mon.call().capitalize()
            prefix = "> " if selected and row == 0 and not move_menu else "  "
            safe_addstr(stdscr, 2, x, prefix + name,0)

            for i in range(4):
                y = 4 + i
                mname = "━"
                if moves[i]:
                    mname = moves[i].call().capitalize()[:20]
                prefix = "> " if selected and row == i + 1 and not move_menu else "  "
                safe_addstr(stdscr, y, x, prefix + mname,0)

        draw_side(5,player_mon,player_moves,col==0)
        draw_side(30,cpu_mon,cpu_moves,col==1)

        if move_menu:
            safe_addstr(stdscr,1,55,"▲" if move_view>0 else " ",0)

            visible_moves = moves_list[move_view:move_view+6]

            for i,m in enumerate(visible_moves):
                idx = move_view + i
                name = m.call().capitalize()
                prefix="> " if idx==move_cursor else "  "
                safe_addstr(stdscr,menu_y+2+i,menu_x,prefix+name,0)
                
            if move_view+6 < len(moves_list):
                safe_addstr(stdscr,8,55,"▼",0)
    
        ok_prefix="> " if row==5 and not move_menu else "  "
        safe_addstr(stdscr,9,20,ok_prefix+"[ OK ]",0)

        key=stdscr.getch()

        if move_menu:
            if key==curses.KEY_UP and move_cursor>0:
                move_cursor-=1
            elif key==curses.KEY_DOWN and move_cursor<len(moves_list)-1:
                move_cursor+=1

            if move_cursor < move_view:
                move_view = move_cursor
            elif move_cursor >= move_view + 6:
                move_view = move_cursor - 5

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
                move_view=0

            elif row==5:
                if player_mon and cpu_mon:
                    return (player_mon,player_moves),(cpu_mon,cpu_moves), mode
                else:
                    textbox(stdscr, "Fill In Everything First Please")
    
def apply_stage(stat, stage):
    if stage >= 0:
        return stat * (2 + stage) / 2
    else:
        return stat * 2 / (2 - stage)

def draw_header(stdscr, player, enemy):
    # capitalize first letter
    p_name = player.base.name.capitalize()
    e_name = enemy.base.name.capitalize()

    # build strings with level inside
    left = f"{p_name} LVL{player.level} EFF{player.statuses} HP {player.hp}/{player.max_hp}"
    right = f"{e_name} LVL{enemy.level} EFF{enemy.statuses} HP {enemy.hp}/{enemy.max_hp}"

    # center both sides nicely
    line = f"┃ {left:^35} ------ {right:^35} ┃"

    safe_addstr(stdscr, 0, 0, line, 14)
    draw_divider(stdscr, 1)

blocks = "▏▎▍▌▋▊▉█"
def make_hp_bar(current, max_hp, length=10):
    if max_hp <= 0:
        return " " * length, 15

    ratio = max(0, min(1, current / max_hp))

    # color logic
    if ratio > 0.5:
        color = 13
    elif ratio > 0.2:
        color = 14
    else:
        color = 15

    total = ratio * length
    full = int(total)
    remainder = total - full

    bar = "█" * full
    if full < length and remainder > 0:
        index = int(remainder * (len(blocks) - 1))
        bar += blocks[index]

    if current > 0 and bar == "":
        bar = "▏"

    bar = bar.ljust(length)

    return bar, color

def draw_main_menu(stdscr, menu_pos, player=None, enemy=None,show_moves=False):
    h, w = stdscr.getmaxyx()
    rows = list(range(1, 13)) + [14] 
    for y in rows:
        safe_addstr(stdscr, y, 0, "┃" + " " * (w - 2) + "┃", 0)
    safe_addstr(stdscr, 13, 0, "┏" + "━" * (w - 2) + "┓",0)
    line = f"├"+  " "*39 + "┬" + "━" * 38 + "┤"
    safe_addstr(stdscr, 15, 0, line[:w].ljust(w), 0)
    player_bar, p_color = make_hp_bar(player.hp, player.max_hp)
    enemy_bar, e_color = make_hp_bar(enemy.hp, enemy.max_hp)
    safe_addstr(stdscr, 15, 2, "HP",0)
    stdscr.attron(curses.color_pair(p_color))
    safe_addstr(stdscr, 15, 4, player_bar,0)
    stdscr.attroff(curses.color_pair(p_color))
    safe_addstr(stdscr, 15, 25, "HP",0)
    stdscr.attron(curses.color_pair(e_color))
    safe_addstr(stdscr, 15, 27, enemy_bar,0)
    stdscr.attroff(curses.color_pair(e_color))
    safe_addstr(stdscr, 16, 0,"├" + "━" * 39 + "┤" + " " * 38 + "┃",0)
    safe_addstr(stdscr, 17, 0, "┃" + " " * 38 + " ┃" + " " * 38 + "┃",0)
    safe_addstr(stdscr, 18, 0, "┃" + " " * 38 + " ┃" + " " * 38 + "┃",0)
    safe_addstr(stdscr, 19, 0,"├" + "━" * 39 + "┤" +  " " * 38 + "┃",0)
    safe_addstr(stdscr, 20, 0,"┃",0)
    safe_addstr(stdscr, 20, 40,"├" + "━" * 38 + "┤",0)
    safe_addstr(stdscr, 21, 0, "┗" + "━" * (w - 2) + "┛",0)
    draw_top_banner(stdscr)
    menu = ["-----Fight-----|","----Pokémon----|","------Bag------|","------Run------|","-","-","-","-"]
    row_start = 1
    col_spacing = 10
    bottom_colors = [7,2,4,6]
    for i in range(4):
        row = row_start + 1 + (i // 2)
        col = (i % 2) * (col_spacing+8)
        text = f"[{menu[i]}]"
        color = curses.color_pair(bottom_colors[i-4])
        if i == menu_pos:
            stdscr.attron(curses.color_pair(8))
            safe_addstr(stdscr, row, col+2, text)
            stdscr.attroff(curses.color_pair(8))
        else:
            stdscr.attron(color)
            safe_addstr(stdscr, row, col+2, text)
            stdscr.attroff(color)

    draw_divider(stdscr, 4)

    bottom_colors = [5,3,2,2]
    row = row_start + 4
    for i in range(4,8):
        col = (i-4)*col_spacing
        text = f" [{menu[i]}] "
        color = curses.color_pair(bottom_colors[i-4])
        if i == menu_pos:
            stdscr.attron(curses.color_pair(1))
            safe_addstr(stdscr, row, col+1, text)
            stdscr.attroff(curses.color_pair(1))
        else:
            stdscr.attron(color)
            safe_addstr(stdscr, row, col+1, text)
            stdscr.attroff(color)

    if show_moves and player:
        move_col = 25  
        move_row_start = row_start + 1
        for idx, move in enumerate(player.moves):
            text = f"{idx+1}. {move.name} PP{move.pp}/{move.pp_max}"
            safe_addstr(stdscr, move_row_start + idx, move_col, text)
            
def draw_moves(stdscr, mon, highlight=-1, col=None, row_start=None):
    if col is None: col = 42
    if row_start is None: row_start = 1
    for idx, move in enumerate(mon.moves):
        text = f"[{f'{move.name} PP{move.pp}/{move.pp_max}':^20}]"
        if idx == highlight:
            stdscr.attron(curses.color_pair(1))
            safe_addstr(stdscr, row_start + idx, col, text)
            stdscr.attroff(curses.color_pair(1))
        else:
            safe_addstr(stdscr, row_start + idx, col, text)

def draw_bag(stdscr, mon, highlight=-1):
    row_start = 1

    for i, item in enumerate(overworld.inventory):
        for name, quantity in item.items():
            text = f"[ {name.upper()} x{quantity} ]"

            if i == highlight:
                stdscr.attron(curses.color_pair(1))
                safe_addstr(stdscr, row_start + i, 42, text)
                stdscr.attroff(curses.color_pair(1))
            else:
                safe_addstr(stdscr, row_start + i, 42, text)
            
def bag_menu(stdscr, player, enemy):
    highlight = 0

    items = overworld.inventory

    while True:
        stdscr.clear()
        draw_top_banner(stdscr)
        draw_main_menu(stdscr, 0, player, enemy)
        stats.substitude.draw(stdscr)
        draw_bag(stdscr, player, highlight)
        draw_header(stdscr, player, enemy)

        key = stdscr.getch()

        if key == curses.KEY_UP:
            if highlight > 0:
                highlight -= 1

        elif key == curses.KEY_DOWN:
            if highlight < len(items) - 1:
                highlight += 1

        elif key == ord("x"):
            return None

        elif key == ord("z"):
            item_dict = items[highlight]
            item_name = list(item_dict.keys())[0]
            item_value = item_dict[item_name]

            return item_name, item_value

def move_menu(stdscr, player, enemy):
    highlight = 0
    max_moves = len(player.moves)
    while True:
        stdscr.clear()
        draw_top_banner(stdscr)
        draw_main_menu(stdscr, 0, player, enemy)  
        stats.substitude.draw(stdscr)
        draw_moves(stdscr, player, highlight)
        draw_header(stdscr, player, enemy)
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

def afightui(stdscr, player, enemy, mode):
    import stats
    curses.curs_set(0)
    stdscr.keypad(True)
    key_map = {
        ord("a"): 4,  
        ord("s"): 5,  
        ord("d"): 6,  
        ord("f"): 7   #fix later
    }

    menu_pos = 0  

    while True:
        turn=None
        stdscr.clear()
        draw_main_menu(stdscr, menu_pos, player, enemy)
        stats.substitude.draw(stdscr)
        draw_header(stdscr, player, enemy)
        stdscr.refresh()

        key = stdscr.getch()
        curses.napms(50)

        if key==curses.KEY_UP and menu_pos>1:
            menu_pos-=2
        elif key==curses.KEY_DOWN and menu_pos<2:
            menu_pos+=2
        elif key==curses.KEY_LEFT and menu_pos%2==1:
            menu_pos-=1
        elif key==curses.KEY_RIGHT and menu_pos%2==0:
            menu_pos+=1

        elif key in key_map:
            choice = key_map[key]
            #textbox(stdscr, f"{['bro'][choice-4]} does not work yet")
            continue
        elif key==ord("z") and menu_pos==3:
            textbox(stdscr,f"You ran away!")
            return "run"
        elif key == ord("z") and menu_pos == 2:
            item = bag_menu(stdscr, player, enemy)

            if item is None:
                continue

            usable = [m for m in enemy.moves if m.pp > 0]
            enemy_move = random.choice(usable) if usable else None

            turn = sorted(
                [
                    (player, "item", item),
                    (enemy, "move", enemy_move)
                ],
                key=lambda x: x[0].spd,
                reverse=True
            )

        elif key==ord("z") and menu_pos==0:
            player_move = move_menu(stdscr, player, enemy)
            if player_move is None:
                continue
            if mode == 0:  
                textbox(stdscr, "Player 2 Turn")
                enemy_move = move_menu(stdscr, enemy, player)
                if enemy_move is None:
                    continue
            else:  
                usable = [m for m in enemy.moves if m.pp > 0]
                enemy_move = random.choice(usable) if usable else None #sinnoh ahh ai
            turn = sorted(
                [(player, "move", player_move), (enemy, "move",enemy_move)],
                key=lambda x: x[0].spd,
                reverse=True
            )
        if turn is None:
            continue
        for user, action_type, action in turn:

            target = enemy if user == player else player

            if action_type == "move":
                move = action

                if move is None or move.pp <= 0:
                    continue

                move.pp -= 1
                pplist[move.order] = move.pp

                redraw_battle(stdscr, player, enemy)

                if random.randint(1, 100) > move.acc and move.acc != -1:
                    textbox(stdscr, f"{user.base.name.capitalize()} used {move.name}!")
                    textbox(stdscr, "But it missed!")
                    continue

                textbox(stdscr, f"{user.base.name.capitalize()} used {move.name}!")

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
                            f"{user.base.name.capitalize()}'s {STAT_DISPLAY[stat]} rose!"
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
                            f"{target.base.name.capitalize()}'s {STAT_DISPLAY[stat]} fell!"
                        )
                dmg = damage_calc(user, target, move, stdscr, player=player, enemy=enemy)

                redraw_battle(stdscr, player, enemy)

                if dmg > 0:
                    mult = type_multiplier(move.type, target)
                    if mult > 1:
                        textbox(stdscr, "It's super effective!")
                    elif mult < 1:
                        textbox(stdscr, "It's not very effective...")
                    if target.hp <= 0:
                        redraw_battle(stdscr, player, enemy)
                        textbox(stdscr, f"{target.base.name.capitalize()} fainted!")
                        player_result = player.result()
                        enemy_result = enemy.result()
                        overworld.hpstorage = [player_result[2],enemy_result[2]]
                        if target == enemy:
                            return "win"
                        else:
                            return "lose"
                        
            elif action_type == "item":
                item_name, item_value = action

                textbox(stdscr, f"{user.base.name.capitalize()}'s Trainer used {item_name}!")

                if item_name == "potion":
                    heal = 20
                    user.hp = min(user.max_hp, user.hp + heal)
                    textbox(stdscr, f"{user.base.name.capitalize()} healed {heal} HP!")

                elif item_name == "fullheal":
                    user.status = None
                    textbox(stdscr, "All status(es) were cleared!")

                elif item_name == "pokeball":
                    if target == enemy:  
                        catch_chance = random.randint(1, 100)

                        if catch_chance > 60:
                            textbox(stdscr, "Gotcha! The Pokémon was caught!")
                            return "caught"
                        else:
                            textbox(stdscr, "Oh no! The Pokémon broke free!")
                    else:
                        textbox(stdscr, "You can't catch a trainers Pokémon!!")

            status_effect_manager(stdscr, player)
            status_effect_manager(stdscr, enemy)