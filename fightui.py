import curses
import random
import stats

# -------------------- Data --------------------
mons = [getattr(stats, f"mon{i}") for i in range(1, 152) if hasattr(stats, f"mon{i}")]
moves_list = [stats.move1, stats.move2, stats.move3, stats.move4]

# -------------------- Utility --------------------
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
        curses.napms(20)
    while True:
        if stdscr.getch() == ord("z"):
            break

# -------------------- Classes --------------------
class BattleMove:
    def __init__(self, move):
        self.name = move[0].strip('"').capitalize()
        self.type = move[1]
        self.pp_max = move[2]
        self.pp = move[2]
        self.power = move[3]
        self.acc = move[4]
        self.desc = move[-1]

class BattleMon:
    def __init__(self, base, level, moves):
        self.base = base
        self.level = level
        self.status = "OK"
        self.max_hp = int(((2*base.hp*level)/100) + level + 10)
        self.hp = self.max_hp
        self.at = int(((2*base.at*level)/100) + 5)
        self.de = int(((2*base.de*level)/100) + 5)
        self.spd = int(((2*base.spd*level)/100) + 5)
        self.moves = [BattleMove(m) for m in moves]

    def name(self):
        return self.base.call().capitalize()

def damage_calc(attacker, defender, move):
    if move.power <= 0: return 0
    base = (((2*attacker.level)/5 + 2) * move.power * attacker.at / defender.de)/50 + 2
    modifier = random.uniform(0.85, 1.0)
    return int(base * modifier)

# -------------------- Selection --------------------
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
    idx = select_from_list(stdscr, pool, f"{label} Pokémon", show_type=True)
    mon = pool.pop(idx)
    chosen = []
    for i in range(4):
        m = select_from_list(stdscr, moves_list, f"{mon.call().capitalize()} Move {i+1}", show_desc=True)
        chosen.append(moves_list[m])
    return mon, chosen

# -------------------- Drawing --------------------
def draw_header(stdscr, player, enemy):
    h, w = stdscr.getmaxyx()
    left = f"{player.name()} [{player.status}] HP {player.hp}/{player.max_hp}"
    right = f"{enemy.name()} [{enemy.status}] HP {enemy.hp}/{enemy.max_hp}"
    safe_addstr(stdscr, 0, 0, (left + " ------ " + right)[:w])
    draw_divider(stdscr, 1)

def draw_moves(stdscr, mon, highlight=-1):
    for j in range(2):
        for i in range(2):
            idx = j*2 + i
            if idx>=len(mon.moves): continue
            move = mon.moves[idx]
            sel = idx==highlight
            safe_addstr(stdscr, 2+j, i*20, f">[{move.name}]<" if sel else f"[{move.name}]")
            safe_addstr(stdscr, 3+j, i*20, f"PP {move.pp}/{move.pp_max}")
    draw_divider(stdscr, 4)

def draw_main_menu(stdscr, menu_pos):
    menu = ["Fight","Bag","Pokémon","Run"]
    y = 2  # menu right below the divider
    for i, item in enumerate(menu):
        if i == menu_pos:
            text = f">[{item}]<"
        else:
            text = f"[{item}]"
        x = (i%2)*25
        safe_addstr(stdscr, y, x, text)
        if i==1: safe_addstr(stdscr, y+1, 0, "")  # just spacing for alignment

# -------------------- Move selection --------------------
def move_menu(stdscr, user):
    highlight = 0
    while True:
        stdscr.clear()
        draw_header(stdscr, user, user)
        draw_moves(stdscr, user, highlight)
        key = stdscr.getch()
        if key == curses.KEY_UP and highlight>1: highlight-=2
        elif key == curses.KEY_DOWN and highlight<2: highlight+=2
        elif key == curses.KEY_LEFT and highlight%2==1: highlight-=1
        elif key == curses.KEY_RIGHT and highlight%2==0 and highlight+1<len(user.moves): highlight+=1
        elif key == ord("x"): return None  # go back to main menu
        elif key == ord("z"):
            move = user.moves[highlight]
            if move.pp>0: return move

# -------------------- Battle Loop --------------------
def afightui(stdscr, player, enemy):
    curses.curs_set(0)
    stdscr.keypad(True)
    menu_pos = 0
    while True:
        stdscr.clear()
        draw_header(stdscr, player, enemy)
        draw_main_menu(stdscr, menu_pos)
        key = stdscr.getch()
        if key==curses.KEY_UP and menu_pos>1: menu_pos-=2
        elif key==curses.KEY_DOWN and menu_pos<2: menu_pos+=2
        elif key==curses.KEY_LEFT and menu_pos%2==1: menu_pos-=1
        elif key==curses.KEY_RIGHT and menu_pos%2==0 and menu_pos+1<4: menu_pos+=1
        elif key==ord("z"):
            if menu_pos==0:  # Fight
                player_move = move_menu(stdscr, player)
                if player_move is None:  # X pressed, cancel
                    continue
                usable = [m for m in enemy.moves if m.pp>0]
                enemy_move = random.choice(usable) if usable else None
                turn = sorted([(player, player_move),(enemy, enemy_move)], key=lambda x:x[0].spd, reverse=True)
                for user, move in turn:
                    if move is None or move.pp<=0: continue
                    target = enemy if user==player else player
                    move.pp-=1
                    dmg=damage_calc(user, target, move)
                    target.hp = max(0, target.hp - dmg)
                    textbox(stdscr, f"{user.name()} used {move.name}! It dealt {dmg} damage.")
                    if target.hp<=0:
                        textbox(stdscr, f"{target.name()} fainted!")
                        return "win" if target==enemy else "lose"
            else:
                textbox(stdscr, f"{['Bag','Pokémon','Run'][menu_pos-1]} is WIP")

# -------------------- Setup --------------------
def battle_setup(stdscr):
    pool = mons.copy()
    p_mon, p_moves = select_pokemon_and_moves(stdscr, pool, "Player")
    e_mon, e_moves = select_pokemon_and_moves(stdscr, pool, "Enemy")
    player = BattleMon(p_mon, 50, p_moves)
    enemy = BattleMon(e_mon, 50, e_moves)
    return afightui(stdscr, player, enemy)
