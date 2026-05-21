import math

class Ball:

  def __init__(self, canvas, x, y, dia, xvel, yvel, color):
    self.canvas = canvas
    self.image = canvas.create_oval(x, y, x+dia, y+dia, fill=color)
    self.dia = dia
    self.xvel = xvel
    self.yvel = yvel
    self.x = x
    self.y = y

  def addHeat(self, n):
    if (self.xvel < 0):
        self.xvel -= pow(n, 1/2)
    else:
        self.xvel += pow(n, 1/2)
    if (self.yvel < 0):
        self.yvel -= pow(n, 1/2)
    else:
        self.yvel += pow(n, 1/2)

  def removeHeat(self, n):
    if (self.xvel < 0):
        self.xvel += pow(n, 1/2)
    else:
        self.xvel -= pow(n, 1/2)
    if (self.yvel < 0):
        self.yvel += pow(n, 1/2)
    else:
        self.yvel -= pow(n, 1/2)

  def scaleTemperature(self, factor):
    if factor <= 0:
      self.xvel = 0
      self.yvel = 0
      return
    scale = math.sqrt(factor)
    self.xvel *= scale
    self.yvel *= scale

  def move(self, top):
    self.x += self.xvel
    self.y += self.yvel

    w = self.canvas.winfo_width()
    h = self.canvas.winfo_height()

    if self.x <= 0:
        self.x = 0.1
        self.xvel *= -1
    elif self.x + self.dia >= w:
        self.x = w - self.dia - 0.1
        self.xvel *= -1

    if self.y <= top:
        self.y = top + 0.1
        self.yvel *= -1
    elif self.y + self.dia >= h:
        self.y = h - self.dia - 0.1
        self.yvel *= -1

    self.canvas.coords(self.image, self.x, self.y, self.x + self.dia, self.y + self.dia)