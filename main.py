import pandas as pd
import pathlib
import curses

def verify_necessary_files():
    path = pathlib.Path(r"storage/data.csv")
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.touch(exist_ok=True)
        pd.Series(name="birthday").to_csv(r"storage/data.csv", index_label="name")
        
def draw_text_logo(screen):
    screen.addstr(0, 2, " [", curses.color_pair(3))
    screen.addstr(0, 4, "Birthday Reminder", curses.color_pair(1))
    screen.addstr(0, 2 + len(" [") + len("Birthday Reminder"), "] ", curses.color_pair(3))
    

def main(screen):
    # Initialize color pairs
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK) # for normal item
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE) # for selected item
    curses.init_pair(3, curses.COLOR_CYAN, curses.COLOR_BLACK) # for [ ]
    
    # Initialize data variables
    base_x = 2
    base_y = 1
    
    curses.curs_set(0)    
    while True:
        # Getting data
        data = pd.read_csv(r"storage/data.csv", index_col="name")
    
        # Drawing UI
        screen.border()
        draw_text_logo(screen)
        
        for id, name in enumerate(data.index):
            screen.addstr(base_y + id, base_x, name, curses.color_pair(1))
        
        # Getting clicked key
        key = screen.getch()
        
        if key == 440: # Alt + x to exit
            break

if __name__ == "__main__":
    verify_necessary_files()
    curses.wrapper(main)