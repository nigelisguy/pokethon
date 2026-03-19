import curses

def run_battle(stdscr):
    import fightui
    from fightui import BattleMon, stats

    curses.start_color()  
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(2, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLACK)

    player = BattleMon(stats.mon1, 50, [stats.move1, stats.move2, stats.move3, stats.move4])
    enemy = BattleMon(stats.mon2, 50, [stats.move5, stats.move6, stats.move7, stats.move8])

    result = fightui.afightui(stdscr, player, enemy)
    return result