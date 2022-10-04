import os
import time
import random

from pimoroni import Button, RGBLED
from picographics import PicoGraphics, DISPLAY_PICO_DISPLAY, PEN_P4

display = PicoGraphics(display=DISPLAY_PICO_DISPLAY, pen_type=PEN_P4, rotate=0)

display.set_backlight(0.5)
display.set_font("bitmap8")

led = RGBLED(6, 7, 8)
led.set_rgb(0, 0, 0)

X, Y = display.get_bounds()
# For line drawing, stop from going OOB
X -= 1
Y -= 1

# The vertical space between lines (from the top of one character to the top of the character below it)
LINE_SPACE = 30

# The pixel at which text rendering starts
LINE_START = 0

# The time between scroll stop and scroll start
SCROLL_TIMEOUT = 50

# Definition of the Button class constructor
# Button(uint pin, Polarity polarity=Polarity::ACTIVE_LOW, uint32_t repeat_time=200, uint32_t hold_time=1000)

button_a = Button(12)
button_b = Button(13)
button_x = Button(14)
button_y = Button(15)

WHITE = display.create_pen(255, 255, 255)
BLACK = display.create_pen(0, 0, 0)
CYAN = display.create_pen(0, 255, 255)
MAGENTA = display.create_pen(255, 0, 255)
YELLOW = display.create_pen(255, 255, 0)
GREEN = display.create_pen(0, 255, 0)
RED = display.create_pen(180, 0, 0)

def clear(update = True):
    display.set_pen(BLACK)
    display.clear()

    if update:
        display.update()

def load_libraries():
    for file in os.listdir():
        if file.endswith(".py") and file != "main.py" and file != "settings.py":
            yield file.replace(".py", "")
    
    # We want the settings option to be at the end of the list
    yield "settings"

def draw_list():
    global games
    global game_index
    global scroll
    global scroll_timer
    global scroll_text

    # We make this global for use with redrawing in other functions
    global vscroll_offset

    # We want to have the view scroll when the cursor gets halfway down the screen
    if 30 * (game_index + 1) > Y // 2:
        # We achieve the scroll effect by applying a negative offset to the Y index
        vscroll_offset = (Y // 2) - (LINE_SPACE * game_index) - 7
        # 7 here is a magic number which corresponds to the space between the bottom of a character and the top of the next
        # It's required to stop the view from jumping when the offset is applied
        # Unfortunately it cannot be calculated, and must be derived from experimentation
        # (because the display library cannot give us a veritcal measurement of a character)
    else:
        vscroll_offset = 0

    # This is slightly inefficient since we're rendering text which is offscreen,
    # but I'm not going to bother optimizing it since we have enough power to compensate
    clear(False)
    display.set_pen(RED)
    for index in range(0, len(games)):
        if index == game_index:
            display.set_pen(MAGENTA)
            text_length = display.measure_text(games[index], 3)
            display.rectangle(LINE_START, LINE_SPACE * index + vscroll_offset, text_length, LINE_SPACE)
            display.set_pen(RED)

            if text_length > X - LINE_START:
                scroll = True
                scroll_text = games[index]
                scroll_timer = SCROLL_TIMEOUT
            else:
                scroll = False
        display.text(games[index], LINE_START, LINE_SPACE * index + vscroll_offset, 10 * Y, 3)
    display.update()

def do_text_scroll():
    global games
    global game_index
    global scroll_text
    global scroll_timer
    global vscroll_offset

    if scroll_timer > 0:
        scroll_timer -= 1
    else:
        display.set_pen(MAGENTA)
        text_length = display.measure_text(scroll_text, 3)
        display.rectangle(LINE_START, LINE_SPACE * game_index + vscroll_offset, X, LINE_SPACE)
        display.set_pen(RED)
        display.text(scroll_text, LINE_START, LINE_SPACE * game_index + vscroll_offset, 10 * Y, 3)

        if text_length > X - LINE_START:
            scroll_text = scroll_text[1:]
            scroll_timer = SCROLL_TIMEOUT
        else:
            scroll_text = games[game_index]
            scroll_timer = 3 * SCROLL_TIMEOUT
        
        display.update()

def loop():
    clear()

    global games
    global game_index
    global scroll
    global scroll_text
    global scroll_timer

    scroll_timer = SCROLL_TIMEOUT
    scroll = False
    scroll_text = ""
    game_index = 0

    draw_list()

    while True:
        if button_x.read():
            if game_index > 0:
                game_index -= 1
                draw_list()
        elif button_y.read():
            if game_index < len(games) - 1:
                game_index += 1
                draw_list()
        elif button_a.read():
            m = __import__(games[game_index])
            m.loop()
            # Delete the loaded module after use to save memory
            m = None
            # redraw list after exiting game to refresh screen
            draw_list()
        elif scroll:
            do_text_scroll()
        time.sleep(0.01)

if __name__ == "__main__":
    global games
    games = list(load_libraries())

    loop()