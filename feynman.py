import tkinter as tk
import time

WIDTH = 2000
HEIGHT = 1500

LEFT_X = 100

WAIT_TIME = 1

INIT_VEL = .01


R2_MASS = 100**3

class MovingRectangle:
    def __init__(self, canvas, x1, y1, x2, y2, color, mass, velocity):
        self.canvas = canvas
        self.rectangle = canvas.create_rectangle(x1, y1, x2, y2, fill=color)
        self.text = canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text="", fill="white")

        self.mass = mass
        self.velocity = velocity
        self.collision_processed = False  # Flag to track if collision has been processed
        self.num_collisions = 0
        
        self.update_velocity_text()

    def move(self):
        self.canvas.move(self.rectangle, self.velocity, 0)
        self.canvas.move(self.text, self.velocity, 0)

    def update_velocity_text(self):
        self.canvas.itemconfig(self.text, text=f"{self.mass} kg\n{round(self.velocity, 8)}")

def move_rectangles(rect1, rect2):
    rect1.move()
    rect2.move()

    rect1.update_velocity_text()
    rect2.update_velocity_text()

    rect1.collision_processed = False  # Reset the flag at the beginning of each frame
    rect2.collision_processed = False

    
    x1_rect1, _, x2_rect1, _ = rect1.canvas.coords(rect1.rectangle)
    x1_rect2, _, _, _ = rect2.canvas.coords(rect2.rectangle)
    if not rect1.collision_processed and not rect2.collision_processed and check_rects_collision(rect1, rect2):
        rect_collision(rect1, rect2)
        rect1.num_collisions += 1
        rect2.num_collisions += 1
        print("Rect Collision #", rect1.num_collisions)

    if check_wall_collision(rect1):
        rect1.velocity *= -1
        rect1.canvas.move(rect1.rectangle, LEFT_X - x1_rect1, 0)
        rect1.canvas.move(rect1.text, LEFT_X - x1_rect1, 0)
        rect1.collision_processed = True
        rect1.num_collisions += 1
        print("Wall Collision #", rect1.num_collisions)

    if check_wall_collision(rect2):
        rect2.velocity *= -1
        rect2.collision_processed = True
        rect2.num_collisions += 1
        update_canvas(True)
        print("! Wall 2 Collision #", rect1.num_collisions)


    update_canvas()
    global WAIT_TIME

    

    root.after(WAIT_TIME, move_rectangles, rect1, rect2)

def rect_collision(rect1, rect2):
    if rect1.collision_processed or rect2.collision_processed:
        return

    m1, v1 = rect1.mass, rect1.velocity
    m2, v2 = rect2.mass, rect2.velocity

    new_rect1_vel = ((m1 - m2) * v1 + 2 * m2 * v2) / (m1 + m2)
    new_rect2_vel = ((m2 - m1) * v2 + 2 * m1 * v1) / (m1 + m2)

    rect1.velocity = new_rect1_vel
    rect2.velocity = new_rect2_vel

    rect1.collision_processed = True
    rect2.collision_processed = True

def check_rects_collision(rect1, rect2):
    x1_rect1, y1_rect1, x2_rect1, y2_rect1 = rect1.canvas.coords(rect1.rectangle)
    x1_rect2, y1_rect2, x2_rect2, y2_rect2 = rect2.canvas.coords(rect2.rectangle)

    # Check for collision in the x-axis
    if x1_rect1 <= x2_rect2 and x2_rect1 >= x1_rect2:
        return True
    return False

def check_wall_collision(rect):
    x1, _, x2, _ = rect.canvas.coords(rect.rectangle)
    if x1 <= LEFT_X:
        return True
    return False

def update_canvas(crossed = False):
    # Check if the label already exists, update its text
    if hasattr(update_canvas, "label"):
        update_canvas.label.config(text=f"Collisions: {rect1.num_collisions}")
    else:
        # Create the label if it doesn't exist
        update_canvas.label = tk.Label(root, text=f"Collisions: {rect1.num_collisions}", font=("Helvetica", 14))
        update_canvas.label.place(relx=1, anchor='ne', x=-20, y=10)

    if rect1.velocity > 0 and rect2.velocity > 0 and rect2.velocity > rect1.velocity:
        update_canvas.label2 = tk.Label(root, text=f"Done", font=("Helvetica", 14))
        update_canvas.label2.place(relx=1, anchor='ne', x=-20, y=50)
    
    if crossed:
        update_canvas.label2 = tk.Label(root, text=f"Invalid", font=("Helvetica", 14))
        update_canvas.label2.place(relx=1, anchor='ne', x=-20, y=50)

    # Calculate the maximum x-coordinate of all rectangles
    max_x = max(canvas.bbox(rect1.rectangle)[2], canvas.bbox(rect2.rectangle)[2])

    # Check if the maximum x-coordinate exceeds the canvas width
    if max_x > WIDTH:
        # Calculate the required scale factor to fit the rectangles within the canvas
        scale_factor = WIDTH / max_x
        canvas.scale("all", 0, 0, scale_factor, 1)




root = tk.Tk()
root.title("Moving Rectangles and Wall Example")

canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="white")
canvas.pack()

bottom_y = HEIGHT - 200

rect1 = MovingRectangle(canvas, WIDTH - 300, bottom_y - 10 - 100, WIDTH - 300 + 100, bottom_y - 10, "blue", 1, 0)
rect2 = MovingRectangle(canvas, WIDTH - 300 + 200, bottom_y - 10 - 100, WIDTH - 300 + 200 + 100, bottom_y - 10, "red", R2_MASS, -INIT_VEL)


move_rectangles(rect1, rect2)

wall_left = canvas.create_line(LEFT_X, bottom_y, LEFT_X, 100, width=2, fill="black")
wall_bottom = canvas.create_line(LEFT_X, bottom_y, WIDTH * 100, bottom_y, width=2, fill="black")

# Add ticks and labels to the line for spacing
tick_spacing = 50
for x in range(0, WIDTH * 100, tick_spacing):
    canvas.create_line(x, bottom_y - 5, x, bottom_y + 5, width=1, fill="black")
    canvas.create_text(x, bottom_y + 15, text=str(x), anchor='n', font=("Helvetica", 8))


root.mainloop()
