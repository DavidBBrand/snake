import turtle
import colorsys
import math
import random

# ── Screen setup ─────────────────────────────────────────────────────────────
screen = turtle.Screen()
screen.setup(width=700, height=700)
screen.bgcolor("black")
screen.tracer(0)

t = turtle.Turtle()
t.speed(0)
t.hideturtle()


def clear():
    t.clearstamps()
    t.clear()
    t.penup()
    t.goto(0, 0)
    t.setheading(0)
    screen.update()


# ══════════════════════════════════════════════════════════════════════════════
# HARMONOGRAPHS
# ══════════════════════════════════════════════════════════════════════════════

def harmonograph(f1=2, f2=3, p1=0, p2=0.5, d=0.0003, steps=6000):
    """Lissajous-style harmonograph with damping."""
    clear()
    # move to starting point without drawing
    t.penup()
    t.goto(280 * math.sin(p1), 280 * math.sin(p2))
    t.pendown()
    for i in range(steps):
        decay = math.e ** (-d * i)
        x = 280 * math.sin(f1 * i * 0.02 + p1) * decay
        y = 280 * math.sin(f2 * i * 0.02 + p2) * decay
        t.pencolor(colorsys.hsv_to_rgb(i / steps, 0.9, 1.0))
        t.goto(x, y)
    t.penup()
    screen.update()
    screen.title(f"Harmonograph  f1={f1} f2={f2} phase={round(p2,2)} decay={d}")


def random_harmonograph():
    f1 = random.choice([1, 2, 3, 4, 5])
    f2 = random.choice([1, 2, 3, 4, 5])
    p2 = random.uniform(0, math.pi)
    d  = random.uniform(0.0002, 0.002)
    harmonograph(f1, f2, p2=p2, d=d)


# ══════════════════════════════════════════════════════════════════════════════
# FRACTALS
# ══════════════════════════════════════════════════════════════════════════════

def koch_snowflake(order=4, size=700):
    """Koch snowflake fractal."""
    clear()
    t.penup()
    t.goto(-size / 2, size / 3)
    t.pendown()

    def koch_line(t, order, size):
        if order == 0:
            t.forward(size)
        else:
            for angle in [60, -120, 60, 0]:
                koch_line(t, order - 1, size / 3)
                t.left(angle)

    hues = [0.55, 0.6, 0.65]
    for side, hue in zip(range(3), hues):
        t.pencolor(colorsys.hsv_to_rgb(hue, 0.8, 1.0))
        koch_line(t, order, size)
        t.right(120)

    screen.update()
    screen.title(f"Koch Snowflake  order={order}")


def sierpinski(order=5, size=900):
    """Sierpinski triangle — recursive, filled triangles."""
    clear()
    total = [0]
    max_pts = 3 ** order

    def filled_triangle(ax, ay, bx, by, cx, cy, hue):
        t.penup()
        t.goto(ax, ay)
        t.fillcolor(colorsys.hsv_to_rgb(hue % 1.0, 0.85, 1.0))
        t.pencolor(colorsys.hsv_to_rgb(hue % 1.0, 0.85, 1.0))
        t.begin_fill()
        t.pendown()
        t.goto(bx, by)
        t.goto(cx, cy)
        t.goto(ax, ay)
        t.end_fill()
        t.penup()

    def draw(ax, ay, bx, by, cx, cy, depth):
        if depth == 0:
            hue = total[0] / max_pts
            filled_triangle(ax, ay, bx, by, cx, cy, hue)
            total[0] += 1
        else:
            mx_ab, my_ab = (ax+bx)/2, (ay+by)/2
            mx_bc, my_bc = (bx+cx)/2, (by+cy)/2
            mx_ca, my_ca = (cx+ax)/2, (cy+ay)/2
            draw(ax, ay, mx_ab, my_ab, mx_ca, my_ca, depth-1)
            draw(mx_ab, my_ab, bx, by, mx_bc, my_bc, depth-1)
            draw(mx_ca, my_ca, mx_bc, my_bc, cx, cy, depth-1)

    h = size * math.sqrt(3) / 2
    ax, ay =  0,          h * 2/3
    bx, by = -size/2,    -h / 3
    cx, cy =  size/2,    -h / 3
    draw(ax, ay, bx, by, cx, cy, order)
    screen.update()
    screen.title(f"Sierpinski Triangle  order={order}")


