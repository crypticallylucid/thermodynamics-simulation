import math
from tkinter import *
from tkinter import ttk
from ball import *
import random
import time

def main():
  window = Tk()
  window.columnconfigure(0, weight=1)
  window.rowconfigure(0, weight=1)

  assume_label1 = Label(window, text="Assume 1px/frame = 255m/s", font=("Arial", 16, "bold"), bg="lightgray")
  assume_label1.pack(fill="x")
  assume_label2 = Label(window, text="Assume all molecules are hydrogen", font=("Arial", 16, "bold"), bg="lightgray")
  assume_label2.pack(fill="x")
  temp = 0
  temp_label1 = Label(window, text=f"Temperature: {temp} K", font=("Arial", 16, "bold"), bg="lightgray")
  temp_label1.pack(fill="x")
  temp_label2 = Label(window, text=f"Temperature: {temp} C", font=("Arial", 16, "bold"), bg="lightgray")
  temp_label2.pack(fill="x")

  canvas = Canvas(window, bg="white")
  canvas.pack(fill="both", expand=True)

  window.update()
  balls = []


  for i in range(5):
    balls.append(Ball(canvas, random.randint(100, 400), random.randint(100, 400), 20, random.uniform(1, 1.5), random.uniform(1, 1.5), "green"))

  while True:
    print("test")
    update(canvas, balls, temp_label1, temp_label2)
    window.update()
    time.sleep(0.01)

def isColliding(ball1, ball2):
  coords1 = ball1.canvas.coords(ball1.image)
  coords2 = ball2.canvas.coords(ball2.image)

  x1, y1 = (coords1[0] + coords1[2])/2, (coords1[1] + coords1[3])/2
  x2, y2 = (coords2[0] + coords2[2])/2, (coords2[1] + coords2[3])/2

  dist = ((x2-x1)**2 + (y2-y1)**2)**0.5
  dist+=0.01

  if dist <= (ball1.dia/2 + ball2.dia/2):
    # TODO: MAKE REAL VELOCITIES LMAO
    ball1.xvel, ball2.xvel = ball2.xvel, ball1.xvel
    ball1.yvel, ball2.yvel = ball2.yvel, ball1.yvel

    overlap = (ball1.dia/2 + ball2.dia/2) - dist
    ball1.canvas.move(ball1.image, -overlap*(x2-x1)/dist, -overlap*(y2-y1)/dist)
    ball2.canvas.move(ball2.image, overlap*(x2-x1)/dist, overlap*(y2-y1)/dist)

def update(canvas, balls, temp_label1, temp_label2):
  temp_label1.config(text=f"Temperature: {calcTemp(balls)} K")
  temp_label2.config(text=f"Temperature: {calcTemp(balls)-273.15} C")
  for i, ball in enumerate(balls):
    ball.move()
    for other in balls[i+1:]:
      isColliding(ball, other)

def calcTemp(balls):
    if not balls: return 0
    
    K_BOLTZMANN = 1.380649e-23
    MASS_NITROGEN = 4.65e-26  # kg
    
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