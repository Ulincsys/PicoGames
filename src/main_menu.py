import os
import time
import random

from pimoroni import Button, RGBLED
from picographics import PicoGraphics, DISPLAY_PICO_DISPLAY, PEN_P4

from utils import ScrollableMenu

display = PicoGraphics(display=DISPLAY_PICO_DISPLAY, pen_type=PEN_P4, rotate=0)

display.set_backlight(1)

display.set_font("bitmap8")
# font_size(1) height = 7
# font_size(2) height = 14


led = RGBLED(6, 7, 8)
led.set_rgb(0, 0, 0)

# Definition of the Button class constructor
# Button(uint pin, Polarity polarity=Polarity::ACTIVE_LOW, uint32_t repeat_time=200, uint32_t hold_time=1000)

def load_libraries():
    for file in os.listdir("src"):
        if file.endswith(".py") and file not in __file__ and file != "settings.py":
            yield file.replace(".py", "")
    
    # We want the settings option to be at the end of the list
    yield "settings"

def loop():
    games = list(load_libraries())

    menu = ScrollableMenu(display, games, font_size=3, color_hl=[255, 255, 255], color_bg=[20, 20, 20], color_fg=[0, 255, 0], color_scrollbar=[255, 0, 0])

    while True:
        game = menu.get_selection()
        if game != False:
            m = __import__("src/" + games[game])
            m.loop()

        time.sleep(0.1)

if __name__ == "__main__":
    loop()