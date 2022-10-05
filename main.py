import os
import time
import random

from pimoroni import Button, RGBLED
from picographics import PicoGraphics, DISPLAY_PICO_DISPLAY, PEN_P4

from utils import ScrollableMenu

display = PicoGraphics(display=DISPLAY_PICO_DISPLAY, pen_type=PEN_P4, rotate=0)

display.set_backlight(1)
display.set_font("bitmap8")

led = RGBLED(6, 7, 8)
led.set_rgb(0, 0, 0)

# Definition of the Button class constructor
# Button(uint pin, Polarity polarity=Polarity::ACTIVE_LOW, uint32_t repeat_time=200, uint32_t hold_time=1000)

def load_libraries():
    for file in os.listdir():
        if file.endswith(".py") and file != "main.py" and file != "settings.py":
            yield file.replace(".py", "")
    
    # We want the settings option to be at the end of the list
    yield "settings"

if __name__ == "__main__":
    games = list(load_libraries())

    menu = ScrollableMenu(display, games)

    while True:
        index, game = menu.get_selection()
        m = __import__(game)
        m.loop()