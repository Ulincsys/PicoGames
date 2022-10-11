import sys
from uio import StringIO

sys.path.append("src")

import main_menu

try:
    main_menu.loop()
except Exception as e:
    display = main_menu.display

    X, Y = display.get_bounds()

    display.reset_pen(0)
    display.reset_pen(1)

    bg = display.create_pen(0, 0, 255)
    fg = display.create_pen(120, 120, 120)

    display.set_pen(bg)
    display.clear()

    tb = StringIO()
    sys.print_exception(e, tb)

    display.set_pen(fg)
    for i, line in enumerate(tb.getvalue().split("\n")):
        display.text(str(line), 0, i * 9, 10 * X, 1)

    display.text(str(e), 0, i * 9, X, 2)
    display.update()