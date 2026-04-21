import curses
import random
import overworld
import fightui , stats
#pls what the sigamammam

last_enemy = None

def create_mon(mon_id, level, move_ids, hp=None, enemytype=None):
    stat_block = getattr(stats, f"mon{mon_id}")
    move_list = [getattr(stats, f"move{m}") for m in move_ids]

    mon = fightui.BattleMon(stat_block, level, move_list, hp)

    # Preserve source data so overworld/save code can reconstruct this mon later.
    mon.mon_id = mon_id
    mon.move_ids = list(move_ids)
    mon.enemytype = enemytype

    return mon

def make_enemy(mon_id, *moves, lvl=1, enemytype="wild"):
    return create_mon(
        mon_id=mon_id,
        level=lvl,
        move_ids=list(moves),
        hp=-1,
        enemytype=enemytype
    )

def enemy_for_room(room):
    if room == 1:
        return make_enemy(5, 340, 340, 340, 340, lvl=2)
    raise ValueError(f"Unsupported room id: {room}")

def calculate_exp_gain(enemy, participants=1, trainer_battle=False):
    base_exp = getattr(enemy.base, "base_exp", 0)
    exp_gain = (base_exp * enemy.level) // 7
    exp_gain //= max(1, participants)

    if trainer_battle:
        exp_gain = (exp_gain * 3) // 2

    return max(1, exp_gain)

def to_battle_party():
    raw_party = [
        getattr(overworld, "Mon1", None),
        getattr(overworld, "Mon2", None),
        getattr(overworld, "Mon3", None),
        getattr(overworld, "Mon4", None),
        getattr(overworld, "Mon5", None),
        getattr(overworld, "Mon6", None),
    ]

    party = []
    for i, mon in enumerate(raw_party):
        if mon is None:
            continue

        hp = overworld.hpstorage[i] if i < len(overworld.hpstorage) else -1

        battle_mon = create_mon(
            mon_id=mon.id,
            level=mon.level,
            move_ids=mon.moves,
            hp=hp,
            enemytype="player"
        )
        battle_mon.party_index = i
        party.append(battle_mon)

    return party

def run_battle(stdscr, room):
    global last_enemy
    player_party = to_battle_party()
    enemy = enemy_for_room(room)
    last_enemy = enemy

    result = fightui.afightui(stdscr, player_party, enemy, 1)
    return result

def to_battle_mon(mon):
    return create_mon(
        mon_id=mon.id,
        level=mon.level,
        move_ids=mon.moves,
        hp=overworld.hpstorage[0],
        enemytype="player"
    )
