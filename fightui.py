import curses
import random
import textwrap
import stats
import overworld
player_result = []
enemy_result = []
EASY_OFFSET=15

# Move type to color pair mapping
MOVE_TYPE_COLORS = {
    "normal": 1,      # WHITE
    "fire": 7,        # RED
    "water": 6,       # BLUE
    "electric": 2,    # YELLOW
    "grass": 4,       # GREEN
    "ice": 3,         # CYAN
    "fighting": 19,   # BROWN
    "poison": 5,      # MAGENTA
    "ground": 19,     # BROWN
    "flying": 3,      # CYAN
    "psychic": 5,     # MAGENTA
    "bug": 4,         # GREEN
    "rock": 19,       # BROWN
    "ghost": 5,       # MAGENTA
    "dragon": 6,      # BLUE
    "dark": 1,        # WHITE
    "steel": 3,       # CYAN
    "fairy": 5,       # MAGENTA
    "sleep": 1,       # WHITE
}

def get_move_color(move_type):
    """Get the color pair for a move based on its type."""
    return MOVE_TYPE_COLORS.get(move_type.lower(), 1)  # Default to WHITE

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

def draw_party(stdscr, party, active_idx, highlight, forced=False):
    row_start = 1
    col = 42

    for i, mon in enumerate(party):
        tags = []

        if i == active_idx:
            tags.append("ACTIVE")
        if mon.hp <= 0:
            tags.append("FNT")

        status_text = " ".join(tags)
        shiny_marker = "✦ " if getattr(mon, "shiny", False) else ""
        text = f"[ {i+1}. {shiny_marker}{mon.base.name.capitalize()} HP {mon.hp}/{mon.max_hp} {status_text} ]"

        if i == highlight:
            stdscr.attron(curses.color_pair(1))
            safe_addstr(stdscr, row_start + i, col, text[:34])
            stdscr.attroff(curses.color_pair(1))
        else:
            safe_addstr(stdscr, row_start + i, col, text[:34])


def apply_status(status_list, new_status, clears=None):
    if new_status in status_list:
        return
    if clears:
        for s in clears:
            if s in status_list:
                status_list.remove(s)
    status_list.append(new_status)

def party_menu(stdscr, party, active_idx, enemy):
    highlight = active_idx

    while True:
        player = party[active_idx]

        player_sprite = getattr(stats, player.base.name.lower(), stats.placeholder)
        enemy_sprite = getattr(stats, enemy.base.name.lower(), stats.placeholder)

        stdscr.clear()
        draw_top_banner(stdscr)
        draw_main_menu(stdscr, 1, player, enemy)
        enemy_sprite.draw(stdscr, "back", "shiny" if enemy.shiny else "normal")
        player_sprite.draw(stdscr, "front", "shiny" if player.shiny else "normal")
        draw_party(stdscr, party, active_idx, highlight, forced=False)
        draw_header(stdscr, player, enemy)
        stdscr.refresh()

        key = stdscr.getch()

        if key == curses.KEY_UP and highlight > 0:
            highlight -= 1
        elif key == curses.KEY_DOWN and highlight < len(party) - 1:
            highlight += 1
        elif key == ord("x"):
            return None
        elif key == ord("z"):
            if highlight == active_idx:
                textbox(stdscr, "That Pokémon is already out!")
                continue
            if party[highlight].hp <= 0:
                textbox(stdscr, "That Pokémon has fainted!")
                continue
            return highlight

def forced_party_menu(stdscr, party, active_idx, enemy):
    alive = [i for i, mon in enumerate(party) if mon.hp > 0]

    if not alive:
        return None

    highlight = alive[0]

    while True:
        player = party[active_idx] if party[active_idx].hp > 0 else party[highlight]

        player_sprite = getattr(stats, player.base.name.lower(), stats.placeholder)
        enemy_sprite = getattr(stats, enemy.base.name.lower(), stats.placeholder)

        stdscr.clear()
        draw_top_banner(stdscr)
        draw_main_menu(stdscr, 1, player, enemy)
        enemy_sprite.draw(stdscr, "back", "shiny" if enemy.shiny else "normal")
        player_sprite.draw(stdscr, "front", "shiny" if player.shiny else "normal")
        draw_party(stdscr, party, active_idx, highlight, forced=True)
        draw_header(stdscr, player, enemy)
        stdscr.refresh()

        key = stdscr.getch()

        if key == curses.KEY_UP:
            pos = alive.index(highlight)
            if pos > 0:
                highlight = alive[pos - 1]

        elif key == curses.KEY_DOWN:
            pos = alive.index(highlight)
            if pos < len(alive) - 1:
                highlight = alive[pos + 1]

        elif key == ord("z"):
            return highlight

def draw_top_banner(stdscr):
    h, w = stdscr.getmaxyx()
    safe_addstr(stdscr, 0, 0, "#" + "#"*(w-2) + "#", 0)

def sdraw_top_banner(stdscr):
    h, w = stdscr.getmaxyx()
    safe_addstr(stdscr, 0, 0, "#" + "#"*(w-2) + "#", 0)
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



