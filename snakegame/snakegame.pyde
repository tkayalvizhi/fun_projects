import time
from Queue import FIFOQueue
from Snake import Snake

side = 20
num_tiles = 30

class Worm(object):
    def __init__(self):
        self.x = int(random(1, num_tiles-2))
        self.y = int(random(1, num_tiles-2))
        
    def show(self):
        fill(255, 0, 0)
        rectMode(CENTER)
        draw_square(self.x, self.y)
    
    def move(self):
        self.x = int(random(1, num_tiles-2))
        self.y = int(random(1, num_tiles-2))
    
    def get_pos(self):
        return (self.x , self.y)
        

class Snake(object):
    class Unit(object):
        def __init__(self, x, y):
            self.x = x
            self.y = y
            self.xdir = 0
            self.ydir = 0
        
        def show(self):
            fill(255, 255, 255)
            rectMode(CENTER)
            draw_square(self.x, self.y)
        
        def set_dir(self, xdir, ydir):
            self.xdir = xdir
            self.ydir = ydir
        
        def move(self):
            self.x += self.xdir
            self.y += self.ydir
            
    def __init__(self):
        self.units = []
        self.units.append(self.Unit(num_tiles/2, num_tiles/2))
        self.worm_collection = FIFOQueue()
    
    def show(self):
        for unit in self.units:
            unit.show()
    
    def get_x(self):
        return self.units[0].x
    
    def get_y(self):
        return self.units[0].y
    
    def set_dir(self):
        
        # change dir of body
        for i in range(len(self.units)-1, 0, -1):
            self.units[i].set_dir(self.units[i-1].xdir, self.units[i-1].ydir)
        
        # change dir of head
        if key == CODED:
            if (keyCode == UP) and (self.units[0].y > 0):
                if (self.units[0].ydir != 1):
                    self.units[0].set_dir(0, -1)
            elif (keyCode == DOWN) and (self.units[0].y < (num_tiles-1)):
                if (self.units[0].ydir != -1):
                    self.units[0].set_dir(0, 1)
            elif (keyCode == LEFT) and (self.units[0].x > 0):
                if (self.units[0].xdir != 1):
                    self.units[0].set_dir(-1, 0)
            elif (keyCode == RIGHT) and (self.units[0].x < (num_tiles-1)):
                if (self.units[0].xdir != -1):
                    self.units[0].set_dir(1, 0)
            else:
                self.game_over()
                
    def move(self):
        for unit in self.units:
            unit.move()
    
    def game_over(self):
        for unit in self.units:
            unit.set_dir(0, 0)
        print('GAME OVER')
        time.sleep(1)
        exit()
        
    def check_self_bite(self):
        for unit in self.units[1:]:
            if (self.units[0].x == unit.x) and (self.units[0].y == unit.y):
                self.game_over()

    def grow(self):
        if self.worm_collection.is_null() == False:
            worm = self.worm_collection.get_last()
            if dist(self.units[-1].x, self.units[-1].y, worm[0], worm[1]) == 0:
                self.units.append(self.Unit(worm[0], worm[1]))
                self.worm_collection.pop_item()
    
    
def draw_square(i, j):
    square(side * i + (side/2), side*j + (side/2), side)


def setup():
    global worm
    global snake
    frameRate(5)
    size(side * num_tiles, side * num_tiles)
    worm = Worm()
    snake = Snake()
    

def draw():
    background(0)
    snake.set_dir()
    
    if dist(snake.get_x(), snake.get_y(), worm.x, worm.y) == 0:
        print('Score!!')
        snake.worm_collection.push_item([worm.x, worm.y])
        worm.move()
        
    snake.grow()
    snake.move()
    worm.show()
    snake.show()
    snake.check_self_bite()
    
    saveFrame(10)
    
    
    
    
    
    

    

            
            
                   
