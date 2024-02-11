import tkinter as tk

class MovingRectangleSimulation:
    def __init__(self, master, init_vel):
        self.master = master
        self.WIDTH = 2000
        self.HEIGHT = 1500
        self.LEFT_X = 100
        self.WAIT_TIME = 1
        self.init_vel = init_vel

        self.num_collisions = 0
        self.sq_len = 100

        self.init_simulation()

    def init_simulation(self):
        self.create_widgets()

    def create_widgets(self):
        self.canvas = tk.Canvas(self.master, width=self.WIDTH, height=self.HEIGHT, bg="white")
        self.canvas.pack()

        bottom_y = self.HEIGHT - 200

        rect1 = MovingRectangle(self.canvas, 1800, bottom_y - 10 - self.sq_len, 1800 + self.sq_len,
                                bottom_y - 10, "blue", 1, 0)
        rect2 = MovingRectangle(self.canvas, 1800 + 200, bottom_y - 10 - self.sq_len, 1800 + 200 + self.sq_len,
                                bottom_y - 10, "red", 100**3, -self.init_vel)

        wall_left = self.canvas.create_line(self.LEFT_X, bottom_y, self.LEFT_X, 100, width=2, fill="black")
        wall_bottom = self.canvas.create_line(self.LEFT_X, bottom_y, self.WIDTH * 100, bottom_y, width=2, fill="black")

        tick_spacing = 50
        for x in range(0, self.WIDTH * 100, tick_spacing):
            self.canvas.create_line(x, bottom_y - 5, x, bottom_y + 5, width=1, fill="black")
            self.canvas.create_text(x, bottom_y + 15, text=str(x), anchor='n', font=("Helvetica", 8))

        self.rect1 = rect1
        self.rect2 = rect2

        self.move_rectangles()

    def move_rectangles(self):
        self.rect1.move()
        self.rect2.move()

        self.rect1.update_velocity_text()
        self.rect2.update_velocity_text()

        self.rect1.collision_processed = False
        self.rect2.collision_processed = False

        if self.check_rects_collision(self.rect1, self.rect2) and not self.rect1.collision_processed and not self.rect2.collision_processed:
            self.handle_collisions(self.rect1, self.rect2)
            self.rect1.num_collisions += 1
            self.rect2.num_collisions += 1

        if self.check_wall_collision(self.rect1):
            self.rect1.velocity *= -1
            self.rect1.collision_processed = True
            self.rect1.num_collisions += 1

        if self.check_wall_collision(self.rect2):
            raise SystemExit

        self.update_canvas()

        self.master.after(self.WAIT_TIME, self.move_rectangles)

    def update_canvas(self):
        print(self.rect1.num_collisions)
        if hasattr(self, "label"):
            self.label.config(text=f"Collisions: {self.rect1.num_collisions}")
        else:
            self.label = tk.Label(self.master, text=f"Collisions: {self.rect1.num_collisions}", font=("Helvetica", 14))
            self.label.place(relx=1, anchor='ne', x=-20, y=10)

        max_x = max(self.canvas.bbox(self.rect1.rectangle)[2], self.canvas.bbox(self.rect2.rectangle)[2])

        if max_x > self.WIDTH:
            scale_factor = self.WIDTH / max_x
            self.canvas.scale("all", 0, 0, scale_factor, 1)

    def handle_collisions(self, rect1, rect2):
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

    def check_rects_collision(self, rect1, rect2):
        x1_rect1, _, x2_rect1, _ = rect1.canvas.coords(rect1.rectangle)
        x1_rect2, _, x2_rect2, _ = rect2.canvas.coords(rect2.rectangle)

        return x1_rect1 <= x2_rect2 and x2_rect1 >= x1_rect2

    def check_wall_collision(self, rect):
        x1, _, _, _ = rect.canvas.coords(rect.rectangle)
        return x1 <= self.LEFT_X

class MovingRectangle:
    def __init__(self, canvas, x1, y1, x2, y2, color, mass, velocity):
        self.canvas = canvas
        self.rectangle = canvas.create_rectangle(x1, y1, x2, y2, fill=color)
        self.text = canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text="", fill="white")

        self.mass = mass
        self.velocity = velocity
        self.collision_processed = False
        self.num_collisions = 0

        self.update_velocity_text()

    def move(self):
        self.canvas.move(self.rectangle, self.velocity, 0)
        self.canvas.move(self.text, self.velocity, 0)

    def update_velocity_text(self):
        self.canvas.itemconfig(self.text, text=f"{self.mass} kg\n{round(self.velocity, 8)}")


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Moving Rectangles and Wall Example")
    app = MovingRectangleSimulation(root, 0.05)
    root.mainloop()