def battle_setup(stdscr, randomizer_mode="normal"):
    return debug_battle_setup(stdscr, randomizer_mode)

def debug_battle_setup(stdscr, randomizer_mode="normal"):
    pool = mons.copy()
    
    mode = choose_mode(stdscr)
    if randomizer_mode == "normal":
        player_team_data, enemy_team_data = select_debug_teams(
            stdscr,
            pool,
            pool.copy(),
            moves_list,
            mode
        )
    else:
        player_team_data, enemy_team_data = random_debug_teams(randomizer_mode)
    
    curses.start_color()
    
    # Create player party
    player_party = []
    for mon_data in player_team_data:
        mon = BattleMon(
            mon_data['mon'],
            mon_data['level'],
            mon_data['moves'],
            shiny=mon_data['shiny'],
            ability=mon_data.get("ability"),
            held_item=mon_data.get("held_item"),
        )
        player_party.append(mon)
    
    if not player_party:
        textbox(stdscr, "No pokemon selected!")
        return

    # Ensure enemy team also has ability/held_item passed through
    return debug_enemy_party_battle(stdscr, player_party, enemy_team_data, mode)


def first_alive_party_index(party):
    for i, mon in enumerate(party):
        if mon.hp > 0:
            return i
    return None


def debug_enemy_party_battle(stdscr, player_party, enemy_team_data, mode):
    for i, enemy_data in enumerate(enemy_team_data):
        active_idx = first_alive_party_index(player_party)
        if active_idx is None:
            return "lose"

        enemy = BattleMon(
            enemy_data['mon'],
            enemy_data['level'],
            enemy_data['moves'],
            shiny=enemy_data['shiny'],
            ability=enemy_data.get("ability"),
            held_item=enemy_data.get("held_item"),
        )

        if i > 0:
            textbox(stdscr, f"Enemy sent out {enemy.base.name.capitalize()}!")

        result = afightui(stdscr, player_party, enemy, mode, active_idx=active_idx)
        if result != "win":
            return result

    return "win"


def random_debug_mon(level):
    mon = random.choice(mons)
    abilities = getattr(mon, "abilities", []) if hasattr(mon, "abilities") else []
    held_items = getattr(mon, "held_items", []) if hasattr(mon, "held_items") else []
    # held_items in pokedata is an array of {item, chance}; but mon.held_items in stats loads it as is.
    # pick first held item if present for determinism in debug.
    held_item = None
    if isinstance(held_items, list) and held_items:
        first = held_items[0]
        if isinstance(first, dict) and "item" in first:
            held_item = first.get("item")
    return {
        'mon': mon,
        'level': level() if callable(level) else level,
        'moves': [random.choice(moves_list) for _ in range(4)],
        'shiny': random.randint(1, 4096) == 1,
        'ability': abilities[0] if abilities else None,
        'held_item': held_item,
    }


def random_debug_teams(randomizer_mode):
    level = 50 if randomizer_mode == "random" else lambda: random.randint(1, 100)
    return (
        [random_debug_mon(level) for _ in range(6)],
        [random_debug_mon(level) for _ in range(6)]
    )

