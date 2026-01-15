import curses
import stats

VISIBLE = 4  # Number of visible items in menus

# Pokémon objects
mons = [getattr(stats, f"mon{i}") for i in range(1, 152) if hasattr(stats, f"mon{i}")]
# Moves are tuples
moves_list = [stats.move1, stats.move2, stats.move3, stats.move4]


def truncate(text, width):
    """Truncate text to fit in terminal width"""
    if len(text) > width:
        return text[:width-3] + "..."
    return text


def safe_addstr(stdscr, y, x, text):
    """Add string safely, truncating to screen width"""
    h, w = stdscr.getmaxyx()
    if y < h:
        stdscr.addstr(y, x, truncate(text, w - x))


def select_from_list(stdscr, items, title="Select", visible=VISIBLE, show_type=False, show_desc=False):
    scroll = 0
    cursor = 0

    while True:
        stdscr.clear()
        h, w = stdscr.getmaxyx()
        safe_addstr(stdscr, 0, 0, title)
        safe_addstr(stdscr, 1, 0, "-" * min(50, w))

        for i in range(visible):
            idx = scroll + i
            if idx >= len(items):
                break

            item = items[idx]

            if hasattr(item, "call"):  # Pokémon
                name = item.call().capitalize()
                if show_type:
                    type1 = getattr(item, "type", "")
                    type2 = getattr(item, "type2", "")
                    types = type1.capitalize()
                    if type2:
                        types += f"/{type2.capitalize()}"
                    line = f"{name} - {types}"
                else:
                    line = name
            else:  # Moves as tuples
                name = item[0].capitalize()
                desc = item[-1] if len(item) > 0 else "#placeholder"
                line = f"{name} - {desc}" if show_desc else name

            line = truncate(line, w - 3)
            if i == cursor:
                safe_addstr(stdscr, i + 2, 0, f"> {line}")
            else:
                safe_addstr(stdscr, i + 2, 0, f"  {line}")

        key = stdscr.getch()
        if key == curses.KEY_UP:
            if cursor > 0:
                cursor -= 1
            elif scroll > 0:
                scroll -= 1
        elif key == curses.KEY_DOWN:
            if cursor < visible - 1 and scroll + cursor + 1 < len(items):
                cursor += 1
            elif scroll + visible < len(items):
                scroll += 1
        elif key == ord("z"):
            return scroll + cursor
        elif key == ord("q"):
            return None
        stdscr.refresh()


def select_pokemon_and_moves(stdscr, mons_pool, label="Player"):
    idx = select_from_list(stdscr, mons_pool, f"{label} Pokémon", show_type=True)
    if idx is None:
        return None, []
    mon = mons_pool.pop(idx)

    selected_moves = []
    for i in range(4):
        move_idx = select_from_list(
            stdscr,
            moves_list,
            f"{mon.call().capitalize()} - Move {i+1}",
            show_desc=True
        )
        if move_idx is None:
            break
        selected_moves.append(moves_list[move_idx])

    return mon, selected_moves


def show_summary(stdscr, player_mon, player_moves, enemy_mon, enemy_moves):
    """
    Compact summary:
    Pokémon name
    move1_name   move2_name
    move3_name   move4_name
    """
    stdscr.clear()
    h, w = stdscr.getmaxyx()
    safe_addstr(stdscr, 0, 0, "Battle Setup Complete (Press Z to Start Battle)")
    safe_addstr(stdscr, 1, 0, "-" * min(50, w))

    def draw_compact(mon, moves, start_row, label):
        safe_addstr(stdscr, start_row, 0, f"{label}: {mon.call().capitalize()}")
        max_width = (w - 6) // 2  # 2 moves per line
        lines_needed = (len(moves) + 1) // 2
        for i in range(lines_needed):
            left_idx = i*2
            right_idx = i*2 + 1
            left_text = moves[left_idx][0].capitalize() if left_idx < len(moves) else ""
            left_text = truncate(left_text, max_width)
            line = f"{left_text:<{max_width}}"
            if right_idx < len(moves):
                right_text = moves[right_idx][0].capitalize()
                right_text = truncate(right_text, max_width)
                line += right_text
            safe_addstr(stdscr, start_row + 1 + i, 2, line)
        return start_row + 1 + lines_needed + 1  # next starting row

    row = 2
    row = draw_compact(player_mon, player_moves, row, "Player")
    row = draw_compact(enemy_mon, enemy_moves, row, "Enemy")
    stdscr.refresh()

    while True:
        key = stdscr.getch()
        if key == ord("z"):
            afightui(stdscr)
            break


def battle_setup(stdscr):
    mons_pool = mons.copy()
    player_mon, player_moves = select_pokemon_and_moves(stdscr, mons_pool, label="Player")
    enemy_mon, enemy_moves = select_pokemon_and_moves(stdscr, mons_pool, label="Enemy")
    show_summary(stdscr, player_mon, player_moves, enemy_mon, enemy_moves)
    return {
        "player": {"mon": player_mon, "moves": player_moves},
        "enemy": {"mon": enemy_mon, "moves": enemy_moves},
    }


def afightui(stdscr):
    curses.curs_set(0)
    stdscr.keypad(True)
    x = 0
    y = 0
    cell_width = 11
    while True:
        stdscr.clear()
        grid = [["--Fight--", "---Bag---"], ["-Pokémon-", "---Run---"]]
        for j in range(2):
            for i in range(2):
                text = grid[j][i].ljust(9)
                cell = f"[{text}]" if i == x and j == y else f" {text} "
                safe_addstr(stdscr, j*2, i*cell_width, cell)
        key = stdscr.getch()
        if key == curses.KEY_UP and y > 0:
            y -= 1
        elif key == curses.KEY_DOWN and y < 1:
            y += 1
        elif key == curses.KEY_LEFT and x > 0:
            x -= 1
        elif key == curses.KEY_RIGHT and x < 1:
            x += 1
        elif key == ord("q"):
            break
