# map generataion

import random as r
import turtle as t
import sys

seed = r.randint(-sys.maxsize-1, sys.maxsize)
seed = seed
print(f'Seed was {seed}.')
r.seed(seed)
size = 35
ratio = 20/size

def createGrid(): 
    # creates a grid of numbers ranging from 0-22
    grid = []
    averagedGrid = []
    for row in range(size+1):
        grid.append([0]*(size+1))
        averagedGrid.append([0]*(size+1))
    for i in range(size+1):
        for j in range(size+1):
            if i==0 or j==0 or i==size or j==size:
                grid[i][j] = 0
            else:
                grid[i][j] = r.randint(0,42)

    # they are now to random
    # want to make each point the average of the points around it
    attemptedspots = [[0,0],[0,1],[0,-1],
                      [1,0],[1,1],[1,-1],
                      [-1,0],[-1,1],[-1,-1]]
    for i in range(size+1):
        for j in range(size+1):
            sum = 0
            todivide = 9
            for spot in attemptedspots:
                # useing error checking to see if a sot is not allowed
                try:
                    sum+=grid[i+spot[0]][j+spot[1]]
                except Exception as e:
                    # we are either on an edge or corner so not all the spots are valid 
                    todivide -=1
            average = int(sum/todivide)
            averagedGrid[i][j] = average

    #print(grid)
    #print()
    #print(averagedGrid)
    return grid, averagedGrid

def colorGrid(generated, calculated): # prints the grid in a turtle window according to the color list
    morecolors = ['#000070', '#0000af', '#0000d5', '#0020ff', '#0050ff', '#0075ff', '#0088ff', '#0098ff', '#00baff', 
                  '#00ffff', '#00ffd5', '#00ffb0', '#00ff90', '#00ff70', '#00ff50', '#00ff30', '#00ff18', '#00ff00', 
                  '#a0ff00', '#bfff00', '#dfff00', '#fff000', '#ffe300', '#ffd000', '#ffc700', '#ffbf00', '#ffb000',
                  '#ffa000', '#ff8000', '#ff6500', '#ff5000', '#ff2800', '#ff0000', '#ff0030', '#ff0050', '#ff0067', 
                  '#ff0080', '#ff00b0', "#ff00c0", '#ff00d0', '#ff00e0', '#ff00f0', '#ff00ff']
    
    # for every color possible we will stamp in a turtle window the coorosponding color
    # i want to see at least a little gradient
    t.shape('square')
    t.hideturtle()
    t.speed(9001)
    screen = t.Screen()
    screenSize = (25*20)
    screen.setup(width=screenSize, height=screenSize)
    screen.bgcolor('black')
    
    t.shapesize(ratio,ratio,1)
    stampSize = 20*ratio
    start = y = -(screenSize/2)+stampSize

    hold = [generated, calculated]
    hold = [calculated]

    for grid in hold:
        t.setx(start)
        t.sety(start)

        for row in range(len(grid)-1,-1,-1):
            for column in range(len(grid)):
                t.color(morecolors[grid[row][column]])
                t.pendown()
                t.stamp()
                t.penup()
                t.fd(stampSize)
            t.setx(start)
            y = y+stampSize
            t.sety(y)
        y = start
    
    screen.exitonclick()

def show():
    random, averaged = createGrid()
    colorGrid(random, averaged)

show()