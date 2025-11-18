import curses


def main(stdscr):
    print("Press 'Esc' to exit.")
    while True:
        key = stdscr.getch()
        if key == 27:  # 27 is the ASCII code for the Escape key
            print("You pressed the Escape key!")
            break


# Start the curses application
curses.wrapper(main)
