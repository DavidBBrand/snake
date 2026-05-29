
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
    "#FF5C00", "#FF3131", "#1F51FF", "#40F994", "#797814",
    "#878BA7", "#92B7A4", "#5ABCB8", "#56DAAB", "#C0F7C4",
    "#A0E3A2", "#F77019", "#2AF850", "#5BDF90", "#674C19",
    "#B9D2B7", "#38B647", "#F31563", "#7F4DB5",
]

# ── Screen ───────────────────────────────────────────────────────────────────
wn = turtle.Screen()
wn.title("Snake Game by @David")
wn.bgcolor("blue")
wn.bgpic("background.gif")
wn.setup(width=600, height=600)
wn.tracer(0)
wn.register_shape("hamburger.gif")

# ── State ────────────────────────────────────────────────────────────────────
score      = 0
high_score = 0
delay      = BASE_DELAY
paused     = False
segments   = []

# ── Snake head ───────────────────────────────────────────────────────────────
head = turtle.Turtle()
head.speed(0)
head.shape("square")
head.color("lime green")
head.penup()
head.goto(0, 0)
head.direction = "stop"

# ── Food ─────────────────────────────────────────────────────────────────────
food = turtle.Turtle()
food.speed(0)
food.shape("hamburger.gif")
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
          font=("Courier", 14, "bold"))

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
              align="center", font=("Courier", 14, "bold"))


def reset_game():
    global score, delay
    time.sleep(0.8)
    head.goto(0, 0)
    head.direction = "stop"
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

def go_down():
    if head.direction != "up":
        head.direction = "down"

def go_left():
    if head.direction != "right":
        head.direction = "left"

def go_right():
    if head.direction != "left":
        head.direction = "right"

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
