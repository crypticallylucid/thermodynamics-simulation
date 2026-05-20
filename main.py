import math
from tkinter import *
from tkinter import ttk
from ball import *
from piston import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import random
import time

def main():
  global window
  window = Tk()

  global assume_label1 
  assume_label1 = Label(window, text="Assume 1px/frame = 255m/s", font=("Arial", 16, "bold"), bg="lightgray")
  assume_label1.pack(anchor="n", fill="x",)
  global assume_label2 
  assume_label2 = Label(window, text="Assume all molecules are nitrogen", font=("Arial", 16, "bold"), bg="lightgray")
  assume_label2.pack(anchor="n", fill="x")

  temp = 0

  global temp_label1
  temp_label1 = Label(window, text=f"Temperature: {temp} K", font=("Arial", 16, "bold"), bg="lightgray")
  temp_label1.pack(anchor="n", fill="x")
  global pressure_label
  pressure_label = Label(window, text=f"Pressure: {temp} Pa", font=("Arial", 16, "bold"), bg="lightgray")
  pressure_label.pack(anchor="n", fill="x")
  global volume_label
  volume_label = Label(window, text=f"Volume: {temp} m³", font=("Arial", 16, "bold"), bg="lightgray")
  volume_label.pack(anchor="n", fill="x")

  global mainframe
  mainframe = Frame(window)
  mainframe.pack(anchor="n", fill="both", expand=True, padx=10, pady=10)

  mainframe.columnconfigure(0, weight=0, minsize=400)
  mainframe.columnconfigure(1, weight=1)
  mainframe.rowconfigure(0, weight=1)

  global canvas
  canvas = Canvas(mainframe, bg="white", width=400, height=400)
  canvas.grid(row=0, column=0, sticky="n", padx=10, pady=10)

  global piston
  piston = Piston(canvas, 0, 0, 410, 20, "blue")
  canvas.bind("<Up>", piston.up)
  canvas.bind("<Down>", piston.down)
  canvas.focus_set()

  global balls
  balls = []
  used = [(0, 0)]

  global temps, pressures, volumes
  temps, pressures, volumes = [], [], []
  
  global figurept, axespt, lsrlpt, plotpt
  figurept = Figure(figsize=(5, 4), dpi=100)
  axespt = figurept.add_subplot(111)
  axespt.set_xlabel("Temperature (K)")
  axespt.set_ylabel("Pressure (Pa)")
  axespt.set_title("Pressure vs Temperature")
  lsrlpt, = axespt.plot([], [], color="blue", label="LSRL", marker="o", markersize=3)
  plotpt = FigureCanvasTkAgg(figurept, master=mainframe)
  plotpt.get_tk_widget().grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

  global figurepv, axespv, lsrlpv, plotpv
  figurepv = Figure(figsize=(5, 4), dpi=100)
  axespv = figurepv.add_subplot(111)
  axespv.set_xlabel("Volume (m³)")
  axespv.set_ylabel("Pressure (Pa)")
  axespv.set_title("Volume vs Pressure")
  lsrlpv, = axespv.plot([], [], color="red", label="LSRL", marker="s", markersize=3)
  plotpv = FigureCanvasTkAgg(figurepv, master=mainframe)
  plotpv.get_tk_widget().grid(row=0, column=2, sticky="nsew", padx=10, pady=10)

  global framecount
  framecount = 0

  window.update_idletasks() 
  window.update()

  # create 50 particles
  while len(balls) < 50:
    xpos = random.randint(1, 399)
    ypos = random.randint(30, 399)
    xvel = random.choice([random.uniform(1, 1.3), random.uniform(-1.3, -1)])
    yvel = random.choice([random.uniform(1, 1.3), random.uniform(-1.3, -1)])
    for pos in used:
      if abs(pos[0]-xpos) > 10 and abs(pos[1]-ypos) > 10:
        balls.append(Ball(canvas, xpos, ypos, 10, xvel, yvel, "green"))
        used.append((xpos, ypos))
        break
  
  canvas.focus_set()
  main_loop()
  window.mainloop()

def main_loop():
  global framecount
  update()
  if (framecount%10 == 0):
    graph()
  framecount += 1
  window.after(10, main_loop)

def isColliding(ball1, ball2):
  x1, y1 =  ball1.x, ball1.y
  x2, y2 = ball2.x, ball2.y

  dist = (x2-x1)**2 + (y2-y1)**2
  
  if dist == 0: return

  if dist <= (ball1.dia/2 + ball2.dia/2)**2:
    dist = math.sqrt(dist)
    dvx = ball1.xvel - ball2.xvel
    dvy = ball1.yvel - ball2.yvel
    dx = x2 - x1
    dy = y2 - y1

    dot_product = (dvx * dx) + (dvy * dy)
    scalar = dot_product / (dist**2)
    
    ball1.xvel -= scalar * dx
    ball1.yvel -= scalar * dy
    ball2.xvel += scalar * dx
    ball2.yvel += scalar * dy

    if (dot_product > 0):
      overlap = (ball1.dia/2 + ball2.dia/2) - dist + 1
      movex = overlap * dx/(2*dist)
      movey = overlap * dy/(2*dist)

      canvas.move(ball1.image, movex, movey)
      canvas.move(ball2.image, -movex, -movey)

      ball1.x -= movex
      ball1.y -= movey
      ball2.x += movex
      ball2.y += movey


def update():
  temp_label1.config(text=f"Temperature: {round(calcTempPres(balls)[0], 3)} K, {round(calcTempPres(balls)[0]-273.15, 3)} C")
  pressure_label.config(text=f"Pressure: {round(calcTempPres(balls)[1], 3)} Pa")
  volume_label.config(text=f"Volume: {calcVolume()} meters cubed")
  for i, ball in enumerate(balls):
    ball.move(piston.barrier)
    for other in balls[i+1:]:
      isColliding(ball, other)

def calcTempPres(balls):
    if not balls: return 0
    
    K_BOLTZMANN = 1.380649e-23
    MASS_NITROGEN = 4.65e-26
    
    MPS_PER_PIXEL = 255.0 
    
    sum_v_sq = 0
    for ball in balls:
        vx_mps = ball.xvel * MPS_PER_PIXEL
        vy_mps = ball.yvel * MPS_PER_PIXEL
        
        sum_v_sq += (vx_mps**2 + vy_mps**2)
    
    mean_v_sq = sum_v_sq / len(balls)
    temperature = (MASS_NITROGEN * mean_v_sq) / (2 * K_BOLTZMANN)
    
    return temperature, temperature/calcVolume()
  
def calcVolume():
  return round(canvas.winfo_width() * (400-piston.barrier) / 640000, 3)

def graph():
  temp, pressure = calcTempPres(balls)
  volume = calcVolume()
  temps.append(temp)
  pressures.append(pressure)
  volumes.append(volume)
  lsrlpt.set_xdata(temps)
  lsrlpt.set_ydata(pressures)
  axespt.relim()
  axespt.autoscale_view()
  plotpt.draw_idle()

  lsrlpv.set_xdata(volumes)
  lsrlpv.set_ydata(pressures)
  axespv.relim()
  axespv.autoscale_view()
  plotpv.draw_idle()
main()