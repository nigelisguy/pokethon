import curses
import datetime
from datetime import date

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
    if date.today().weekday() == 1 and text == "67676767":
        stdscr.addstr(2, 0, f"Redeemed Nothing! Check your game/savefile!")   
    else:
        stdscr.addstr(2, 0, f"ERROR: {text} IS INVALID OR THE DATE FOR REDEMPTION HAS EXPIRED!")    
    stdscr.refresh()
    stdscr.getch()
