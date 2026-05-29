import turtle
import colorsys
import time

# --- Configuration ---
# Number of iterations determines the complexity/density of the spiral
NUM_ITERATIONS = 760
# Size multiplier for the initial shape side length
SIZE = 800
# Angle to turn after drawing each simple shape
ANGLE_TURN = 113  # Using a non-divisor of 360 creates a much more complex pattern

# --- Setup ---
# Initialize the screen and set a nice dark background
screen = turtle.Screen()
screen.setup(width=600, height=600)
screen.bgcolor("black")
screen.title("Hypnotic Colorful Spiral")
turtle.speed(0)  # Set speed to fastest (0)
turtle.hideturtle() # Make the turtle invisible

# Set the turtle position to the center (starting point)
turtle.penup()
turtle.goto(0, 0)
turtle.pendown()

# Set up the colorsys module for HSL to RGB conversion
# H (Hue) is between 0 and 1, used to cycle through colors
hue = 0.0

print(f"Starting to draw a complex spiral with {NUM_ITERATIONS} steps...")

# --- Drawing Loop ---
for i in range(NUM_ITERATIONS):
    # 1. Calculate the color (HSV to RGB)
    # The hue cycles from 0.0 (red) to 1.0 (back to red)
    hue = i / NUM_ITERATIONS
    # Get the R, G, B components (each 0-1)
    rgb_color = colorsys.hsv_to_rgb(hue, 0.2, 0.7) # S=0.8 (saturation), V=1.0 (value/brightness)

    # 2. Set the pen color
    # The turtle library uses RGB tuples (0-255), so we multiply by 255
    turtle.pencolor(rgb_color)

    # 3. Draw the simple geometric shape (a line segment in this case)
    # The length of the line increases with 'i' to create the spiral effect
    line_length = (i * SIZE) / NUM_ITERATIONS + 10

    turtle.forward(line_length)

    # 4. Turn to prepare for the next line segment
    turtle.left(ANGLE_TURN)

    # Optional: Speed up the drawing process if NUM_ITERATIONS is very high
    # if i % 50 == 0 and i > 0:
    #     screen.update()

print("Drawing complete.")

# --- Conclusion ---
# Prevent the window from closing immediately
turtle.done()