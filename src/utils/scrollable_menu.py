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
    def color_hl_fg(self):
        return self.hl_fg
    
    @color_hl_fg.setter
    def color_hl_fg(self, values):
        self.hl_fg = self.display.create_pen(*values)

    @property
    def color_scrollbar(self):
        return self.scroll_fg
    
    @color_scrollbar.setter
    def color_scrollbar(self, values):
        self.scroll_fg = self.display.create_pen(*values)

    @property
    def color_scrollbar_bg(self):
        return self.scroll_bg
    
    @color_scrollbar_bg.setter
    def color_scrollbar_bg(self, values):
        self.scroll_bg = self.display.create_pen(*values)
    
    @property
    def btn_prev(self):
        return self._prev.read()
    
    @btn_prev.setter
    def btn_prev(self, value):
        self._prev = Button(value)
    
    @property
    def btn_next(self):
        return self._next.read()
    
    @btn_next.setter
    def btn_next(self, value):
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
    
    # The vertical space between lines
    @property
    def line_space(self):
        # The font is 7 * font_size pixels high
        return self.font_size * 7 + 2 * self.text_padding_around
    
    # button_a = Button(12)
    # button_b = Button(13)
    # button_x = Button(14)
    # button_y = Button(15)

    def __init__(self, display, items = [], btn_prev = 15, btn_next = 14, btn_sel = 12, btn_exit = 13, color_bg = [0, 0, 0], color_fg = [255, 0, 0], color_hl = [0, 255, 0], color_hl_fg = [0, 0, 0], color_scrollbar = [0, 0, 0], color_scrollbar_bg = [30, 30, 30], font_size = 3, hscroll_timeout = 50, scrollbar_width = 4):
        # Set up attributes
        self.display = display
        self.font_size = font_size
        # The time between hoizontal scroll stop and restart
        self.hscroll_timeout = hscroll_timeout
        self.vscroll_offset = 0
        self.scrollbar_width = scrollbar_width

        self.active_scrolling = False
        self.scroll_text = ""
        self.scroll_countdown = 0

        self.color_bg = color_bg
        self.color_fg = color_fg
        self.color_hl = color_hl
        self.color_hl_fg = color_hl_fg
        self.color_scrollbar = color_scrollbar
        self.color_scrollbar_bg = color_scrollbar_bg

        self.items = items

        self.btn_exit = btn_exit
        self.btn_next = btn_next
        self.btn_prev = btn_prev
        self.btn_sel = btn_sel

        X, Y = display.get_bounds()
        self.X = X - 1
        self.Y = Y - 1
        # The horizontal pixel column at which text rendering starts
        self.line_start = scrollbar_width + 2
        self.text_padding_around = 4
        self.selected_index = 0
    
    def clear(self, update = True):
        self.display.set_pen(self.bg)
        self.display.clear()

        if update:
            self.display.update()
        
        self.display.set_pen(self.fg)
    
    def draw_list(self):
        # We want to have the view scroll when the cursor gets halfway down the screen
        if 30 * (self.selected_index + 1) > self.Y // 2:
            # We achieve the scroll effect by applying a negative offset to the Y index
            self.vscroll_offset = (self.Y // 2) - (self.line_space * self.selected_index)
        else:
            self.vscroll_offset = 0
        
        self.clear(False)

        # Only draw the scrollbar if it's needed
        self._line_start = self.line_start
        if self.scrollbar_width > 0 and len(self.items) * self.line_space > self.Y:
            scrollbar_height = self.Y // len(self.items)
            self.display.set_pen(self.color_scrollbar_bg)
            self.display.rectangle(0, 0, self.line_start, self.Y)
            self.display.set_pen(self.color_scrollbar)
            self.display.rectangle(0, self.selected_index * scrollbar_height, self.scrollbar_width, scrollbar_height)
        elif self.scrollbar_width > 0:
            self._line_start = 2

        self.display.set_pen(self.fg)
        for index in range(0, len(self.items)):
            if index == self.selected_index:
                self.display.set_pen(self.hl)
                text_length = self.text_padding_around + self.display.measure_text(self.items[index], self.font_size)
                self.display.rectangle(self._line_start, self.line_space * index + self.vscroll_offset, text_length, self.line_space)
                self.display.set_pen(self.hl_fg)

                if text_length > self.X - self._line_start:
                    self.active_scrolling = True
                    self.scroll_text = self.items[index]
                    self.scroll_countdown = self.hscroll_timeout
                else:
                    self.active_scrolling = False
            else:
            	self.display.set_pen(self.fg)
            self.display.text(self.items[index], self.text_padding_around + self._line_start, self.text_padding_around + self.line_space * index + self.vscroll_offset, 10 * self.Y, 3)
        self.display.update()
    
    def do_text_scroll(self):
        if self.scroll_countdown > 0:
            self.scroll_countdown -= 1
        else:
            self.display.set_pen(self.hl)
            text_length = self.text_padding_around + self.display.measure_text(self.scroll_text, self.font_size)
            self.display.rectangle(self._line_start, self.line_space * self.selected_index + self.vscroll_offset, text_length, self.line_space)
            self.display.set_pen(self.hl_fg)
            self.display.text(self.scroll_text, self.text_padding_around + self._line_start, self.text_padding_around + self.line_space * self.selected_index + self.vscroll_offset, 10 * self.Y, self.font_size)

            if text_length > self.X - self._line_start:
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
                return self.selected_index
            elif self.btn_exit:
                return False
            elif self.active_scrolling:
                self.do_text_scroll()
            time.sleep(0.01)

    def __setitem__(self, key, value):
        setattr(self, key, value)
    
    def __getitem__(self, key):
        getattr(self, key)
    
    def __len__(self):
        return len(self.items)
