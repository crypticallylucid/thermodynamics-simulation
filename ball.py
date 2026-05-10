class Ball:

  def __init__(self, canvas, x, y, dia, xvel, yvel, color):
    self.canvas = canvas
    self.image = canvas.create_oval(x, y, x+dia, y+dia, fill=color)
    self.dia = dia
    self.xvel = xvel
    self.yvel = yvel

  def move(self):
    coords = self.canvas.coords(self.image)
    if (coords[2] >= self.canvas.winfo_width() or coords[0]<0):
      self.xvel = -self.xvel
    if (coords[3] >= self.canvas.winfo_height() or coords[1]<0):
      self.yvel = -self.yvel
    if (coords[0] < 0):
      self.canvas.move(self.image, -coords[0], 0)
    if (coords[1] < 0):
      self.canvas.move(self.image, 0, -coords[1])
    if (coords[2] > self.canvas.winfo_width()):
      self.canvas.move(self.image, self.canvas.winfo_width()-coords[2], 0)
    if (coords[3] > self.canvas.winfo_height()):
      self.canvas.move(self.image, 0, self.canvas.winfo_height()-coords[3])
    self.canvas.move(self.image, self.xvel, self.yvel)