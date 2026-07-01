import curses
import datetime
import overworld
from datetime import date
try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    requests = None
    REQUESTS_AVAILABLE = False

class MysteryGiftSystem:
    def __init__(self, url):
        self.url = url

    def get_data(self):
        if not REQUESTS_AVAILABLE:
            raise RuntimeError("The 'requests' package is not installed. Install it with: pip install requests\nMystery Gift feature is disabled without it (recommended).")
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
    gift = None
    max_attempts = 3

    for attempt in range(1, max_attempts + 1):
        try:
            gift = gift_system.get_gift(text)
            break
        except Exception as e:
            # If requests is available, handle its specific exceptions.
            if REQUESTS_AVAILABLE and requests is not None:
                if isinstance(e, requests.exceptions.Timeout):
                    stdscr.move(2, 0)
                    stdscr.clrtoeol()
                    if attempt < max_attempts:
                        stdscr.addstr(2, 0, "Mystery Gift server timed out. Retrying...")
                        stdscr.refresh()
                    else:
                        stdscr.addstr(2, 0, "ERROR: Mystery Gift server timed out. Please try again later.")
                        stdscr.refresh()
                        stdscr.getch()
                        return
                else:
                    stdscr.move(2, 0)
                    stdscr.clrtoeol()
                    stdscr.addstr(2, 0, "ERROR: Mystery Gift server could not be reached. Please try again later.")
                    stdscr.refresh()
                    stdscr.getch()
                    return
            else:
                stdscr.move(2, 0)
                stdscr.clrtoeol()
                stdscr.addstr(2, 0, "Optional feature missing: install 'requests' to enable Mystery Gift (recommended).\nInstall with: pip install requests")
                stdscr.refresh()
                stdscr.getch()
                return

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

    else:
        stdscr.addstr(2, 0, f"ERROR: {text} IS INVALID OR THE DATE FOR REDEMPTION HAS EXPIRED!")
    stdscr.refresh()
    stdscr.getch()