def select_debug_teams(stdscr, player_pool, cpu_pool, moves_list, mode):
    
    # Initialize team data structures
    player_team = [{'mon': None, 'level': 50, 'moves': [None]*4, 'shiny': False, 'ability': None, 'held_item': None} for _ in range(6)]
    enemy_team = [{'mon': None, 'level': 50, 'moves': [None]*4, 'shiny': False, 'ability': None, 'held_item': None} for _ in range(6)]
    
    col = 0  # 0 for player, 1 for enemy
    team_idx = 0  # which pokemon in the team (0-5)
    row = 0  # which row: 0=pokemon, 1=level, 2=moves, 3=shiny, 4=ok
    
    move_menu = False
    move_cursor = 0
    move_view = 0
    move_slot = 0  # which move slot (0-3)
    move_slot_menu = False  # are we selecting which move slot to edit?
    
    while True:
        stdscr.clear()
        
        # Draw header
        safe_addstr(stdscr, 0, 5, "DEBUG BATTLE SETUP", 0)
        safe_addstr(stdscr, 1, 5, "← Player Team", 0)
        safe_addstr(stdscr, 1, 35, "Enemy Team →", 0)
        safe_addstr(stdscr, 2, 5, "[Arrow Keys] Navigate | [Z] Select | [C] Confirm | [X] Back", 0)
        
        if move_menu:
            current_team = player_team if col == 0 else enemy_team
            current_mon = current_team[team_idx]['mon']
            shiny_mark = "✦ " if current_team[team_idx]['shiny'] else ""
            current_mon_name = f"{shiny_mark}{current_mon.call().capitalize()}" if current_mon else "Pokemon"

            # Fullscreen overwrite background
            h, w = stdscr.getmaxyx()
            for clear_y in range(h):
                safe_addstr(stdscr, clear_y, 0, " " * (w - 1), 0)

            safe_addstr(stdscr, 0, 0, f"Select Move {move_slot+1}/4", 0)
            safe_addstr(stdscr, 1, 0, f"for {current_mon_name[:24]}", 0)
            safe_addstr(stdscr, 2, 0, "[Arrow Keys] Navigate | [Z] Select | [X] Back", 0)

            visible_moves = moves_list[move_view:move_view+20]

            if move_view > 0:
                safe_addstr(stdscr, 3, 0, "▲", 0)

            for i, m in enumerate(visible_moves):
                idx = move_view + i
                name = m.call().capitalize()
                prefix = "> " if idx == move_cursor else "  "
                safe_addstr(stdscr, 4 + i, 0, prefix + name[:40], 0)

            if move_view + 20 < len(moves_list):
                safe_addstr(stdscr, 24, 0, "▼", 0)

            # Updated moves display at top right
            safe_addstr(stdscr, 0, 50, "Current Moves:", 0)
            mon_data = current_team[team_idx]
            for i in range(4):
                move_name = mon_data['moves'][i].call().capitalize() if mon_data['moves'][i] else "[Empty]"
                prefix = "> " if move_slot == i else "  "
                if mon_data['moves'][i]:
                    move_color = get_move_color(mon_data['moves'][i].type)
                    stdscr.attron(curses.color_pair(move_color))
                    safe_addstr(stdscr, 1 + i, 50, f"{prefix}{i+1}. {move_name[:24]}")
                    stdscr.attroff(curses.color_pair(move_color))
                else:
                    safe_addstr(stdscr, 1 + i, 50, f"{prefix}{i+1}. {move_name[:24]}", 0)
        else:
            draw_debug_team_side(stdscr, 3, player_team, col == 0, team_idx, row)
            draw_debug_team_side(stdscr, 3, enemy_team, col == 1, team_idx, row, x_offset=35)
            
            if row == 2:
                current_team = player_team if col == 0 else enemy_team
                mon_data = current_team[team_idx]
                safe_addstr(stdscr, 10, 5, "Moves for selected Pokemon:", 0)
                for i in range(4):
                    move_name = mon_data['moves'][i].call().capitalize() if mon_data['moves'][i] else "[Empty]"
                    prefix = "> " if move_slot == i else "  "
                    if mon_data['moves'][i]:
                        move_color = get_move_color(mon_data['moves'][i].type)
                        stdscr.attron(curses.color_pair(move_color))
                        safe_addstr(stdscr, 11 + i, 5, f"{prefix}{i+1}. {move_name[:20]}")
                        stdscr.attroff(curses.color_pair(move_color))
                    else:
                        safe_addstr(stdscr, 11 + i, 5, f"{prefix}{i+1}. {move_name[:20]}", 0)
        
        stdscr.refresh()
        key = stdscr.getch()
        
        if move_menu:
            # Handle move selection
            if key == curses.KEY_UP and move_cursor > 0:
                move_cursor -= 1
            elif key == curses.KEY_DOWN and move_cursor < len(moves_list) - 1:
                move_cursor += 1
            elif key == curses.KEY_LEFT and move_slot > 0:
                move_slot -= 1
            elif key == curses.KEY_RIGHT and move_slot < 3:
                move_slot += 1

            if move_cursor < move_view:
                move_view = move_cursor
            elif move_cursor >= move_view + 20:
                move_view = move_cursor - 19

            elif key == ord("z"):
                current_team = player_team if col == 0 else enemy_team
                current_team[team_idx]['moves'][move_slot] = moves_list[move_cursor]
                move_menu = False
            elif key == ord("x"):
                move_menu = False
            continue
        
        
        if key == curses.KEY_LEFT and row > 0:
            row -= 1
            move_slot = 0  
        elif key == curses.KEY_RIGHT and row < 3:
            row += 1
            move_slot = 0  
        elif key == curses.KEY_UP:
            if row == 2:  
                if move_slot > 0:
                    move_slot -= 1
            else:
                if team_idx > 0:  
                    team_idx -= 1
                else:  
                    col = 0
        elif key == curses.KEY_DOWN:
            if row == 2:  
                if move_slot < 3:
                    move_slot += 1
            else:
                if team_idx < 5:  
                    team_idx += 1
                else: 
                    col = 1
                    team_idx = 0
        
        elif key == ord("z"):
            current_team = player_team if col == 0 else cpu_pool if col == 1 else player_team
            current_team = player_team if col == 0 else enemy_team
            
            if row == 0:  
                pool = player_pool if col == 0 else cpu_pool
                i = select_from_list_scroll(stdscr, pool, f"Select Pokemon for slot {team_idx+1}", show_type=True)
                if i is not None:
                    chosen = pool.pop(i)
                    current_team[team_idx]['mon'] = chosen
                    
                    abilities = getattr(chosen, "abilities", []) if hasattr(chosen, "abilities") else []
                    held_items = getattr(chosen, "held_items", []) if hasattr(chosen, "held_items") else []
                    held_item = None
                    if isinstance(held_items, list) and held_items:
                        first = held_items[0]
                        if isinstance(first, dict) and "item" in first:
                            held_item = first.get("item")
                    current_team[team_idx]['ability'] = abilities[0] if abilities else None
                    current_team[team_idx]['held_item'] = held_item
            
            elif row == 1:  
                level = select_level(stdscr, current_team[team_idx]['level'])
                if level is not None:
                    current_team[team_idx]['level'] = level
            
            elif row == 2:  
                if current_team[team_idx]['mon'] is None:
                    textbox(stdscr, "Please select a Pokemon first!")
                else:
                    move_menu = True
                    move_cursor = 0
                    move_view = 0
            
            elif row == 3:  # Toggle shiny
                current_team[team_idx]['shiny'] = not current_team[team_idx]['shiny']
        
        elif key == ord("c"):  
            valid_player = [t for t in player_team if t['mon'] is not None]
            valid_enemy = [t for t in enemy_team if t['mon'] is not None]
            
            if valid_player and valid_enemy:
                return valid_player, valid_enemy
            else:
                textbox(stdscr, "Both teams need at least one pokemon!")