def dragon_curve(order=12):
    """Dragon curve fractal."""
    clear()

    def dragon(t, order, size, sign):
        if order == 0:
            t.pendown()
            t.forward(size)
        else:
            t.left(sign * 45)
            dragon(t, order - 1, size / math.sqrt(2), 1)
            t.right(sign * 90)
            dragon(t, order - 1, size / math.sqrt(2), -1)
            t.left(sign * 45)

    t.penup()
    t.goto(-50, 0)
    hue_counter = [0.0]

    # Colour by redefining forward
    original_forward = t.forward
    step_count = [0]

    def colored_forward(dist):
        t.pencolor(colorsys.hsv_to_rgb(step_count[0] / 4096, 0.9, 1.0))
        step_count[0] += 1
        original_forward(dist)

    t.forward = colored_forward
    dragon(t, order, 300, 1)
    t.forward = original_forward
    screen.update()
    screen.title(f"Dragon Curve  order={order}")


def recursive_tree(order=8, size=200, angle=25):
    """Recursive fractal tree."""
    clear()
    t.penup()
    t.goto(0, -280)
    t.setheading(90)

    def branch(length, depth):
        if depth == 0:
            return
        hue = 0.3 - (depth / order) * 0.25
        sat = 0.4 + (depth / order) * 0.5
        t.pencolor(colorsys.hsv_to_rgb(hue, sat, 0.9))
        t.pensize(max(1, depth * 0.8))
        t.pendown()
        t.forward(length)
        pos, heading = t.position(), t.heading()
        t.left(angle)
        branch(length * 0.7, depth - 1)
        t.penup()
        t.goto(pos)
        t.setheading(heading)
        t.right(angle)
        branch(length * 0.7, depth - 1)
        t.penup()
        t.goto(pos)
        t.setheading(heading)

    branch(size, order)
    t.pensize(1)
    screen.update()
    screen.title(f"Recursive Tree  depth={order} angle={angle}°")


# ══════════════════════════════════════════════════════════════════════════════
# MENU
# ══════════════════════════════════════════════════════════════════════════════

MENU = """
╔══════════════════════════════════╗
║       GEOMETRY EXPLORER          ║
╠══════════════════════════════════╣
║  HARMONOGRAPHS                   ║
║   h  — harmonograph (custom)     ║
║   r  — random harmonograph       ║
║                                  ║
║  FRACTALS                        ║
║   k  — Koch snowflake            ║
║   s  — Sierpinski triangle       ║
║   d  — dragon curve              ║
║   t  — recursive tree            ║
║                                  ║
║   q  — quit                      ║
╚══════════════════════════════════╝
"""

print(MENU)
recursive_tree()  # draw something on launch

while True:
    try:
        cmd = input("Choose [h/r/k/s/d/t/q]: ").strip().lower()
    except (EOFError, KeyboardInterrupt):
        break

    if cmd == "q":
        break

    elif cmd == "h":
        try:
            f1  = int(input("  frequency 1 (1-5, default 2): ") or 2)
            f2  = int(input("  frequency 2 (1-5, default 3): ") or 3)
            p2  = float(input("  phase offset (0-3.14, default 1.57): ") or 1.57)
            d   = float(input("  decay (0.0001-0.005, default 0.0005): ") or 0.0005)
            harmonograph(f1, f2, p2=p2, d=d)
        except ValueError:
            print("  Invalid input, try again.")

    elif cmd == "r":
        random_harmonograph()

    elif cmd == "k":
        try:
            order = int(input("  order (1-6, default 4): ") or 4)
            if order > 6:
                print("  Capping at 6 — higher orders cause a stack overflow.")
                order = 6
            koch_snowflake(order)
        except ValueError:
            print("  Invalid input.")

    elif cmd == "s":
        try:
            order = int(input("  order (1-9, default 5): ") or 5)
            if order > 9:
                print("  Capping at 9.")
                order = 9
            sierpinski(order)
        except ValueError:
            print("  Invalid input.")

    elif cmd == "d":
        try:
            order = int(input("  order (6-14, default 12): ") or 12)
            dragon_curve(order)
        except ValueError:
            print("  Invalid input.")

    elif cmd == "t":
        try:
            depth = int(input("  depth (4-10, default 8): ") or 8)
            angle = float(input("  branch angle (15-45, default 25): ") or 25)
            recursive_tree(depth, angle=angle)
        except ValueError:
            print("  Invalid input.")

    else:
        print("  Unknown command.")

screen.bye()
