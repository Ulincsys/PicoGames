from pimoroni import Button
from utils import Interactible
import time

class SliderOption(Interactible):
    @property
    def next(self):
        if self.value + self.step > self.end:
            return None
        
        self.value += self.step
        return self.value
    
    @property
    def previous(self):
        if self.value - self.step < self.start:
            return None
        
        self.value -= self.step
        return self.value

    def __init__(self, display, slider_range = [0, 1, 0.1], default = 0.5, btn_inc = 15, btn_dec = 14, btn_sel = 12, btn_exit = 13, color_bg = [0, 0, 0], color_fg = [255, 255, 255], color_slider = [30, 30, 30], color_selector = [0, 255, 0], color_endpoint = [255, 0, 255]):
        # Set up attributes
        self.display = display

        self.font_size = 3
        
        self.start = slider_range[0]
        self.end = slider_range[1]
        self.step = slider_range[2]

        self.value = default

        self.button_property("btn_inc", "_next")
        self.button_property("btn_dec", "_prev")
        self.button_property("btn_save", "_save")
        self.button_property("btn_cancel", "_cancel")

        self.btn_inc = btn_inc
        self.btn_dec = btn_dec

        self.color_property("color_fg", "_fg")
        self.color_property("color_bg", "_bg")
        self.color_property("color_slider", "_slider")
        self.color_property("color_selector", "_selector")
        self.color_property("color_endpoint", "_endpoint")