def select_level(stdscr, current_level):
    level = current_level
    
    while True:
        stdscr.clear()
        safe_addstr(stdscr, 0, 5, f"Select Level (Current: {level})", 0)
        safe_addstr(stdscr, 2, 5, "↑/↓ to adjust, [Z] to confirm, [X] to cancel", 0)
        
        level_display = f"Level: {level}"
        stdscr.attron(curses.color_pair(1))
        safe_addstr(stdscr, 5, 5, level_display, 0)
        stdscr.attroff(curses.color_pair(1))
        
        stdscr.refresh()
        key = stdscr.getch()
        
        if key == curses.KEY_UP and level < 100:
            level += 1
        elif key == curses.KEY_DOWN and level > 1:
            level -= 1
        elif key == ord("z"):
            return level
        elif key == ord("x"):
            return None

def draw_debug_team_side(stdscr, start_y, team, is_selected, team_idx, row, x_offset=5):
    """Draw a team selection side (player or enemy)"""
    
    for i in range(6):
        y = start_y + i
        mon_data = team[i]
        
        highlight = is_selected and team_idx == i
        
        if row == 0 and highlight:
            stdscr.attron(curses.color_pair(1))
      
        if mon_data['mon']:
            shiny_mark = "✦ " if mon_data['shiny'] else ""
            mon_name = f"{shiny_mark}{mon_data['mon'].call().capitalize()}"
        else:
            mon_name = "[Empty]"
        
        safe_addstr(stdscr, y, x_offset, f"{i+1}. {mon_name[:15]:<15}", 0)
        
        if row == 0 and highlight:
            stdscr.attroff(curses.color_pair(1))
        
        if row == 1 and highlight:
            stdscr.attron(curses.color_pair(1))
        safe_addstr(stdscr, y, x_offset + 18, f"L{mon_data['level']:<2}", 0)
        if row == 1 and highlight:
            stdscr.attroff(curses.color_pair(1))
            
        shiny_mark = "✦" if mon_data['shiny'] else " "
        if row == 3 and highlight:
            stdscr.attron(curses.color_pair(1))
        safe_addstr(stdscr, y, x_offset + 24, shiny_mark, 0)
        if row == 3 and highlight:
            stdscr.attroff(curses.color_pair(1))

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
        dmg = mon.max_hp // 16 #57 
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

        visible_items = items[view:view+22]

        if view > 0:
            safe_addstr(stdscr,1,5,"▲",0)

        for i,item in enumerate(visible_items):
            idx = view + i
            name = item.call().capitalize()
            prefix = "> " if idx == cursor else "  "
            safe_addstr(stdscr,2+i,5,prefix+name,0)

        if view+10 < len(items):
            safe_addstr(stdscr,23,5,"▼",0)

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
        elif cursor >= view + 20:
            view = cursor - 19

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


def safe_addstr_raw(stdscr, y, x, text, attr=0):
    try:
        h, w = stdscr.getmaxyx()
        if y < h and x < w:
            stdscr.addstr(y, x, str(text)[:w - x], attr)
    except curses.error:
        pass


def draw_divider(stdscr, y):
    h, w = stdscr.getmaxyx()

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

def item_name(item_id):
    if item_id is None:
        return "None"
    items = getattr(stats, "ITEMS", {}) if hasattr(stats, "ITEMS") else {}
    item = items.get(item_id)
    if isinstance(item, dict) and item.get("name"):
        return item["name"]
    return str(item_id)

def mons_effect_box(stdscr, mon, kind, message, specific_name=None):
    h, w = stdscr.getmaxyx()
    top = max(0, h - 12)  

    mon_name = mon.base.name.capitalize()
    header_label = specific_name if specific_name is not None else kind
    title = f"{mon_name}'s {header_label}"
    title = title[: w - 4] if w > 4 else title

    safe_addstr(stdscr, top + 0, 0, "╔" + "═" * (w - 2) + "╗ ", 0)
    safe_addstr(stdscr, top + 1, 0, "║" + " " * (w - 2) + "║", 0)
    safe_addstr(stdscr, top + 2, 0, "╚" + "═" * (w - 2) + "╝", 0)

    safe_addstr(stdscr, top + 1, 2, title, 0)
    stdscr.refresh()
    textbox(stdscr, message)

