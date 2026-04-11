import pandas as pd
import pathlib
import curses
from datetime import datetime

def verify_necessary_files():
    path = pathlib.Path(r"storage/data.csv")
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.touch(exist_ok=True)
        pd.Series(name="birthdate").to_csv(r"storage/data.csv", index_label="name")
        
def draw_text_logo(screen):
    screen.addstr(0, 2, " [", curses.color_pair(3))
    screen.addstr(0, 4, "Birthday Reminder", curses.color_pair(1))
    screen.addstr(0, 2 + len(" [") + len("Birthday Reminder"), "] ", curses.color_pair(3))
    
def draw_hotkeys(screen):
    h, w = screen.getmaxyx()
    
    # Functional hotkeys
    screen.addstr(h - 3, 2, "Navigate: Up/Down", curses.color_pair(4))
    screen.addstr(h - 3, 22, "Edit: Enter", curses.color_pair(4))

    # Exit hotkey
    screen.addstr(h - 2, 2, "Exit: Alt + X", curses.color_pair(6))

def main(screen):
    # Initialize color pairs
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK) # for normal item
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE) # for selected item
    curses.init_pair(3, curses.COLOR_CYAN, curses.COLOR_BLACK) # for [ ], age
    curses.init_pair(4, curses.COLOR_MAGENTA, curses.COLOR_BLACK) # for >, hotkeys
    curses.init_pair(5, curses.COLOR_YELLOW, curses.COLOR_BLACK) # for upcoming birthdays
    curses.init_pair(6, curses.COLOR_RED, curses.COLOR_BLACK) # for exit hotkey
    curses.init_pair(7, curses.COLOR_GREEN, curses.COLOR_BLACK) # for birthdays
    
    # Initialize data variables
    base_x = 4
    base_y = 4
    index = 0
    
    curses.curs_set(0)
    while True:
        # Getting data
        data = [x for x in pd.read_csv(r"storage/data.csv").values]

        max_spaces = max(len(f"{item[0]}") for item in data)
        max_spaces += 2
        # max_age_chars = len(str(len(data) - 1)) + len(" -> ")
        max_age_chars = max(len(f"{(datetime.now() - datetime.strptime(item[1], "%d.%m.%Y")).days // 365}") for item in data)
    
        # Drawing UI
        screen.border()
        draw_text_logo(screen)
        
        screen.addstr(base_y - 2, base_x + max_age_chars, "Age", curses.color_pair(3))
        screen.addstr(base_y - 2, base_x + max_age_chars + 6, "Name", curses.color_pair(1))
        screen.addstr(base_y - 2, base_x + max_age_chars + 7 + max_spaces, "Birthdate", curses.color_pair(5))
        
        for id, row in enumerate(data):
            x = base_x + max_age_chars + 5
            
            name = row[0]
            birthdate = row[1]
            age = (datetime.now() - datetime.strptime(birthdate, "%d.%m.%Y")).days // 365
            left_days = (datetime.strptime(birthdate[:-4] + str(datetime.now().year), "%d.%m.%Y") - datetime.strptime(f"{datetime.now().day}.{datetime.now().month}.{datetime.now().year}", "%d.%m.%Y")).days
            
            color_for_birthdate = 1
            info = f" - in {left_days} days"
            
            if left_days <= 30 and left_days > 0:
                color_for_birthdate = 5
                
            elif left_days == 0:
                color_for_birthdate = 7
                info = " - TODAY!"
            
            else:
                info = ""
                                    
            if id == index:
                screen.addstr(base_y + id, x - max_age_chars - 4, ">", curses.color_pair(4))
                screen.addstr(base_y + id, x - 2 - max_age_chars + (max_age_chars - len(str(age))), str(age), curses.color_pair(3))
                screen.addstr(base_y + id, x, ' ' + name + ' ', curses.color_pair(2))
                screen.addstr(base_y + id, x + len(name) + (max_spaces - len(name)) + 2, birthdate + info, curses.color_pair(color_for_birthdate))
            else:
                screen.addstr(base_y + id, x - 2 - max_age_chars + (max_age_chars - len(str(age))), str(age), curses.color_pair(3))
                screen.addstr(base_y + id, x, ' ' + name + ' ', curses.color_pair(1))
                screen.addstr(base_y + id, x + len(name) + (max_spaces - len(name)) + 2, birthdate + info, curses.color_pair(color_for_birthdate))
        
        draw_hotkeys(screen)
        
        # Getting clicked key
        key = screen.getch()
        
        if key == 440: # Alt + x to exit
            break
        
        elif key == curses.KEY_UP:
            index = (index - 1) % len(data)
            
        elif key == curses.KEY_DOWN:
            index = (index + 1) % len(data)
            
        screen.clear()

if __name__ == "__main__":
    verify_necessary_files()
    curses.wrapper(main)