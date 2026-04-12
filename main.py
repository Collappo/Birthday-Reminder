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

def input_field(screen, prompt, text=""):
    h, w = screen.getmaxyx()
    edit_win_h, edit_win_w = 9, 60
    edit_win = curses.newwin(
        edit_win_h, edit_win_w, h // 2 - edit_win_h // 2 - 1, w // 2 - edit_win_w // 2
    )
    edit_win.border(0)
    
    edit_win.addstr(1, edit_win_w // 2 - len(prompt) // 2, prompt)
    input_str = text
    cursor_pos = len(input_str)
    while True:
        edit_win.addstr(2, 2, " " * (edit_win_w - 4), curses.color_pair(2))  # clear line
        edit_win.addstr(2, 3, input_str, curses.color_pair(2))
        edit_win.move(2, 3 + cursor_pos)
        edit_win.refresh()
        key = screen.getch()
        if key == curses.KEY_ENTER or key in [10, 13]:  # Enter
            break
        elif key == 27:  # Escape
            return None
        elif key == curses.KEY_BACKSPACE or key == 8:
            if cursor_pos > 0:
                input_str = input_str[:cursor_pos-1] + input_str[cursor_pos:]
                cursor_pos -= 1
        elif key == curses.KEY_LEFT:
            if cursor_pos > 0:
                cursor_pos -= 1
        elif key == curses.KEY_RIGHT:
            if cursor_pos < len(input_str):
                cursor_pos += 1
        elif 32 <= key <= 126:  # printable
            input_str = input_str[:cursor_pos] + chr(key) + input_str[cursor_pos:]
            cursor_pos += 1
    return input_str

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

        # Calculate max spaces for name
        names = [item[0] for item in data] + ["Add new person"]
        max_spaces = max(len(name) for name in names) + 2 if names else 16

        # Calculate max age chars
        if data:
            max_age_chars = max(len(str((datetime.now() - datetime.strptime(item[1], "%d.%m.%Y")).days // 365)) for item in data)
        else:
            max_age_chars = 2  # for "Add new person", no age
    
        # Drawing UI
        screen.border()
        draw_text_logo(screen)
        
        screen.addstr(base_y - 2, base_x + max_age_chars, "Age", curses.color_pair(3))
        screen.addstr(base_y - 2, base_x + max_age_chars + 6, "Name", curses.color_pair(1))
        screen.addstr(base_y - 2, base_x + max_age_chars + 7 + max_spaces, "Birthdate", curses.color_pair(5))
        
        for id, row in enumerate(data + [None]):  # Add None for "Add new person"
            x = base_x + max_age_chars + 5
            y_pos = base_y + id if id < len(data) else base_y + id + 1
            
            if id < len(data):
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
            else:
                # Add new person
                name = "Add new person"
                birthdate = ""
                age = ""
                color_for_birthdate = 1
                info = ""
                                    
            if id == index:
                screen.addstr(y_pos, x - max_age_chars - 4, ">", curses.color_pair(4))
                if id < len(data):
                    screen.addstr(y_pos, x - 2 - max_age_chars + (max_age_chars - len(str(age))), str(age), curses.color_pair(3))
                screen.addstr(y_pos, x, ' ' + name + ' ', curses.color_pair(2))
                screen.addstr(y_pos, x + len(name) + (max_spaces - len(name)) + 2, birthdate + info, curses.color_pair(color_for_birthdate))
            else:
                if id < len(data):
                    screen.addstr(y_pos, x - 2 - max_age_chars + (max_age_chars - len(str(age))), str(age), curses.color_pair(3))
                screen.addstr(y_pos, x, ' ' + name + ' ', curses.color_pair(1))
                screen.addstr(y_pos, x + len(name) + (max_spaces - len(name)) + 2, birthdate + info, curses.color_pair(color_for_birthdate))
        
        draw_hotkeys(screen)
        
        # Getting clicked key
        key = screen.getch()
        
        if key == 440: # Alt + x to exit
            break
        
        elif key == curses.KEY_UP:
            index = (index - 1) % (len(data) + 1)
            
        elif key == curses.KEY_DOWN:
            index = (index + 1) % (len(data) + 1)
            
        elif key == curses.KEY_ENTER or key in [10, 13]: # Enter to edit
            if index < len(data):
                # edit existing
                name = data[index][0]
                birthdate = data[index][1]
            else:
                # add new
                name = ""
                birthdate = ""
            
            # edit name
            new_name = input_field(screen, "Enter name:", name)
            if new_name is None:
                screen.clear()
                continue
            
            # edit birthdate
            new_birthdate = input_field(screen, "Enter birthdate (dd.mm.yyyy):", birthdate)
            if new_birthdate is None:
                screen.clear()
                continue
            
            # validate birthdate
            try:
                datetime.strptime(new_birthdate, "%d.%m.%Y")
            except ValueError:
                # invalid, show error
                screen.addstr(center_y + 2, center_x, "Invalid date format!", curses.color_pair(6))
                screen.getch()
                screen.clear()
                continue
            
            # update data
            if index < len(data):
                data[index] = [new_name, new_birthdate]
            else:
                data.append([new_name, new_birthdate])
            
            # save to csv
            df = pd.DataFrame(data, columns=['name', 'birthdate'])
            df.to_csv(r"storage/data.csv", index=False)
            screen.clear()
            
        screen.clear()

if __name__ == "__main__":
    verify_necessary_files()
    curses.wrapper(main)