def ability_trigger_message(mon):
    ability_id = getattr(mon, "ability", None)
    if ability_id == "mold_breaker":
        return "breaks the mold!"
    return None

def item_trigger_message(mon):
    item_id = getattr(mon, "held_item", None)
    if item_id == "leftovers":
        return "Recovered some HP with its LEFTOVERS!"
    return None

def apply_leftovers(stdscr, mon):
    leftovers_id = getattr(mon, "held_item", None)
    if leftovers_id != "leftovers":
        return False

    #heals 1/16 of max hp each turn, but does during enemy + player (buff)
    heal = max(1, mon.max_hp // 16)
    if mon.hp <= 0:
        return False

    if mon.hp >= mon.max_hp:
        return False

    mon.hp = min(mon.max_hp, mon.hp + heal)
    mons_effect_box(
        stdscr,
        mon,
        "Item",
        "recovers some hp with its leftovers!",
        specific_name=item_name(getattr(mon, "held_item", None))
    )
    return True

def draw_pokeball_overlay(stdscr, start_y=2, start_x=49, shift=0, color=None):
    art = [
"          █████████         ",
"       █████#####█████      ",
"     ███#############███    ",
"     ███####█████####███    ",
"     ████████   ████████    ",
"     ███    █████    ███    ",
"      ███           ███     ",
"        █████   █████       ",
"          █████████         ",
"                            ",
"                            ",
    ]
    if color is None:
        color = curses.color_pair(7)

    for i, line in enumerate(art):
        try:
            stdscr.addstr(start_y + i, start_x + shift, line, color)
        except curses.error:
            pass


def animate_pokeball(stdscr, player, enemy, shakes=3, success=True):
    start_y, start_x = 2, 49
    shifts = [0, 2]
    color = curses.color_pair(7)

    for index in range(shakes):
        for shift in shifts:
            redraw_battle(stdscr, player, enemy)
            draw_pokeball_overlay(stdscr, start_y, start_x, shift, color)
            stdscr.refresh()
            curses.napms(120)

        if index < shakes - 1:
            curses.napms(2000)

    if success:
        redraw_battle(stdscr, player, enemy)
        draw_pokeball_overlay(stdscr, start_y, start_x, shifts[-1], color)
        stdscr.refresh()
        curses.napms(180)
    else:
        redraw_battle(stdscr, player, enemy)
        draw_pokeball_overlay(stdscr, start_y, start_x, shifts[-1], color)
        try:
            stdscr.addstr(start_y + 4, start_x + 10, "x", curses.color_pair(7))
        except curses.error:
            pass
        stdscr.refresh()
        curses.napms(180)
        redraw_battle(stdscr, player, enemy)


def flash_mon(stdscr, player, enemy, is_enemy=False, flashes=4):
    mon = enemy if is_enemy else player
    sprite = getattr(stats, mon.base.name.lower(), stats.placeholder)
    sprite_type = "back" if is_enemy else "front"
    
    for _ in range(flashes):
        redraw_battle(stdscr, player, enemy)
        stdscr.refresh()
        curses.napms(100)
        
        # Draw blank space over the sprite
        if is_enemy:
            for y in range(11):
                safe_addstr(stdscr, 2 + y, 53, " " * 25, 0)
        else:
            for y in range(11):
                safe_addstr(stdscr, 2 + y, 2, " " * 25, 0)
        stdscr.refresh()
        curses.napms(100)

def shiny_animation(stdscr, player, enemy, is_enemy=False, flashes=6):
    """Animate a shiny pokemon appearing with flashing effect"""
    mon = enemy if is_enemy else player
    sprite = getattr(stats, mon.base.name.lower(), stats.placeholder)
    sprite_type = "back" if is_enemy else "front"

    for i in range(flashes):
        variant = "shiny" if i % 2 == 0 else "normal"
        redraw_battle(stdscr, player, enemy)
        sprite.draw(stdscr, sprite_type, variant)
        stdscr.refresh()
        curses.napms(150)

        
def redraw_battle(stdscr, player, enemy, menu_pos=0):
    stdscr.clear()
    draw_top_banner(stdscr)
    draw_main_menu(stdscr, menu_pos, player, enemy)
    player_sprite = getattr(stats, player.base.name.lower(), stats.placeholder)
    enemy_sprite = getattr(stats, enemy.base.name.lower(), stats.placeholder)
    enemy_sprite.draw(stdscr, "back", "shiny" if enemy.shiny else "normal")
    player_sprite.draw(stdscr, "front", "shiny" if player.shiny else "normal")
    draw_header(stdscr, player, enemy)

    # Ability boxes under each sprite
    # Battle layout uses 80x24; sprites render around y=2..12 and x=2 / 53.
    # We'll show ability starting at y=14 with small labels.
    p_ability = ability_name(getattr(player, "ability", None))
    e_ability = ability_name(getattr(enemy, "ability", None))

    safe_addstr(stdscr, 14, 2, f"Ability: {p_ability}"[:38])
    safe_addstr(stdscr, 14, 42, f"Ability: {e_ability}"[:38])

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
    def __init__(self, base, level, moves, hp=-1, shiny=False, ability=None, held_item=None):
        self.base = base
        self.level = level
        self.shiny = shiny
        self.ability = ability
        self.held_item = held_item
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
        self.moves = [
            BattleMove(move_instance, order=i)
            for i, move_instance in enumerate(moves)
            if move_instance is not None
        ]

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

    if dmg > 0 and player and enemy:
        is_enemy_taking_damage = defender == enemy
        flash_mon(stdscr, player, enemy, is_enemy=is_enemy_taking_damage, flashes=3)

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
    options = ["Player vs Player", "Player vs Bot","Online, if i ever learn to use api(s)..."]
    cursor = 0

    while True:
        stdscr.clear()
        safe_addstr(stdscr, 0, 0, "CHOOSE MODE", 0)

        for i, opt in enumerate(options):
            prefix = "> " if i == cursor else "  "
            safe_addstr(stdscr, 2+i, 0, prefix + opt, 0)

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
                mname = "#"
                move_color = 1
                if moves[i]:
                    mname = moves[i].call().capitalize()[:20]
                    move_color = get_move_color(moves[i].type)
                prefix = "> " if selected and row == i + 1 and not move_menu else "  "
                if moves[i]:
                    stdscr.attron(curses.color_pair(move_color))
                    safe_addstr(stdscr, y, x, prefix + mname)
                    stdscr.attroff(curses.color_pair(move_color))
                else:
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
    p_name = player.base.name.capitalize()
    e_name = enemy.base.name.capitalize()
    p_shiny = "✦ " if getattr(player, "shiny", False) else ""
    e_shiny = "✦ " if getattr(enemy, "shiny", False) else ""
    left = f"{p_shiny}{p_name} LVL{player.level} EFF{player.statuses} HP {player.hp}/{player.max_hp}"
    right = f"{e_shiny}{e_name} LVL{enemy.level} EFF{enemy.statuses} HP {enemy.hp}/{enemy.max_hp}"
    line = f"# {left:^35} ------ {right:^35} #"
    safe_addstr(stdscr, 0, 0, line, 14)
    draw_divider(stdscr, 1)

def ability_name(ability_id):
    if ability_id is None:
        return "None"
    # ability_id stored in mons is an id string like "blaze"
    ability = getattr(stats, "ABILITIES", {}).get(ability_id, None) if hasattr(stats, "ABILITIES") else None
    if isinstance(ability, dict) and ability.get("name"):
        return ability["name"]
    return str(ability_id)

blocks = "▏▎▍▌▋▊▉█"
def make_hp_bar(current, max_hp, length=10):
    if max_hp <= 0:
        return "░" * length, 15

    ratio = max(0, min(1, current / max_hp))

    # color logic
    if ratio > 0.5:
        color = 13
    elif ratio > 0.2:
        color = 14
    else:
        color = 15

    total_blocks = ratio * length
    full_blocks = int(total_blocks)
    remainder = total_blocks - full_blocks

    bar = "█" * full_blocks
    if full_blocks < length and remainder > 0:
        partial_index = max(0, min(int(remainder * len(blocks)), len(blocks) - 1))
        bar += blocks[partial_index]

    bar = bar.ljust(length, "░")

    return bar, color

def draw_main_menu(stdscr, menu_pos, player=None, enemy=None,show_moves=False):
    h, w = stdscr.getmaxyx()
    rows = list(range(1, 13)) + [14] 
    for y in rows:
        safe_addstr(stdscr, y, 0, "#" + " " * (w - 2) + "#", 0)
    safe_addstr(stdscr, 13, 0, "#" + "#" * (w - 2) + "#",0)
    line = f"#"+  " "*39 + "#" + "#" * 38 + "#"
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
    safe_addstr(stdscr, 16, 0,"#" + "#" * 39 + "#" + " " * 38 + "#",0)
    safe_addstr(stdscr, 17, 0, "#" + " " * 38 + " #" + " " * 38 + "#",0)
    safe_addstr(stdscr, 18, 0, "#" + " " * 38 + " #" + " " * 38 + "#",0)
    safe_addstr(stdscr, 19, 0,"#" + "#" * 39 + "#" +  " " * 38 + "#",0)
    safe_addstr(stdscr, 20, 0,"#",0)
    safe_addstr(stdscr, 20, 40,"#" + "#" * 38 + "#",0)
    safe_addstr(stdscr, 21, 0, "#" + "#" * (w - 2) + "#",0)
    draw_top_banner(stdscr)
    menu = ["-----Fight-----|","----Pokémon----|","------Bag------|","------Run------|","#","#","#","#"]
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
            move_color = get_move_color(move.type)
            stdscr.attron(curses.color_pair(move_color))
            safe_addstr(stdscr, move_row_start + idx, move_col, text)
            stdscr.attroff(curses.color_pair(move_color))
            
def draw_moves(stdscr, mon, highlight=-1, col=None, row_start=None):
    if col is None: col = 42
    if row_start is None: row_start = 1
    for idx, move in enumerate(mon.moves):
        text = f"[{f'{move.name} PP{move.pp}/{move.pp_max}':^20}]"
        move_color = get_move_color(move.type)
        if idx == highlight:
            stdscr.attron(curses.color_pair(1))
            safe_addstr(stdscr, row_start + idx, col, text)
            stdscr.attroff(curses.color_pair(1))
        else:
            stdscr.attron(curses.color_pair(move_color))
            safe_addstr(stdscr, row_start + idx, col, text)
            stdscr.attroff(curses.color_pair(move_color))


def show_move_info(stdscr, move, attacker, defender):
    def effectiveness_text(mult):
        if mult == 0:
            return "0x (Not Effective)"
        if mult == 0.5:
            return "0.5x (Not Very Effective)"
        if mult == 1:
            return "1x (Effective)"
        if mult == 2:
            return "2x (Super Effective!)"
        return f"{mult:.1f}x"

    est_damage = None
    if move.power > 0 and move.category in ("physical", "special"):
        if move.category == "physical":
            atk = apply_stage(attacker.at, attacker.stage_at)
            defense = apply_stage(defender.de, defender.stage_de)
        else:
            atk = apply_stage(attacker.spa, attacker.stage_spa)
            defense = apply_stage(defender.spd_def, defender.stage_spd_def)

        base = (((2 * attacker.level) / 5 + 2) * move.power * atk / defense) / 50 + 2
        est = base * type_multiplier(move.type, defender) * 0.925
        est_damage = max(0, int(est))

    def effectiveness_attr(mult):
        if mult == 0:
            return curses.color_pair(5)
        if mult == 0.5:
            return curses.color_pair(7)
        if mult == 1:
            return curses.color_pair(1)
        if mult == 2:
            return curses.color_pair(4)
        return curses.color_pair(6)

    mult = type_multiplier(move.type, defender)
    info_lines = [
        f"{move.name}",
        f"{'-' * 76}",
        f"Type: {move.type.capitalize()} ({move.category})",
        f"Base Power: {move.power}",
        f"Accuracy: {'--' if move.acc == -1 else str(move.acc) + '%'}",
        f"{'-' * 76}",
        f"PP: {move.pp}/{move.pp_max}",
        f"Damage Multiplier: {effectiveness_text(mult)}",
        f"{'-' * 76}",
    ]

    damage_pct = None
    if est_damage is not None and defender.max_hp > 0:
        damage_pct = int(est_damage / defender.max_hp * 100)
        info_lines.append(f"Damage: -{damage_pct}% Enemy")
    if getattr(move, 'rhit', 0) and move.rhit > 1:
        info_lines.append(f"Hits {move.rhit} times")
    if getattr(move, 'crits', 0):
        info_lines.append(f"Crit: {move.crits}%")
    if getattr(move, 'enefc', None):
        info_lines.append(f"Secondary: {move.enefc}")
    h, w = stdscr.getmaxyx()
    if getattr(move, 'desc', None):
        info_lines.append('-' * 76)
        info_lines.append("Description:")
        wrap_width = max(10, w - 6)
        for desc_line in textwrap.wrap(move.desc, wrap_width):
            info_lines.append(desc_line)

    top = 0
    left = 0
    bottom = h - 1
    right = w - 1

    while True:
        stdscr.clear()

        border_width = right - left + 1
        safe_addstr_raw(stdscr, top, left, "#" * border_width)
        safe_addstr_raw(stdscr, bottom, left, "#" * border_width)
        for y in range(top + 1, bottom):
            safe_addstr_raw(stdscr, y, left, "#")
            safe_addstr_raw(stdscr, y, right, "#")
            safe_addstr_raw(stdscr, y, left + 1, " " * max(0, border_width - 2))

        content_x = left + 2
        content_y = top + 1
        for idx, line in enumerate(info_lines):
            line_y = content_y + idx
            if line_y < bottom:
                if line.startswith("Effectiveness:"):
                    safe_addstr_raw(stdscr, line_y, content_x, "Effectiveness: ")
                    safe_addstr_raw(stdscr, line_y, content_x + len("Effectiveness: "), effectiveness_text(mult), effectiveness_attr(mult))
                else:
                    safe_addstr_raw(stdscr, line_y, content_x, line)

        stdscr.refresh()

        if stdscr.getch() == ord("c"):
            return


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
    player_sprite = getattr(stats, player.base.name.lower(), stats.placeholder)
    enemy_sprite = getattr(stats, enemy.base.name.lower(), stats.placeholder)

    while True:
        stdscr.clear()
        draw_top_banner(stdscr)
        draw_main_menu(stdscr, 0, player, enemy)
        enemy_sprite.draw(stdscr, "back", "shiny" if enemy.shiny else "normal")
        player_sprite.draw(stdscr, "front", "shiny" if player.shiny else "normal")
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
    player_sprite = getattr(stats, player.base.name.lower(), stats.placeholder)
    enemy_sprite = getattr(stats, enemy.base.name.lower(), stats.placeholder)
    while True:
        stdscr.clear()
        draw_top_banner(stdscr)
        draw_main_menu(stdscr, 0, player, enemy)  
        enemy_sprite.draw(stdscr, "back", "shiny" if enemy.shiny else "normal")
        player_sprite.draw(stdscr, "front", "shiny" if player.shiny else "normal")
        draw_moves(stdscr, player, highlight)
        if max_moves == 0:
            safe_addstr(stdscr, 1, 42, "[    No moves    ]")
       
        draw_header(stdscr, player, enemy)
        key = stdscr.getch()

        if max_moves == 0:
            if key in (ord("x"), ord("z")):
                return None
            continue

        if key == curses.KEY_UP:
            if highlight > 0:
                highlight -= 1
        elif key == curses.KEY_DOWN:
            if highlight < max_moves - 1:
                highlight += 1
        elif key == ord("c") and max_moves > 0:            show_move_info(stdscr, player.moves[highlight], player, enemy)
        elif key == ord("x"):
            return None
        elif key == ord("z"):
            move = player.moves[highlight]
            if move.pp > 0:
                return move       
            
def afightui(stdscr, party, enemy, mode, active_idx=0, can_run=True):
    player = party[active_idx]
    overworld.last_battle_slot = getattr(player, "party_index", 0)
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
    player_sprite = getattr(stats, player.base.name.lower(), stats.placeholder)
    enemy_sprite = getattr(stats, enemy.base.name.lower(), stats.placeholder)

    # Show shiny animations for initial pokemon
    redraw_battle(stdscr, player, enemy)
    if player.shiny:
        shiny_animation(stdscr, player, enemy, is_enemy=False, flashes=6)
    if enemy.shiny:
        shiny_animation(stdscr, player, enemy, is_enemy=True, flashes=6)
    redraw_battle(stdscr, player, enemy)

    while True:
        turn=None
        stdscr.clear()
        draw_main_menu(stdscr, menu_pos, player, enemy)
        enemy_sprite.draw(stdscr, "back", "shiny" if enemy.shiny else "normal")
        player_sprite.draw(stdscr, "front", "shiny" if player.shiny else "normal")
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
            continue
        elif key==ord("z") and menu_pos==3:
            if not can_run:
                textbox(stdscr, "You can't run from a trainer battle!")
                continue
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

        elif key == ord("z") and menu_pos == 1:
            new_idx = party_menu(stdscr, party, active_idx, enemy)
            if new_idx is not None:
                textbox(stdscr, f"Go! {party[new_idx].base.name.capitalize()}!")
                active_idx = new_idx
                player = party[active_idx]
                player_sprite = getattr(stats, player.base.name.lower(), stats.placeholder)
                overworld.last_battle_slot = getattr(player, "party_index", 0)
                redraw_battle(stdscr, player, enemy)
                if player.shiny:
                    shiny_animation(stdscr, player, enemy, is_enemy=False, flashes=6)
                redraw_battle(stdscr, player, enemy)
                continue

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

            # If this Pokémon already fainted earlier in the same turn,
            # it must not act again (otherwise it can damage the replacement mon).
            if user.hp <= 0:
                continue

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

                ability_msg = ability_trigger_message(user)
                if ability_msg:
                    mons_effect_box(
                        stdscr,
                        user,
                        "Ability",
                        ability_msg,
                        specific_name=ability_name(getattr(user, "ability", None))
                    )

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
                    for mon in party:
                        if hasattr(mon, "party_index"):
                            overworld.hpstorage[mon.party_index] = mon.hp
                            

                    if target == enemy:
                        return "win"
                    else:
                        alive = [i for i, mon in enumerate(party) if mon.hp > 0]
                        if not alive:
                            return "lose"

                        new_idx = forced_party_menu(stdscr, party, active_idx, enemy)
                        if new_idx is None:
                            return "lose"

                        active_idx = new_idx
                        player = party[active_idx]
                        player_sprite = getattr(stats, player.base.name.lower(), stats.placeholder)
                        overworld.last_battle_slot = getattr(player, "party_index", 0)
                        textbox(stdscr, f"Go! {player.base.name.capitalize()}!")
                        redraw_battle(stdscr, player, enemy)
                        if player.shiny:
                            shiny_animation(stdscr, player, enemy, is_enemy=False, flashes=6)
                        redraw_battle(stdscr, player, enemy)
                        continue
                        
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
                    if target == enemy and getattr(enemy, "enemytype", "wild") != "trainer":
                        catch_chance = random.randint(1, 100)
                        success = catch_chance > 10
                        if success:
                            animate_pokeball(stdscr, player, enemy, shakes=3, success=True)
                            textbox(stdscr, "Gotcha! The Pokémon was caught!")
                            return ("caught", target)
                        else:
                            shake_count = random.randint(1, 3)
                            animate_pokeball(stdscr, player, enemy, shakes=shake_count, success=False)
                            textbox(stdscr, "The Pokémon broke free!")
                    else:
                        textbox(stdscr, "You can't catch a trainer's Pokémon!")

            status_effect_manager(stdscr, player)
            status_effect_manager(stdscr, enemy)

            # Held item passive effects (Leftovers)
            apply_leftovers(stdscr, player)
            apply_leftovers(stdscr, enemy)
