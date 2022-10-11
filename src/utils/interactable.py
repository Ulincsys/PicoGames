from pimoroni import Button

class Interactible:
    def color_property(self, name, private_alias, help = ""):
        def get_color(self):
            return getattr(self, private_alias)
        
        def set_color(self, value):
            if isinstance(value, int):
                setattr(self, private_alias, value)
            else:
                setattr(self, private_alias, self.display.create_pen(*value))
        
        setattr(type(self), name, property(get_color, set_color, doc = help))
    
    def button_property(self, name, private_alias, help = ""):
        def get_button(self):
            return getattr(self, private_alias).read()

        def set_button(self, value):
            if isinstance(value, Button):
                setattr(self, private_alias, value)
            else:
                setattr(self, private_alias, Button(value))
        
        setattr(type(self), name, property(get_button, set_button, doc = help))