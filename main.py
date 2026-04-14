import pandas as pd
import os
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
    screen.addstr(h - 3, 22, "Edit/Select: Enter", curses.color_pair(4))

    # Exit hotkey
    screen.addstr(h - 2, 2, "Exit: Alt + X", curses.color_pair(6))
    
def draw_warning(screen, message):
    h, w = screen.getmaxyx()
    
    warning_win_h, warning_win_w = 5, len(message) + 10
    warning_win = curses.newwin(
        warning_win_h, warning_win_w, h // 2 - warning_win_h // 2 - 1, w // 2 - warning_win_w // 2
    )
    warning_win.border()
    
    warning_win .addstr(1, warning_win_w // 2 - len(message) // 2, message, curses.color_pair(6))
    warning_win .addstr(3, 2, "Skip: Enter", curses.color_pair(4))
    
    warning_win.getch()

def draw_input(screen, prompt, text=""):
    h, w = screen.getmaxyx()

    edit_win_h, edit_win_w = 8, 60
    edit_win = curses.newwin(
        edit_win_h, edit_win_w, h // 2 - edit_win_h // 2 - 1, w // 2 - edit_win_w // 2
    )
    edit_win.border()
    edit_win.addstr(1, edit_win_w // 2 - len(prompt) // 2, prompt, curses.color_pair(1))
    edit_win.addstr(3, 2, text, curses.color_pair(2))
    edit_win.addstr(5, 2, "Save: Enter", curses.color_pair(4))
    edit_win.addstr(6, 2, "Cancel: Esc", curses.color_pair(4))
    edit_win.refresh()

    curses.curs_set(1)  # Show the cursor
    edit_win.move(3, 2 + len(text))  # Move cursor to the end of the text
    current_text = list(text)  # Convert text to a list for easier manipulation
    cursor_pos = len(current_text)

    while True:
        key = edit_win.getch()

        if key in (curses.KEY_ENTER, 10, 13):  # Enter key to save
            curses.curs_set(0)  # Hide cursor again
            return "".join(current_text)

        elif key == 27:  # ESC key to cancel the edit
            curses.curs_set(0)  # Hide cursor again
            return text  # Return the original text unchanged

        elif key in (curses.KEY_BACKSPACE, 127, 8):
            if cursor_pos > 0:
                del current_text[cursor_pos - 1]
                cursor_pos -= 1

        elif (
            key == curses.KEY_DC
        ):  # Delete key to delete the character under the cursor
            if cursor_pos < len(current_text):
                del current_text[cursor_pos]

        elif key == curses.KEY_LEFT:  # Move cursor left
            if cursor_pos > 0:
                cursor_pos -= 1

        elif key == curses.KEY_RIGHT:  # Move cursor right
            if cursor_pos < len(current_text):
                cursor_pos += 1

        elif key == curses.KEY_HOME or key == 443:  # Move cursor to the start of the line
            cursor_pos = 0

        elif key == curses.KEY_END or key == 444:  # Move cursor to the end of the line
            cursor_pos = len(current_text)

        elif 32 <= key <= 126:  # Insert a printable character
            current_text.insert(cursor_pos, chr(key))
            cursor_pos += 1

        # Update the window with the current text and move the cursor
        edit_win.addstr(
            3,
            2,
            "".join(current_text) + " " * (edit_win_w - 4 - len(current_text)),
            curses.color_pair(2),
        )
        edit_win.move(3, 2 + cursor_pos)
        edit_win.refresh()

def app(screen):
    # Initialize color pairs
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK) # for normal item
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE) # for selected item
    curses.init_pair(3, curses.COLOR_CYAN, curses.COLOR_BLACK) # for [ ], age
    curses.init_pair(4, curses.COLOR_MAGENTA, curses.COLOR_BLACK) # for >, hotkeys
    curses.init_pair(5, curses.COLOR_YELLOW, curses.COLOR_BLACK) # for upcoming birthdays
    curses.init_pair(6, curses.COLOR_RED, curses.COLOR_BLACK) # for exit hotkey, warnings
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
                info = f" - in {left_days} day(s)"
                
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
            new_name = draw_input(screen, "Enter name:", name)
            if new_name is None:
                screen.clear()
                continue
            
            # edit birthdate
            new_birthdate = draw_input(screen, "Enter birthdate (dd.mm.yyyy):", birthdate)
            if new_birthdate is None:
                screen.clear()
                continue
            
            # validate birthdate
            try:
                datetime.strptime(new_birthdate, "%d.%m.%Y")
            except ValueError:
                # invalid
                draw_warning(screen, "Invalid date format!")
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
        
def main():
    BASE_DIR = pathlib.Path(__file__).resolve().parent
    os.chdir(BASE_DIR)
    verify_necessary_files()
    curses.wrapper(app)
    
if __name__ == "__main__":
    main()