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

class Ball:

    @property
    def center(self):
        return self.x, self.y

    @center.setter
    def center(self, value):
        self.x, self.y = value
    
    @property
    def size(self):
        return self.radius
    
    @size.setter
    def size(self, value):
        self.radius = value

    def __init__(self, center_x = 0, center_y = 0, radius = 5, speed = 1, start_angle = 45):
        self.speed: int = speed
        self.speed_x: int = speed
        self.speed_y: int = speed
        self.angle: int = start_angle
        self.radius: int = radius
        self.x: int = center_x
        self.y: int = center_y
    
    def __getitem__(self, key: str):
        if hasattr(self, key):
            return getattr(self, key)
        else:
            raise KeyError(f"The key {key} is not valid for type <Ball>")
    
    def __setitem__(self, key: str, value): # : Union[int, Tuple[int, int]]
        if hasattr(self, key):
            setattr(self, key, value)
        else:
            raise KeyError(f"The key {key} is not valid for type <Ball>")


class Board:
    def __init__(self, ball = None):
        # Store the center of the screen for ball placement
        self.center_x = X // 2
        self.center_y = Y // 2

        self.ball = ball or Ball(self.center_x, self.center_y)
        self.score_width = 70
        self.score_size = 2
        self.level = 1

        # start with a paddle size of 37% screen height
        self.bar_h = int(Y * 0.37)

        # The speed at which paddles move
        self.move_delta = 4

        # Allow player and ball movement
        self.active = False

        # Calculate start position of player paddles
        self.p1 = self.center_y - self.bar_h // 2
        self.p2 = self.center_y - self.bar_h // 2

        self.score1 = 0
        self.score2 = 0
        
        self.reset()
        
    def draw_box(self):
        display.line(0, 0, X, 0)
        display.line(0, Y, X, Y)
        display.line(0, 0, 0, Y)
        display.line(X, 0, X, Y)
    
    def draw_ball(self):
        x, y = self.ball.center
        size = self.ball.size

        def edge_detect():
            if x + size > X or x - size < 0:
                if self.ball.speed_x < 1:
                    self.next_round(False)
                else:
                    self.next_round(True)
            if y + size > Y or y - size < 0:
                self.ball.speed_y *= -1
                return True
            
            return False
        
        def player_detect():
            if self.ball.speed_x < 0:
                if x - size < 8 and y >= self.p1 and y < (self.p1 + self.bar_h):
                    self.ball.speed_x *= -1
            elif self.ball.speed_x > 0:
                if x + size > X - 8 and y >= self.p2 and y < (self.p2 + self.bar_h):
                    self.ball.speed_x *= -1

        if self.active:
            x += self.ball.speed_x
            y += self.ball.speed_y

            self.ball.center = x, y

            if not edge_detect():
                player_detect()

        display.circle(self.ball["x"], self.ball["y"], self.ball.size)
    
    def draw_players(self):
        display.rectangle(4, self.p1, 4, self.bar_h)
        display.rectangle(X - 8, self.p2, 4, self.bar_h)

    def draw_scoreboard(self):
        score_center = self.score_width // 2
        display.set_pen(WHITE)

        # Text measurement for score alignment
        divider_width = display.measure_text("|", self.score_size)
        # p1_width = display.measure_text(f"{self.score1}-", self.score_size)
        p2_width = display.measure_text(f"{self.score2}", self.score_size)

        divider_start = self.center_x
        p1_start = self.center_x - score_center + divider_width
        p2_start = self.center_x + score_center - p2_width

        # debug line used for scoreboard testing
        # display.line(self.center_x - score_center, 3, self.center_x + score_center, 3)

        display.text("|", divider_start, 7, 1, self.score_size)
        display.text(str(self.score1), p1_start, 7, 1, self.score_size)
        display.text(str(self.score2), p2_start, 7, 1, self.score_size)
    
    def inc_p1(self):
        # Move P1 (left) paddle up
        if(self.p1 > self.move_delta):
            self.p1 -= self.move_delta
        else:
            self.p1 = self.move_delta
    
    def dec_p1(self):
        # Move P1 (left) paddle down
        if(self.p1 < (Y - self.bar_h - self.move_delta)):
            self.p1 += self.move_delta
        else:
            self.p1 = Y - self.bar_h - self.move_delta

    def inc_p2(self):
        # Move P2 (right) paddle up
        if(self.p2 > self.move_delta):
            self.p2 -= self.move_delta
        else:
            self.p2 = self.move_delta
    
    def dec_p2(self):
        # Move P2 (right) paddle down
        if(self.p2 < (Y - self.bar_h - self.move_delta)):
            self.p2 += self.move_delta
        else:
            self.p2 = Y - self.bar_h - self.move_delta
    
    def next_round(self, p1_score):
        if p1_score:
            self.score1 += 1
        else:
            self.score2 += 1
        
        self.ball.center = self.center_x, self.center_y

        self.ball.speed_x = self.ball.speed if random.randint(0, 1) else -1 * self.ball.speed
        self.ball.speed_y = self.ball.speed if random.randint(0, 1) else -1 * self.ball.speed

        self.p1 = self.center_y - self.bar_h // 2
        self.p2 = self.center_y - self.bar_h // 2
    
    def start_game(self):
        self.active = True

        start_text_size = display.measure_text("PLAY BALL!", 3)
        text_start = self.center_x - start_text_size // 2

        self.update()
        display.text("PLAY BALL", text_start, Y - 30, 240, 3)
        display.update()

        time.sleep(1)

    # update the screen
    def update(self):
        # clear the screen
        display.set_pen(BLACK)
        display.clear()

        # redraw elements
        self.draw_scoreboard()
        display.set_pen(WHITE)
        self.draw_box()
        self.draw_players()
        self.draw_ball()
        display.update()
    
    def reset(self):
        self.active = False
        self.ball = Ball(self.center_x, self.center_y)
        self.update()
        text_size = display.measure_text("Use X to begin", 3)
        text_start = self.center_x - text_size // 2
        display.set_pen(GREEN)
        display.text("Use X to begin", text_start, Y - 60, 240, 3)
        display.text("Use B for help", text_start, Y - 30, 240, 3)
        display.update()
    
    def pause(self):
        text_size = display.measure_text("Use A to resume", 3)
        text_start = self.center_x - text_size // 2
        display.set_pen(GREEN)
        display.text("Use A to resume", text_start, Y - 60, 240, 3)
        display.text("Use B to exit", text_start, Y - 30, 240, 3)
        display.update()

        while True:
            if button_a.read():
                return False
            elif button_b.read():
                return True
            time.sleep(0.01)

