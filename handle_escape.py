import sys
import time

ESC = '\x1b'
PY3K = sys.version_info >= (3,)
if PY3K:
    from msvcrt import kbhit, getwch as _getch
else:
    from msvcrt import kbhit, getch as _getch
while not kbhit() or _getch() != ESC:
    print(time.asctime())
    time.sleep(1)
