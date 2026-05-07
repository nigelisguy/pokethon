import curses
import datetime
import overworld
from datetime import date

def giftmon(stdscr,id,name,level,m1=0,m2=0,m3=0,m4=0,shiny=False):
    from overworld import MonOver, party_mons, add_to_party_or_pc, remove_id, picked_items
    new_mon = MonOver(
        rotation=len(party_mons) + 1,
        id=id,
        name=name,
        moves=list(m1,m2,m3,m4),
        level=level,
        exp=0,
        shiny=shiny
    )

    add_to_party_or_pc(stdscr, new_mon)
    if remove_id is not None:
        picked_items.add(remove_id)

def gifted(stdscr):
    stdscr.clear()

    stdscr.addstr(0, 0, "Enter Mystery Gift: ")
    stdscr.refresh()

    text = ""
    while True:
        key = stdscr.get_wch() 

        if key == '\n': 
            break
        elif key == '\x7f':  
            text = text[:-1]
            y, x = stdscr.getyx()
            stdscr.move(y, x - 1)
            stdscr.delch()
        else:
            text += str(key)
            stdscr.addstr(str(key))
    if date.today().weekday() == 1 and text == "superalpha":
        giftedmon = giftmon(stdscr, 90, "Mewtwo", 100, m1=1, m2=2, m3=3, m4=4, shiny=True)
        stdscr.addstr(2, 0, f"Redeemed Successfully! Check your game/savefile!")   
    else:
        stdscr.addstr(2, 0, f"ERROR: {text} IS INVALID OR THE DATE FOR REDEMPTION HAS EXPIRED!")    
    stdscr.refresh()
    stdscr.getch()
