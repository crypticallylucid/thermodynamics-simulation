import math
from tkinter import *
from tkinter import ttk
from ball import *
from piston import *
import random
import time

def main():
  global window
  window = Tk()
  window.columnconfigure(0, weight=1)
  window.rowconfigure(0, weight=1)

  global assume_label1 
  assume_label1 = Label(window, text="Assume 1px/frame = 255m/s", font=("Arial", 16, "bold"), bg="lightgray")
  assume_label1.pack(fill="x",)
  global assume_label2 
  assume_label2 = Label(window, text="Assume all molecules are nitrogen", font=("Arial", 16, "bold"), bg="lightgray")
  assume_label2.pack(fill="x")

  temp = 0
  global temp_label1
  temp_label1 = Label(window, text=f"Temperature: {temp} K", font=("Arial", 16, "bold"), bg="lightgray")
  temp_label1.pack(fill="x")
  global temp_label2 
  temp_label2 = Label(window, text=f"Temperature: {temp} C", font=("Arial", 16, "bold"), bg="lightgray")
  temp_label2.pack(fill="x")

  global canvas
  canvas = Canvas(window, bg="white", width=400, height=400)
  canvas.pack()

  global piston
  piston = Piston(canvas, 0, 0, 400, 20, "blue")
  canvas.bind("<Up>", piston.up)
  canvas.bind("<Down>", piston.down)
  canvas.focus_set()

  global volume
  volume = canvas.width * piston.barrier / 160000

  window.update()
  global balls
  balls = []
  used = [(0, 0)]

  # create 50 particles
  while len(balls) < 50:
    xpos = random.randint(1, canvas.winfo_width()-1)
    ypos = random.randint(1, canvas.winfo_height()-1)
    xvel = random.choice([random.uniform(1, 1.3), random.uniform(-1.3, -1)])
    yvel = random.choice([random.uniform(1, 1.3), random.uniform(-1.3, -1)])
    for pos in used:
      if abs(pos[0]-xpos) > 10 and abs(pos[1]-ypos) > 10:
        balls.append(Ball(canvas, xpos, ypos, 10, xvel, yvel, "green"))
        used.append((xpos, ypos))
        break

  main_loop()
  window.mainloop()

def main_loop():
  update(balls, temp_label1, temp_label2)
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


def update(balls, temp_label1, temp_label2):
  temp_label1.config(text=f"Temperature: {round(calcTempPres(balls), 3)} K")
  temp_label2.config(text=f"Temperature: {round(calcTempPres(balls)-273.15, 3)} C")
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
    
    return temperature
main()