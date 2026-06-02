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
t.pensize(1)


def clear():
    t.clearstamps()
    t.clear()
    t.penup()
    t.goto(0, 0)
    t.setheading(0)
    t.pensize(1)
    screen.update()


# ══════════════════════════════════════════════════════════════════════════════
# SPIROGRAPHS  (hypotrochoids & epitrochoids)
# ══════════════════════════════════════════════════════════════════════════════

def spirograph(R=150, r=53, d=120, steps=2000):
    """
    Hypotrochoid: inner circle of radius r rolls inside outer circle R.
    d = distance from center of inner circle to drawing point.
    """
    clear()
    t.penup()
    x0 = (R - r) * math.cos(0) + d * math.cos(0)
    y0 = (R - r) * math.sin(0) - d * math.sin(0)
    t.goto(x0, y0)
    t.pendown()
    for i in range(steps):
        angle = 2 * math.pi * i / steps
        x = (R - r) * math.cos(angle) + d * math.cos((R - r) / r * angle)
        y = (R - r) * math.sin(angle) - d * math.sin((R - r) / r * angle)
        t.pencolor(colorsys.hsv_to_rgb(i / steps, 0.9, 1.0))
        t.goto(x, y)
    t.penup()
    screen.update()
    screen.title(f"Spirograph  R={R} r={r} d={d}")


def epitrochoid(R=100, r=40, d=80, steps=3000):
    """
    Epitrochoid: small circle rolls around the OUTSIDE of large circle.
    """
    clear()
    t.penup()
    t.goto((R + r) + d, 0)
    t.pendown()
    for i in range(steps):
        angle = 2 * math.pi * i / steps
        x = (R + r) * math.cos(angle) - d * math.cos((R + r) / r * angle)
        y = (R + r) * math.sin(angle) - d * math.sin((R + r) / r * angle)
        t.pencolor(colorsys.hsv_to_rgb(i / steps, 0.9, 1.0))
        t.goto(x, y)
    t.penup()
    screen.update()
    screen.title(f"Epitrochoid  R={R} r={r} d={d}")


def random_spirograph():
    R = random.randint(100, 200)
    r = random.randint(20, R - 10)
    d = random.randint(20, 180)
    spirograph(R, r, d, steps=5000)


# ══════════════════════════════════════════════════════════════════════════════
# LISSAJOUS FIGURES
# ══════════════════════════════════════════════════════════════════════════════

def lissajous(a=3, b=4, delta=math.pi/4, steps=2000, size=280):
    """
    Classic Lissajous curve: x = sin(at + delta), y = sin(bt)
    """
    clear()
    t.penup()
    t.goto(size * math.sin(delta), 0)
    t.pendown()
    for i in range(steps + 1):
        angle = 2 * math.pi * i / steps
        x = size * math.sin(a * angle + delta)
        y = size * math.sin(b * angle)
        t.pencolor(colorsys.hsv_to_rgb(i / steps, 0.9, 1.0))
        t.goto(x, y)
    t.penup()
    screen.update()
    screen.title(f"Lissajous  a={a} b={b} δ={round(delta, 2)}")


def lissajous_sweep(a=3, b=4, steps=1500, size=250):
    """Draws multiple Lissajous curves sweeping through delta values."""
    clear()
    for phase_i in range(12):
        delta = phase_i * math.pi / 12
        hue_base = phase_i / 12
        t.penup()
        t.goto(size * math.sin(delta), 0)
        t.pendown()
        for i in range(steps + 1):
            angle = 2 * math.pi * i / steps
            x = size * math.sin(a * angle + delta)
            y = size * math.sin(b * angle)
            t.pencolor(colorsys.hsv_to_rgb((hue_base + i / steps * 0.08) % 1.0, 0.85, 1.0))
            t.goto(x, y)
        t.penup()
    screen.update()
    screen.title(f"Lissajous Sweep  a={a} b={b}")


# ══════════════════════════════════════════════════════════════════════════════
# CELLULAR AUTOMATA  (1D rules projected onto 2D canvas)
# ══════════════════════════════════════════════════════════════════════════════

