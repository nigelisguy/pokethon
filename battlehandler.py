import curses
import random
import overworld
import fightui , stats
#pls what the sigamammam

last_enemy = None
last_defeated_enemies = []

TRAINERS = {
    "room2_guard": {
        "name": "Bug Kid",
        "party": [
            (10, 3, [340, 340, 340, 340]),
            (13, 4, [340, 340, 340, 340]),
        ],
    },
}

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

def make_trainer_party(trainer_id):
    trainer = TRAINERS[trainer_id]
    party_data = trainer["party"][:6]
    return [
        create_mon(
            mon_id=mon_id,
            level=level,
            move_ids=moves,
            hp=-1,
            enemytype="trainer"
        )
        for mon_id, level, moves in party_data
    ]

def sync_player_hp(player_party):
    for mon in player_party:
        if hasattr(mon, "party_index"):
            overworld.hpstorage[mon.party_index] = mon.hp

def active_battle_index(player_party):
    for i, mon in enumerate(player_party):
        if mon.hp > 0 and getattr(mon, "party_index", None) == overworld.last_battle_slot:
            return i

    for i, mon in enumerate(player_party):
        if mon.hp > 0:
            return i

    return None

def enemy_for_room(room):
    if room == 1:
        spawnlist=[19,16,21]
        return make_enemy(random.choice(spawnlist), 340, 340, 340, 340, lvl=random.randint(2, 4))
    raise ValueError(f"Unsupported room id: {room}")

def calculate_exp_gain(enemy, participants=1, trainer_battle=False):
    base_exp = getattr(enemy.base, "base_exp", 0)
    participants = max(1, participants)
    trainer_multiplier = 3 if trainer_battle else 2

    exp_gain = (base_exp * enemy.level * trainer_multiplier) // (7 * participants * 2)

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
    active_idx = active_battle_index(player_party)
    if active_idx is None:
        return "lose"

    enemy = enemy_for_room(room)
    last_enemy = enemy

    result = fightui.afightui(stdscr, player_party, enemy, 1, active_idx=active_idx)
    sync_player_hp(player_party)
    return result

def run_trainer_battle(stdscr, trainer_id):
    global last_enemy, last_defeated_enemies
    player_party = to_battle_party()
    enemy_party = make_trainer_party(trainer_id)
    last_defeated_enemies = []

    for i, enemy in enumerate(enemy_party):
        last_enemy = enemy
        active_idx = active_battle_index(player_party)
        if active_idx is None:
            return "lose"

        if i > 0:
            trainer_name = TRAINERS[trainer_id]["name"]
            fightui.textbox(stdscr, f"{trainer_name} sent out {enemy.base.name.capitalize()}!")

        result = fightui.afightui(stdscr, player_party, enemy, 1, active_idx=active_idx, can_run=False)
        sync_player_hp(player_party)

        if result != "win":
            return result

        last_defeated_enemies.append(enemy)

        active_mon = overworld.get_party_mon(overworld.last_battle_slot)
        if active_mon is not None:
            gained_exp = calculate_exp_gain(enemy, trainer_battle=True)
            active_mon.expgain(stdscr, gained_exp)

    return "win"

def to_battle_mon(mon):
    return create_mon(
        mon_id=mon.id,
        level=mon.level,
        move_ids=mon.moves,
        hp=overworld.hpstorage[0],
        enemytype="player"
    )
