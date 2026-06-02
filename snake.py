
# Snake Game in Python 3
# By @David

import turtle
import time
import random

# ── Constants ────────────────────────────────────────────────────────────────
GRID       = 20          # px per cell
BORDER     = 290         # wall boundary
BASE_DELAY = 0.12        # starting frame delay (seconds)
MIN_DELAY  = 0.04        # fastest the game can get
SPEED_STEP = 0.003       # how much delay drops per food eaten

BODY_COLORS = [
    # greens (grass snakes, green tree pythons, rough green snakes)
    "#4A7C3F", "#5A8F3C", "#6B8E23", "#3B6E2A", "#7A9E4E",
    # browns & tans (garter snakes, rat snakes, king snakes)
    "#8B6914", "#A0785A", "#7B5B3A", "#C4A265", "#9E7B4A",
    # blacks & dark grays (black racers, indigo snakes)
    "#2C2C2C", "#3D3D3D", "#1A1A1A", "#4A4040", "#333333",
    # reds & oranges (corn snakes, milk snakes)
    "#B84A2A", "#C4622D", "#A03820", "#D4733A", "#8B3A1E",
    # yellows & olives (bull snakes, pine snakes)
    "#9E8B3A", "#B8A44A", "#7A6E28", "#C4A83A", "#8B7A30",
]

# ── Screen ───────────────────────────────────────────────────────────────────
wn = turtle.Screen()
wn.title("Snake Game by @David")
wn.bgcolor("#1A0505")
wn.bgpic("background.gif")
wn.setup(width=600, height=600)
wn.tracer(0)
FOOD_FRAMES = 12
for _i in range(FOOD_FRAMES):
    wn.register_shape(f"burger_{_i:02d}.gif")
wn.register_shape("head_right.gif")
wn.register_shape("head_left.gif")
wn.register_shape("head_up.gif")
wn.register_shape("head_down.gif")

# ── State ────────────────────────────────────────────────────────────────────
score      = 0
high_score = 0
delay      = BASE_DELAY
paused        = False
segments      = []
burger_frame  = 0

# ── Snake head ───────────────────────────────────────────────────────────────
head = turtle.Turtle()
head.speed(0)
head.shape("head_right.gif")
head.color("lime green")
head.penup()
head.goto(0, 0)
head.direction = "stop"

# ── Food ─────────────────────────────────────────────────────────────────────
food = turtle.Turtle()
food.speed(0)
food.shape("burger_00.gif")
food.penup()
food.goto(0, 100)

# ── Score display ─────────────────────────────────────────────────────────────
pen = turtle.Turtle()
pen.speed(0)
pen.shape("square")
pen.color("white")
pen.penup()
pen.hideturtle()
pen.goto(0, 265)
pen.write("Score: 0   High Score: 0", align="center",
          font=("Impact", 16, "normal"))

# ── Overlay pen (game-over / paused messages) ─────────────────────────────────
overlay = turtle.Turtle()
overlay.speed(0)
overlay.shape("square")
overlay.penup()
overlay.hideturtle()
overlay.color("white")


# ── Helpers ───────────────────────────────────────────────────────────────────
def update_score():
    pen.clear()
    pen.write(f"Score: {score}   High Score: {high_score}",
              align="center", font=("Impact", 16, "normal"))


def reset_game():
    global score, delay
    time.sleep(0.8)
    head.goto(0, 0)
    head.direction = "stop"
    head.shape("head_right.gif")
    for seg in segments:
        seg.goto(1000, 1000)
    segments.clear()
    score = 0
    delay = BASE_DELAY
    overlay.clear()
    update_score()


def show_message(msg):
    overlay.goto(0, 0)
    overlay.write(msg, align="center", font=("Courier", 20, "bold"))


# ── Movement ──────────────────────────────────────────────────────────────────
def go_up():
    if head.direction != "down":
        head.direction = "up"
        head.shape("head_up.gif")

def go_down():
    if head.direction != "up":
        head.direction = "down"
        head.shape("head_down.gif")

def go_left():
    if head.direction != "right":
        head.direction = "left"
        head.shape("head_left.gif")

def go_right():
    if head.direction != "left":
        head.direction = "right"
        head.shape("head_right.gif")

def toggle_pause():
    global paused
    paused = not paused
    if paused:
        show_message("PAUSED  —  press Space to resume")
    else:
        overlay.clear()

def move():
    if   head.direction == "up":    head.sety(head.ycor() + GRID)
    elif head.direction == "down":  head.sety(head.ycor() - GRID)
    elif head.direction == "left":  head.setx(head.xcor() - GRID)
    elif head.direction == "right": head.setx(head.xcor() + GRID)


# ── Key bindings ──────────────────────────────────────────────────────────────
wn.listen()
wn.onkeypress(go_up,       "w")
wn.onkeypress(go_down,     "s")
wn.onkeypress(go_left,     "a")
wn.onkeypress(go_right,    "d")
wn.onkeypress(go_up,       "Up")
wn.onkeypress(go_down,     "Down")
wn.onkeypress(go_left,     "Left")
wn.onkeypress(go_right,    "Right")
wn.onkeypress(toggle_pause,"space")


# ── Main game loop ────────────────────────────────────────────────────────────
while True:
    wn.update()

    # Spin the burger
    burger_frame = (burger_frame + 1) % FOOD_FRAMES
    food.shape(f"burger_{burger_frame:02d}.gif")

    if paused:
        time.sleep(0.05)
        continue

    # Wall collision
    if head.xcor() > BORDER or head.xcor() < -BORDER \
            or head.ycor() > BORDER or head.ycor() < -BORDER:
        show_message("GAME OVER")
        reset_game()
        continue

    # Food collision
    if head.distance(food) < GRID:
        # Relocate food (avoid placing on snake)
        while True:
            x = random.randint(-14, 14) * GRID
            y = random.randint(-14, 14) * GRID
            if all(seg.distance(x, y) >= GRID for seg in segments):
                break
        food.goto(x, y)

        # Grow snake
        seg = turtle.Turtle()
        seg.speed(0)
        seg.shape("square")
        seg.shapesize(0.6, 0.6)  # ~12×12 px — narrower than grid for snake look
        seg.color(random.choice(BODY_COLORS))
        seg.penup()
        segments.append(seg)

        # Speed up (capped)
        delay = max(MIN_DELAY, delay - SPEED_STEP)

        # Score
        score += 10
        if score > high_score:
            high_score = score
        update_score()

    # Shift body segments
    for i in range(len(segments) - 1, 0, -1):
        segments[i].goto(segments[i-1].xcor(), segments[i-1].ycor())
    if segments:
        segments[0].goto(head.xcor(), head.ycor())

    move()

    # Self-collision (skip first 2 segments — they overlap the head on turn)
    for seg in segments[2:]:
        if seg.distance(head) < GRID:
            show_message("GAME OVER")
            reset_game()
            break

    time.sleep(delay)

wn.mainloop()
