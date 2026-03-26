import curses
#wip
def run_battle(stdscr):
    import fightui
    from fightui import BattleMon, stats

    player = BattleMon(stats.mon1, 50, [stats.move1, stats.move2, stats.move3, stats.move4])
    enemy = BattleMon(stats.mon2, 50, [stats.move5, stats.move6, stats.move7, stats.move8])

    result = fightui.afightui(stdscr, player, enemy)
    return result