import curses
import random
#pls what the sigamammam
def run_battle(stdscr,room):
    import fightui
    from fightui import BattleMon, stats, player_result, enemy_result
    player = BattleMon(stats.mon1, 5, [stats.move1, stats.move2, stats.move3, stats.move4])
    if room == 1:
        enemy = BattleMon(stats.mon16, 2, [stats.move5, stats.move6, stats.move7, stats.move8])

    result =  fightui.afightui(stdscr, player, enemy)
    return result
    