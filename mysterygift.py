import curses
import datetime
import overworld
from datetime import date
import requests

class MysteryGiftSystem:
    def __init__(self, url):
        self.url = url

    def get_data(self):
        response = requests.get(self.url, timeout=10)
        response.raise_for_status()
        return response.json()

    def get_gift(self, code):
        today = date.today()
        data = self.get_data()

        for gift in data.get("mystery_gifts", []):
            if gift["code"] == code:
                start = date.fromisoformat(gift["start_date"])
                end = date.fromisoformat(gift["end_date"])

                if start <= today <= end:
                    return gift

        return None

def giftmon(stdscr,id,name,level,m1=0,m2=0,m3=0,m4=0,shiny=False):
    from overworld import MonOver, party_mons, add_to_party_or_pc, picked_items
    new_mon = MonOver(
        rotation=len(party_mons) + 1,
        id=id,
        name=name,
        moves=[m1, m2, m3, m4],
        level=level,
        exp=0,
        shiny=shiny
    )

    add_to_party_or_pc(stdscr, new_mon)
    picked_items.add(new_mon.id)

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
    gift_system = MysteryGiftSystem("https://pokethon-api.onrender.com/config")
    gift = gift_system.get_gift(text)

    if gift:
        mon = gift["mon"]

        giftmon(
            stdscr,
            mon["id"],
            mon["name"],
            mon["level"],
            m1=mon["moves"][0],
            m2=mon["moves"][1],
            m3=mon["moves"][2],
            m4=mon["moves"][3],
            shiny=mon["shiny"]
        )

        stdscr.addstr(2, 0, "Redeemed Successfully! Check your game/savefile!")
    else:
        stdscr.addstr(2, 0, f"ERROR: {text} IS INVALID OR THE DATE FOR REDEMPTION HAS EXPIRED!")
    stdscr.refresh()
    stdscr.getch()
