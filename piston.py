class Piston:
    
    def __init__(self, canvas, x, y, width, height, color):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        piston = canvas.create_rectangle(x, y, x + width, y + height, fill=color, tags="drag")
    
    def up(event):
        if (self.y < 10):
            self.canvas.move(piston, 0, -self.y)
            self.y = 0
        else:
            self.canvas.move(piston, 0, -10)
            self.y -= 10
        
    def down(event):
        if (self.y > 190):
            self.canvas.move(piston, 0, 200-self.y)
            self.y = 200
        else:
            self.canvas.move(piston, 0, 10)
            self.y += 10
