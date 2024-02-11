import simpy
import tkinter as tk
import random

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

BUS_ARRIVAL_MEAN = 3
PERSON_ARRIVAL_MEAN = 0.1

BUS_SIZE = 30

ARRIVALS = [ random.expovariate(1 / BUS_ARRIVAL_MEAN) for _ in range(40) ]

PEOPLE = [ random.expovariate(1 / PERSON_ARRIVAL_MEAN) for _ in range(1000) ]


def bus_arrival(env, line, len_queue):

    while True:
        next_bus = ARRIVALS.pop()

        yield env.timeout(next_bus)

        bus_load = min(BUS_SIZE, len_queue)

        for _ in range(bus_load):
            line.pop()

        # TODO: look into scanning_customer() and understand how the logic deals with people entering the line, canvas.


def create_clock(env):
    """
        This generator is meant to be used as a SimPy event to update the clock
        and the data in the UI
    """
    
    while True:
        yield env.timeout(0.05)
        clock.tick(env.now)


def person_enters_line(env, line):
    id = 0
    while True:
        next_person = PEOPLE.pop()

        yield env.timeout(next_person)

        line.append(id)
        id += 1


class ClockAndData:
    def __init__(self, canvas, x1, y1, x2, y2, time):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.canvas = canvas
        self.canvas.update()

    def tick(self, time):
        self.canvas.delete(self.time)
        self.canvas.delete(self.seller_wait)
        self.canvas.delete(self.scan_wait)

        self.time = canvas.create_text(self.x1 + 10, self.y1 + 10, text = "Time = "+str(round(time, 1))+"m", anchor = tk.NW)
        
        a3.cla()
        a3.set_xlabel("Time")
        a3.set_ylabel("Arrivals")
        a3.bar([ t for (t, a) in arrivals.items() ], [ a for (t, a) in arrivals.items() ])
        
        data_plot.draw()
        self.canvas.update()

class QueueGraphics:
    text_height = 30
    icon_top_margin = -8
    
    def __init__(self, icon_file, icon_width, queue_name, num_lines, canvas, x_top, y_top):
        self.icon_file = icon_file
        self.icon_width = icon_width
        self.queue_name = queue_name
        self.num_lines = num_lines
        self.canvas = canvas
        self.x_top = x_top
        self.y_top = y_top

        self.image = tk.PhotoImage(file = self.icon_file)
        self.icons = defaultdict(lambda: [])
        for i in range(num_lines):
            canvas.create_text(x_top, y_top + (i * self.text_height), anchor = tk.NW, text = f"{queue_name} #{i + 1}")
        self.canvas.update()

    def add_to_line(self, seller_number):
        count = len(self.icons[seller_number])
        x = self.x_top + 60 + (count * self.icon_width)
        y = self.y_top + ((seller_number - 1) * self.text_height) + self.icon_top_margin
        self.icons[seller_number].append(
                self.canvas.create_image(x, y, anchor = tk.NW, image = self.image)
        )
        self.canvas.update()

    def remove_from_line(self, seller_number):
        if len(self.icons[seller_number]) == 0: return
        to_del = self.icons[seller_number].pop()
        self.canvas.delete(to_del)
        self.canvas.update()

def Line(canvas, x_top, y_top):
    return QueueGraphics("C:/Users/ericb/Documents/Repos\Feynman/images/group.gif", 25, "Seller", line, canvas, x_top, y_top)

if __name__ == "__main__":

    main = tk.Tk()
    main.title("Gate Simulation")
    main.config(bg="#fff")
    # logo = tk.PhotoImage(file = "images/LogoDattivo.png")
    top_frame = tk.Frame(main)
    top_frame.pack(side=tk.TOP, expand = False)
    tk.Label(top_frame, bg = "#000007", height = 15, width = 300).pack(side=tk.LEFT, expand = False)
    canvas = tk.Canvas(main, image=None, width = 1300, height = 350, bg = "white")
    canvas.pack(side=tk.TOP, expand = False)

    f = plt.Figure(figsize=(2, 2), dpi=72)
    a3 = f.add_subplot(121)
    a3.plot()
    a1 = f.add_subplot(222)
    a1.plot()
    a2 = f.add_subplot(224)
    a2.plot()
    data_plot = FigureCanvasTkAgg(f, master=main)
    data_plot.get_tk_widget().config(height = 400)
    data_plot.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)



    clock = ClockAndData(canvas, 1100, 260, 1290, 340, 0)
    line = Line(canvas, 340, 20)

    env = simpy.rt.RealtimeEnvironment(factor=0.1, strict=False)

    line = [simpy.Resource(env, capacity=1)]

    env.process(person_enters_line(env, line))
    env.process(bus_arrival(env, line))
    env.process(create_clock(env))


    env.run(until=60)