# display.pixel_span(x, y, length)

# display.line(x1, y1, dx, dy)

# display.text(message, x, y, width, size)

def show_help():
    global board
    display.set_pen(BLACK)
    display.clear()
    display.set_pen(WHITE)

    title_size = display.measure_text("PONG", 3)
    display.text("PONG", board.center_x - title_size // 2, 0, X, 3)
    display.text("Use A & B to move l-paddle", 0, 40, X, 2)
    display.text("Use X & Y to move r-paddle", 0, 60, X, 2)
    display.text("Use X + Y to pause", 0, 80, X, 2)
    display.text("Use B to return to game", 0, Y - 20, X, 2)

    display.update()

    while not button_b.read():
        time.sleep(0.01)

def loop():
    global board
    board = Board()

    global button_a, button_b, button_x, button_y

    while True:
        if board.active:
            if button_x.read():
                if button_y.read():
                    if board.pause():
                        # Player has exited game
                        break
                board.inc_p2()
            elif button_y.read():
                board.dec_p2()

            if button_a.read():
                board.inc_p1()
            elif button_b.read():
                board.dec_p1()
            
            board.update()
        elif button_x.read():
            board.start_game()
            button_a = Button(12, repeat_time = 1)
            button_b = Button(13, repeat_time = 1)
            button_x = Button(14, repeat_time = 1)
            button_y = Button(15, repeat_time = 1)
        elif button_b.read():
            show_help()
            board.reset()

        time.sleep(0.01)
