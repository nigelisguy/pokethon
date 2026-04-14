import curses
import random
import overworld
#pls what the sigamammam
def to_battle_mon(mon):
    from fightui import BattleMon, stats

    stat_block = getattr(stats, f"mon{mon.id}")

    move_list = [
        getattr(stats, f"move{m}") for m in mon.moves
    ]

    return BattleMon(stat_block, mon.level, move_list, overworld.hpstorage[0])
def run_battle(stdscr,room):
    import fightui
    from fightui import BattleMon, stats, player_result, enemy_result
    try:
        value = overworld.hpstorage[0]
        
    except(IndexError,AttributeError):
        value = -1
    player = to_battle_mon(overworld.Mon1)
    if room == 1:
        enemy = BattleMon(stats.mon16, 2, [stats.move5, stats.move6, stats.move7, stats.move8])

    result = fightui.afightui(stdscr, player, enemy, 1)
    return result

    