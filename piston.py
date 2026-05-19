class Piston:
    
    def __init__(self, canvas, x, y, width, height, color):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.piston = canvas.create_rectangle(x, y, x + width, y + height, fill=color)
        self.barrier = y + height
    
    def up(self, event):
        if (self.y < 10):
            self.canvas.move(self.piston, 0, -self.y)
            self.y = 0
            self.barrier = self.height
        else:
            self.canvas.move(self.piston, 0, -10)
            self.y -= 10
            self.barrier -= 10
            
        
    def down(self, event):
        if (self.y > 190):
            self.canvas.move(self.piston, 0, 200-self.y)
            self.y = 200
            self.barrier = self.y + self.height
        else:
            self.canvas.move(self.piston, 0, 10)
            self.y += 10
            self.barrier += 10