def cellular_automata(rule_num=90, rows=160, cols=321):
    """
    1D elementary cellular automaton.
    Each row is drawn top-to-bottom. Rule 90 = Sierpinski, Rule 110 = complex.
    """
    clear()
    rule = [(rule_num >> i) & 1 for i in range(8)]
    cell_size = min(680 // cols, 680 // rows)

    # start with single cell in center
    cells = [0] * cols
    cells[cols // 2] = 1

    start_x = -(cols * cell_size) // 2
    start_y =  (rows * cell_size) // 2

    t.shape("square")
    t.shapesize(cell_size / 20, cell_size / 20)

    for row in range(rows):
        hue = row / rows
        t.fillcolor(colorsys.hsv_to_rgb(hue, 0.85, 1.0))
        t.pencolor(colorsys.hsv_to_rgb(hue, 0.85, 1.0))
        for col in range(cols):
            if cells[col]:
                t.penup()
                t.goto(start_x + col * cell_size, start_y - row * cell_size)
                t.stamp()
        # next generation
        new_cells = [0] * cols
        for col in range(cols):
            left   = cells[(col - 1) % cols]
            center = cells[col]
            right  = cells[(col + 1) % cols]
            idx = (left << 2) | (center << 1) | right
            new_cells[col] = rule[idx]
        cells = new_cells

    t.hideturtle()
    t.shape("classic")
    screen.update()
    screen.title(f"Cellular Automaton  Rule {rule_num}")


# ══════════════════════════════════════════════════════════════════════════════
# SYMMETRY / MANDALA
# ══════════════════════════════════════════════════════════════════════════════

def mandala(folds=10, petals=6, size=270, steps=400):
    """
    Draws a symmetric mandala using rotational symmetry.
    Each petal is a Lissajous-like curve, rotated around the center.
    """
    clear()
    for fold in range(folds):
        angle_offset = 2 * math.pi * fold / folds
        hue = fold / folds
        t.pencolor(colorsys.hsv_to_rgb(hue, 0.9, 1.0))
        t.penup()
        for i in range(steps + 1):
            theta = 2 * math.pi * i / steps
            r = size * abs(math.sin(petals * theta / 2))
            x = r * math.cos(theta + angle_offset)
            y = r * math.sin(theta + angle_offset)
            if i == 0:
                t.goto(x, y)
                t.pendown()
            else:
                t.pencolor(colorsys.hsv_to_rgb((hue + i / steps * 0.1) % 1.0, 0.9, 1.0))
                t.goto(x, y)
        t.penup()
    screen.update()
    screen.title(f"Mandala  folds={folds} petals={petals}")


def rose_curve(n=7, d=4, size=280, steps=3000):
    """
    Rose curve: r = cos(n/d * theta). When n/d is irrational-ish, very dense.
    """
    clear()
    t.penup()
    t.goto(size, 0)
    t.pendown()
    total = steps * d
    for i in range(total + 1):
        theta = 2 * math.pi * i / steps
        r = size * math.cos((n / d) * theta)
        x = r * math.cos(theta)
        y = r * math.sin(theta)
        t.pencolor(colorsys.hsv_to_rgb(i / total, 0.9, 1.0))
        t.goto(x, y)
    t.penup()
    screen.update()
    screen.title(f"Rose Curve  n={n} d={d}")


# ══════════════════════════════════════════════════════════════════════════════
# MENU
# ══════════════════════════════════════════════════════════════════════════════

MENU = """
╔════════════════════════════════════╗
║       GEOMETRY EXPLORER  II        ║
╠════════════════════════════════════╣
║  SPIROGRAPHS                       ║
║   s  — hypotrochoid (custom)       ║
║   e  — epitrochoid (custom)        ║
║   r  — random spirograph           ║
║                                    ║
║  LISSAJOUS                         ║
║   l  — Lissajous figure            ║
║   w  — Lissajous sweep             ║
║                                    ║
║  CELLULAR AUTOMATA                 ║
║   c  — 1D rule (try 90, 110, 30)   ║
║                                    ║
║  SYMMETRY                          ║
║   m  — mandala                     ║
║   o  — rose curve                  ║
║                                    ║
║   q  — quit                        ║
╚════════════════════════════════════╝
"""

print(MENU)
mandala()  # draw something on launch

while True:
    try:
        cmd = input("Choose [s/e/r/l/w/c/m/o/q]: ").strip().lower()
    except (EOFError, KeyboardInterrupt):
        break

    if cmd == "q":
        break

    elif cmd == "s":
        try:
            R = int(input("  outer radius R (50-250, default 150): ") or 150)
            r = int(input("  inner radius r (10-R-1, default 53): ") or 53)
            d = int(input("  pen distance d (10-200, default 120): ") or 120)
            spirograph(R, r, d)
        except ValueError:
            print("  Invalid input.")

    elif cmd == "e":
        try:
            R = int(input("  base radius R (50-150, default 100): ") or 100)
            r = int(input("  rolling radius r (10-80, default 40): ") or 40)
            d = int(input("  pen distance d (10-150, default 80): ") or 80)
            epitrochoid(R, r, d)
        except ValueError:
            print("  Invalid input.")

    elif cmd == "r":
        random_spirograph()

    elif cmd == "l":
        try:
            a     = int(input("  frequency a (1-9, default 3): ") or 3)
            b     = int(input("  frequency b (1-9, default 4): ") or 4)
            delta = float(input("  phase delta (0-3.14, default 0.785): ") or 0.785)
            lissajous(a, b, delta)
        except ValueError:
            print("  Invalid input.")

    elif cmd == "w":
        try:
            a = int(input("  frequency a (1-9, default 3): ") or 3)
            b = int(input("  frequency b (1-9, default 4): ") or 4)
            lissajous_sweep(a, b)
        except ValueError:
            print("  Invalid input.")

    elif cmd == "c":
        try:
            rule = int(input("  rule number (0-255, default 90): ") or 90)
            if not 0 <= rule <= 255:
                print("  Must be 0-255.")
            else:
                cellular_automata(rule)
        except ValueError:
            print("  Invalid input.")

    elif cmd == "m":
        try:
            folds  = int(input("  folds (3-20, default 10): ") or 10)
            petals = int(input("  petals (2-12, default 6): ") or 6)
            mandala(folds, petals)
        except ValueError:
            print("  Invalid input.")

    elif cmd == "o":
        try:
            n = int(input("  numerator n (1-12, default 7): ") or 7)
            d = int(input("  denominator d (1-12, default 4): ") or 4)
            rose_curve(n, d)
        except ValueError:
            print("  Invalid input.")

    else:
        print("  Unknown command.")

screen.bye()
