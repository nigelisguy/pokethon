import curses
import datetime

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

    stdscr.addstr(2, 0, f"ERROR: {text} IS A INVALID CODE!")
    stdscr.refresh()
    stdscr.getch()
