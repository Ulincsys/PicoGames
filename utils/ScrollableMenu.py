from pimoroni import Button
import time

class ScrollableMenu:
    @property
    def color_bg(self):
        return self.bg

    @color_bg.setter
    def color_bg(self, values):
        self.bg = self.display.create_pen(*values)
    
    @property
    def color_fg(self):
        return self.fg
    
    @color_fg.setter
    def color_fg(self, values):
        self.fg = self.display.create_pen(*values)
    
    @property
    def color_hl(self):
        return self.hl
    
    @color_hl.setter
    def color_hl(self, values):
        self.hl = self.display.create_pen(*values)
    
    @property
    def btn_prev(self):
        return self._prev.read()
    
    @btn_prev.setter
    def btn_dn(self, value):
        self._prev = Button(value)
    
    @property
    def btn_next(self):
        return self._next.read()
    
    @btn_next.setter
    def btn_up(self, value):
        self._next = Button(value)
    
    @property
    def btn_sel(self):
        return self._select.read()
    
    @btn_sel.setter
    def btn_sel(self, value):
        self._select = Button(value)
    
    @property
    def btn_exit(self):
        return self._exit.read()

    @btn_exit.setter
    def btn_exit(self, value):
        self._exit = Button(value)
    
    # button_a = Button(12)
    # button_b = Button(13)
    # button_x = Button(14)
    # button_y = Button(15)

    def __init__(self, display, items = [], font_size = 3, hscroll_timeout = 50, btn_prev = 14, btn_next = 15, btn_sel = 12, btn_exit = 13, color_bg = [0, 0, 0], color_fg = [255, 0, 0], color_hl = [0, 255, 0]):
        # Set up attributes
        self.display = display
        self.font_size = font_size
        # The time between hoizontal scroll stop and restart
        self.hscroll_timeout = hscroll_timeout
        self.vscroll_offset = 0

        self.active_scrolling = False
        self.scroll_text = ""
        self.scroll_countdown = 0

        self.color_bg = color_bg
        self.color_fg = color_fg
        self.color_hl = color_hl

        self.items = items

        self.btn_exit = btn_exit
        self.btn_next = btn_next
        self.btn_prev = btn_prev
        self.btn_sel = btn_sel

        # The vertical space between lines (from the top of one character to the top of the character below it)
        self.line_space = 10 * font_size
        X, Y = display.get_bounds()
        self.X = X - 1
        self.Y = Y - 1
        # The horizontal pixel column at which text rendering starts
        self.line_start = 0
        self.selected_index = 0
    
    def clear(self, update = True):
        self.display.set_pen(self.bg)
        self.display.clear()

        if update:
            self.display.update()
        
        self.display.set_pen(self.fg)
    
    def draw_list(self):
        # We want to have the view scroll when the cursor gets halfway down the screen
        if 30 * (self.selected_index + 1) > Y // 2:
            # We achieve the scroll effect by applying a negative offset to the Y index
            vscroll_offset = (Y // 2) - (self.line_space * self.selected_index) - 7
            # 7 here is a magic number which corresponds to the space between the bottom of a character and the top of the next
            # It's required to stop the view from jumping when the offset is applied
            # Unfortunately it cannot be calculated, and must be derived from experimentation
            # (because the display library cannot give us a veritcal measurement of a character)
        else:
            vscroll_offset = 0
        
        self.clear(False)
        self.display.set_pen(self.fg)
        for index in range(0, len(self.items)):
            if index == self.selected_index:
                self.display.set_pen(self.hl)
                text_length = self.display.measure_text(self.items[index], self.font_size)
                self.display.rectangle(self.line_start, self.line_space * index + vscroll_offset, text_length, self.line_space)
                self.display.set_pen(self.fg)

                if text_length > self.X - self.line_start:
                    self.active_scrolling = True
                    self.scroll_text = self.items[index]
                    self.scroll_countdown = self.hscroll_timeout
                else:
                    self.active_scrolling = False
            self.display.text(self.items[index], self.line_start, self.line_space * index + vscroll_offset, 10 * self.Y, 3)
        self.display.update()
    
    def do_text_scroll(self):
        if self.scroll_countdown > 0:
            self.scroll_countdown -= 1
        else:
            self.display.set_pen(self.hl)
            text_length = self.display.measure_text(self.scroll_text, self.font_size)
            self.display.rectangle(self.line_start, self.line_space * self.selected_index + self.vscroll_offset, self.X, self.line_space)
            self.display.set_pen(self.fg)
            self.display.text(self.scroll_text, self.line_start, self.line_space * self.selected_index + self.vscroll_offset, 10 * self.Y, self.font_size)

            if text_length > self.X - self.line_start:
                self.scroll_text = self.scroll_text[1:]
                self.scroll_countdown = self.hscroll_timeout
            else:
                self.scroll_text = self.items[self.selected_index]
                self.scroll_countdown = 3 * self.hscroll_timeout
            
            self.display.update()
    
    def get_selection(self):
        self.draw_list()

        while True:
            if self.btn_next:
                if self.selected_index > 0:
                    self.selected_index -= 1
                    self.draw_list()
            elif self.btn_prev:
                if self.selected_index < len(self.items) - 1:
                    self.selected_index += 1
                    self.draw_list()
            elif self.btn_sel:
                return self.selected_index, self.items[self.selected_index]
            elif self.active_scrolling:
                self.do_text_scroll()
            time.sleep(0.01)

    def __setitem__(self, key, value):
        setattr(self, key, value)
    
    def __getitem__(self, key):
        getattr(self, key)
    
    def __len__(self):
        return len(self.items)