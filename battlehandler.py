import curses
import random
import overworld
import fightui , stats
#pls what the sigamammam
def create_mon(mon_id, level, move_ids, hp=None, enemytype=None):

    stat_block = getattr(stats, f"mon{mon_id}")
    move_list = [getattr(stats, f"move{m}") for m in move_ids]

    mon = fightui.BattleMon(stat_block, level, move_list, hp)

    # attach custom attribute
    mon.enemytype = enemytype

    return mon
import overworld

def make_enemy(mon_id, *moves, lvl=1, enemytype="wild"):
    return create_mon(
        mon_id=mon_id,
        level=lvl,
        move_ids=list(moves),
        hp=-1,
        enemytype=enemytype
    )

def to_battle_mon(mon):
    return create_mon(
        mon_id=mon.id,
        level=mon.level,
        move_ids=mon.moves,
        hp=overworld.hpstorage[0],
        enemytype="player"
    )

def run_battle(stdscr, room):
    import overworld
    import fightui

    player = to_battle_mon(overworld.Mon1)

    if room == 1:
        enemy = make_enemy(16, 5, 6, 7, 8, lvl=2)

    result = fightui.afightui(stdscr, player, enemy, 1)
    return result