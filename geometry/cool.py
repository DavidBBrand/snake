import turtle
import colorsys

NUM_ITERATIONS = 500
SIZE = 1000

screen = turtle.Screen()
screen.setup(width=600, height=600)
screen.bgcolor("black")
screen.tracer(0)

t = turtle.Turtle()
t.speed(0)
t.hideturtle()


def draw(angle_turn):
    t.clear()
    t.penup()
    t.goto(0, 0)
    t.setheading(0)
    t.pendown()
    for i in range(NUM_ITERATIONS):
        t.pencolor(colorsys.hsv_to_rgb(i / NUM_ITERATIONS, 0.8, 0.9))
        t.forward((i * SIZE) / NUM_ITERATIONS + 10)
        t.left(angle_turn)
    screen.update()
    screen.title(f"Hypnotic Colorful Spiral — angle: {angle_turn}")


current_angle = 72.0
draw(current_angle)

while True:
    try:
        raw = input("Enter new angle (0.1 – 359.9), or q to quit: ").strip()
        if raw.lower() == "q":
            break
        angle = float(raw)
        if 0.1 <= angle <= 359.9:
            current_angle = angle
            draw(current_angle)
        else:
            print("Please enter a value between 0.1 and 359.9")
    except ValueError:
        print("Invalid input — enter a number like 72 or 137.5")

screen.bye()
